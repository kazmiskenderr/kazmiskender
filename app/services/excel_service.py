"""Excel report generation service using pandas and openpyxl."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable, Mapping

import pandas as pd


class ExcelReportService:
    """Create simple Excel reports from iterable dictionaries."""

    def export(self, rows: Iterable[Mapping[str, object]], output_path: Path) -> Path:
        df = pd.DataFrame(list(rows))
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_excel(output_path, index=False)
        return output_path
