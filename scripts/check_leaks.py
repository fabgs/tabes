#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Detector de fugas de TabES: bloquea secretos, datos personales y ficheros prohibidos.

Modos:
  --staged   lo que entra en el próximo commit (hook pre-commit de Git)
  --push     commits que se van a subir, sus mensajes y sus autores (hook pre-push de Git)
  --history  todo el historial (CI)
  --tree     todos los ficheros no ignorados del árbol de trabajo
  --hook     hook PreToolUse de Claude Code: lee por stdin el JSON de la llamada y, si el
             comando hace `git commit` o `git push`, revisa antes de permitirlo

Falso positivo con un dato inventado: añade "leakcheck: allow" en esa línea y explícalo en el PR.

Lista privada: `.leakcheck-denylist.txt` en la raíz (ignorado por Git). Una cadena por línea
que nunca debe publicarse (DNI, dirección, teléfono, CIF, nombres reales...). `#` = comentario.

Sin dependencias: solo biblioteca estándar de Python >= 3.9.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
import subprocess
import sys
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

ALLOW_MARKER = "leakcheck: allow"
DENYLIST_FILE = ".leakcheck-denylist.txt"
MAX_FILE_BYTES = 2 * 1024 * 1024
MAX_PRINTED = 60
DATA_SHEET_OK_DIRS = {"fixtures", "templates", "plantillas"}
WALK_SKIP_DIRS = {
    ".git", "comercial", "node_modules", ".venv", "venv", "__pycache__",
    ".mypy_cache", ".ruff_cache", ".pytest_cache", "staticfiles", "media",
}

# --------------------------------------------------------------------------- rutas

FORBIDDEN_PATHS: list[tuple[str, str]] = [
    ("comercial/", "carpeta de documentos comerciales (datos personales)"),
    ("backups/", "copias de seguridad"),
    ("data/", "carpeta de datos reales"),
    ("exports/", "exportaciones con datos reales"),
    (".env", "variables de entorno con secretos"),
    (".env.*", "variables de entorno con secretos"),
    ("*.pem", "clave privada o certificado"),
    ("*.key", "clave privada"),
    ("*.p8", "clave privada (p. ej. APNs)"),
    ("*.p12", "certificado con clave privada"),
    ("*.pfx", "certificado con clave privada"),
    ("*.jks", "almacén de claves de firma Android"),
    ("*.keystore", "almacén de claves de firma Android"),
    ("*.mobileprovision", "perfil de aprovisionamiento iOS"),
    ("*.kdbx", "base de datos de contraseñas"),
    ("id_rsa*", "clave SSH"),
    ("id_ed25519*", "clave SSH"),
    ("id_ecdsa*", "clave SSH"),
    ("credentials.json", "credenciales"),
    ("google-services.json", "configuración de Firebase"),
    ("GoogleService-Info.plist", "configuración de Firebase"),
    ("*.sql", "volcado de base de datos"),
    ("*.sql.gz", "volcado de base de datos"),
    ("*.dump", "volcado de base de datos"),
    ("*.sqlite3", "base de datos"),
    ("*.db", "base de datos"),
    ("settings.local.json", "ajustes locales de Claude Code"),
    (DENYLIST_FILE, "lista privada de datos sensibles"),
]
PATH_EXCEPTIONS = {".env.example"}


def forbidden_reason(path: str) -> str | None:
    p = PurePosixPath(path.replace("\\", "/"))
    name = p.name
    if name in PATH_EXCEPTIONS:
        return None
    dirs = set(p.parts[:-1])
    for pattern, reason in FORBIDDEN_PATHS:
        if pattern.endswith("/"):
            if pattern[:-1] in dirs:
                return reason
        elif fnmatch.fnmatch(name, pattern):
            return reason
    if name.lower().endswith((".csv", ".xlsx", ".xls", ".ods")) and not (DATA_SHEET_OK_DIRS & dirs):
        return "hoja de datos fuera de fixtures/ o plantillas/ (¿datos reales?)"
    return None


