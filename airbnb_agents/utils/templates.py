"""Message templates for guest communication."""


TEMPLATES = {
    "inquiry_response": (
        "Hi {guest_name},\n\n"
        "Thank you for your interest in {property_name}! "
        "I'd be happy to host you.\n\n"
        "{property_details}\n\n"
        "The space is available for your requested dates "
        "({check_in} to {check_out}). "
        "The total for {num_nights} night(s) would be {total_price}.\n\n"
        "Please let me know if you have any questions!\n\n"
        "Best regards,\n{host_name}"
    ),

    "booking_confirmation": (
        "Hi {guest_name},\n\n"
        "Great news — your booking at {property_name} is confirmed!\n\n"
        "Booking Details:\n"
        "- Check-in: {check_in} at {check_in_time}\n"
        "- Check-out: {check_out} at {check_out_time}\n"
        "- Guests: {num_guests}\n"
        "- Total: {total_price}\n\n"
        "I'll send you check-in instructions closer to your arrival date.\n\n"
        "Looking forward to hosting you!\n{host_name}"
    ),

    "check_in_instructions": (
        "Hi {guest_name},\n\n"
        "Welcome! Here are your check-in instructions for {property_name}:\n\n"
        "Address: {address}\n"
        "Check-in time: {check_in_time}\n\n"
        "Access Instructions:\n"
        "{access_instructions}\n\n"
        "WiFi Network: {wifi_network}\n"
        "WiFi Password: {wifi_password}\n\n"
        "Parking: {parking_info}\n\n"
        "House Rules:\n{house_rules}\n\n"
        "If you need anything during your stay, don't hesitate to reach out!\n\n"
        "Enjoy your stay!\n{host_name}"
    ),

    "check_out_reminder": (
        "Hi {guest_name},\n\n"
        "I hope you've been enjoying your stay at {property_name}!\n\n"
        "Just a friendly reminder that check-out is tomorrow at {check_out_time}.\n\n"
        "Before you leave, please:\n"
        "- Lock all doors and windows\n"
        "- Turn off all lights and appliances\n"
        "- Place used towels in the bathroom\n"
        "- Take out any trash\n"
        "- Leave the keys {key_instructions}\n\n"
        "Thank you for being a wonderful guest! "
        "If you enjoyed your stay, I'd really appreciate a review.\n\n"
        "Safe travels!\n{host_name}"
    ),

    "review_request": (
        "Hi {guest_name},\n\n"
        "Thank you for staying at {property_name}! "
        "I hope you had a wonderful time.\n\n"
        "If you have a moment, I'd really appreciate if you could leave a review "
        "of your experience. Your feedback helps future guests and helps me "
        "continue improving.\n\n"
        "Thank you again for choosing to stay with us!\n\n"
        "Best,\n{host_name}"
    ),

    "maintenance_notification": (
        "Maintenance Alert - {property_name}\n\n"
        "Issue: {issue_title}\n"
        "Priority: {priority}\n"
        "Description: {description}\n\n"
        "Assigned to: {assigned_to}\n"
        "Estimated cost: {estimated_cost}\n\n"
        "Please address this {urgency}."
    ),

    "cleaning_assignment": (
        "Cleaning Assignment - {property_name}\n\n"
        "Date: {scheduled_date}\n"
        "Check-out at: {check_out_time}\n"
        "Next check-in at: {next_check_in_time}\n\n"
        "Checklist:\n{checklist}\n\n"
        "Please confirm when completed."
    ),

    "price_adjustment_alert": (
        "Price Adjustment - {property_name}\n\n"
        "Date Range: {start_date} to {end_date}\n"
        "Previous Price: {old_price}/night\n"
        "New Price: {new_price}/night\n"
        "Reason: {reason}\n\n"
        "Expected impact: {expected_impact}"
    ),

    "monthly_report_summary": (
        "Monthly Report - {property_name} - {month}/{year}\n\n"
        "Revenue: {total_revenue}\n"
        "Expenses: {total_expenses}\n"
        "Net Income: {net_income}\n"
        "Occupancy Rate: {occupancy_rate}%\n"
        "Average Nightly Rate: {avg_nightly_rate}\n"
        "Number of Bookings: {num_bookings}\n\n"
        "Top Expense Categories:\n{expense_breakdown}\n\n"
        "{insights}"
    ),
}


def render_template(template_name: str, **kwargs) -> str:
    """Render a message template with the given variables."""
    template = TEMPLATES.get(template_name)
    if not template:
        raise ValueError(f"Unknown template: {template_name}")
    try:
        return template.format(**kwargs)
    except KeyError as e:
        raise ValueError(f"Missing template variable: {e}")
