from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# singular file names in routes package
from app.routes import (
    health,
    user,
    employee,
    location,
    service,
    time,
    reservation,
    payment,
    cancellation,
    analytics,
)

app = FastAPI(
    title="Analytics Service",
    version="1.0.0",
    description="Analytics & CRUD service with documented routes",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# register routers
app.include_router(health.router)
app.include_router(user.router)
app.include_router(employee.router)
app.include_router(location.router)
app.include_router(service.router)
app.include_router(time.router)
app.include_router(reservation.router)
app.include_router(payment.router)
app.include_router(cancellation.router)
app.include_router(analytics.router)

@app.get("/")
def root():
    return {"service": "analytics", "status": "ok"}
