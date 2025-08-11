from pydantic import BaseModel, Field, conint, confloat
from typing import Optional
from datetime import date, datetime

class Message(BaseModel):
    message: str

class UserIn(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: str = Field(..., min_length=3, max_length=255)

class UserOut(UserIn):
    id: int

class EmployeeIn(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    role: str = Field(..., min_length=1, max_length=255)

class EmployeeOut(EmployeeIn):
    id: int

class LocationIn(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    address: Optional[str] = Field(None, max_length=255)

class LocationOut(LocationIn):
    id: int

class ServiceIn(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    price: confloat(ge=0)

class ServiceOut(ServiceIn):
    id: int

class TimeDimIn(BaseModel):
    date: date
    year: conint(ge=1970, le=2100)
    month: conint(ge=1, le=12)
    day: conint(ge=1, le=31)

class TimeDimOut(TimeDimIn):
    id: int

class ReservationIn(BaseModel):
    user_id: int
    service_id: int
    location_id: int
    date: date

class ReservationOut(ReservationIn):
    id: int

class PaymentIn(BaseModel):
    reservation_id: int
    amount: confloat(ge=0)
    method: str = Field(..., min_length=1, max_length=64)
    paid_at: datetime

class PaymentOut(PaymentIn):
    id: int

class CancellationIn(BaseModel):
    reservation_id: int
    reason: Optional[str] = Field(None, max_length=500)
    cancelled_at: datetime

class CancellationOut(CancellationIn):
    id: int

class ReservationsPerMonthItem(BaseModel):
    year: int
    month: int
    total: int

class RevenueByServiceItem(BaseModel):
    service_id: int
    service_name: str
    revenue: float

class ReservationsByLocationItem(BaseModel):
    location_id: int
    location_name: str
    total: int

class TopUserItem(BaseModel):
    user_id: int
    total_reservations: int
