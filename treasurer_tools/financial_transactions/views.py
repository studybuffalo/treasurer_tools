"""Views for the transactions app"""

from datetime import datetime
from reportlab import lib
from reportlab.lib.units import mm
from reportlab.platypus import (
    Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
)

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from branch_details.models import Branch

from treasurer_tools.pdf.styles import STYLES
from treasurer_tools.pdf.canvases import PageNumCanvas

from .forms import CompiledForms
from .models import FinancialTransaction

def generate_pdf_header(branch_details, transaction):
    # Access image from the storage module (in case not saved locally)
    logo_storage = default_storage.open(branch_details.logo.name, 'rb')

    # Get and resize logo (max height = 25 mm, max width = 75 mm)
    logo_details = lib.utils.ImageReader(logo_storage)
    width, height = logo_details.getSize()

    # If aspect ratio > 1/3, need to scale by max height
    if (height / width) > 0.333:
        logo = Image(
            logo_storage,
            width=((25 * mm) / height) * width,
            height=25 * mm,
        )
    # Otherwise, need to scale by max width
    else:
        logo = Image(
            logo_storage,
            width=75 * mm,
            height=((75 * mm) / width) * height,
        )


    if transaction.transaction_type == 'e':
        header_title = 'Branch Expense Claim Form'
    else:
        header_title = 'Branch Deposit Form'

    header_table = Table(
        [[logo, header_title]],
        colWidths=[90 * mm, 90 * mm],
    )

    header_table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'Helvetica-Bold', 16),
        ('ALIGNMENT', (0, 0), (0, 0), 'LEFT'),
        ('ALIGNMENT', (1, 0), (1, 0), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    return header_table

def generate_pdf_transaction_details(branch_details, transaction):
    # Get all relevant details
    branch_name = branch_details.name_full if branch_details.name_full else ''
    payee_payer = transaction.payee_payer
    name = payee_payer.name if payee_payer.name else ''
    address = payee_payer.address if payee_payer.address else ''
    city = payee_payer.city if payee_payer.city else ''
    province = payee_payer.province if payee_payer.province else ''
    postal_code = payee_payer.postal_code if payee_payer.postal_code else ''
    phone = payee_payer.phone if payee_payer.phone  else ''

    # Table to hold the payee/payer details

    details_table = Table(
        [
            [
                'Branch Name:',
                Paragraph(branch_name, STYLES['normal'])
            ],
            [
                'Payee Name:',
                Paragraph(name, STYLES['normal'])
            ],
            [
                'Payee Address:',
                Paragraph(address, STYLES['normal_center'])
            ],
            ['', 'Mailing address'],
            [
                '',
                Paragraph(city, STYLES['normal_center']),
                Paragraph(province, STYLES['normal_center']),
                Paragraph(postal_code, STYLES['normal_center']),
                Paragraph(phone, STYLES['normal_center'])],
            ['', 'City', 'Province', 'Postal Code', 'Telephone'],
        ],
        colWidths=[40 * mm, 65 * mm, 20 * mm, 25 * mm, 40 * mm]
    )

    details_table.setStyle(TableStyle([
        # Overall table styles
        ('FONT', (0, 0), (-1, -1), 'Helvetica', 12),


        # Branch Name styles
        ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 10),
        ('LINEBELOW', (1, 0), (-1, 0), 1, lib.colors.black),
        ('SPAN', (1, 0), (-1, 0)),

        # Payee/Payer Name styles
        ('LINEBELOW', (1, 1), (-1, 1), 1, lib.colors.black),
        ('SPAN', (1, 1), (-1, 1)),

        # Payee/Payer Address styles
        ('FONT', (1, 3), (-1, 3), 'Helvetica-Oblique', 8),
        ('FONT', (1, 5), (-1, 5), 'Helvetica-Oblique', 8),
        ('LINEBELOW', (1, 2), (-1, 2), 1, lib.colors.black),
        ('LINEBELOW', (1, 4), (-1, 4), 1, lib.colors.black),
        ('SPAN', (1, 2), (-1, 2)),
        ('SPAN', (1, 3), (-1, 3)),
        ('ALIGNMENT', (1, 2), (-1, 5), 'CENTER'),
        ('VALIGN', (1, 3), (-1, 3), 'TOP'),
        ('VALIGN', (1, 5), (-1, 5), 'TOP'),
    ]))

    return details_table

