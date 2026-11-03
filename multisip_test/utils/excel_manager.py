import os
import time
from pathlib import Path
from typing import List, Dict, Any, Optional
import openpyxl
from utils.excel_utils import ExcelUtils


class ExcelManager:
    """
    Manages loading test scenarios, recording execution statuses (PASS/FAIL),
    and saving audit-ready execution workbooks without mutating the original template.
    """

    def __init__(self, file_path: str):
        self.source_path = Path(file_path).resolve()
        if not self.source_path.exists():
            raise FileNotFoundError(f"Excel test file not found at: {self.source_path}")

        self.wb = openpyxl.load_workbook(self.source_path)
        self.sheet = self.wb.active
        self.headers = [cell.value for cell in self.sheet[1]]
        self.col_map = {name: idx + 1 for idx, name in enumerate(self.headers) if name}

    def get_all_test_cases(self) -> List[Dict[str, Any]]:
        """Reads rows into a list of dictionaries keyed by column name."""
        test_cases = []
        for row_idx in range(2, self.sheet.max_row + 1):
            row_data = {"__row_idx__": row_idx}
            for header, col_idx in self.col_map.items():
                row_data[header] = self.sheet.cell(row=row_idx, column=col_idx).value
            if row_data.get("Test_ID"):
                test_cases.append(row_data)
        return test_cases

    def update_test_status(
        self,
        row_idx: int,
        status: str,
        actual_result: str = "",
        screenshot_path: str = "",
        error_message: str = "",
    ):
        """Updates test execution outcome, styling, and audit trails."""
        now_str = time.strftime("%Y-%m-%d %H:%M:%S")

        status_col = self.col_map.get("Status")
        actual_col = self.col_map.get("Actual_Result")
        ts_col = self.col_map.get("Execution_Timestamp")
        screen_col = self.col_map.get("Screenshot_Path")
        err_col = self.col_map.get("Error_Details")

        if status_col:
            cell = self.sheet.cell(row=row_idx, column=status_col, value=status.upper())
            cell.alignment = ExcelUtils.CENTER_ALIGN
            cell.border = ExcelUtils.THIN_BORDER
            if status.upper() == "PASS":
                cell.fill = ExcelUtils.PASS_FILL
                cell.font = ExcelUtils.PASS_FONT
            elif status.upper() == "FAIL":
                cell.fill = ExcelUtils.FAIL_FILL
                cell.font = ExcelUtils.FAIL_FONT
            else:
                cell.fill = ExcelUtils.SKIP_FILL
                cell.font = ExcelUtils.SKIP_FONT

        if actual_col and actual_result:
            c = self.sheet.cell(row=row_idx, column=actual_col, value=actual_result)
            c.font = ExcelUtils.DEFAULT_FONT
            c.border = ExcelUtils.THIN_BORDER

        if ts_col:
            c = self.sheet.cell(row=row_idx, column=ts_col, value=now_str)
            c.alignment = ExcelUtils.CENTER_ALIGN
            c.font = ExcelUtils.DEFAULT_FONT
            c.border = ExcelUtils.THIN_BORDER

        if screen_col and screenshot_path:
            c = self.sheet.cell(row=row_idx, column=screen_col, value=screenshot_path)
            c.font = ExcelUtils.DEFAULT_FONT
            c.border = ExcelUtils.THIN_BORDER

        if err_col and error_message:
            c = self.sheet.cell(row=row_idx, column=err_col, value=error_message)
            c.font = ExcelUtils.DEFAULT_FONT
            c.border = ExcelUtils.THIN_BORDER

    def save_results(self, output_dir: Optional[str] = None) -> str:
        """Saves results into a new timestamped file to preserve original template."""
        if output_dir:
            out_folder = Path(output_dir)
        else:
            out_folder = self.source_path.parent

        out_folder.mkdir(parents=True, exist_ok=True)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        stem = self.source_path.stem
        output_file = out_folder / f"{stem}_results_{timestamp}.xlsx"

        ExcelUtils.auto_fit_columns(self.sheet)
        self.wb.save(output_file)
        print(f"Test run results saved to: {output_file}")
        return str(output_file)

