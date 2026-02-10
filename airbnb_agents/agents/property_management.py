"""
Property Management Agent

Handles property operations and maintenance:
- Cleaning schedule coordination
- Maintenance request tracking
- Inventory management
- Vendor coordination
- Property inspections
- Turnover management between guests
"""

from datetime import date, datetime, timedelta
from typing import Optional

from ..models.property import (
    Booking,
    CleaningStatus,
    CleaningTask,
    MaintenancePriority,
    MaintenanceRequest,
    MaintenanceStatus,
    Property,
)
from ..utils.helpers import format_currency, generate_id


DEFAULT_CLEANING_CHECKLIST = {
    "kitchen": [
        "Clean all countertops",
        "Wash dishes / run dishwasher",
        "Clean stovetop and oven",
        "Wipe down appliances",
        "Clean sink",
        "Empty trash and replace bag",
        "Restock dish soap and sponge",
    ],
    "bathroom": [
        "Scrub toilet inside and out",
        "Clean shower/tub",
        "Clean sink and mirror",
        "Replace towels (bath, hand, washcloth)",
        "Restock toilet paper and soap",
        "Clean floors",
        "Empty trash",
    ],
    "bedroom": [
        "Change all linens (sheets, pillowcases)",
        "Make bed with fresh bedding",
        "Dust all surfaces",
        "Empty trash",
        "Check under bed",
        "Organize closet/hangers",
    ],
    "living_area": [
        "Vacuum/mop floors",
        "Dust all surfaces",
        "Wipe remote controls",
        "Fluff and arrange pillows",
        "Clean windows (if needed)",
        "Empty trash",
    ],
    "general": [
        "Check all lights are working",
        "Check HVAC/thermostat",
        "Test smoke/CO detectors",
        "Lock all windows",
        "Set entry code for next guest",
        "Take photos of clean property",
        "Report any damage or issues",
    ],
}

INVENTORY_ESSENTIALS = {
    "bathroom": [
        {"item": "Toilet paper rolls", "min_quantity": 4},
        {"item": "Hand soap", "min_quantity": 1},
        {"item": "Shampoo", "min_quantity": 1},
        {"item": "Conditioner", "min_quantity": 1},
        {"item": "Body wash", "min_quantity": 1},
        {"item": "Bath towels", "min_quantity": 4},
        {"item": "Hand towels", "min_quantity": 4},
        {"item": "Washcloths", "min_quantity": 4},
    ],
    "kitchen": [
        {"item": "Dish soap", "min_quantity": 1},
        {"item": "Sponges", "min_quantity": 2},
        {"item": "Paper towels", "min_quantity": 2},
        {"item": "Trash bags", "min_quantity": 5},
        {"item": "Coffee/tea", "min_quantity": 1},
        {"item": "Sugar", "min_quantity": 1},
        {"item": "Salt and pepper", "min_quantity": 1},
    ],
    "general": [
        {"item": "Light bulbs (spare)", "min_quantity": 2},
        {"item": "Batteries (AA)", "min_quantity": 4},
        {"item": "First aid kit", "min_quantity": 1},
        {"item": "Fire extinguisher", "min_quantity": 1},
    ],
}


