"""
Orchestrator Agent

Central coordinator that:
- Routes tasks to the appropriate specialized agent
- Manages the overall workflow across all agents
- Provides a unified interface for property management
- Generates cross-agent reports and dashboards
- Handles event-driven triggers (new booking, checkout, etc.)
"""

from datetime import date, datetime, timedelta
from typing import Optional

from ..models.property import (
    Booking,
    BookingStatus,
    ExpenseCategory,
    Guest,
    MaintenancePriority,
    Property,
)
from ..utils.helpers import format_currency, generate_id, occupancy_rate
from .guest_communication import GuestCommunicationAgent
from .pricing import PricingAgent
from .property_management import PropertyManagementAgent
from .listing_optimization import ListingOptimizationAgent
from .financial import FinancialAgent


class Orchestrator:
    """Central coordinator for all Airbnb business agents."""

    def __init__(self, host_name: str = "Your Host"):
        self.host_name = host_name
        self.guest_agent = GuestCommunicationAgent(host_name)
        self.pricing_agent = PricingAgent()
        self.property_agent = PropertyManagementAgent()
        self.listing_agent = ListingOptimizationAgent()
        self.financial_agent = FinancialAgent()

        self.properties: dict[str, Property] = {}
        self.bookings: dict[str, Booking] = {}
        self.guests: dict[str, Guest] = {}
        self.event_log: list[dict] = []

    # ── Property Management ──────────────────────────────────────

    def add_property(self, property: Property) -> str:
        """Register a new property in the system."""
        self.properties[property.property_id] = property
        self.property_agent.initialize_inventory(property.property_id)
        self._log_event("property_added", property.property_id, f"Added property: {property.name}")
        return property.property_id

    def get_property(self, property_id: str) -> Optional[Property]:
        """Get a property by ID."""
        return self.properties.get(property_id)

    def list_properties(self) -> list[Property]:
        """List all registered properties."""
        return list(self.properties.values())

    # ── Booking Lifecycle ────────────────────────────────────────

    def handle_new_inquiry(
        self,
        property_id: str,
        guest_name: str,
        guest_email: str,
        check_in: date,
        check_out: date,
        num_guests: int = 1,
        message: str = "",
    ) -> dict:
        """Handle a new booking inquiry end-to-end."""
        property = self.properties.get(property_id)
        if not property:
            return {"error": f"Property {property_id} not found"}

        guest = Guest(
            guest_id=generate_id("guest"),
            name=guest_name,
            email=guest_email,
        )
        self.guests[guest.guest_id] = guest

        # Get pricing
        pricing = self.pricing_agent.calculate_booking_total(
            property, check_in, check_out
        )

        # Generate response
        response_msg = self.guest_agent.respond_to_inquiry(
            property, guest, check_in, check_out
        )

        self._log_event("inquiry_received", property_id, f"Inquiry from {guest_name}")

        return {
            "guest_id": guest.guest_id,
            "response_message": response_msg,
            "pricing": pricing,
            "property_name": property.name,
            "available": True,
        }

    def handle_new_booking(
        self,
        property_id: str,
        guest_id: str,
        check_in: date,
        check_out: date,
        num_guests: int,
        total_price: Optional[float] = None,
    ) -> dict:
        """Process a new confirmed booking."""
        property = self.properties.get(property_id)
        guest = self.guests.get(guest_id)
        if not property or not guest:
            return {"error": "Property or guest not found"}

        # Calculate price if not provided
        if total_price is None:
            pricing = self.pricing_agent.calculate_booking_total(
                property, check_in, check_out
            )
            total_price = pricing["total"]

        booking = Booking(
            booking_id=generate_id("book"),
            property_id=property_id,
            guest=guest,
            check_in=check_in,
            check_out=check_out,
            num_guests=num_guests,
            total_price=total_price,
            cleaning_fee=property.cleaning_fee,
            status=BookingStatus.CONFIRMED,
        )
        self.bookings[booking.booking_id] = booking

        # Send confirmation
        confirmation = self.guest_agent.send_booking_confirmation(property, booking)

        # Schedule cleaning
        self.property_agent.schedule_cleaning(property, booking)

        # Record revenue
        self.financial_agent.record_revenue(booking)

        self._log_event(
            "booking_confirmed", property_id,
            f"Booking {booking.booking_id} confirmed for {guest.name}"
        )

        return {
            "booking_id": booking.booking_id,
            "confirmation_message": confirmation,
            "total_price": format_currency(total_price),
            "check_in": check_in.isoformat(),
            "check_out": check_out.isoformat(),
        }

    def handle_check_in(self, booking_id: str) -> dict:
        """Process a guest check-in."""
        booking = self.bookings.get(booking_id)
        if not booking:
            return {"error": "Booking not found"}

        property = self.properties.get(booking.property_id)
        booking.status = BookingStatus.CHECKED_IN

        instructions = self.guest_agent.send_check_in_instructions(property, booking)

        self._log_event(
            "guest_checked_in", booking.property_id,
            f"{booking.guest.name} checked in"
        )

        return {
            "booking_id": booking_id,
            "status": "checked_in",
            "instructions_sent": True,
            "instructions": instructions,
        }

    def handle_check_out(self, booking_id: str) -> dict:
        """Process a guest checkout."""
        booking = self.bookings.get(booking_id)
        if not booking:
            return {"error": "Booking not found"}

        property = self.properties.get(booking.property_id)
        booking.status = BookingStatus.CHECKED_OUT

        # Send checkout reminder (would normally be pre-scheduled)
        self.guest_agent.send_check_out_reminder(property, booking)

        # Schedule review request
        self.guest_agent.send_review_request(property, booking)

        # Check for next booking and plan turnover
        next_booking = self._get_next_booking(booking.property_id, booking.check_out)
        turnover = self.property_agent.plan_turnover(property, booking, next_booking)

        self._log_event(
            "guest_checked_out", booking.property_id,
            f"{booking.guest.name} checked out"
        )

        return {
            "booking_id": booking_id,
            "status": "checked_out",
            "review_request_sent": True,
            "turnover_plan": turnover,
            "next_guest": next_booking.guest.name if next_booking else None,
        }

    def handle_guest_message(
        self, booking_id: str, message_text: str
    ) -> dict:
        """Route and respond to an incoming guest message."""
        booking = self.bookings.get(booking_id)
        if not booking:
            return {"error": "Booking not found"}

        property = self.properties.get(booking.property_id)
        response = self.guest_agent.handle_guest_message(
            message_text, property, booking
        )

        return {
            "booking_id": booking_id,
            "guest": booking.guest.name,
            "response": response,
            "auto_generated": True,
        }

    # ── Maintenance ──────────────────────────────────────────────

    def report_issue(
        self,
        property_id: str,
        title: str,
        description: str,
        priority: str = "medium",
        reported_by: str = "",
    ) -> dict:
        """Report a maintenance issue."""
        priority_enum = MaintenancePriority(priority)
        request = self.property_agent.create_maintenance_request(
            property_id, title, description, priority_enum
        )

        # Auto-record as expense estimate
        if request.estimated_cost > 0:
            self.financial_agent.record_expense(
                property_id,
                ExpenseCategory.MAINTENANCE,
                request.estimated_cost,
                f"Maintenance: {title} (estimated)",
            )

        self._log_event(
            "maintenance_reported", property_id,
            f"Issue reported: {title} [{priority}]"
        )

        return {
            "request_id": request.request_id,
            "title": title,
            "priority": priority,
            "status": request.status.value,
        }

    # ── Pricing ──────────────────────────────────────────────────

    def get_pricing_recommendation(
        self, property_id: str, check_in: date, check_out: date
    ) -> dict:
        """Get a pricing recommendation for specific dates."""
        property = self.properties.get(property_id)
        if not property:
            return {"error": "Property not found"}

        bookings = self._get_property_bookings(property_id)
        occ = self._calculate_occupancy(property_id)

        return self.pricing_agent.calculate_booking_total(
            property, check_in, check_out, occ
        )

    def get_price_suggestions(self, property_id: str, days: int = 30) -> list[dict]:
        """Get price adjustment suggestions for upcoming dates."""
        property = self.properties.get(property_id)
        if not property:
            return []

        bookings = self._get_property_bookings(property_id)
        return self.pricing_agent.suggest_price_adjustments(property, bookings, days)

    # ── Listing ──────────────────────────────────────────────────

    def optimize_listing(self, property_id: str) -> dict:
        """Run listing optimization analysis."""
        property = self.properties.get(property_id)
        if not property:
            return {"error": "Property not found"}

        titles = self.listing_agent.generate_title(property)
        description = self.listing_agent.generate_description(property)
        score = self.listing_agent.evaluate_listing(property)
        keywords = self.listing_agent.suggest_seo_keywords(property)
        photos = self.listing_agent.get_photo_recommendations(property)

        return {
            "property": property.name,
            "suggested_titles": titles,
            "generated_description": description,
            "listing_score": {
                "overall": score.overall_score,
                "title": score.title_score,
                "description": score.description_score,
                "amenities": score.amenities_score,
                "photos": score.photos_score,
            },
            "recommendations": score.recommendations,
            "seo_keywords": keywords,
            "photo_recommendations": photos,
        }

    # ── Financial Reports ────────────────────────────────────────

    def get_financial_summary(
        self, property_id: str, start_date: date, end_date: date
    ) -> dict:
        """Get a financial summary for a property."""
        return self.financial_agent.generate_pnl(property_id, start_date, end_date)

    def get_monthly_report(
        self, property_id: str, year: int, month: int
    ) -> str:
        """Get a formatted monthly report."""
        property = self.properties.get(property_id)
        if not property:
            return "Property not found"

        bookings = self._get_property_bookings(property_id)
        return self.financial_agent.generate_monthly_report(
            property, bookings, year, month
        )

    def get_tax_summary(self, property_id: str, year: int) -> dict:
        """Get tax preparation summary."""
        return self.financial_agent.generate_tax_summary(property_id, year)

    # ── Dashboard ────────────────────────────────────────────────

    def get_dashboard(self) -> dict:
        """Get a high-level business dashboard across all properties."""
        today = date.today()
        month_start = today.replace(day=1)

        dashboard = {
            "date": today.isoformat(),
            "total_properties": len(self.properties),
            "properties": [],
            "active_bookings": 0,
            "upcoming_checkouts_today": [],
            "upcoming_checkins_today": [],
            "unread_messages": len(self.guest_agent.get_unread_messages()),
            "urgent_maintenance": [],
            "total_revenue_mtd": 0.0,
            "total_expenses_mtd": 0.0,
        }

        for prop_id, property in self.properties.items():
            prop_bookings = self._get_property_bookings(prop_id)
            active = [
                b for b in prop_bookings
                if b.status in (BookingStatus.CONFIRMED, BookingStatus.CHECKED_IN)
                and b.check_in <= today <= b.check_out
            ]
            dashboard["active_bookings"] += len(active)

            # Today's check-ins/outs
            for b in prop_bookings:
                if b.check_in == today:
                    dashboard["upcoming_checkins_today"].append({
                        "booking_id": b.booking_id,
                        "property": property.name,
                        "guest": b.guest.name,
                    })
                if b.check_out == today:
                    dashboard["upcoming_checkouts_today"].append({
                        "booking_id": b.booking_id,
                        "property": property.name,
                        "guest": b.guest.name,
                    })

            # Property status
            prop_status = self.property_agent.get_property_status(property)
            occ = self._calculate_occupancy(prop_id)

            # MTD financials
            revenues = self.financial_agent.get_revenue(prop_id, month_start, today)
            expenses = self.financial_agent.get_expenses(prop_id, start_date=month_start, end_date=today)
            mtd_rev = sum(r.gross_amount for r in revenues)
            mtd_exp = sum(e.amount for e in expenses)
            dashboard["total_revenue_mtd"] += mtd_rev
            dashboard["total_expenses_mtd"] += mtd_exp

            dashboard["properties"].append({
                "name": property.name,
                "property_id": prop_id,
                "occupancy_rate": occ,
                "active_guests": len(active),
                "revenue_mtd": format_currency(mtd_rev),
                "expenses_mtd": format_currency(mtd_exp),
                "open_issues": prop_status["open_maintenance_count"],
                "needs_attention": prop_status["needs_attention"],
            })

        # Urgent maintenance across all properties
        urgent = self.property_agent.get_urgent_issues()
        dashboard["urgent_maintenance"] = [
            {
                "property_id": r.property_id,
                "title": r.title,
                "priority": r.priority.value,
            }
            for r in urgent
        ]

        dashboard["total_revenue_mtd"] = format_currency(dashboard["total_revenue_mtd"])
        dashboard["total_expenses_mtd"] = format_currency(dashboard["total_expenses_mtd"])

        return dashboard

    def get_daily_tasks(self) -> list[dict]:
        """Get today's action items across all properties."""
        today = date.today()
        tasks = []

        # Check-ins today
        for b in self.bookings.values():
            if b.check_in == today and b.status == BookingStatus.CONFIRMED:
                tasks.append({
                    "type": "check_in",
                    "priority": "high",
                    "description": f"Send check-in instructions to {b.guest.name}",
                    "booking_id": b.booking_id,
                    "property_id": b.property_id,
                })

        # Check-outs today
        for b in self.bookings.values():
            if b.check_out == today and b.status == BookingStatus.CHECKED_IN:
                tasks.append({
                    "type": "check_out",
                    "priority": "high",
                    "description": f"Process checkout for {b.guest.name}",
                    "booking_id": b.booking_id,
                    "property_id": b.property_id,
                })

        # Pending cleanings
        for task in self.property_agent.cleaning_tasks:
            if task.scheduled_date == today and task.status.value == "pending":
                prop = self.properties.get(task.property_id)
                tasks.append({
                    "type": "cleaning",
                    "priority": "high",
                    "description": f"Cleaning due at {prop.name if prop else task.property_id}",
                    "task_id": task.task_id,
                    "property_id": task.property_id,
                })

        # Unread messages
        unread = self.guest_agent.get_unread_messages()
        for msg in unread:
            tasks.append({
                "type": "message",
                "priority": "medium",
                "description": f"Unread message in booking {msg.booking_id}",
                "booking_id": msg.booking_id,
            })

        # Urgent maintenance
        for issue in self.property_agent.get_urgent_issues():
            tasks.append({
                "type": "maintenance",
                "priority": "critical" if issue.priority == MaintenancePriority.CRITICAL else "high",
                "description": f"Urgent: {issue.title}",
                "request_id": issue.request_id,
                "property_id": issue.property_id,
            })

        # Scheduled messages due
        due_messages = self.guest_agent.get_pending_messages()
        for msg in due_messages:
            tasks.append({
                "type": "scheduled_message",
                "priority": "medium",
                "description": f"Send scheduled {msg['type']} for booking {msg['booking_id']}",
                "booking_id": msg["booking_id"],
            })

        # Sort by priority
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        tasks.sort(key=lambda t: priority_order.get(t["priority"], 99))

        return tasks

    # ── Internal Helpers ─────────────────────────────────────────

    def _get_property_bookings(self, property_id: str) -> list[Booking]:
        """Get all bookings for a property."""
        return [b for b in self.bookings.values() if b.property_id == property_id]

    def _get_next_booking(
        self, property_id: str, after_date: date
    ) -> Optional[Booking]:
        """Get the next upcoming booking for a property."""
        future = [
            b for b in self.bookings.values()
            if b.property_id == property_id
            and b.check_in >= after_date
            and b.status == BookingStatus.CONFIRMED
        ]
        if not future:
            return None
        return min(future, key=lambda b: b.check_in)

    def _calculate_occupancy(self, property_id: str, days: int = 30) -> float:
        """Calculate recent occupancy rate for a property."""
        today = date.today()
        start = today - timedelta(days=days)
        bookings = self._get_property_bookings(property_id)

        booked_nights = 0
        for b in bookings:
            if b.check_out < start or b.check_in > today:
                continue
            overlap_start = max(b.check_in, start)
            overlap_end = min(b.check_out, today)
            booked_nights += max(0, (overlap_end - overlap_start).days)

        return occupancy_rate(booked_nights, days)

    def _log_event(self, event_type: str, property_id: str, description: str):
        """Log a business event."""
        self.event_log.append({
            "event_id": generate_id("evt"),
            "type": event_type,
            "property_id": property_id,
            "description": description,
            "timestamp": datetime.now().isoformat(),
        })
