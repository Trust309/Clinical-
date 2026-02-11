"""
Financial Agent

Handles all financial tracking and reporting:
- Expense tracking and categorization
- Revenue tracking and analysis
- Profit/loss reporting
- Tax preparation support
- Monthly/annual financial summaries
- Budget management
"""

from collections import defaultdict
from datetime import date
from typing import Optional

from ..models.property import (
    Booking,
    Expense,
    ExpenseCategory,
    Property,
    Revenue,
)
from ..utils.helpers import format_currency, generate_id
from ..utils.templates import render_template


class FinancialAgent:
    """Agent responsible for financial tracking and reporting."""

    def __init__(self):
        self.expenses: list[Expense] = []
        self.revenues: list[Revenue] = []
        self.budgets: dict[str, dict] = {}

    # ── Expense Tracking ─────────────────────────────────────────

    def record_expense(
        self,
        property_id: str,
        category: ExpenseCategory,
        amount: float,
        description: str,
        expense_date: Optional[date] = None,
        vendor: str = "",
        receipt_url: str = "",
        tax_deductible: bool = True,
    ) -> Expense:
        """Record a new expense."""
        expense = Expense(
            expense_id=generate_id("exp"),
            property_id=property_id,
            category=category,
            amount=amount,
            description=description,
            date=expense_date or date.today(),
            vendor=vendor,
            receipt_url=receipt_url,
            tax_deductible=tax_deductible,
        )
        self.expenses.append(expense)
        return expense

    def get_expenses(
        self,
        property_id: Optional[str] = None,
        category: Optional[ExpenseCategory] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> list[Expense]:
        """Get expenses with optional filters."""
        results = self.expenses
        if property_id:
            results = [e for e in results if e.property_id == property_id]
        if category:
            results = [e for e in results if e.category == category]
        if start_date:
            results = [e for e in results if e.date >= start_date]
        if end_date:
            results = [e for e in results if e.date <= end_date]
        return results

    def get_expense_breakdown(
        self,
        property_id: str,
        start_date: date,
        end_date: date,
    ) -> dict:
        """Get expense breakdown by category for a period."""
        expenses = self.get_expenses(property_id, start_date=start_date, end_date=end_date)
        breakdown = defaultdict(float)
        for exp in expenses:
            breakdown[exp.category.value] += exp.amount

        total = sum(breakdown.values())
        return {
            "period": f"{start_date.isoformat()} to {end_date.isoformat()}",
            "total": round(total, 2),
            "total_formatted": format_currency(total),
            "by_category": {
                cat: {
                    "amount": round(amt, 2),
                    "formatted": format_currency(amt),
                    "percentage": round((amt / total) * 100, 1) if total else 0,
                }
                for cat, amt in sorted(breakdown.items(), key=lambda x: -x[1])
            },
            "num_expenses": len(expenses),
        }

    # ── Revenue Tracking ─────────────────────────────────────────

    def record_revenue(
        self,
        booking: Booking,
        platform_fee_pct: float = 3.0,
    ) -> Revenue:
        """Record revenue from a booking."""
        platform_fee = booking.total_price * (platform_fee_pct / 100)
        net = booking.total_price - platform_fee

        revenue = Revenue(
            booking_id=booking.booking_id,
            property_id=booking.property_id,
            gross_amount=booking.total_price,
            platform_fee=round(platform_fee, 2),
            cleaning_fee=booking.cleaning_fee,
            net_amount=round(net, 2),
            date=booking.check_out,
        )
        self.revenues.append(revenue)
        return revenue

    def get_revenue(
        self,
        property_id: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> list[Revenue]:
        """Get revenue records with optional filters."""
        results = self.revenues
        if property_id:
            results = [r for r in results if r.property_id == property_id]
        if start_date:
            results = [r for r in results if r.date >= start_date]
        if end_date:
            results = [r for r in results if r.date <= end_date]
        return results

    # ── Profit & Loss ────────────────────────────────────────────

    def generate_pnl(
        self,
        property_id: str,
        start_date: date,
        end_date: date,
    ) -> dict:
        """Generate a profit and loss statement."""
        revenues = self.get_revenue(property_id, start_date, end_date)
        expenses = self.get_expenses(property_id, start_date=start_date, end_date=end_date)

        gross_revenue = sum(r.gross_amount for r in revenues)
        platform_fees = sum(r.platform_fee for r in revenues)
        net_revenue = sum(r.net_amount for r in revenues)
        total_expenses = sum(e.amount for e in expenses)
        net_income = net_revenue - total_expenses

        expense_breakdown = defaultdict(float)
        for exp in expenses:
            expense_breakdown[exp.category.value] += exp.amount

        return {
            "property_id": property_id,
            "period": f"{start_date.isoformat()} to {end_date.isoformat()}",
            "revenue": {
                "gross": round(gross_revenue, 2),
                "gross_formatted": format_currency(gross_revenue),
                "platform_fees": round(platform_fees, 2),
                "platform_fees_formatted": format_currency(platform_fees),
                "net_revenue": round(net_revenue, 2),
                "net_revenue_formatted": format_currency(net_revenue),
                "num_bookings": len(revenues),
            },
            "expenses": {
                "total": round(total_expenses, 2),
                "total_formatted": format_currency(total_expenses),
                "breakdown": {
                    cat: round(amt, 2)
                    for cat, amt in sorted(expense_breakdown.items(), key=lambda x: -x[1])
                },
                "num_expenses": len(expenses),
            },
            "net_income": round(net_income, 2),
            "net_income_formatted": format_currency(net_income),
            "profit_margin": round((net_income / gross_revenue) * 100, 1) if gross_revenue else 0,
        }

    # ── Monthly / Annual Reports ─────────────────────────────────

    def generate_monthly_report(
        self,
        property: Property,
        bookings: list[Booking],
        year: int,
        month: int,
    ) -> str:
        """Generate a formatted monthly financial report."""
        start = date(year, month, 1)
        if month == 12:
            end = date(year + 1, 1, 1)
        else:
            end = date(year, month + 1, 1)

        pnl = self.generate_pnl(property.property_id, start, end)

        # Calculate occupancy
        month_bookings = [
            b for b in bookings
            if b.check_in < end and b.check_out > start
            and b.property_id == property.property_id
        ]
        booked_nights = sum(
            min(b.check_out, end).toordinal() - max(b.check_in, start).toordinal()
            for b in month_bookings
        )
        total_nights = (end - start).days
        occ_rate = round((booked_nights / total_nights) * 100, 1) if total_nights else 0

        avg_nightly = (
            pnl["revenue"]["gross"] / booked_nights if booked_nights else 0
        )

        expense_lines = "\n".join(
            f"  {cat}: {format_currency(amt)}"
            for cat, amt in pnl["expenses"]["breakdown"].items()
        )

        insights = self._generate_insights(pnl, occ_rate, avg_nightly)

        return render_template(
            "monthly_report_summary",
            property_name=property.name,
            month=month,
            year=year,
            total_revenue=pnl["revenue"]["gross_formatted"],
            total_expenses=pnl["expenses"]["total_formatted"],
            net_income=pnl["net_income_formatted"],
            occupancy_rate=occ_rate,
            avg_nightly_rate=format_currency(avg_nightly),
            num_bookings=pnl["revenue"]["num_bookings"],
            expense_breakdown=expense_lines or "  No expenses recorded",
            insights=insights,
        )

    def generate_annual_summary(
        self,
        property_id: str,
        year: int,
    ) -> dict:
        """Generate an annual financial summary."""
        start = date(year, 1, 1)
        end = date(year + 1, 1, 1)

        pnl = self.generate_pnl(property_id, start, end)

        # Monthly breakdown
        monthly = {}
        for month in range(1, 13):
            m_start = date(year, month, 1)
            if month == 12:
                m_end = date(year + 1, 1, 1)
            else:
                m_end = date(year, month + 1, 1)
            m_rev = sum(
                r.gross_amount for r in self.get_revenue(property_id, m_start, m_end)
            )
            m_exp = sum(
                e.amount for e in self.get_expenses(property_id, start_date=m_start, end_date=m_end)
            )
            monthly[month] = {
                "revenue": round(m_rev, 2),
                "expenses": round(m_exp, 2),
                "net": round(m_rev - m_exp, 2),
            }

        return {
            "year": year,
            "property_id": property_id,
            "annual_pnl": pnl,
            "monthly_breakdown": monthly,
            "best_month": max(monthly, key=lambda m: monthly[m]["net"]),
            "worst_month": min(monthly, key=lambda m: monthly[m]["net"]),
        }

    # ── Tax Support ──────────────────────────────────────────────

    def generate_tax_summary(
        self,
        property_id: str,
        year: int,
    ) -> dict:
        """Generate a tax preparation summary for a property."""
        start = date(year, 1, 1)
        end = date(year + 1, 1, 1)

        revenues = self.get_revenue(property_id, start, end)
        expenses = self.get_expenses(property_id, start_date=start, end_date=end)

        deductible = [e for e in expenses if e.tax_deductible]
        non_deductible = [e for e in expenses if not e.tax_deductible]

        deductible_by_category = defaultdict(float)
        for exp in deductible:
            deductible_by_category[exp.category.value] += exp.amount

        total_income = sum(r.gross_amount for r in revenues)
        total_deductible = sum(e.amount for e in deductible)

        return {
            "tax_year": year,
            "property_id": property_id,
            "gross_rental_income": round(total_income, 2),
            "gross_income_formatted": format_currency(total_income),
            "total_deductible_expenses": round(total_deductible, 2),
            "total_deductible_formatted": format_currency(total_deductible),
            "taxable_income": round(total_income - total_deductible, 2),
            "taxable_income_formatted": format_currency(total_income - total_deductible),
            "deductible_by_category": {
                cat: {
                    "amount": round(amt, 2),
                    "formatted": format_currency(amt),
                }
                for cat, amt in sorted(deductible_by_category.items(), key=lambda x: -x[1])
            },
            "non_deductible_total": round(sum(e.amount for e in non_deductible), 2),
            "num_receipts": sum(1 for e in deductible if e.receipt_url),
            "missing_receipts": sum(1 for e in deductible if not e.receipt_url),
            "note": "This is for informational purposes only. Consult a tax professional for actual tax filing.",
        }

    # ── Budget Management ────────────────────────────────────────

    def set_budget(
        self,
        property_id: str,
        category: ExpenseCategory,
        monthly_limit: float,
    ):
        """Set a monthly budget for an expense category."""
        if property_id not in self.budgets:
            self.budgets[property_id] = {}
        self.budgets[property_id][category.value] = monthly_limit

    def check_budget_status(
        self,
        property_id: str,
        year: int,
        month: int,
    ) -> list[dict]:
        """Check spending against budget for the current month."""
        if property_id not in self.budgets:
            return []

        start = date(year, month, 1)
        if month == 12:
            end = date(year + 1, 1, 1)
        else:
            end = date(year, month + 1, 1)

        results = []
        for category_name, limit in self.budgets[property_id].items():
            category = ExpenseCategory(category_name)
            spent = sum(
                e.amount
                for e in self.get_expenses(property_id, category, start, end)
            )
            remaining = limit - spent
            results.append({
                "category": category_name,
                "budget": limit,
                "spent": round(spent, 2),
                "remaining": round(remaining, 2),
                "pct_used": round((spent / limit) * 100, 1) if limit else 0,
                "over_budget": spent > limit,
            })

        return results

    # ── Helpers ───────────────────────────────────────────────────

    def _generate_insights(
        self, pnl: dict, occupancy_rate: float, avg_nightly: float
    ) -> str:
        """Generate actionable insights from financial data."""
        insights = []

        margin = pnl.get("profit_margin", 0)
        if margin > 60:
            insights.append("Strong profit margin. Operations are running efficiently.")
        elif margin > 30:
            insights.append("Healthy profit margin. Look for ways to optimize expenses further.")
        elif margin > 0:
            insights.append("Thin profit margin. Review expense categories for potential savings.")
        else:
            insights.append("Negative margin this period. Expenses exceeded revenue.")

        if occupancy_rate > 80:
            insights.append(f"Excellent occupancy at {occupancy_rate}%. Consider raising prices.")
        elif occupancy_rate > 50:
            insights.append(f"Good occupancy at {occupancy_rate}%. Room to grow with better marketing or pricing.")
        else:
            insights.append(f"Low occupancy at {occupancy_rate}%. Consider lowering prices or improving listing.")

        return "\n".join(f"• {i}" for i in insights)
