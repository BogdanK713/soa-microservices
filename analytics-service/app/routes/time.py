from fastapi import APIRouter, HTTPException
from app.db import get_connection

router = APIRouter()

@router.get("/")
def get_all():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM time")
    results = cursor.fetchall()
    conn.close()
    return results

@router.get("/{item_id}")
def get_one(item_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM time WHERE id = %s", (item_id,))
    item = cursor.fetchone()
    conn.close()
    if not item:
        raise HTTPException(status_code=404, detail="Time entry not found")
    return item

@router.post("/")
def create(data: dict):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO time (year, month, week, quarter, day_in_month, day_in_week, hour) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (data['year'], data['month'], data['week'], data['quarter'], data['day_in_month'], data['day_in_week'], data['hour'])
    )
    conn.commit()
    conn.close()
    return {"message": "Time entry created"}

@router.put("/{item_id}")
def update(item_id: int, data: dict):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE time SET year = %s, month = %s, week = %s, quarter = %s, day_in_month = %s, day_in_week = %s, hour = %s WHERE id = %s",
        (data['year'], data['month'], data['week'], data['quarter'], data['day_in_month'], data['day_in_week'], data['hour'], item_id)
    )
    conn.commit()
    conn.close()
    return {"message": "Time entry updated"}

@router.delete("/{item_id}")
def delete(item_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM time WHERE id = %s", (item_id,))
    conn.commit()
    conn.close()
    return {"message": "Time entry deleted"}