def generate_pdf_transaction_items(transaction):
    # Header data for the items table
    items_rows = [
        [
            Paragraph(
                'Purchase Date YYYY-MMM-DD',
                STYLES['bold_tiny_center']
            ),
            Paragraph('Description', STYLES['bold_tiny_center']),
            Paragraph('Amount Before Tax', STYLES['bold_tiny_center']),
            Paragraph('GST/HST', STYLES['bold_tiny_center']),
            Paragraph('Total', STYLES['bold_tiny_center']),
            Paragraph('Budget Year', STYLES['bold_tiny_center']),
            Paragraph('Account Code', STYLES['bold_tiny_center']),
        ],
    ]

    # Add each transaction item
    items = transaction.items.all()

    for item in items:
        # Get financial code details for item
        code = item.financial_codes.first()

        items_rows.append([
            item.date_item.strftime('%Y-%b-%d'),
            Paragraph(item.description, STYLES['normal_tiny']),
            '${}'.format(item.amount),
            '${}'.format(item.gst),
            '${}'.format(item.total),
            Paragraph(
                code.financial_code_group.budget_year.short_name,
                STYLES['normal_tiny_center']
            ),
            code.code,
        ])

    # Add the table footer
    items_rows.append([
        '',
        'TOTAL',
        '${}'.format(transaction.total_before_tax),
        '${}'.format(transaction.total_tax),
        '${}'.format(transaction.total),
        '',
        ''
    ])

    items_table = Table(
        items_rows,
        colWidths=[
            25 * mm, 55 * mm, 20 * mm, 20 * mm, 20 * mm, 30 * mm, 20 * mm
        ]
    )

    items_table.setStyle(TableStyle([
        # Overall table styles
        ('FONT', (0, 0), (-1, -1), 'Helvetica', 8),
        ('BOX', (0, 0), (-1, -2), 1, lib.colors.black),
        ('INNERGRID', (0, 0), (-1, -2), 1, lib.colors.black),
        ('ALIGNMENT', (0, 0), (-1, 0), 'CENTRE'),

        # Header styles
        ('BACKGROUND', (0, 0), (-1, 0), lib.colors.lightgrey),

        # Item styles
        ('VALIGN', (0, 1), (-1, -2), 'TOP'),

        # Date styles
        ('ALIGNMENT', (0, 0), (0, -1), 'CENTRE'),

        # Dollar amount styles
        ('FONTSIZE', (2, 1), (4, -1), 8),
        ('ALIGNMENT', (2, 1), (4, -1), 'RIGHT'),

        # Account code styles
        ('ALIGNMENT', (5, 1), (6, -1), 'CENTRE'),

        # Footer style
        ('FONT', (1, -1), (4, -1), 'Helvetica-Bold'),
        ('BACKGROUND', (2, -1), (4, -1), lib.colors.lightgrey),
        ('BOX', (2, -1), (4, -1), 1, lib.colors.black),
        ('INNERGRID', (2, -1), (4, -1), 1, lib.colors.black),
        ('ALIGNMENT', (1, -1), (4, -1), 'RIGHT'),
        ('VALIGN', (1, -1), (4, -1), 'MIDDLE'),
    ]))

    return items_table

def generate_pdf_transaction_notes(transaction):
    # Table to hold any transation notes
    notes_table = Table(
        [
            ['Notes:', Paragraph('', STYLES['normal'])],
        ],
        colWidths=[20 * mm, 170 * mm],
    )

    return notes_table

