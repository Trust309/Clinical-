"""
Pricing & Revenue Agent

Handles dynamic pricing and revenue optimization:
- Base price adjustments based on demand signals
- Seasonal pricing strategies
- Weekend/weekday differentiation
- Last-minute and far-out booking pricing
- Event-based price surges
- Occupancy-driven discounts
- Competitor price awareness
- Revenue forecasting
"""

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Optional

from ..models.property import Booking, Property
from ..utils.helpers import (
    date_range,
    format_currency,
    get_season,
    is_weekend,
    occupancy_rate,
)


@dataclass
class PriceRule:
    """A pricing rule that adjusts the base price."""
    name: str
    multiplier: float
    priority: int = 0
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    days_of_week: list[int] = field(default_factory=list)  # 0=Mon, 6=Sun
    min_stay: int = 0
    active: bool = True


@dataclass
class PriceRecommendation:
    """A price recommendation for a specific date."""
    date: date
    base_price: float
    recommended_price: float
    applied_rules: list[str]
    confidence: float  # 0-1

    @property
    def adjustment_pct(self) -> float:
        if self.base_price == 0:
            return 0
        return round(((self.recommended_price - self.base_price) / self.base_price) * 100, 1)


class PricingAgent:
    """Agent responsible for dynamic pricing and revenue optimization."""

    def __init__(self):
        self.price_rules: list[PriceRule] = []
        self.price_history: list[dict] = []
        self.competitor_prices: dict[str, list[dict]] = {}
        self._setup_default_rules()

    def _setup_default_rules(self):
        """Initialize default pricing rules."""
        self.price_rules = [
            PriceRule(
                name="weekend_premium",
                multiplier=1.20,
                priority=1,
                days_of_week=[4, 5],  # Friday, Saturday
            ),
            PriceRule(
                name="summer_peak",
                multiplier=1.30,
                priority=2,
            ),
            PriceRule(
                name="winter_low",
                multiplier=0.85,
                priority=2,
            ),
            PriceRule(
                name="last_minute_discount",
                multiplier=0.88,
                priority=3,
            ),
            PriceRule(
                name="far_advance_discount",
                multiplier=0.95,
                priority=3,
            ),
            PriceRule(
                name="weekly_stay_discount",
                multiplier=0.90,
                priority=4,
                min_stay=7,
            ),
            PriceRule(
                name="monthly_stay_discount",
                multiplier=0.75,
                priority=4,
                min_stay=28,
            ),
            PriceRule(
                name="new_year_surge",
                multiplier=1.50,
                priority=5,
            ),
            PriceRule(
                name="high_demand_surge",
                multiplier=1.25,
                priority=5,
            ),
            PriceRule(
                name="low_occupancy_discount",
                multiplier=0.85,
                priority=6,
            ),
        ]

    def calculate_price(
        self,
        property: Property,
        target_date: date,
        num_nights: int = 1,
        current_occupancy: float = 50.0,
    ) -> PriceRecommendation:
        """Calculate the recommended price for a specific date."""
        base = property.base_price
        price = base
        applied_rules = []
        today = date.today()
        days_until = (target_date - today).days

        # Weekend premium
        if is_weekend(target_date):
            rule = self._get_rule("weekend_premium")
            if rule and rule.active:
                price *= rule.multiplier
                applied_rules.append(f"Weekend premium (+{int((rule.multiplier - 1) * 100)}%)")

        # Seasonal adjustments
        season = get_season(target_date)
        if season == "summer":
            rule = self._get_rule("summer_peak")
            if rule and rule.active:
                price *= rule.multiplier
                applied_rules.append(f"Summer peak (+{int((rule.multiplier - 1) * 100)}%)")
        elif season == "winter" and target_date.month not in (12,):
            rule = self._get_rule("winter_low")
            if rule and rule.active:
                price *= rule.multiplier
                applied_rules.append(f"Winter low ({int((rule.multiplier - 1) * 100)}%)")

        # New Year's surge
        if target_date.month == 12 and target_date.day >= 28:
            rule = self._get_rule("new_year_surge")
            if rule and rule.active:
                price *= rule.multiplier
                applied_rules.append("New Year's surge (+50%)")

        # Last-minute discount (within 3 days)
        if 0 < days_until <= 3 and current_occupancy < 60:
            rule = self._get_rule("last_minute_discount")
            if rule and rule.active:
                price *= rule.multiplier
                applied_rules.append("Last-minute discount (-12%)")

        # Far-advance discount (more than 90 days)
        if days_until > 90:
            rule = self._get_rule("far_advance_discount")
            if rule and rule.active:
                price *= rule.multiplier
                applied_rules.append("Advance booking discount (-5%)")

        # Length-of-stay discounts
        if num_nights >= 28:
            rule = self._get_rule("monthly_stay_discount")
            if rule and rule.active:
                price *= rule.multiplier
                applied_rules.append("Monthly stay discount (-25%)")
        elif num_nights >= 7:
            rule = self._get_rule("weekly_stay_discount")
            if rule and rule.active:
                price *= rule.multiplier
                applied_rules.append("Weekly stay discount (-10%)")

        # Occupancy-based adjustments
        if current_occupancy > 85:
            rule = self._get_rule("high_demand_surge")
            if rule and rule.active:
                price *= rule.multiplier
                applied_rules.append("High demand surge (+25%)")
        elif current_occupancy < 40:
            rule = self._get_rule("low_occupancy_discount")
            if rule and rule.active:
                price *= rule.multiplier
                applied_rules.append("Low occupancy discount (-15%)")

        confidence = self._calculate_confidence(days_until, applied_rules)

        return PriceRecommendation(
            date=target_date,
            base_price=base,
            recommended_price=round(price, 2),
            applied_rules=applied_rules,
            confidence=confidence,
        )

    def get_price_calendar(
        self,
        property: Property,
        start_date: date,
        end_date: date,
        current_occupancy: float = 50.0,
    ) -> list[PriceRecommendation]:
        """Generate a price calendar for a date range."""
        num_nights = (end_date - start_date).days
        return [
            self.calculate_price(property, d, num_nights, current_occupancy)
            for d in date_range(start_date, end_date)
        ]

    def calculate_booking_total(
        self,
        property: Property,
        check_in: date,
        check_out: date,
        current_occupancy: float = 50.0,
    ) -> dict:
        """Calculate the total price for a booking across all nights."""
        recommendations = self.get_price_calendar(
            property, check_in, check_out, current_occupancy
        )
        nightly_prices = [r.recommended_price for r in recommendations]
        subtotal = sum(nightly_prices)

        return {
            "nightly_prices": [
                {"date": r.date.isoformat(), "price": r.recommended_price, "rules": r.applied_rules}
                for r in recommendations
            ],
            "subtotal": round(subtotal, 2),
            "cleaning_fee": property.cleaning_fee,
            "total": round(subtotal + property.cleaning_fee, 2),
            "avg_nightly": round(subtotal / len(nightly_prices), 2) if nightly_prices else 0,
            "num_nights": len(nightly_prices),
        }

    def analyze_revenue(
        self,
        property: Property,
        bookings: list[Booking],
        period_start: date,
        period_end: date,
    ) -> dict:
        """Analyze revenue performance for a property over a period."""
        period_bookings = [
            b for b in bookings
            if b.check_in >= period_start and b.check_out <= period_end
        ]

        total_revenue = sum(b.total_price for b in period_bookings)
        total_nights_booked = sum(b.num_nights for b in period_bookings)
        total_nights_available = (period_end - period_start).days

        occ_rate = occupancy_rate(total_nights_booked, total_nights_available)
        avg_nightly = total_revenue / total_nights_booked if total_nights_booked else 0
        revpar = total_revenue / total_nights_available if total_nights_available else 0

        return {
            "period": f"{period_start.isoformat()} to {period_end.isoformat()}",
            "total_revenue": round(total_revenue, 2),
            "total_revenue_formatted": format_currency(total_revenue),
            "num_bookings": len(period_bookings),
            "nights_booked": total_nights_booked,
            "nights_available": total_nights_available,
            "occupancy_rate": occ_rate,
            "avg_nightly_rate": round(avg_nightly, 2),
            "avg_nightly_formatted": format_currency(avg_nightly),
            "revpar": round(revpar, 2),
            "revpar_formatted": format_currency(revpar),
        }

    def suggest_price_adjustments(
        self,
        property: Property,
        bookings: list[Booking],
        lookahead_days: int = 30,
    ) -> list[dict]:
        """Suggest price adjustments based on booking patterns."""
        suggestions = []
        today = date.today()

        # Check each upcoming date
        for day_offset in range(lookahead_days):
            target = today + timedelta(days=day_offset)
            is_booked = any(
                b.check_in <= target < b.check_out
                for b in bookings
                if b.status in ("confirmed", "checked_in")
            )

            if is_booked:
                continue

            # Calculate occupancy for the surrounding week
            week_start = target - timedelta(days=target.weekday())
            week_end = week_start + timedelta(days=7)
            week_bookings = sum(
                1 for d in date_range(week_start, week_end)
                if any(b.check_in <= d < b.check_out for b in bookings)
            )
            week_occ = occupancy_rate(week_bookings, 7)

            rec = self.calculate_price(property, target, 1, week_occ)

            if rec.adjustment_pct != 0:
                suggestions.append({
                    "date": target.isoformat(),
                    "current_price": property.base_price,
                    "recommended_price": rec.recommended_price,
                    "adjustment_pct": rec.adjustment_pct,
                    "rules": rec.applied_rules,
                    "week_occupancy": week_occ,
                    "confidence": rec.confidence,
                })

        return suggestions

    def add_custom_rule(self, rule: PriceRule):
        """Add a custom pricing rule."""
        self.price_rules.append(rule)

    def set_competitor_prices(self, competitor_name: str, prices: list[dict]):
        """Store competitor pricing data for reference."""
        self.competitor_prices[competitor_name] = prices

    def get_competitive_position(self, property: Property, target_date: date) -> dict:
        """Analyze pricing position relative to competitors."""
        my_price = self.calculate_price(property, target_date).recommended_price
        competitor_avg = 0
        count = 0

        for name, prices in self.competitor_prices.items():
            for entry in prices:
                if entry.get("date") == target_date.isoformat():
                    competitor_avg += entry["price"]
                    count += 1

        if count == 0:
            return {
                "my_price": my_price,
                "competitor_avg": None,
                "position": "no_data",
                "recommendation": "Not enough competitor data to compare.",
            }

        competitor_avg /= count
        diff_pct = ((my_price - competitor_avg) / competitor_avg) * 100

        if diff_pct > 15:
            position = "above_market"
            rec = "Consider lowering price to stay competitive."
        elif diff_pct < -15:
            position = "below_market"
            rec = "You may be underpricing. Consider raising the price."
        else:
            position = "competitive"
            rec = "Your pricing is in line with the market."

        return {
            "my_price": my_price,
            "competitor_avg": round(competitor_avg, 2),
            "difference_pct": round(diff_pct, 1),
            "position": position,
            "recommendation": rec,
        }

    def _get_rule(self, name: str) -> Optional[PriceRule]:
        """Get a pricing rule by name."""
        for rule in self.price_rules:
            if rule.name == name:
                return rule
        return None

    def _calculate_confidence(self, days_until: int, applied_rules: list) -> float:
        """Estimate confidence in the price recommendation."""
        base_confidence = 0.7

        # More data points = higher confidence
        if len(applied_rules) >= 2:
            base_confidence += 0.1

        # Nearer dates have higher confidence
        if days_until <= 7:
            base_confidence += 0.15
        elif days_until <= 30:
            base_confidence += 0.1
        elif days_until > 90:
            base_confidence -= 0.15

        # Competitor data boosts confidence
        if self.competitor_prices:
            base_confidence += 0.1

        return min(max(base_confidence, 0.1), 1.0)
