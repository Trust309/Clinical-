"""
Flask API for the Airbnb Business Agents system.

Provides REST endpoints to interact with all agents through the Orchestrator.
"""

from datetime import date, datetime
from flask import Flask, jsonify, request
from flask_cors import CORS

from .agents.orchestrator import Orchestrator
from .models.property import Property, PropertyType, ExpenseCategory, MaintenancePriority
from .config import HOST_NAME

app = Flask(__name__)
CORS(app)

orchestrator = Orchestrator(host_name=HOST_NAME)


# ── Property Endpoints ───────────────────────────────────────────

@app.route("/api/properties", methods=["GET"])
def list_properties():
    """List all properties."""
    props = orchestrator.list_properties()
    return jsonify({
        "properties": [
            {
                "property_id": p.property_id,
                "name": p.name,
                "address": p.address,
                "type": p.property_type.value,
                "bedrooms": p.bedrooms,
                "bathrooms": p.bathrooms,
                "max_guests": p.max_guests,
                "base_price": p.base_price,
            }
            for p in props
        ]
    })


@app.route("/api/properties", methods=["POST"])
def add_property():
    """Add a new property."""
    data = request.json
    prop = Property(
        property_id=data.get("property_id", ""),
        name=data["name"],
        address=data["address"],
        property_type=PropertyType(data.get("type", "entire_home")),
        bedrooms=data.get("bedrooms", 1),
        bathrooms=data.get("bathrooms", 1),
        max_guests=data.get("max_guests", 2),
        base_price=data.get("base_price", 100.0),
        cleaning_fee=data.get("cleaning_fee", 50.0),
        amenities=data.get("amenities", []),
        house_rules=data.get("house_rules", []),
        check_in_time=data.get("check_in_time", "15:00"),
        check_out_time=data.get("check_out_time", "11:00"),
        wifi_password=data.get("wifi_password", ""),
        lockbox_code=data.get("lockbox_code", ""),
        parking_info=data.get("parking_info", ""),
    )
    if not prop.property_id:
        from .utils.helpers import generate_id
        prop.property_id = generate_id("prop")

    orchestrator.add_property(prop)
    return jsonify({"property_id": prop.property_id, "name": prop.name}), 201


# ── Booking Endpoints ────────────────────────────────────────────

@app.route("/api/inquiries", methods=["POST"])
def handle_inquiry():
    """Handle a new booking inquiry."""
    data = request.json
    result = orchestrator.handle_new_inquiry(
        property_id=data["property_id"],
        guest_name=data["guest_name"],
        guest_email=data["guest_email"],
        check_in=date.fromisoformat(data["check_in"]),
        check_out=date.fromisoformat(data["check_out"]),
        num_guests=data.get("num_guests", 1),
        message=data.get("message", ""),
    )
    return jsonify(result)


@app.route("/api/bookings", methods=["POST"])
def create_booking():
    """Create a new confirmed booking."""
    data = request.json
    result = orchestrator.handle_new_booking(
        property_id=data["property_id"],
        guest_id=data["guest_id"],
        check_in=date.fromisoformat(data["check_in"]),
        check_out=date.fromisoformat(data["check_out"]),
        num_guests=data.get("num_guests", 1),
        total_price=data.get("total_price"),
    )
    return jsonify(result), 201


@app.route("/api/bookings/<booking_id>/check-in", methods=["POST"])
def check_in(booking_id):
    """Process a guest check-in."""
    return jsonify(orchestrator.handle_check_in(booking_id))


@app.route("/api/bookings/<booking_id>/check-out", methods=["POST"])
def check_out(booking_id):
    """Process a guest check-out."""
    return jsonify(orchestrator.handle_check_out(booking_id))


@app.route("/api/bookings/<booking_id>/messages", methods=["POST"])
def send_message(booking_id):
    """Handle an incoming guest message."""
    data = request.json
    result = orchestrator.handle_guest_message(booking_id, data["message"])
    return jsonify(result)


# ── Pricing Endpoints ────────────────────────────────────────────

@app.route("/api/pricing/<property_id>", methods=["GET"])
def get_pricing(property_id):
    """Get pricing recommendation for dates."""
    check_in = date.fromisoformat(request.args["check_in"])
    check_out = date.fromisoformat(request.args["check_out"])
    result = orchestrator.get_pricing_recommendation(property_id, check_in, check_out)
    return jsonify(result)