# --------------------------------------------------------------------------- contenido

PLACEHOLDER_HINTS = (
    "example", "ejemplo", "changeme", "change-me", "cambiar", "dummy", "fake", "falso",
    "test", "prueba", "placeholder", "xxxx", "****", "<", ">", "${", "{{", "%(",
    "env(", "environ", "getenv", "your", "tu_", "tu-",
)
LOCAL_HOSTS = {"localhost", "127.0.0.1", "0.0.0.0", "db", "postgres", "redis", "valkey", "host.docker.internal"}
ALLOWED_EMAIL_DOMAINS = (
    "example.com", "example.org", "example.net", "example", "ejemplo.org", "ejemplo.com",
    "ejemplo.es", "test", "invalid", "localhost", "users.noreply.github.com", "noreply.github.com",
)
ALLOWED_EMAILS = {"noreply@anthropic.com", "noreply@github.com"}
DNI_LETTERS = "TRWAGMYFPDXBNJZSQVHLCKE"


def _not_placeholder(value: str) -> bool:
    v = value.lower()
    return not any(h in v for h in PLACEHOLDER_HINTS)


def email_is_leak(address: str) -> bool:
    address = address.strip().strip("<>").lower()
    if address in ALLOWED_EMAILS or "@" not in address:
        return False
    local, domain = address.rsplit("@", 1)
    domain = domain.rstrip(".")
    if local == "git" and domain in {"github.com", "gitlab.com", "bitbucket.org"}:
        return False
    return not any(domain == d or domain.endswith("." + d) for d in ALLOWED_EMAIL_DOMAINS)


def _dni(m: re.Match[str]) -> bool:
    return DNI_LETTERS[int(m.group(1)) % 23] == m.group(2).upper()


def _nie(m: re.Match[str]) -> bool:
    n = "XYZ".index(m.group(1).upper())
    return DNI_LETTERS[int(f"{n}{m.group(2)}") % 23] == m.group(3).upper()


def _cif(m: re.Match[str]) -> bool:
    digits, control = m.group(2), m.group(3).upper()
    total = sum(int(digits[i]) for i in (1, 3, 5))
    for i in (0, 2, 4, 6):
        d = int(digits[i]) * 2
        total += d // 10 + d % 10
    c = (10 - total % 10) % 10
    return control == str(c) or control == "JABCDEFGHI"[c]


def _iban(m: re.Match[str]) -> bool:
    raw = re.sub(r"\s", "", m.group(0)).upper()
    moved = raw[4:] + raw[:4]
    number = "".join(str(int(ch, 36)) for ch in moved)
    return int(number) % 97 == 1


def _phone(m: re.Match[str]) -> bool:
    digits = re.sub(r"\D", "", m.group(0))
    if len(digits) == 11 and digits.startswith("34"):
        digits = digits[2:]
    rest = digits[1:]
    return len(set(rest)) > 1 and rest not in {"12345678", "23456789", "87654321", "98765432"}


@dataclass(frozen=True)
class Rule:
    reason: str
    pattern: re.Pattern[str]
    is_leak: Callable[[re.Match[str]], bool] | None = None
    sample_group: int | str = 0


