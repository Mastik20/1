"""Persistence helpers for the institute domain model."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .institute import Institute


class DataManager:
    """Handle saving and loading institute data."""

    @staticmethod
    def save(institute: Institute, file_path: str | Path) -> None:
        """Persist the institute to the provided JSON file."""
        path = Path(file_path)
        if not path.parent.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
        data = institute.to_dict()
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False))

    @staticmethod
    def load(file_path: str | Path) -> Institute:
        """Load institute data from the provided JSON file."""
        path = Path(file_path)
        content = path.read_text()
        raw_data: Any = json.loads(content)
        if not isinstance(raw_data, dict):
            raise ValueError("Serialized institute data must be a JSON object")
        return Institute.from_dict(raw_data)
