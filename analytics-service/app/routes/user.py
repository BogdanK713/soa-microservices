from fastapi import APIRouter, HTTPException
from app.db import get_connection

router = APIRouter()

@router.get("/")
def get_all():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user")
    results = cursor.fetchall()
    conn.close()
    return results

@router.get("/{item_id}")
def get_one(item_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user WHERE id = %s", (item_id,))
    item = cursor.fetchone()
    conn.close()
    if not item:
        raise HTTPException(status_code=404, detail="User not found")
    return item

@router.post("/")
def create(data: dict):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO user (first_name, last_name, email, points) VALUES (%s, %s, %s, %s)",
        (data['first_name'], data['last_name'], data['email'], data['points'])
    )
    conn.commit()
    conn.close()
    return {"message": "User created"}

@router.put("/{item_id}")
def update(item_id: int, data: dict):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE user SET first_name = %s, last_name = %s, email = %s, points = %s WHERE id = %s",
        (data['first_name'], data['last_name'], data['email'], data['points'], item_id)
    )
    conn.commit()
    conn.close()
    return {"message": "User updated"}

@router.delete("/{item_id}")
def delete(item_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user WHERE id = %s", (item_id,))
    conn.commit()
    conn.close()
    return {"message": "User deleted"}