RULES: list[Rule] = [
    Rule("clave privada", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    Rule("clave de AWS", re.compile(r"(?<![A-Z0-9])(?:AKIA|ASIA)[0-9A-Z]{16}(?![A-Z0-9])")),
    Rule("token de GitHub", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{50,})")),
    Rule("token de Slack", re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}")),
    Rule("clave de Stripe", re.compile(r"\b[rs]k_live_[0-9A-Za-z]{20,}")),
    Rule("clave de Google", re.compile(r"\bAIza[0-9A-Za-z_\-]{35}")),
    Rule("clave de API (sk-...)", re.compile(r"\bsk-(?:ant-|proj-)?[A-Za-z0-9_\-]{32,}")),
    Rule("token JWT", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}")),
    Rule(
        "secreto escrito en el código",
        re.compile(
            r"""(?i)(?P<key>[\w.-]*(?:secret|passw(?:or)?d|pwd|token|api[_-]?key|access[_-]?key|"""
            r"""private[_-]?key|auth[_-]?key)[\w.-]*)["']?\s*(?::|=|=>)\s*["'](?P<value>[^"'\s]{8,})["']"""
        ),
        lambda m: _not_placeholder(m.group("value")),
        "value",
    ),
    Rule(
        "secreto en variable de entorno o YAML",
        re.compile(
            r"(?m)^\s*(?:export\s+)?(?P<key>[A-Z0-9_]*(?:SECRET|PASSWORD|PASSWD|TOKEN|API_KEY|ACCESS_KEY|"
            r"PRIVATE_KEY)[A-Z0-9_]*)\s*[:=]\s*(?P<value>[^\s#'\"$]{8,})\s*$"
        ),
        lambda m: _not_placeholder(m.group("value")),
        "value",
    ),
    Rule(
        "cadena de conexión con contraseña",
        re.compile(
            r"(?i)\b(?:postgres(?:ql)?|mysql|mariadb|rediss?|amqp|mongodb(?:\+srv)?)://"
            r"(?P<user>[^:/\s@]+):(?P<password>[^@\s]+)@(?P<host>[^/:\s]+)"
        ),
        lambda m: m.group("host").lower() not in LOCAL_HOSTS and _not_placeholder(m.group("password")),
        "password",
    ),
    Rule("IBAN", re.compile(r"(?<![\w])ES\d{2}(?:[ ]?\d{4}){5}(?![\w])"), _iban),
    Rule("DNI", re.compile(r"(?<![\w])(\d{8})[- ]?([A-Za-z])(?![\w])"), _dni),
    Rule("NIE", re.compile(r"(?<![\w])([XYZxyz])[- ]?(\d{7})[- ]?([A-Za-z])(?![\w])"), _nie),
    Rule("CIF", re.compile(r"(?<![\w])([ABCDEFGHJNPQRSUVW])[- ]?(\d{7})[- ]?([0-9A-Ja-j])(?![\w])"), _cif),
    Rule(
        "teléfono",
        re.compile(
            r"(?<![\w+])(?:\+34[ .-]?)?[6-9]\d{2}(?:(?:[ .-]?\d{3}){2}|(?:[ .-]?\d{2}){3})(?![\w])"
        ),
        _phone,
    ),
    Rule(
        "email real",
        re.compile(r"[A-Za-z0-9._%+-]+@(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,}"),
        lambda m: email_is_leak(m.group(0)),
    ),
]


# --------------------------------------------------------------------------- informe


@dataclass(frozen=True)
class Finding:
    where: str
    line: int | None
    reason: str
    sample: str = ""

    def render(self) -> str:
        loc = f"{self.where}:{self.line}" if self.line else self.where
        return f"  - {loc}: {self.reason}" + (f" [{self.sample}]" if self.sample else "")


def mask(value: str) -> str:
    value = value.strip()
    if len(value) <= 4:
        return "*" * len(value)
    return f"{value[:2]}… ({len(value)} car.)"


def load_denylist(root: Path) -> list[str]:
    path = root / DENYLIST_FILE
    if not path.is_file():
        return []
    items = []
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        item = raw.strip()
        if item and not item.startswith("#") and len(item) >= 4:
            items.append(item.casefold())
    return items


def scan_line(where: str, lineno: int | None, text: str, denylist: list[str]) -> list[Finding]:
    if ALLOW_MARKER in text:
        return []
    found: list[Finding] = []
    folded = text.casefold()
    for item in denylist:
        if item in folded:
            found.append(Finding(where, lineno, "dato de la lista privada (.leakcheck-denylist.txt)"))
    for rule in RULES:
        for m in rule.pattern.finditer(text):
            if rule.is_leak is None or rule.is_leak(m):
                found.append(Finding(where, lineno, rule.reason, mask(m.group(rule.sample_group))))
    return found


def scan_blob(path: str, content: bytes, denylist: list[str]) -> list[Finding]:
    found: list[Finding] = []
    reason = forbidden_reason(path)
    if reason:
        found.append(Finding(path, None, f"fichero prohibido: {reason}"))
    if len(content) > MAX_FILE_BYTES:
        found.append(Finding(path, None, f"fichero de {len(content) / 1_048_576:.1f} MB (¿datos o binario grande?)"))
    if b"\0" in content[:8192]:
        return found
    text = content.decode("utf-8", errors="replace")
    for i, line in enumerate(text.splitlines(), start=1):
        found.extend(scan_line(path, i, line, denylist))
    return found


# --------------------------------------------------------------------------- git


class GitError(RuntimeError):
    pass


def git(cwd: Path, *args: str) -> bytes:
    r = subprocess.run(["git", "-c", "core.quotepath=off", *args], cwd=cwd, capture_output=True)
    if r.returncode != 0:
        raise GitError(r.stderr.decode("utf-8", errors="replace").strip() or f"git {' '.join(args)} falló")
    return r.stdout


def repo_root(cwd: Path) -> Path | None:
    r = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=cwd, capture_output=True)
    if r.returncode != 0:
        return None
    return Path(r.stdout.decode("utf-8", errors="replace").strip())


