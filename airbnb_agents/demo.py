"""
Demo script showing the Airbnb Business Agents system in action.

Run: python -m airbnb_agents.demo
"""

from datetime import date, timedelta

from .agents.orchestrator import Orchestrator
from .models.property import Property, PropertyType, ExpenseCategory


def run_demo():
    print("=" * 60)
    print("  AIRBNB BUSINESS AGENTS - DEMO")
    print("=" * 60)

    # ── Setup ────────────────────────────────────────────────
    host = Orchestrator(host_name="Alex")

    # Add a property
    prop = Property(
        property_id="prop_001",
        name="Sunny Downtown Loft",
        address="123 Main St, Austin, TX 78701",
        property_type=PropertyType.ENTIRE_HOME,
        bedrooms=2,
        bathrooms=1,
        max_guests=4,
        base_price=150.00,
        cleaning_fee=75.00,
        amenities=["WiFi", "Kitchen", "Air conditioning", "Washer", "Dryer",
                    "Free parking", "TV", "Coffee maker", "Workspace"],
        house_rules=["No smoking", "No parties", "Quiet hours 10 PM - 8 AM",
                      "Max 4 guests"],
        wifi_password="SunnyLoft2025",
        lockbox_code="4821",
        parking_info="Free driveway parking for 1 vehicle",
    )
    host.add_property(prop)
    print(f"\n[+] Property added: {prop.name}")

    # ── 1. Handle an Inquiry ─────────────────────────────────
    print("\n" + "-" * 60)
    print("1. HANDLING A GUEST INQUIRY")
    print("-" * 60)

    check_in = date.today() + timedelta(days=14)
    check_out = check_in + timedelta(days=3)

    inquiry = host.handle_new_inquiry(
        property_id="prop_001",
        guest_name="Sarah Johnson",
        guest_email="sarah@example.com",
        check_in=check_in,
        check_out=check_out,
        num_guests=2,
    )
    print(f"\nGuest: Sarah Johnson")
    print(f"Dates: {check_in} to {check_out}")
    print(f"\nAuto-generated response:\n{inquiry['response_message'][:300]}...")
    print(f"\nPricing: {inquiry['pricing']['num_nights']} nights = ${inquiry['pricing']['total']}")

    # ── 2. Confirm Booking ───────────────────────────────────
    print("\n" + "-" * 60)
    print("2. CONFIRMING THE BOOKING")
    print("-" * 60)

    booking = host.handle_new_booking(
        property_id="prop_001",
        guest_id=inquiry["guest_id"],
        check_in=check_in,
        check_out=check_out,
        num_guests=2,
    )
    booking_id = booking["booking_id"]
    print(f"\nBooking confirmed: {booking_id}")
    print(f"Total: {booking['total_price']}")
    print(f"Confirmation sent to guest.")
    print(f"Scheduled: check-in instructions, checkout reminder, review request")

    # ── 3. Guest Message ─────────────────────────────────────
    print("\n" + "-" * 60)
    print("3. HANDLING A GUEST MESSAGE")
    print("-" * 60)

    msg_result = host.handle_guest_message(
        booking_id, "Hi! Is there WiFi at the apartment?"
    )
    print(f"\nGuest asks: 'Is there WiFi at the apartment?'")
    print(f"\nAuto-response:\n{msg_result['response']}")

    # ── 4. Check-in ──────────────────────────────────────────
    print("\n" + "-" * 60)
    print("4. PROCESSING CHECK-IN")
    print("-" * 60)

    checkin_result = host.handle_check_in(booking_id)
    print(f"\nCheck-in processed for booking {booking_id}")
    print(f"Instructions sent: {checkin_result['instructions_sent']}")
    print(f"\nInstructions preview:\n{checkin_result['instructions'][:300]}...")

    # ── 5. Report an Issue ───────────────────────────────────
    print("\n" + "-" * 60)
    print("5. REPORTING A MAINTENANCE ISSUE")
    print("-" * 60)

    issue = host.report_issue(
        property_id="prop_001",
        title="Leaky kitchen faucet",
        description="Guest reported a slow drip from the kitchen faucet",
        priority="medium",
    )
    print(f"\nMaintenance request created: {issue['request_id']}")
    print(f"Priority: {issue['priority']}")

    # ── 6. Record Expense ────────────────────────────────────
    print("\n" + "-" * 60)
    print("6. RECORDING EXPENSES")
    print("-" * 60)

    host.financial_agent.record_expense(
        "prop_001", ExpenseCategory.CLEANING, 75.00,
        "Post-checkout cleaning", vendor="CleanCo"
    )
    host.financial_agent.record_expense(
        "prop_001", ExpenseCategory.SUPPLIES, 45.00,
        "Restocking toiletries and linens"
    )
    host.financial_agent.record_expense(
        "prop_001", ExpenseCategory.UTILITIES, 120.00,
        "Monthly electric bill"
    )
    print("\nRecorded 3 expenses: cleaning ($75), supplies ($45), utilities ($120)")

    # ── 7. Check-out ─────────────────────────────────────────
    print("\n" + "-" * 60)
    print("7. PROCESSING CHECK-OUT")
    print("-" * 60)

    checkout_result = host.handle_check_out(booking_id)
    print(f"\nCheck-out processed for booking {booking_id}")
    print(f"Review request sent: {checkout_result['review_request_sent']}")
    print(f"Turnover tight: {checkout_result['turnover_plan']['tight_turnaround']}")

    # ── 8. Pricing Suggestions ───────────────────────────────
    print("\n" + "-" * 60)
    print("8. PRICING SUGGESTIONS")
    print("-" * 60)

    suggestions = host.get_price_suggestions("prop_001", days=14)
    print(f"\nPrice suggestions for next 14 days: {len(suggestions)} adjustments")
    for s in suggestions[:5]:
        print(f"  {s['date']}: ${s['current_price']} -> ${s['recommended_price']} ({s['adjustment_pct']:+.1f}%)")

    # ── 9. Listing Optimization ──────────────────────────────
    print("\n" + "-" * 60)
    print("9. LISTING OPTIMIZATION")
    print("-" * 60)

    optimization = host.optimize_listing("prop_001")
    print(f"\nListing Score: {optimization['listing_score']['overall']}/100")
    print(f"\nSuggested Titles:")
    for t in optimization["suggested_titles"]:
        print(f"  - {t}")
    print(f"\nRecommendations:")
    for r in optimization["recommendations"]:
        print(f"  * {r}")

    # ── 10. Dashboard ────────────────────────────────────────
    print("\n" + "-" * 60)
    print("10. BUSINESS DASHBOARD")
    print("-" * 60)

    dashboard = host.get_dashboard()
    print(f"\nTotal Properties: {dashboard['total_properties']}")
    print(f"Active Bookings: {dashboard['active_bookings']}")
    print(f"Revenue MTD: {dashboard['total_revenue_mtd']}")
    print(f"Expenses MTD: {dashboard['total_expenses_mtd']}")
    print(f"Unread Messages: {dashboard['unread_messages']}")
    print(f"Urgent Maintenance: {len(dashboard['urgent_maintenance'])}")

    for p in dashboard["properties"]:
        print(f"\n  {p['name']}:")
        print(f"    Occupancy: {p['occupancy_rate']}%")
        print(f"    Revenue MTD: {p['revenue_mtd']}")
        print(f"    Open Issues: {p['open_issues']}")

    # ── 11. Daily Tasks ──────────────────────────────────────
    print("\n" + "-" * 60)
    print("11. TODAY'S TASKS")
    print("-" * 60)

    tasks = host.get_daily_tasks()
    if tasks:
        for t in tasks:
            print(f"  [{t['priority'].upper()}] {t['description']}")
    else:
        print("  No tasks for today!")

    print("\n" + "=" * 60)
    print("  DEMO COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    run_demo()
