# 默认使用 uv 运行，可通过环境覆盖：`make bump-version PYTHON=python3`
PYTHON ?= uv run python

.PHONY: bump-version help

help:
	@echo "Usage:"
	@echo "  make bump-version VERSION=<x> [ARGS='--dry-run -q']"
	@echo "Examples:"
	@echo "  make bump-version"
	@echo "  make bump-version VERSION=0.1.0.dev12"
	@echo "  make bump-version VERSION=0.1.0.dev12 ARGS='--dry-run'"

# 版本号管理：读取/写入 pyproject.toml 和 src/lark_helper/__init__.py
bump-version:
	$(PYTHON) scripts/bump_version.py $(VERSION) $(ARGS)


