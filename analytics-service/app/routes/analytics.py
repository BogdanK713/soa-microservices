from fastapi import APIRouter
from app.db import get_connection

router = APIRouter()

@router.get("/reservations-per-month")
def reservations_per_month():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT month, COUNT(*) as total_reservations
        FROM reservation
        JOIN time ON reservation.time_id = time.id
        GROUP BY month
        ORDER BY month
    """)
    results = cursor.fetchall()
    conn.close()
    return results

@router.get("/revenue-by-service")
def revenue_by_service():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT service.name, COUNT(*) as reservations, SUM(service.price) as total_revenue
        FROM reservation
        JOIN service ON reservation.service_id = service.id
        GROUP BY service.name
    """)
    results = cursor.fetchall()
    conn.close()
    return results

@router.get("/reservations-by-location")
def reservations_by_location():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT location.name, COUNT(*) as total_reservations
        FROM reservation
        JOIN location ON reservation.location_id = location.id
        GROUP BY location.name
    """)
    results = cursor.fetchall()
    conn.close()
    return results

@router.get("/top-users")
def top_users():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT user.first_name, user.last_name, COUNT(*) as total_reservations
        FROM reservation
        JOIN user ON reservation.user_id = user.id
        GROUP BY user.id
        ORDER BY total_reservations DESC
        LIMIT 5
    """)
    results = cursor.fetchall()
    conn.close()
    return results
