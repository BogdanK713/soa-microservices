from fastapi import APIRouter, HTTPException, status
from app.db import get_db_connection
from app.models import LocationIn, LocationOut

router = APIRouter(prefix="/locations", tags=["locations"])

@router.get("/", response_model=list[LocationOut])
def list_locations():
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id, name, address FROM locations")
    rows = cur.fetchall()
    cur.close(); conn.close()
    return rows

@router.get("/{location_id}", response_model=LocationOut, responses={404: {"description": "Not found"}})
def get_location(location_id: int):
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id, name, address FROM locations WHERE id=%s", (location_id,))
    row = cur.fetchone()
    cur.close(); conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Location not found")
    return row

@router.post("/", response_model=LocationOut, status_code=status.HTTP_201_CREATED,
             responses={400: {"description": "Bad request"}})
def create_location(payload: LocationIn):
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    try:
        cur.execute("INSERT INTO locations (name, address) VALUES (%s, %s)", (payload.name, payload.address))
        conn.commit(); new_id = cur.lastrowid
    except Exception as e:
        conn.rollback(); raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close(); conn.close()
    return LocationOut(id=new_id, **payload.dict())

@router.put("/{location_id}", response_model=LocationOut, responses={404: {"description": "Not found"}})
def update_location(location_id: int, payload: LocationIn):
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id FROM locations WHERE id=%s", (location_id,))
    if not cur.fetchone():
        cur.close(); conn.close()
        raise HTTPException(status_code=404, detail="Location not found")
    cur.execute("UPDATE locations SET name=%s, address=%s WHERE id=%s",
                (payload.name, payload.address, location_id))
    conn.commit(); cur.close(); conn.close()
    return LocationOut(id=location_id, **payload.dict())

@router.delete("/{location_id}", status_code=status.HTTP_204_NO_CONTENT, responses={404: {"description": "Not found"}})
def delete_location(location_id: int):
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id FROM locations WHERE id=%s", (location_id,))
    if not cur.fetchone():
        cur.close(); conn.close()
        raise HTTPException(status_code=404, detail="Location not found")
    cur.execute("DELETE FROM locations WHERE id=%s", (location_id,))
    conn.commit(); cur.close(); conn.close()
    return None
