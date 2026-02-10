"""
Guest Communication Agent

Handles all guest-facing communication throughout the booking lifecycle:
- Responding to inquiries and questions
- Booking confirmations
- Pre-arrival check-in instructions
- During-stay support
- Check-out reminders
- Post-stay review requests
- Automated message scheduling
"""

from datetime import date, datetime, timedelta
from typing import Optional

from ..models.property import (
    Booking,
    BookingStatus,
    Guest,
    Message,
    Property,
)
from ..utils.helpers import format_currency, generate_id
from ..utils.templates import render_template


class GuestCommunicationAgent:
    """Agent responsible for managing all guest communications."""

    def __init__(self, host_name: str = "Your Host"):
        self.host_name = host_name
        self.message_log: list[Message] = []
        self.scheduled_messages: list[dict] = []
        self.auto_responses: dict[str, str] = {}
        self._setup_auto_responses()

    def _setup_auto_responses(self):
        """Configure keyword-based auto-responses for common questions."""
        self.auto_responses = {
            "wifi": "The WiFi details are included in your check-in instructions. Let me resend them for you!",
            "parking": "I'll send you the parking details right away.",
            "check-in": "Check-in time is {check_in_time}. I'll send full instructions the day before your arrival.",
            "check-out": "Check-out time is {check_out_time}. I'll send a reminder the evening before.",
            "early check-in": "I'll do my best to accommodate early check-in. Let me check with our cleaning team and get back to you.",
            "late check-out": "I'll check if late check-out is available for your dates and get back to you shortly.",
            "towels": "Extra towels are available in the linen closet. Let me know if you need anything else!",
            "hot water": "I'm sorry you're having trouble with the hot water. Let me walk you through the water heater, or I can send someone over.",
            "noise": "I'm sorry about the noise. I'll look into this and address it right away.",
            "cancel": "I understand plans change. Please check the cancellation policy in your booking details, or I can walk you through the options.",
            "extend": "I'd love to extend your stay! Let me check availability for those extra nights.",
            "recommend": "I'd be happy to share some local recommendations! What are you looking for — restaurants, activities, or sightseeing?",
        }

    def respond_to_inquiry(
        self, property: Property, guest: Guest, check_in: date, check_out: date
    ) -> str:
        """Generate a response to a new booking inquiry."""
        num_nights = (check_out - check_in).days
        nightly_total = property.base_price * num_nights
        total = nightly_total + property.cleaning_fee

        amenities_text = ", ".join(property.amenities[:6]) if property.amenities else "all essentials included"
        property_details = (
            f"The space features {property.bedrooms} bedroom(s), "
            f"{property.bathrooms} bathroom(s), and accommodates up to "
            f"{property.max_guests} guests. Amenities include: {amenities_text}."
        )

        message = render_template(
            "inquiry_response",
            guest_name=guest.name,
            property_name=property.name,
            property_details=property_details,
            check_in=check_in.strftime("%B %d, %Y"),
            check_out=check_out.strftime("%B %d, %Y"),
            num_nights=num_nights,
            total_price=format_currency(total),
            host_name=self.host_name,
        )

        self._log_message(
            booking_id="inquiry",
            sender="host",
            content=message,
            auto_generated=True,
        )
        return message

    def send_booking_confirmation(self, property: Property, booking: Booking) -> str:
        """Send a booking confirmation message to the guest."""
        message = render_template(
            "booking_confirmation",
            guest_name=booking.guest.name,
            property_name=property.name,
            check_in=booking.check_in.strftime("%B %d, %Y"),
            check_out=booking.check_out.strftime("%B %d, %Y"),
            check_in_time=property.check_in_time,
            check_out_time=property.check_out_time,
            num_guests=booking.num_guests,
            total_price=format_currency(booking.total_price),
            host_name=self.host_name,
        )

        self._log_message(booking.booking_id, "host", message, auto_generated=True)

        # Schedule follow-up messages
        self._schedule_check_in_instructions(property, booking)
        self._schedule_check_out_reminder(property, booking)
        self._schedule_review_request(property, booking)

        return message

    def send_check_in_instructions(self, property: Property, booking: Booking) -> str:
        """Send detailed check-in instructions to the guest."""
        house_rules = "\n".join(f"  - {rule}" for rule in property.house_rules) if property.house_rules else "  - Please treat the space as your own"

        access_instructions = property.special_instructions or f"Lockbox code: {property.lockbox_code}"

        message = render_template(
            "check_in_instructions",
            guest_name=booking.guest.name,
            property_name=property.name,
            address=property.address,
            check_in_time=property.check_in_time,
            access_instructions=access_instructions,
            wifi_network=property.name.replace(" ", "_") + "_WiFi",
            wifi_password=property.wifi_password or "See printed card in the unit",
            parking_info=property.parking_info or "Street parking available",
            house_rules=house_rules,
            host_name=self.host_name,
        )

        self._log_message(booking.booking_id, "host", message, auto_generated=True)
        return message

    def send_check_out_reminder(self, property: Property, booking: Booking) -> str:
        """Send a check-out reminder to the guest."""
        message = render_template(
            "check_out_reminder",
            guest_name=booking.guest.name,
            property_name=property.name,
            check_out_time=property.check_out_time,
            key_instructions=property.special_instructions or "where you found them",
            host_name=self.host_name,
        )

        self._log_message(booking.booking_id, "host", message, auto_generated=True)
        return message

    def send_review_request(self, property: Property, booking: Booking) -> str:
        """Send a review request after checkout."""
        message = render_template(
            "review_request",
            guest_name=booking.guest.name,
            property_name=property.name,
            host_name=self.host_name,
        )

        self._log_message(booking.booking_id, "host", message, auto_generated=True)
        return message

    def handle_guest_message(
        self, message_text: str, property: Property, booking: Booking
    ) -> str:
        """Process an incoming guest message and generate an appropriate response."""
        self._log_message(booking.booking_id, "guest", message_text)

        message_lower = message_text.lower()

        # Check for keyword matches
        for keyword, response in self.auto_responses.items():
            if keyword in message_lower:
                formatted_response = response.format(
                    check_in_time=property.check_in_time,
                    check_out_time=property.check_out_time,
                )
                full_response = f"Hi {booking.guest.name},\n\n{formatted_response}\n\nBest,\n{self.host_name}"
                self._log_message(
                    booking.booking_id, "host", full_response, auto_generated=True
                )
                return full_response

        # Default response for unrecognized messages
        default = (
            f"Hi {booking.guest.name},\n\n"
            f"Thanks for reaching out! I've received your message and will "
            f"get back to you shortly.\n\n"
            f"Best,\n{self.host_name}"
        )
        self._log_message(booking.booking_id, "host", default, auto_generated=True)
        return default

    def get_pending_messages(self) -> list[dict]:
        """Get all scheduled messages that are due to be sent."""
        now = datetime.now()
        due = [m for m in self.scheduled_messages if m["send_at"] <= now]
        return due

    def get_scheduled_messages(self) -> list[dict]:
        """Get all future scheduled messages."""
        now = datetime.now()
        return [m for m in self.scheduled_messages if m["send_at"] > now]

    def get_conversation_history(self, booking_id: str) -> list[Message]:
        """Retrieve message history for a booking."""
        return [m for m in self.message_log if m.booking_id == booking_id]

    def get_unread_messages(self) -> list[Message]:
        """Get all unread messages from guests."""
        return [m for m in self.message_log if not m.read and m.sender == "guest"]

    def generate_guest_summary(self, guest: Guest, bookings: list[Booking]) -> str:
        """Generate a summary of a guest's history for context."""
        total_spent = sum(b.total_price for b in bookings)
        total_nights = sum(b.num_nights for b in bookings)

        summary = f"Guest: {guest.name}\n"
        summary += f"Email: {guest.email}\n"
        summary += f"Total stays: {len(bookings)}\n"
        summary += f"Total nights: {total_nights}\n"
        summary += f"Total spent: {format_currency(total_spent)}\n"
        if guest.rating:
            summary += f"Rating: {guest.rating}/5\n"
        if guest.notes:
            summary += f"Notes: {guest.notes}\n"
        return summary

    def _schedule_check_in_instructions(self, property: Property, booking: Booking):
        """Schedule check-in instructions to be sent the day before arrival."""
        send_at = datetime.combine(
            booking.check_in - timedelta(days=1),
            datetime.strptime("14:00", "%H:%M").time(),
        )
        self.scheduled_messages.append({
            "type": "check_in_instructions",
            "booking_id": booking.booking_id,
            "property_id": property.property_id,
            "send_at": send_at,
            "sent": False,
        })

    def _schedule_check_out_reminder(self, property: Property, booking: Booking):
        """Schedule a check-out reminder for the evening before departure."""
        send_at = datetime.combine(
            booking.check_out - timedelta(days=1),
            datetime.strptime("18:00", "%H:%M").time(),
        )
        self.scheduled_messages.append({
            "type": "check_out_reminder",
            "booking_id": booking.booking_id,
            "property_id": property.property_id,
            "send_at": send_at,
            "sent": False,
        })

    def _schedule_review_request(self, property: Property, booking: Booking):
        """Schedule a review request for the day after checkout."""
        send_at = datetime.combine(
            booking.check_out + timedelta(days=1),
            datetime.strptime("10:00", "%H:%M").time(),
        )
        self.scheduled_messages.append({
            "type": "review_request",
            "booking_id": booking.booking_id,
            "property_id": property.property_id,
            "send_at": send_at,
            "sent": False,
        })

    def _log_message(
        self,
        booking_id: str,
        sender: str,
        content: str,
        auto_generated: bool = False,
    ):
        """Log a message to the conversation history."""
        msg = Message(
            message_id=generate_id("msg"),
            booking_id=booking_id,
            sender=sender,
            content=content,
            auto_generated=auto_generated,
        )
        self.message_log.append(msg)
