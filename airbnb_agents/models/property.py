"""Data models for Airbnb properties and related entities."""

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import Optional


class PropertyType(Enum):
    ENTIRE_HOME = "entire_home"
    PRIVATE_ROOM = "private_room"
    SHARED_ROOM = "shared_room"
    HOTEL_ROOM = "hotel_room"


class BookingStatus(Enum):
    INQUIRY = "inquiry"
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CHECKED_IN = "checked_in"
    CHECKED_OUT = "checked_out"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class MaintenanceStatus(Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    URGENT = "urgent"


class MaintenancePriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class CleaningStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    INSPECTED = "inspected"


class ExpenseCategory(Enum):
    CLEANING = "cleaning"
    MAINTENANCE = "maintenance"
    SUPPLIES = "supplies"
    UTILITIES = "utilities"
    INSURANCE = "insurance"
    MORTGAGE = "mortgage"
    PROPERTY_TAX = "property_tax"
    MANAGEMENT_FEE = "management_fee"
    MARKETING = "marketing"
    FURNISHING = "furnishing"
    OTHER = "other"


@dataclass
class Property:
    property_id: str
    name: str
    address: str
    property_type: PropertyType
    bedrooms: int
    bathrooms: int
    max_guests: int
    base_price: float
    cleaning_fee: float
    amenities: list = field(default_factory=list)
    house_rules: list = field(default_factory=list)
    check_in_time: str = "15:00"
    check_out_time: str = "11:00"
    wifi_password: str = ""
    lockbox_code: str = ""
    parking_info: str = ""
    special_instructions: str = ""
    active: bool = True
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class Guest:
    guest_id: str
    name: str
    email: str
    phone: str = ""
    language: str = "en"
    previous_stays: int = 0
    rating: Optional[float] = None
    notes: str = ""


@dataclass
class Booking:
    booking_id: str
    property_id: str
    guest: Guest
    check_in: date
    check_out: date
    num_guests: int
    total_price: float
    cleaning_fee: float
    service_fee: float = 0.0
    status: BookingStatus = BookingStatus.PENDING
    special_requests: str = ""
    created_at: datetime = field(default_factory=datetime.now)

    @property
    def num_nights(self) -> int:
        return (self.check_out - self.check_in).days

    @property
    def nightly_rate(self) -> float:
        if self.num_nights == 0:
            return 0
        return (self.total_price - self.cleaning_fee - self.service_fee) / self.num_nights


@dataclass
class MaintenanceRequest:
    request_id: str
    property_id: str
    title: str
    description: str
    priority: MaintenancePriority = MaintenancePriority.MEDIUM
    status: MaintenanceStatus = MaintenanceStatus.OPEN
    estimated_cost: float = 0.0
    actual_cost: float = 0.0
    assigned_to: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None


@dataclass
class CleaningTask:
    task_id: str
    property_id: str
    booking_id: str
    scheduled_date: date
    assigned_to: str = ""
    status: CleaningStatus = CleaningStatus.PENDING
    checklist_completed: dict = field(default_factory=dict)
    notes: str = ""
    cost: float = 0.0


@dataclass
class Expense:
    expense_id: str
    property_id: str
    category: ExpenseCategory
    amount: float
    description: str
    date: date
    receipt_url: str = ""
    tax_deductible: bool = True
    vendor: str = ""


@dataclass
class Revenue:
    booking_id: str
    property_id: str
    gross_amount: float
    platform_fee: float
    cleaning_fee: float
    net_amount: float
    payout_date: Optional[date] = None
    date: date = field(default_factory=date.today)


@dataclass
class Message:
    message_id: str
    booking_id: str
    sender: str  # "host" or "guest"
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    read: bool = False
    auto_generated: bool = False
