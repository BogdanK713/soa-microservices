from fastapi import APIRouter, HTTPException
from app.db import get_connection

router = APIRouter()

@router.get("/")
def get_all():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM employee")
    results = cursor.fetchall()
    conn.close()
    return results

@router.get("/{item_id}")
def get_one(item_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM employee WHERE id = %s", (item_id,))
    item = cursor.fetchone()
    conn.close()
    if not item:
        raise HTTPException(status_code=404, detail="Employee not found")
    return item

@router.post("/")
def create(data: dict):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO employee (first_name, last_name, position, employee_code, emso) VALUES (%s, %s, %s, %s, %s)",
        (data['first_name'], data['last_name'], data['position'], data['employee_code'], data['emso'])
    )
    conn.commit()
    conn.close()
    return {"message": "Employee created"}

@router.put("/{item_id}")
def update(item_id: int, data: dict):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE employee SET first_name = %s, last_name = %s, position = %s, employee_code = %s, emso = %s WHERE id = %s",
        (data['first_name'], data['last_name'], data['position'], data['employee_code'], data['emso'], item_id)
    )
    conn.commit()
    conn.close()
    return {"message": "Employee updated"}

@router.delete("/{item_id}")
def delete(item_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employee WHERE id = %s", (item_id,))
    conn.commit()
    conn.close()
    return {"message": "Employee deleted"}
