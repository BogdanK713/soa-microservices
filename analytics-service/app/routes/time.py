from fastapi import APIRouter, HTTPException, status
from app.db import get_db_connection
from app.models import TimeDimIn, TimeDimOut

router = APIRouter(prefix="/time", tags=["time"])

@router.get("/", response_model=list[TimeDimOut])
def list_time_dim():
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id, date, year, month, day FROM time_dim")
    rows = cur.fetchall()
    cur.close(); conn.close()
    return rows

@router.get("/{time_id}", response_model=TimeDimOut, responses={404: {"description": "Not found"}})
def get_time_dim(time_id: int):
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id, date, year, month, day FROM time_dim WHERE id=%s", (time_id,))
    row = cur.fetchone()
    cur.close(); conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="TimeDim not found")
    return row

@router.post("/", response_model=TimeDimOut, status_code=status.HTTP_201_CREATED,
             responses={400: {"description": "Bad request"}})
def create_time_dim(payload: TimeDimIn):
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    try:
        cur.execute("INSERT INTO time_dim (date, year, month, day) VALUES (%s, %s, %s, %s)",
                    (payload.date, payload.year, payload.month, payload.day))
        conn.commit(); new_id = cur.lastrowid
    except Exception as e:
        conn.rollback(); raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close(); conn.close()
    return TimeDimOut(id=new_id, **payload.dict())

@router.put("/{time_id}", response_model=TimeDimOut, responses={404: {"description": "Not found"}})
def update_time_dim(time_id: int, payload: TimeDimIn):
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id FROM time_dim WHERE id=%s", (time_id,))
    if not cur.fetchone():
        cur.close(); conn.close()
        raise HTTPException(status_code=404, detail="TimeDim not found")
    cur.execute("UPDATE time_dim SET date=%s, year=%s, month=%s, day=%s WHERE id=%s",
                (payload.date, payload.year, payload.month, payload.day, time_id))
    conn.commit(); cur.close(); conn.close()
    return TimeDimOut(id=time_id, **payload.dict())

@router.delete("/{time_id}", status_code=status.HTTP_204_NO_CONTENT, responses={404: {"description": "Not found"}})
def delete_time_dim(time_id: int):
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id FROM time_dim WHERE id=%s", (time_id,))
    if not cur.fetchone():
        cur.close(); conn.close()
        raise HTTPException(status_code=404, detail="TimeDim not found")
    cur.execute("DELETE FROM time_dim WHERE id=%s", (time_id,))
    conn.commit(); cur.close(); conn.close()
    return None