def split_z(raw: bytes) -> list[str]:
    return [p.decode("utf-8", errors="replace") for p in raw.split(b"\0") if p]


def has_commits(root: Path) -> bool:
    return subprocess.run(["git", "rev-parse", "--verify", "HEAD"], cwd=root, capture_output=True).returncode == 0


def check_identity(root: Path) -> list[Finding]:
    r = subprocess.run(["git", "config", "user.email"], cwd=root, capture_output=True)
    email = r.stdout.decode("utf-8", errors="replace").strip()
    if not email:
        return [Finding("git config user.email", None, "no hay email de Git configurado")]
    if email_is_leak(email):
        return [Finding(
            "git config user.email", None,
            "tu email de Git saldría público en cada commit; usa el anónimo de GitHub "
            "(ID+usuario@users.noreply.github.com)",
            mask(email),
        )]
    return []


def scan_staged(root: Path, include_worktree: bool) -> list[Finding]:
    denylist = load_denylist(root)
    found = check_identity(root)
    staged = split_z(git(root, "diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z"))
    for path in staged:
        found.extend(scan_blob(path, git(root, "show", f":{path}"), denylist))
    if include_worktree:
        others = split_z(git(root, "ls-files", "-m", "-o", "--exclude-standard", "-z"))
        for path in others:
            if path in staged:
                continue
            full = root / path
            if full.is_file():
                found.extend(scan_blob(path, full.read_bytes(), denylist))
    return found


def _range_args_from_stdin(lines: Iterable[str]) -> list[list[str]]:
    ranges = []
    for line in lines:
        parts = line.split()
        if len(parts) != 4:
            continue
        _local_ref, local_sha, _remote_ref, remote_sha = parts
        if set(local_sha) == {"0"}:
            continue  # se borra una rama remota: no se sube nada
        if set(remote_sha) == {"0"}:
            ranges.append([local_sha, "--not", "--remotes"])
        else:
            ranges.append([f"{remote_sha}..{local_sha}"])
    return ranges


def default_push_ranges(root: Path) -> list[list[str]]:
    if not has_commits(root):
        return []
    r = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"], cwd=root, capture_output=True
    )
    if r.returncode == 0:
        return [["@{u}..HEAD"]]
    return [["HEAD", "--not", "--remotes"]]


