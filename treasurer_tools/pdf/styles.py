"""The standard styles used for PDF generation."""

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.styles import ParagraphStyle


STYLES = {
    'title': ParagraphStyle(
        'title',
        alignment=TA_CENTER,
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=24,
        spaceBefore=0,
        spaceAfter=0,
    ),
    'normal': ParagraphStyle(
        'normal',
        alignment=TA_LEFT,
        fontName='Helvetica',
        fontSize=12,
        leading=15,
    ),
    'normal_centered': ParagraphStyle(
        'normal',
        alignment=TA_CENTER,
        fontName='Helvetica',
        fontSize=12,
        leading=15,
    ),
    'bold': ParagraphStyle(
        'normal',
        alignment=TA_LEFT,
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
    ),
    'bold_small': ParagraphStyle(
        'normal',
        alignment=TA_LEFT,
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=12,
    ),
    'bold_tiny': ParagraphStyle(
        'normal',
        alignment=TA_LEFT,
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
    ),
    'bold_tiny_center': ParagraphStyle(
        'normal',
        alignment=TA_CENTER,
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
    ),
    'table_header': ParagraphStyle(
        'table_header',
        fontSize=17,
        leading=20,
        textColor=colors.white,
    ),
    'table_header_color': colors.Color(red=78/255, green=78/255, blue=78/255),
    'fax_table_header': ParagraphStyle(
        'table_header',
        fontSize=14,
        leading=16,
        textColor=colors.white,
    ),
    'fax_disclaimer': ParagraphStyle(
        'disclaimer',
        alignment=TA_CENTER,
        fontSize=8,
        leading=8,
        spaceBefore=0,
        spaceAfter=0,
        fontName='Helvetica-Oblique',
    )
}