class PropertyManagementAgent:
    """Agent responsible for property operations and maintenance."""

    def __init__(self):
        self.maintenance_requests: list[MaintenanceRequest] = []
        self.cleaning_tasks: list[CleaningTask] = []
        self.inventory: dict[str, dict] = {}
        self.vendors: dict[str, dict] = {}
        self.inspection_log: list[dict] = []

    # ── Cleaning Management ──────────────────────────────────────

    def schedule_cleaning(
        self,
        property: Property,
        booking: Booking,
        cleaner_name: str = "",
        cost: float = 0.0,
    ) -> CleaningTask:
        """Schedule a cleaning task for a checkout."""
        task = CleaningTask(
            task_id=generate_id("clean"),
            property_id=property.property_id,
            booking_id=booking.booking_id,
            scheduled_date=booking.check_out,
            assigned_to=cleaner_name,
            status=CleaningStatus.PENDING,
            checklist_completed={
                area: {item: False for item in items}
                for area, items in DEFAULT_CLEANING_CHECKLIST.items()
            },
            cost=cost or property.cleaning_fee,
        )
        self.cleaning_tasks.append(task)
        return task

    def get_cleaning_schedule(
        self, property_id: str, start: date, end: date
    ) -> list[CleaningTask]:
        """Get cleaning tasks for a property within a date range."""
        return [
            t for t in self.cleaning_tasks
            if t.property_id == property_id and start <= t.scheduled_date <= end
        ]

    def update_cleaning_status(
        self, task_id: str, status: CleaningStatus, notes: str = ""
    ) -> Optional[CleaningTask]:
        """Update the status of a cleaning task."""
        for task in self.cleaning_tasks:
            if task.task_id == task_id:
                task.status = status
                if notes:
                    task.notes = notes
                return task
        return None

    def complete_checklist_item(
        self, task_id: str, area: str, item: str
    ) -> bool:
        """Mark a cleaning checklist item as completed."""
        for task in self.cleaning_tasks:
            if task.task_id == task_id:
                if area in task.checklist_completed:
                    if item in task.checklist_completed[area]:
                        task.checklist_completed[area][item] = True
                        return True
        return False

    def get_cleaning_checklist(self) -> dict:
        """Return the standard cleaning checklist."""
        return DEFAULT_CLEANING_CHECKLIST

    # ── Maintenance Management ───────────────────────────────────

    def create_maintenance_request(
        self,
        property_id: str,
        title: str,
        description: str,
        priority: MaintenancePriority = MaintenancePriority.MEDIUM,
        estimated_cost: float = 0.0,
        assigned_to: str = "",
    ) -> MaintenanceRequest:
        """Create a new maintenance request."""
        request = MaintenanceRequest(
            request_id=generate_id("maint"),
            property_id=property_id,
            title=title,
            description=description,
            priority=priority,
            estimated_cost=estimated_cost,
            assigned_to=assigned_to,
        )
        self.maintenance_requests.append(request)
        return request

    def get_maintenance_requests(
        self,
        property_id: Optional[str] = None,
        status: Optional[MaintenanceStatus] = None,
        priority: Optional[MaintenancePriority] = None,
    ) -> list[MaintenanceRequest]:
        """Get maintenance requests with optional filters."""
        results = self.maintenance_requests
        if property_id:
            results = [r for r in results if r.property_id == property_id]
        if status:
            results = [r for r in results if r.status == status]
        if priority:
            results = [r for r in results if r.priority == priority]
        return results

    def update_maintenance_status(
        self,
        request_id: str,
        status: MaintenanceStatus,
        actual_cost: Optional[float] = None,
        notes: str = "",
    ) -> Optional[MaintenanceRequest]:
        """Update the status of a maintenance request."""
        for req in self.maintenance_requests:
            if req.request_id == request_id:
                req.status = status
                if actual_cost is not None:
                    req.actual_cost = actual_cost
                if status == MaintenanceStatus.COMPLETED:
                    req.completed_at = datetime.now()
                return req
        return None

    def get_urgent_issues(self) -> list[MaintenanceRequest]:
        """Get all urgent and critical open maintenance issues."""
        return [
            r for r in self.maintenance_requests
            if r.priority in (MaintenancePriority.HIGH, MaintenancePriority.CRITICAL)
            and r.status not in (MaintenanceStatus.COMPLETED,)
        ]

    # ── Inventory Management ─────────────────────────────────────

    def initialize_inventory(self, property_id: str):
        """Initialize inventory tracking for a property."""
        self.inventory[property_id] = {}
        for area, items in INVENTORY_ESSENTIALS.items():
            for item_info in items:
                key = f"{area}:{item_info['item']}"
                self.inventory[property_id][key] = {
                    "area": area,
                    "item": item_info["item"],
                    "min_quantity": item_info["min_quantity"],
                    "current_quantity": item_info["min_quantity"],
                    "last_restocked": date.today().isoformat(),
                }

    def update_inventory(
        self, property_id: str, area: str, item: str, quantity: int
    ) -> bool:
        """Update inventory quantity for an item."""
        key = f"{area}:{item}"
        if property_id in self.inventory and key in self.inventory[property_id]:
            self.inventory[property_id][key]["current_quantity"] = quantity
            return True
        return False

    def get_low_inventory(self, property_id: str) -> list[dict]:
        """Get items that are below minimum quantity."""
        if property_id not in self.inventory:
            return []
        low_items = []
        for key, item_data in self.inventory[property_id].items():
            if item_data["current_quantity"] < item_data["min_quantity"]:
                low_items.append({
                    "area": item_data["area"],
                    "item": item_data["item"],
                    "current": item_data["current_quantity"],
                    "minimum": item_data["min_quantity"],
                    "need": item_data["min_quantity"] - item_data["current_quantity"],
                })
        return low_items

    def generate_shopping_list(self, property_id: str) -> list[dict]:
        """Generate a shopping list based on low inventory."""
        return self.get_low_inventory(property_id)

    # ── Vendor Management ────────────────────────────────────────

    def add_vendor(
        self,
        name: str,
        service_type: str,
        phone: str = "",
        email: str = "",
        rate: float = 0.0,
        notes: str = "",
    ) -> dict:
        """Add a vendor/service provider."""
        vendor_id = generate_id("vendor")
        vendor = {
            "vendor_id": vendor_id,
            "name": name,
            "service_type": service_type,
            "phone": phone,
            "email": email,
            "rate": rate,
            "notes": notes,
            "rating": None,
            "jobs_completed": 0,
        }
        self.vendors[vendor_id] = vendor
        return vendor

    def get_vendors(self, service_type: Optional[str] = None) -> list[dict]:
        """Get vendors, optionally filtered by service type."""
        vendors = list(self.vendors.values())
        if service_type:
            vendors = [v for v in vendors if v["service_type"] == service_type]
        return vendors

    # ── Turnover Management ──────────────────────────────────────

    def plan_turnover(
        self,
        property: Property,
        checkout_booking: Booking,
        checkin_booking: Optional[Booking] = None,
    ) -> dict:
        """Plan the turnover between guests."""
        checkout_date = checkout_booking.check_out
        gap_hours = None

        if checkin_booking:
            checkout_time = datetime.strptime(property.check_out_time, "%H:%M")
            checkin_time = datetime.strptime(property.check_in_time, "%H:%M")
            gap_hours = (checkin_time - checkout_time).total_seconds() / 3600

        cleaning = self.schedule_cleaning(property, checkout_booking)

        plan = {
            "checkout_date": checkout_date.isoformat(),
            "checkout_time": property.check_out_time,
            "cleaning_task_id": cleaning.task_id,
            "checklist": DEFAULT_CLEANING_CHECKLIST,
            "next_checkin": None,
            "turnaround_hours": gap_hours,
            "tight_turnaround": gap_hours is not None and gap_hours < 5,
        }

        if checkin_booking:
            plan["next_checkin"] = {
                "date": checkin_booking.check_in.isoformat(),
                "time": property.check_in_time,
                "guest_name": checkin_booking.guest.name,
                "num_guests": checkin_booking.num_guests,
            }

        return plan

    # ── Property Inspection ──────────────────────────────────────

    def log_inspection(
        self,
        property_id: str,
        inspector: str,
        findings: list[str],
        issues_found: list[dict] = None,
    ) -> dict:
        """Log a property inspection."""
        entry = {
            "inspection_id": generate_id("insp"),
            "property_id": property_id,
            "inspector": inspector,
            "date": datetime.now().isoformat(),
            "findings": findings,
            "issues_found": issues_found or [],
            "num_issues": len(issues_found) if issues_found else 0,
        }
        self.inspection_log.append(entry)

        # Auto-create maintenance requests for issues found
        if issues_found:
            for issue in issues_found:
                self.create_maintenance_request(
                    property_id=property_id,
                    title=issue.get("title", "Inspection finding"),
                    description=issue.get("description", ""),
                    priority=MaintenancePriority(issue.get("priority", "medium")),
                )

        return entry

    def get_property_status(self, property: Property) -> dict:
        """Get a comprehensive status overview of a property."""
        prop_id = property.property_id
        open_maintenance = self.get_maintenance_requests(
            property_id=prop_id, status=MaintenanceStatus.OPEN
        )
        urgent_issues = [
            r for r in open_maintenance
            if r.priority in (MaintenancePriority.HIGH, MaintenancePriority.CRITICAL)
        ]
        pending_cleanings = [
            t for t in self.cleaning_tasks
            if t.property_id == prop_id and t.status == CleaningStatus.PENDING
        ]
        low_inventory = self.get_low_inventory(prop_id)

        return {
            "property": property.name,
            "property_id": prop_id,
            "open_maintenance_count": len(open_maintenance),
            "urgent_issues_count": len(urgent_issues),
            "urgent_issues": [
                {"title": r.title, "priority": r.priority.value}
                for r in urgent_issues
            ],
            "pending_cleanings": len(pending_cleanings),
            "low_inventory_items": len(low_inventory),
            "low_inventory": low_inventory,
            "needs_attention": len(urgent_issues) > 0 or len(low_inventory) > 3,
        }
