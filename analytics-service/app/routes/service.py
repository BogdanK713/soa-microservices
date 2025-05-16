from fastapi import APIRouter, HTTPException
from app.db import get_connection

router = APIRouter()

@router.get("/")
def get_all():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM service")
    results = cursor.fetchall()
    conn.close()
    return results

@router.get("/{item_id}")
def get_one(item_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM service WHERE id = %s", (item_id,))
    item = cursor.fetchone()
    conn.close()
    if not item:
        raise HTTPException(status_code=404, detail="Service not found")
    return item

@router.post("/")
def create(data: dict):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO service (name, price, valid_until, service_code) VALUES (%s, %s, %s, %s)",
        (data['name'], data['price'], data['valid_until'], data['service_code'])
    )
    conn.commit()
    conn.close()
    return {"message": "Service created"}

@router.put("/{item_id}")
def update(item_id: int, data: dict):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE service SET name = %s, price = %s, valid_until = %s, service_code = %s WHERE id = %s",
        (data['name'], data['price'], data['valid_until'], data['service_code'], item_id)
    )
    conn.commit()
    conn.close()
    return {"message": "Service updated"}

@router.delete("/{item_id}")
def delete(item_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM service WHERE id = %s", (item_id,))
    conn.commit()
    conn.close()
    return {"message": "Service deleted"}
