from fastapi import APIRouter, HTTPException
from app.db import get_connection

router = APIRouter()

@router.get("/")
def get_all():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM cancellation")
    results = cursor.fetchall()
    conn.close()
    return results

@router.get("/{item_id}")
def get_one(item_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM cancellation WHERE id = %s", (item_id,))
    item = cursor.fetchone()
    conn.close()
    if not item:
        raise HTTPException(status_code=404, detail="Cancellation not found")
    return item

@router.post("/")
def create(data: dict):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO cancellation (name, description) VALUES (%s, %s)",
        (data['name'], data['description'])
    )
    conn.commit()
    conn.close()
    return {"message": "Cancellation created"}

@router.put("/{item_id}")
def update(item_id: int, data: dict):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE cancellation SET name = %s, description = %s WHERE id = %s",
        (data['name'], data['description'], item_id)
    )
    conn.commit()
    conn.close()
    return {"message": "Cancellation updated"}

@router.delete("/{item_id}")
def delete(item_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cancellation WHERE id = %s", (item_id,))
    conn.commit()
    conn.close()
    return {"message": "Cancellation deleted"}