@app.route("/api/pricing/<property_id>/suggestions", methods=["GET"])
def get_price_suggestions(property_id):
    """Get price adjustment suggestions."""
    days = int(request.args.get("days", 30))
    suggestions = orchestrator.get_price_suggestions(property_id, days)
    return jsonify({"suggestions": suggestions})


# ── Listing Endpoints ────────────────────────────────────────────

@app.route("/api/listings/<property_id>/optimize", methods=["GET"])
def optimize_listing(property_id):
    """Run listing optimization analysis."""
    return jsonify(orchestrator.optimize_listing(property_id))


# ── Maintenance Endpoints ────────────────────────────────────────

@app.route("/api/maintenance", methods=["POST"])
def report_issue():
    """Report a maintenance issue."""
    data = request.json
    result = orchestrator.report_issue(
        property_id=data["property_id"],
        title=data["title"],
        description=data.get("description", ""),
        priority=data.get("priority", "medium"),
    )
    return jsonify(result), 201


@app.route("/api/maintenance/<property_id>", methods=["GET"])
def get_maintenance(property_id):
    """Get maintenance requests for a property."""
    requests_list = orchestrator.property_agent.get_maintenance_requests(property_id)
    return jsonify({
        "requests": [
            {
                "request_id": r.request_id,
                "title": r.title,
                "priority": r.priority.value,
                "status": r.status.value,
                "created_at": r.created_at.isoformat(),
            }
            for r in requests_list
        ]
    })


# ── Financial Endpoints ──────────────────────────────────────────

@app.route("/api/financials/<property_id>/summary", methods=["GET"])
def financial_summary(property_id):
    """Get financial summary for a property."""
    start = date.fromisoformat(request.args["start_date"])
    end = date.fromisoformat(request.args["end_date"])
    return jsonify(orchestrator.get_financial_summary(property_id, start, end))


@app.route("/api/financials/<property_id>/report/<int:year>/<int:month>", methods=["GET"])
def monthly_report(property_id, year, month):
    """Get monthly financial report."""
    report = orchestrator.get_monthly_report(property_id, year, month)
    return jsonify({"report": report})


@app.route("/api/financials/<property_id>/tax/<int:year>", methods=["GET"])
def tax_summary(property_id, year):
    """Get tax preparation summary."""
    return jsonify(orchestrator.get_tax_summary(property_id, year))


@app.route("/api/expenses", methods=["POST"])
def record_expense():
    """Record a new expense."""
    data = request.json
    expense = orchestrator.financial_agent.record_expense(
        property_id=data["property_id"],
        category=ExpenseCategory(data["category"]),
        amount=data["amount"],
        description=data["description"],
        vendor=data.get("vendor", ""),
    )
    return jsonify({
        "expense_id": expense.expense_id,
        "amount": expense.amount,
        "category": expense.category.value,
    }), 201


# ── Dashboard Endpoints ──────────────────────────────────────────

@app.route("/api/dashboard", methods=["GET"])
def dashboard():
    """Get the business dashboard."""
    return jsonify(orchestrator.get_dashboard())


@app.route("/api/tasks", methods=["GET"])
def daily_tasks():
    """Get today's action items."""
    return jsonify({"tasks": orchestrator.get_daily_tasks()})


# ── API Info ─────────────────────────────────────────────────────

@app.route("/", methods=["GET"])
def api_info():
    """API information."""
    return jsonify({
        "name": "Airbnb Business Agents API",
        "version": "1.0.0",
        "endpoints": {
            "properties": "/api/properties",
            "inquiries": "/api/inquiries",
            "bookings": "/api/bookings",
            "pricing": "/api/pricing/<property_id>",
            "listings": "/api/listings/<property_id>/optimize",
            "maintenance": "/api/maintenance",
            "financials": "/api/financials/<property_id>/summary",
            "dashboard": "/api/dashboard",
            "tasks": "/api/tasks",
        },
    })


def run():
    """Run the API server."""
    app.run(host="0.0.0.0", port=5001, debug=True)


if __name__ == "__main__":
    run()
