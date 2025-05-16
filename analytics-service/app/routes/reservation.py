from fastapi import APIRouter, HTTPException
from app.db import get_connection

router = APIRouter()

@router.get("/")
def get_all():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM reservation")
    results = cursor.fetchall()
    conn.close()
    return results

@router.get("/{item_id}")
def get_one(item_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM reservation WHERE id = %s", (item_id,))
    item = cursor.fetchone()
    conn.close()
    if not item:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return item

@router.post("/")
def create(data: dict):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO reservation (
            payment_id, cancellation_id, time_id, user_id, employee_id,
            location_id, service_id, company_id, sms_sent
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            data['payment_id'], data['cancellation_id'], data['time_id'], data['user_id'],
            data['employee_id'], data['location_id'], data['service_id'],
            data['company_id'], data['sms_sent']
        )
    )
    conn.commit()
    conn.close()
    return {"message": "Reservation created"}

@router.put("/{item_id}")
def update(item_id: int, data: dict):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE reservation SET
            payment_id = %s, cancellation_id = %s, time_id = %s, user_id = %s,
            employee_id = %s, location_id = %s, service_id = %s, company_id = %s,
            sms_sent = %s
        WHERE id = %s
        """,
        (
            data['payment_id'], data['cancellation_id'], data['time_id'], data['user_id'],
            data['employee_id'], data['location_id'], data['service_id'],
            data['company_id'], data['sms_sent'], item_id
        )
    )
    conn.commit()
    conn.close()
    return {"message": "Reservation updated"}

@router.delete("/{item_id}")
def delete(item_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reservation WHERE id = %s", (item_id,))
    conn.commit()
    conn.close()
    return {"message": "Reservation deleted"}