def generate_pdf_submission_details(transaction, user_name):
    # TODO: Use proper submission tracking details in this section
    base_style = [
        # Overall table styles
        ('FONT', (0, 0), (-1, -1), 'Helvetica', 10, 9),
        ('FONT', (0, 2), (-1, 2), 'Helvetica-Oblique', 8, 8),
        ('FONT', (0, 4), (-1, 4), 'Helvetica-Oblique', 8, 8),
        ('FONT', (0, 6), (-1, 6), 'Helvetica-Oblique', 8, 8),
        ('ALIGNMENT', (0, 0), (-1, -1), 'CENTRE'),

        # Header style
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 8, 10),
        ('BACKGROUND', (0, 0), (-1, 0), lib.colors.lightgrey),
        ('BOX', (0, 0), (-1, 0), 1, lib.colors.black),
        ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),

        # Submitted by styles
        ('BOX', (0, 0), (2, -1), 1, lib.colors.black),
        ('LINEBELOW', (1, 1), (1, 1), 0.5, lib.colors.black),
        ('LINEBELOW', (1, 5), (1, 5), 0.5, lib.colors.black),

        # Authorized by or Processed by styles
        ('BOX', (3, 0), (5, -1), 1, lib.colors.black),
        ('LINEBELOW', (4, 1), (4, 1), 0.5, lib.colors.black),
        ('LINEBELOW', (4, 3), (4, 3), 0.5, lib.colors.black),
        ('LINEBELOW', (4, 5), (4, 5), 0.5, lib.colors.black),
    ]

    if transaction.transaction_type == 'e':
        submission_table = Table(
            [
                ['', 'SUBMITTED BY', '', '', 'AUTHORIZED BY', '', '', 'PROCESSED BY', ''],
                [
                    '', '', '',
                    '', '', '',
                    '', user_name, ''
                ],
                ['', 'Name', '', '', 'Name', '', '', 'Name', ''],
                [
                    '', '', '',
                    '', '', '',
                    '', 'CSHP-AB Treasurer', ''
                ],
                ['', '', '', '', 'Position', '', '', 'Position', ''],
                [
                    '', transaction.date_submitted.strftime('%Y-%b-%d'), '',
                    '', '', '',
                    '', '', ''
                ],
                ['', 'Date', '', '', 'Date', '', '', 'Date', ''],
            ],
            colWidths=[
                2 * mm, 59 * mm, 2 * mm,
                2 * mm, 60 * mm, 2 * mm,
                2 * mm, 59 * mm, 2 * mm
            ],
        )

        # Add the additional processed by styles
        base_style.append(('BOX', (6, 0), (8, -1), 1, lib.colors.black))
        base_style.append(('LINEBELOW', (7, 1), (7, 1), 0.5, lib.colors.black))
        base_style.append(('LINEBELOW', (7, 3), (7, 3), 0.5, lib.colors.black))
        base_style.append(('LINEBELOW', (7, 5), (7, 5), 0.5, lib.colors.black))
    else:
        submission_table = Table(
            [
                ['', 'SUBMITTED BY', '', '', 'PROCESSED BY', ''],
                [
                    '', '', '',
                    '', user_name, '',
                ],
                ['', 'Name', '', '', 'Name', ''],
                [
                    '', '', '',
                    '', 'CSHP-AB Treasurer', ''
                ],
                ['', '', '', '', 'Position', ''],
                [
                    '', transaction.date_submitted.strftime('%Y-%b-%d'), '',
                    '', '', ''
                ],
                ['', 'Date', '', '', 'Date', ''],
            ],
            colWidths=[
                2 * mm, 59 * mm, 2 * mm,
                2 * mm, 60 * mm, 2 * mm,
                2 * mm, 59 * mm, 2 * mm
            ],
        )

    # Apply table styles
    submission_table.setStyle(TableStyle(base_style))

    return submission_table

@login_required
def dashboard(request):
    """Main dashboard to expenses and revenue"""
    return render(request, "transactions/index.html")

@login_required
def request_transactions_list(request):
    """Retrieves list of transactions"""

    # Get all transactions
    transactions = FinancialTransaction.objects.all().order_by("-date_submitted")

    # Filter by type
    transaction_type = request.GET.get("transaction_type", "a")

    if transaction_type == "e":
        transactions = transactions.filter(transaction_type="e")
    elif transaction_type == "r":
        transactions = transactions.filter(transaction_type="r")

    # Filter by date
    date_start = request.GET.get("date_start", None)
    date_end = request.GET.get("date_end", None)

    if date_start:
        transactions = transactions.filter(date_submitted__gte=date_start)

    if date_end:
        transactions = transactions.filter(date_submitted__lte=date_end)

    return render(
        request,
        "transactions/transactions.html",
        context={
            "transactions": transactions
        }
    )