def scan_commits(root: Path, ranges: list[list[str]]) -> list[Finding]:
    denylist = load_denylist(root)
    found: list[Finding] = []
    for rng in ranges:
        names = git(root, "log", "--format=", "--name-only", "--diff-filter=ACMR", *rng)
        for path in sorted(set(names.decode("utf-8", errors="replace").splitlines())):
            if path and (reason := forbidden_reason(path)):
                found.append(Finding(path, None, f"fichero prohibido en el historial: {reason}"))

        authors = git(root, "log", "--format=%ae%n%ce", *rng).decode("utf-8", errors="replace").splitlines()
        for email in sorted(set(a for a in authors if a)):
            if email_is_leak(email):
                found.append(Finding("autor de commit", None, "email personal en los metadatos del commit", mask(email)))

        log = git(root, "log", "--format=%x1eCOMMIT %h%n%B", *rng).decode("utf-8", errors="replace")
        for block in log.split("\x1e"):
            if not block.strip():
                continue
            header, _, body = block.partition("\n")
            for i, line in enumerate(body.splitlines(), start=1):
                found.extend(scan_line(f"mensaje de commit {header[7:]}", i, line, denylist))

        diff = git(root, "log", "-p", "-U0", "--no-color", "--no-ext-diff", "--format=%x1eCOMMIT %h", *rng)
        current: str | None = None
        new_line = 0
        for raw in diff.decode("utf-8", errors="replace").splitlines():
            if raw.startswith("\x1eCOMMIT "):
                current = None
            elif raw.startswith("+++ "):
                current = raw[6:] if raw.startswith("+++ b/") else None
            elif raw.startswith("@@"):
                m = re.search(r"\+(\d+)", raw)
                new_line = int(m.group(1)) if m else 0
            elif raw.startswith("+") and current is not None:
                found.extend(scan_line(current, new_line, raw[1:], denylist))
                new_line += 1
    return found


def walk_tree(base: Path) -> list[str]:
    out = []
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames[:] = [d for d in dirnames if d not in WALK_SKIP_DIRS]
        for f in filenames:
            out.append(Path(dirpath, f).relative_to(base).as_posix())
    return out


def scan_tree(cwd: Path) -> list[Finding]:
    root = repo_root(cwd)
    base = root or cwd
    denylist = load_denylist(base)
    paths = split_z(git(base, "ls-files", "-co", "--exclude-standard", "-z")) if root else walk_tree(base)
    found: list[Finding] = []
    for path in paths:
        full = base / path
        if full.is_file():
            found.extend(scan_blob(path, full.read_bytes(), denylist))
    return found


# --------------------------------------------------------------------------- hook de Claude Code

SEGMENT = r"[^\n|;&]*?"
COMMIT_RE = re.compile(rf"\bgit\b{SEGMENT}\bcommit\b")
PUSH_RE = re.compile(rf"\bgit\b{SEGMENT}\bpush\b|\bgh\s+repo\s+create\b{SEGMENT}--push\b")
POLICY_RULES = [
    (re.compile(r"--no-verify\b"), "no se permite saltarse los hooks (--no-verify)"),
    (re.compile(rf"\bcommit\b{SEGMENT}\s-[A-Za-z]*n[A-Za-z]*(?=\s|$)"), "no se permite saltarse los hooks (commit -n)"),
    (re.compile(rf"\bgit\b{SEGMENT}\badd\b{SEGMENT}\s(?:-[A-Za-z]*f[A-Za-z]*|--force)(?=\s|$)"),
     "no se permite forzar ficheros ignorados (git add -f)"),
    (re.compile(r"-c\s+core\.hooksPath"), "no se permite desactivar los hooks de Git"),
]


