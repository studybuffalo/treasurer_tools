"""The standard styles used for PDF generation."""

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
    'normal_small': ParagraphStyle(
        'normal',
        alignment=TA_LEFT,
        fontName='Helvetica',
        fontSize=10,
        leading=12,
    ),
    'normal_tiny': ParagraphStyle(
        'normal',
        alignment=TA_LEFT,
        fontName='Helvetica',
        fontSize=8,
        leading=10,
    ),
    'normal_center': ParagraphStyle(
        'normal',
        alignment=TA_CENTER,
        fontName='Helvetica',
        fontSize=12,
        leading=15,
    ),
    'normal_small_center': ParagraphStyle(
        'normal',
        alignment=TA_CENTER,
        fontName='Helvetica',
        fontSize=10,
        leading=12,
    ),
    'normal_tiny_center': ParagraphStyle(
        'normal',
        alignment=TA_CENTER,
        fontName='Helvetica',
        fontSize=8,
        leading=10,
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
}