@login_required
def transaction_add(request, t_type):
    """Generates and processes form to add a transaction"""
    # POST request - try and save data
    if request.method == "POST":
        compiled_forms = CompiledForms(t_type, "POST", request.POST, request.FILES)

        if compiled_forms.is_valid():
            compiled_forms.save()

            # Redirect to a new URL:
            messages.success(request, "Transaction successfully added")

            return HttpResponseRedirect(reverse("financial_transactions:dashboard"))
    # GET request - generate blank form and formset
    else:
        compiled_forms = CompiledForms(
            t_type, "GET", request.POST, request.FILES,
        )

    return render(
        request,
        "transactions/add_edit.html",
        {
            "forms": compiled_forms,
            "page_name": "Add new {}".format(t_type),
            "type": "add",
        },
    )

@login_required
def transaction_edit(request, t_type, transaction_id):
    """Generate and processes form to edit transactions"""
    # POST request - try and save data
    if request.method == "POST":
        compiled_forms = CompiledForms(
            t_type, "POST", request.POST, request.FILES, transaction_id=transaction_id
        )

        if compiled_forms.is_valid():
            compiled_forms.save()

            # Redirect to a new URL:
            messages.success(request, "Transaction successfully edited")

            return HttpResponseRedirect(reverse("financial_transactions:dashboard"))
    # GET request - generate blank form and formset
    else:
        compiled_forms = CompiledForms(
            t_type, "GET", request.POST, request.FILES, transaction_id=transaction_id,
        )

    return render(
        request,
        "transactions/add_edit.html",
        {
            "forms": compiled_forms,
            "page_name": "Edit {}".format(t_type),
            "type": "edit",
        },
    )

@login_required
def transaction_delete(request, t_type, transaction_id):
    """Generates and handles delete requests of a transaction"""

    # Get the Transaction instance
    transaction = get_object_or_404(FinancialTransaction, id=transaction_id)

    # If this is a POST request then process the Form data
    if request.method == "POST":
        transaction.delete()

        # Redirect back to main list
        messages.success(request, "Transaction deleted")

        return HttpResponseRedirect(reverse("financial_transactions:dashboard"))

    return render(
        request,
        "transactions/delete.html",
        {
            "page_name": t_type,
            "delete_message": t_type,
            "item_to_delete": transaction,
        },
    )

@login_required
def transaction_pdf(request, transaction_id):
    """Generates a PDF version of the provided transaction"""

    # Set the PDF metadata
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="somefilename.pdf"'
    response['title'] = 'Test'

    # Get the branch details for the header (currently uses last entry)
    # TODO: Allow for multiple branches with different details
    branch_details = Branch.objects.last()

    # Get the transaction instance
    transaction = get_object_or_404(FinancialTransaction, id=transaction_id)

    # Generate a PDF title
    pdf_title = '{}.pdf'.format(str(transaction))

    # Create the PDF object, using the response object as its "file."
    # Page size = 8.5" or 215.9 mm - rounded to 215 mm
    doc = SimpleDocTemplate(
        response,
        pagesize=lib.pagesizes.letter,
        title=pdf_title,
        topMargin=12.5 * mm,
        rightMargin=12.5 * mm,
        bottomMargin=12.5 * mm,
        leftMargin=12.5 * mm,
    )

    elements = []

    elements.append(generate_pdf_header(branch_details, transaction))
    elements.append(Spacer(190 * mm, 10))
    elements.append(generate_pdf_transaction_details(branch_details, transaction))
    elements.append(Spacer(190 * mm, 10))
    elements.append(generate_pdf_transaction_items(transaction))
    elements.append(Spacer(190 * mm, 10))

    if transaction.submission_notes:
        elements.append(generate_pdf_transaction_notes(transaction))
        elements.append(Spacer(190 * mm, 10))

    elements.append(
        generate_pdf_submission_details(transaction, request.user.name)
    )

    # Assemble and return the final PDF document
    doc.build(elements, canvasmaker=PageNumCanvas)

    return response
