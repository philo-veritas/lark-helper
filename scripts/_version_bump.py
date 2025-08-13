from __future__ import annotations

import re
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

PYPROJECT_SECTION_HEADER_PATTERN = re.compile(r"^\s*\[(?P<section>[^\]]+)\]\s*$")
PYPROJECT_VERSION_PATTERN = re.compile(
    r'^(?P<prefix>\s*version\s*=\s*")(?P<version>[^"]+)(?P<suffix>".*)$'
)
INIT_VERSION_PATTERN = re.compile(
    r'^(?P<prefix>\s*__version__\s*=\s*")(?P<version>[^"]+)(?P<suffix>".*)$'
)


@dataclass
class VersionInfo:
    pyproject_version: str | None
    init_version: str | None


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_current_versions(root: Path) -> VersionInfo:
    pyproject = root / "pyproject.toml"
    init_file = root / "src" / "lark_helper" / "__init__.py"

    py_v: str | None = None
    in_project = False
    for line in _read_text(pyproject).splitlines():
        m = PYPROJECT_SECTION_HEADER_PATTERN.match(line)
        if m:
            in_project = m.group("section").strip() == "project"
            continue
        if in_project:
            m2 = PYPROJECT_VERSION_PATTERN.match(line)
            if m2:
                py_v = m2.group("version")
                break

    init_v: str | None = None
    for line in _read_text(init_file).splitlines():
        m = INIT_VERSION_PATTERN.match(line)
        if m:
            init_v = m.group("version")
            break

    return VersionInfo(pyproject_version=py_v, init_version=init_v)


def replace_version_in_pyproject(pyproject_path: Path, new_version: str) -> tuple[str, bool]:
    original = pyproject_path.read_text(encoding="utf-8")
    lines = original.splitlines(keepends=True)
    in_project = False
    changed = False
    old_version = ""

    for i, line in enumerate(lines):
        stripped = line.rstrip("\r\n")
        ending = line[len(stripped) :]

        m = PYPROJECT_SECTION_HEADER_PATTERN.match(stripped)
        if m:
            in_project = m.group("section").strip() == "project"

        if in_project:
            match = PYPROJECT_VERSION_PATTERN.match(stripped)
            if match:
                old_version = match.group("version")
                if old_version != new_version:
                    lines[i] = (
                        f"{match.group('prefix')}{new_version}{match.group('suffix')}{ending}"
                    )
                    changed = True
                break

    if not old_version:
        raise RuntimeError("未在 pyproject.toml 的 [project] 段找到 version 字段")

    if changed:
        pyproject_path.write_text("".join(lines), encoding="utf-8")

    return old_version, changed


def replace_version_in_init(init_path: Path, new_version: str) -> tuple[str, bool]:
    original = init_path.read_text(encoding="utf-8")
    lines = original.splitlines(keepends=True)
    changed = False
    old_version = ""

    for i, line in enumerate(lines):
        stripped = line.rstrip("\r\n")
        ending = line[len(stripped) :]

        match = INIT_VERSION_PATTERN.match(stripped)
        if match:
            old_version = match.group("version")
            if old_version != new_version:
                lines[i] = f"{match.group('prefix')}{new_version}{match.group('suffix')}{ending}"
                changed = True
            break

    if not old_version:
        raise RuntimeError("未在 __init__.py 中找到 __version__ 字段")

    if changed:
        init_path.write_text("".join(lines), encoding="utf-8")

    return old_version, changed


def run(
    version: str | None,
    root: str,
    dry_run: bool,
    quiet: bool,
    *,
    echo: Callable[[str], None] | None = None,
    err_echo: Callable[[str], None] | None = None,
) -> int:
    if echo is None:
        echo = print
    if err_echo is None:  # pragma: no cover - 默认 stderr 输出

        def _err(s: str) -> None:
            print(s, file=sys.stderr)

        err_echo = _err

    root_path = Path(root).resolve()
    pyproject_path = root_path / "pyproject.toml"
    init_path = root_path / "src" / "lark_helper" / "__init__.py"

    if not pyproject_path.exists() or not init_path.exists():
        err_echo("未找到 pyproject.toml 或 __init__.py，请检查 --root 是否正确")
        return 2

    versions = read_current_versions(root_path)

    if version is None:
        if not quiet:
            echo(f"pyproject.toml version: {versions.pyproject_version}")
            echo(f"__init__.py    version: {versions.init_version}")
            if versions.pyproject_version != versions.init_version:
                err_echo("警告：两个位置的版本号不一致")
        return 0

    new_version = version

    if dry_run:
        if not quiet:
            echo(f"[dry-run] 将 {versions.pyproject_version} -> {new_version} 写入 pyproject.toml")
            echo(f"[dry-run] 将 {versions.init_version} -> {new_version} 写入 __init__.py")
        return 0

    old_py, changed_py = replace_version_in_pyproject(pyproject_path, new_version)
    old_init, changed_init = replace_version_in_init(init_path, new_version)

    if not quiet:
        echo(
            f"pyproject.toml: {old_py} -> {new_version}"
            + (" (已更新)" if changed_py else " (无变化)")
        )
        echo(
            f"__init__.py   : {old_init} -> {new_version}"
            + (" (已更新)" if changed_init else " (无变化)")
        )

    return 0
