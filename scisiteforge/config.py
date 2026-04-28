from __future__ import annotations

import json
from pathlib import Path
from typing import Any


DEFAULT_THEME = "evo-edu"


def load_config(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save_config(path: str | Path, config: dict[str, Any]) -> None:
    Path(path).write_text(json.dumps(config, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def resolve_path(value: str | Path | None, base_dir: str | Path | None = None) -> Path | None:
    if value in (None, ""):
        return None
    path = Path(value)
    if path.is_absolute() or base_dir is None:
        return path
    return Path(base_dir) / path
