from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter


class ExcelUtils:
    """Helper methods for OpenPyXL styling, borders, and column formatting."""

    HEADER_FILL = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
    HEADER_FONT = Font(name="Calibri", size=11, bold=True, color="FFFFFF")

    PASS_FILL = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
    PASS_FONT = Font(name="Calibri", size=10, bold=True, color="006100")

    FAIL_FILL = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
    FAIL_FONT = Font(name="Calibri", size=10, bold=True, color="9C0006")

    SKIP_FILL = PatternFill(start_color="FFEB9C", end_color="FFEB9C", fill_type="solid")
    SKIP_FONT = Font(name="Calibri", size=10, bold=True, color="9C6500")

    DEFAULT_FONT = Font(name="Calibri", size=10)
    BOLD_FONT = Font(name="Calibri", size=10, bold=True)

    CENTER_ALIGN = Alignment(horizontal="center", vertical="center", wrap_text=True)
    LEFT_ALIGN = Alignment(horizontal="left", vertical="center", wrap_text=True)

    THIN_BORDER = Border(
        left=Side(style="thin", color="D9D9D9"),
        right=Side(style="thin", color="D9D9D9"),
        top=Side(style="thin", color="D9D9D9"),
        bottom=Side(style="thin", color="D9D9D9"),
    )

    @classmethod
    def style_header_row(cls, sheet, row_num: int = 1):
        """Applies header styling to the given row in the worksheet."""
        for cell in sheet[row_num]:
            cell.fill = cls.HEADER_FILL
            cell.font = cls.HEADER_FONT
            cell.alignment = cls.CENTER_ALIGN
            cell.border = cls.THIN_BORDER

    @classmethod
    def auto_fit_columns(cls, sheet, max_width: int = 50):
        """Adjusts column widths based on cell contents."""
        for col in sheet.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                val = str(cell.value or "")
                lines = val.split("\n")
                line_max = max(len(l) for l in lines) if lines else 0
                max_len = max(max_len, line_max)
            sheet.column_dimensions[col_letter].width = min(max(max_len + 3, 12), max_width)

