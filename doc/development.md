## 开发环境与版本号管理

### 安装开发依赖

推荐使用 uv：

```bash
uv pip install -e .[dev]
```

或使用 pip：

```bash
pip install -e .[dev]
```

### 版本号管理

本项目通过 Makefile 提供 `make bump-version` 任务，同时读取/更新以下两个位置的版本号：
- `pyproject.toml` `[project].version`
- `src/lark_helper/__init__.py` 中的 `__version__`

用法：

```bash
# 查看当前版本
make bump-version

# 预览更新到 0.1.0.dev12（不写入）
make bump-version VERSION=0.1.0.dev12 ARGS="--dry-run"

# 实际写入两个文件
make bump-version VERSION=0.1.0.dev12
```

可选变量：
- `VERSION`：目标版本号，省略则仅显示当前两处版本号
- `ARGS`：透传给底层命令的其他参数，例如 `--dry-run`、`-q`

如果不使用 Makefile，也可以直接调用脚本：

```bash
python3 scripts/bump_version.py                        # 查看版本
python3 scripts/bump_version.py 0.1.0.dev12 --dry-run
python3 scripts/bump_version.py 0.1.0.dev12            # 写入
```

### 实现与约束

- 替换逻辑保留文件原有行内缩进与换行风格（不改变引号、空格与行尾换行风格）
- 若两处版本不一致，会提示警告
- 失败时返回非 0 退出码


