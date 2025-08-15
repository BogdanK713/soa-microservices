# analytics-service/app/models.py
import datetime as dt
from typing import Optional
from pydantic import BaseModel, Field, EmailStr

# ---------- Users ----------
class UserIn(BaseModel):
    first_name: Optional[str] = Field(None, example="Ana")
    last_name: Optional[str] = Field(None, example="Novak")
    email: EmailStr = Field(..., example="ana@example.com")

class UserOut(UserIn):
    id: int

# ---------- Time Dimension ----------
class TimeDimIn(BaseModel):
    date: dt.date = Field(..., example="2025-05-15")
    year: int = Field(..., ge=1970, le=2100, example=2025)
    month: int = Field(..., ge=1, le=12, example=5)
    day: int = Field(..., ge=1, le=31, example=15)

class TimeDimOut(TimeDimIn):
    id: int

# ---------- Employees ----------
class EmployeeIn(BaseModel):
    name: str = Field(..., example="Marko Marković")
    role: Optional[str] = Field(None, example="Barber")

class EmployeeOut(EmployeeIn):
    id: int

# ---------- Locations ----------
class LocationIn(BaseModel):
    name: str = Field(..., example="Center")
    address: Optional[str] = Field(None, example="Glavna 1")

class LocationOut(LocationIn):
    id: int

# ---------- Services ----------
class ServiceIn(BaseModel):
    name: str = Field(..., example="Haircut")
    description: Optional[str] = Field(None, example="Regular haircut")
    price: float = Field(..., ge=0, example=19.99)

class ServiceOut(ServiceIn):
    id: int

# ---------- Payments ----------
class PaymentIn(BaseModel):
    reservation_id: int = Field(..., example=101)
    amount: float = Field(..., ge=0, example=29.00)
    method: Optional[str] = Field(None, example="card")
    paid_at: dt.datetime = Field(default_factory=dt.datetime.utcnow)

class PaymentOut(PaymentIn):
    id: int

# ---------- Cancellations ----------
class CancellationIn(BaseModel):
    reservation_id: int = Field(..., example=101)
    reason: Optional[str] = Field(None, example="customer no-show")
    cancelled_at: dt.datetime = Field(default_factory=dt.datetime.utcnow)

class CancellationOut(CancellationIn):
    id: int

# ---------- Reservations ----------
class ReservationIn(BaseModel):
    user_id: int = Field(..., example=5)
    service_id: int = Field(..., example=2)
    location_id: int = Field(..., example=1)
    date: dt.date = Field(..., example="2025-05-15")
    amount: Optional[float] = Field(None, ge=0, example=29.0)

class ReservationOut(ReservationIn):
    id: int

# ---------- Analytics DTOs (za /analytics/* rute) ----------
class ReservationsPerMonthItem(BaseModel):
    month: int = Field(..., ge=1, le=12, example=5)
    count: int = Field(..., ge=0, example=42)

class RevenueByServiceItem(BaseModel):
    service_name: str = Field(..., example="Haircut")
    total_revenue: float = Field(..., ge=0, example=199.95)

class ReservationsByLocationItem(BaseModel):
    location_name: str = Field(..., example="Center")
    count: int = Field(..., ge=0, example=30)

class TopUserItem(BaseModel):
    user_id: int = Field(..., example=5)
    user_email: EmailStr = Field(..., example="ana@example.com")
    total_amount: float = Field(..., ge=0, example=349.50)
