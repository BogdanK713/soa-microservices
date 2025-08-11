from fastapi import APIRouter, HTTPException, status
from app.db import get_db_connection
from app.models import EmployeeIn, EmployeeOut

router = APIRouter(prefix="/employees", tags=["employees"])

@router.get("/", response_model=list[EmployeeOut])
def list_employees():
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id, name, role FROM employees")
    rows = cur.fetchall()
    cur.close(); conn.close()
    return rows

@router.get("/{employee_id}", response_model=EmployeeOut, responses={404: {"description": "Not found"}})
def get_employee(employee_id: int):
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id, name, role FROM employees WHERE id=%s", (employee_id,))
    row = cur.fetchone()
    cur.close(); conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Employee not found")
    return row

@router.post("/", response_model=EmployeeOut, status_code=status.HTTP_201_CREATED,
             responses={400: {"description": "Bad request"}})
def create_employee(payload: EmployeeIn):
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    try:
        cur.execute("INSERT INTO employees (name, role) VALUES (%s, %s)", (payload.name, payload.role))
        conn.commit(); new_id = cur.lastrowid
    except Exception as e:
        conn.rollback(); raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close(); conn.close()
    return EmployeeOut(id=new_id, **payload.dict())

@router.put("/{employee_id}", response_model=EmployeeOut, responses={404: {"description": "Not found"}})
def update_employee(employee_id: int, payload: EmployeeIn):
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id FROM employees WHERE id=%s", (employee_id,))
    if not cur.fetchone():
        cur.close(); conn.close()
        raise HTTPException(status_code=404, detail="Employee not found")
    cur.execute("UPDATE employees SET name=%s, role=%s WHERE id=%s",
                (payload.name, payload.role, employee_id))
    conn.commit(); cur.close(); conn.close()
    return EmployeeOut(id=employee_id, **payload.dict())

@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT, responses={404: {"description": "Not found"}})
def delete_employee(employee_id: int):
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id FROM employees WHERE id=%s", (employee_id,))
    if not cur.fetchone():
        cur.close(); conn.close()
        raise HTTPException(status_code=404, detail="Employee not found")
    cur.execute("DELETE FROM employees WHERE id=%s", (employee_id,))
    conn.commit(); cur.close(); conn.close()
    return None
