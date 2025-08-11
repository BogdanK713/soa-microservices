from fastapi import APIRouter, HTTPException, status
from app.db import get_db_connection
from app.models import ServiceIn, ServiceOut

router = APIRouter(prefix="/services", tags=["services"])

@router.get("/", response_model=list[ServiceOut])
def list_services():
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id, name, description, price FROM services")
    rows = cur.fetchall()
    cur.close(); conn.close()
    return rows

@router.get("/{service_id}", response_model=ServiceOut, responses={404: {"description": "Not found"}})
def get_service(service_id: int):
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id, name, description, price FROM services WHERE id=%s", (service_id,))
    row = cur.fetchone()
    cur.close(); conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Service not found")
    return row

@router.post("/", response_model=ServiceOut, status_code=status.HTTP_201_CREATED,
             responses={400: {"description": "Bad request"}})
def create_service(payload: ServiceIn):
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    try:
        cur.execute("INSERT INTO services (name, description, price) VALUES (%s, %s, %s)",
                    (payload.name, payload.description, payload.price))
        conn.commit(); new_id = cur.lastrowid
    except Exception as e:
        conn.rollback(); raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close(); conn.close()
    return ServiceOut(id=new_id, **payload.dict())

@router.put("/{service_id}", response_model=ServiceOut, responses={404: {"description": "Not found"}})
def update_service(service_id: int, payload: ServiceIn):
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id FROM services WHERE id=%s", (service_id,))
    if not cur.fetchone():
        cur.close(); conn.close()
        raise HTTPException(status_code=404, detail="Service not found")
    cur.execute("UPDATE services SET name=%s, description=%s, price=%s WHERE id=%s",
                (payload.name, payload.description, payload.price, service_id))
    conn.commit(); cur.close(); conn.close()
    return ServiceOut(id=service_id, **payload.dict())

@router.delete("/{service_id}", status_code=status.HTTP_204_NO_CONTENT, responses={404: {"description": "Not found"}})
def delete_service(service_id: int):
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id FROM services WHERE id=%s", (service_id,))
    if not cur.fetchone():
        cur.close(); conn.close()
        raise HTTPException(status_code=404, detail="Service not found")
    cur.execute("DELETE FROM services WHERE id=%s", (service_id,))
    conn.commit(); cur.close(); conn.close()
    return None
