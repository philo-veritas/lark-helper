#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

try:
    import click  # type: ignore[import-not-found]
except Exception:  # pragma: no cover - 环境缺少依赖时的兜底提示
    click = None  # type: ignore[assignment]

from _version_bump import run as core_run


def main() -> int:
    if click is None:
        print(
            "需要 click，请先安装：pip install click 或 uv pip install click",
            file=sys.stderr,
        )
        return 2

    @click.command()
    @click.argument("version", required=False)
    @click.option(
        "--root",
        default=str(Path(__file__).resolve().parents[1]),
        show_default=True,
        help="仓库根目录路径，默认取脚本上级目录",
    )
    @click.option("--dry-run", is_flag=True, help="仅显示将要发生的变更，不写回文件")
    @click.option("-q", "--quiet", is_flag=True, help="静默模式，减少输出")
    def cli(version: str | None, root: str, dry_run: bool, quiet: bool) -> None:
        code = core_run(version, root, dry_run, quiet)
        raise SystemExit(code)

    cli()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


