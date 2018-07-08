"""Views for the reports app"""

from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from bank_reconciliation.models import ReconciliationMatch
from bank_transactions.models import BankTransaction
from financial_codes.models import FinancialCodeSystem, BudgetYear, FinancialCode
from financial_transactions.models import FinancialTransaction
from investments.models import Investment


@login_required
def dashboard(request):
    """Main dashboard to view reports"""
    return render(
        request,
        "reports/index.html",
        context={},
    )

@login_required
def income_statement_dashboard(request):
    """Dashboard to generate account summary views"""

    return render(
        request,
        "reports/income_statement.html",
        context={
            "financial_code_systems": FinancialCodeSystem.objects.all(),
        },
    )

@login_required
def retrieve_income_statement(request):
    """Retrieves data for account summary report"""

    financial_code_system = request.GET.get("financial_code_system", None)
    date_start = request.GET.get("date_start", None)
    date_end = request.GET.get("date_end", None)

    if all([financial_code_system, date_start, date_end]):
        revenue_code_totals = FinancialCode.objects.values("code", "description").filter(
            Q(financial_code_group__budget_year__financial_code_system__id=financial_code_system)
            & Q(financial_code_group__type="r")
            & Q(financialcodematch__item__transaction__date_submitted__gte=date_start)
            & Q(financialcodematch__item__transaction__date_submitted__lte=date_end)
        ).annotate(
            total=Sum("financialcodematch__item__amount") + Sum("financialcodematch__item__gst")
        )

        expense_code_totals = FinancialCode.objects.values("code", "description").filter(
            Q(financial_code_group__budget_year__financial_code_system__id=financial_code_system)
            & Q(financial_code_group__type="e")
            & Q(financialcodematch__item__transaction__date_submitted__gte=date_start)
            & Q(financialcodematch__item__transaction__date_submitted__lte=date_end)
        ).annotate(
            total=Sum("financialcodematch__item__amount") + Sum("financialcodematch__item__gst")
        )
    else:
        revenue_code_totals = None
        expense_code_totals = None

    return render(
        request,
        "reports/income_statement_report.html",
        context={
            "revenue_codes": revenue_code_totals,
            "expense_codes": expense_code_totals,
        }
    )

@login_required
def retrieve_balance_sheet(request):
    """Retrieves data for the balance sheet report"""
    # Need all assets vs. All Liabilities
    # Need on hand cash, investments, accounts payable
    # Need any debt or liability (accounts payable)

    budget_year_id = request.GET.get("budget_year", None)

    if budget_year_id:
        budget_year = get_object_or_404(BudgetYear, id=budget_year_id)
        date_end = budget_year.date_end

        # CALCULATE CASH
        # Get all the bank transactions between start and end date
        bank_transaction_totals = BankTransaction.objects.filter(
            date_transaction__lte=date_end
        ).aggregate(
            debit=Sum("amount_debit"), credit=Sum("amount_credit")
        )
        debit = bank_transaction_totals["debit"] if bank_transaction_totals["debit"] else 0
        credit = bank_transaction_totals["credit"] if bank_transaction_totals["credit"] else 0
        cash = credit - debit

        # CALCULATE INVESTMENTS
        # Get all investments that started before/during this budget year
        # and haven't matured
        investment_totals = Investment.objects.filter(
            Q(date_invested__lte=date_end)
            & Q(date_matured__gte=date_end)
        ).aggregate(total=Sum("amount_matured"))
        investments = investment_totals['total'] if investment_totals['total'] else 0

        # CALCULATE ACCOUNTS RECEIVABLE
        # Get all the reconciled transactions
        reconciled_transactions = list(ReconciliationMatch.objects.values_list(
            "financial_transaction__id", flat=True
        ))

        # Get all the revenue transactions that have not been reconciled
        revenue_transactions = FinancialTransaction.objects.filter(
            transaction_type="r"
        ).exclude(
            id__in=reconciled_transactions
        )

        # Cycle through each transaction and total the amount
        accounts_receivable = 0

        for transaction in revenue_transactions:
            accounts_receivable += transaction.total

        # TOTAL ASSETS
        assets_total = cash + investments + accounts_receivable

        # CALCULATE DEBT
        # Not currently being tracked in application
        debt = 0

        # CALCULATE ACCOUNTS PAYABLE
        # Get all the expense transactions that have not been reconciled
        expense_transactions = FinancialTransaction.objects.filter(
            transaction_type="e"
        ).exclude(
            id__in=reconciled_transactions
        )

        # Cycle through each transaction and total the amount
        accounts_payable = 0

        for transaction in expense_transactions:
            accounts_payable += transaction.total

        # TOTAL LIABILITIES
        liabilities_total = debt + accounts_payable
    else:
        cash = 0
        investments = 0
        accounts_receivable = 0
        assets_total = 0
        debt = 0
        accounts_payable = 0
        liabilities_total = 0

    return JsonResponse({
        "cash": cash,
        "investments": investments,
        "accounts_receivable": accounts_receivable,
        "assets_total": assets_total,
        "debt": debt,
        "accounts_payable": accounts_payable,
        "liabilities_total": liabilities_total,
    })

@login_required
def balance_sheet_dashboard(request):
    """Dashboard to generate balance sheet views"""

    return render(
        request,
        "reports/balance_sheet.html",
        context={
            "financial_code_systems": FinancialCodeSystem.objects.all(),
        },
    )
