from fastapi import FastAPI
from app.routes import reservation, user, employee, location, service, time, payment, cancellation, analytics

app = FastAPI(
    title="Analytics (Reservation) Service",
    description="FastAPI service for analytics with full CRUD support",
    version="1.0.0"
)

app.include_router(reservation.router, prefix="/reservations")
app.include_router(user.router, prefix="/users")
app.include_router(employee.router, prefix="/employees")
app.include_router(location.router, prefix="/locations")
app.include_router(service.router, prefix="/services")
app.include_router(time.router, prefix="/times")
app.include_router(payment.router, prefix="/payments")
app.include_router(cancellation.router, prefix="/cancellations")
app.include_router(analytics.router, prefix="/analytics")