def hook_main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError) as exc:
        print(f"check_leaks: no se pudo leer la entrada del hook ({exc}); bloqueado por seguridad.", file=sys.stderr)
        return 2
    command = str((payload.get("tool_input") or {}).get("command") or "")
    is_commit, is_push = bool(COMMIT_RE.search(command)), bool(PUSH_RE.search(command))
    adds = bool(re.search(r"\bgit\b[^\n|;&]*?\badd\b", command))
    if not (is_commit or is_push or adds):
        return 0

    found: list[Finding] = []
    for pattern, reason in POLICY_RULES:
        if pattern.search(command):
            found.append(Finding("comando", None, reason))
    if not (is_commit or is_push):
        return report(found, "git add", hook=True)

    cwd = Path(str(payload.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()))
    root = repo_root(cwd)
    if root is None:
        if is_commit:
            found.extend(scan_tree(cwd))
        return report(found, "commit sin repositorio", hook=True)

    hooks_path = subprocess.run(["git", "config", "--get", "core.hooksPath"], cwd=root, capture_output=True)
    if hooks_path.stdout.decode().strip() != ".githooks" and "core.hooksPath .githooks" not in command:
        found.append(Finding(
            "git config", None,
            "los hooks de Git no están activados; ejecuta: git config core.hooksPath .githooks",
        ))
    try:
        if is_commit:
            found.extend(scan_staged(root, include_worktree=True))
        if is_push:
            found.extend(check_identity(root))
            found.extend(scan_commits(root, default_push_ranges(root)))
    except GitError as exc:
        found.append(Finding("git", None, f"no se pudo completar la revisión ({exc}); bloqueado por seguridad"))
    label = "commit + push" if is_commit and is_push else "commit" if is_commit else "push"
    return report(found, label, hook=True)


# --------------------------------------------------------------------------- salida


def report(found: list[Finding], label: str, *, hook: bool) -> int:
    unique = list(dict.fromkeys(found))
    if not unique:
        if not hook:
            print(f"check_leaks ({label}): sin fugas.")
        return 0
    err = sys.stderr
    print(f"check_leaks ({label}): BLOQUEADO, {len(unique)} problema(s):", file=err)
    for f in unique[:MAX_PRINTED]:
        print(f.render(), file=err)
    if len(unique) > MAX_PRINTED:
        print(f"  ... y {len(unique) - MAX_PRINTED} más.", file=err)
    print(
        "Quita el dato o muévelo a una variable de entorno. Si es un dato inventado, añade "
        f"'{ALLOW_MARKER}' en esa línea y explícalo en el PR. No uses --no-verify.",
        file=err,
    )
    if hook:
        print("Claude: no esquives esta comprobación. Enseña estos hallazgos al usuario y corrígelos.", file=err)
    return 2 if hook else 1


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
        except (AttributeError, ValueError):
            pass
    parser = argparse.ArgumentParser(description="Detector de fugas de TabES")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--staged", action="store_true", help="lo que entra en el próximo commit")
    mode.add_argument("--push", action="store_true", help="commits que se van a subir")
    mode.add_argument("--history", action="store_true", help="todo el historial")
    mode.add_argument("--tree", action="store_true", help="todos los ficheros no ignorados")
    mode.add_argument("--hook", action="store_true", help="hook PreToolUse de Claude Code")
    args = parser.parse_args(argv)

    if args.hook:
        return hook_main()
    cwd = Path.cwd()
    try:
        if args.tree:
            return report(scan_tree(cwd), "árbol de trabajo", hook=False)
        root = repo_root(cwd)
        if root is None:
            print("check_leaks: no es un repositorio de Git.", file=sys.stderr)
            return 1
        if args.staged:
            return report(scan_staged(root, include_worktree=False), "commit", hook=False)
        if args.push:
            stdin_lines = [] if sys.stdin is None or sys.stdin.isatty() else sys.stdin.read().splitlines()
            ranges = _range_args_from_stdin(stdin_lines) or default_push_ranges(root)
            return report(check_identity(root) + scan_commits(root, ranges), "push", hook=False)
        ranges = [["HEAD"]] if has_commits(root) else []
        return report(scan_commits(root, ranges), "historial", hook=False)
    except GitError as exc:
        print(f"check_leaks: error de git: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
