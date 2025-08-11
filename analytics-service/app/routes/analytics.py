from fastapi import APIRouter
from app.db import get_db_connection
from app.models import (
    ReservationsPerMonthItem,
    RevenueByServiceItem,
    ReservationsByLocationItem,
    TopUserItem,
)

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/reservations-per-month", response_model=list[ReservationsPerMonthItem])
def reservations_per_month():
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT YEAR(date) AS year, MONTH(date) AS month, COUNT(*) AS total
        FROM reservations
        GROUP BY YEAR(date), MONTH(date)
        ORDER BY YEAR(date), MONTH(date)
    """)
    rows = cur.fetchall()
    cur.close(); conn.close()
    return rows

@router.get("/revenue-by-service", response_model=list[RevenueByServiceItem])
def revenue_by_service():
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT s.id AS service_id, s.name AS service_name, IFNULL(SUM(p.amount), 0) AS revenue
        FROM services s
        LEFT JOIN reservations r ON r.service_id = s.id
        LEFT JOIN payments p ON p.reservation_id = r.id
        GROUP BY s.id, s.name
        ORDER BY revenue DESC
    """)
    rows = cur.fetchall()
    cur.close(); conn.close()
    return rows

@router.get("/reservations-by-location", response_model=list[ReservationsByLocationItem])
def reservations_by_location():
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT l.id AS location_id, l.name AS location_name, COUNT(r.id) AS total
        FROM locations l
        LEFT JOIN reservations r ON r.location_id = l.id
        GROUP BY l.id, l.name
        ORDER BY total DESC
    """)
    rows = cur.fetchall()
    cur.close(); conn.close()
    return rows

@router.get("/top-users", response_model=list[TopUserItem])
def top_users():
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT user_id, COUNT(*) AS total_reservations
        FROM reservations
        GROUP BY user_id
        ORDER BY total_reservations DESC
        LIMIT 10
    """)
    rows = cur.fetchall()
    cur.close(); conn.close()
    return rows
