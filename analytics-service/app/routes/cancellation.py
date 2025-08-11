from fastapi import APIRouter, HTTPException, status
from app.db import get_db_connection
from app.models import CancellationIn, CancellationOut

router = APIRouter(prefix="/cancellations", tags=["cancellations"])

@router.get("/", response_model=list[CancellationOut])
def list_cancellations():
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id, reservation_id, reason, cancelled_at FROM cancellations")
    rows = cur.fetchall()
    cur.close(); conn.close()
    return rows

@router.get("/{cancellation_id}", response_model=CancellationOut, responses={404: {"description": "Not found"}})
def get_cancellation(cancellation_id: int):
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id, reservation_id, reason, cancelled_at FROM cancellations WHERE id=%s", (cancellation_id,))
    row = cur.fetchone()
    cur.close(); conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Cancellation not found")
    return row

@router.post("/", response_model=CancellationOut, status_code=status.HTTP_201_CREATED,
             responses={400: {"description": "Bad request"}})
def create_cancellation(payload: CancellationIn):
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    try:
        cur.execute(
            "INSERT INTO cancellations (reservation_id, reason, cancelled_at) VALUES (%s, %s, %s)",
            (payload.reservation_id, payload.reason, payload.cancelled_at)
        )
        conn.commit(); new_id = cur.lastrowid
    except Exception as e:
        conn.rollback(); raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close(); conn.close()
    return CancellationOut(id=new_id, **payload.dict())

@router.put("/{cancellation_id}", response_model=CancellationOut, responses={404: {"description": "Not found"}})
def update_cancellation(cancellation_id: int, payload: CancellationIn):
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id FROM cancellations WHERE id=%s", (cancellation_id,))
    if not cur.fetchone():
        cur.close(); conn.close()
        raise HTTPException(status_code=404, detail="Cancellation not found")
    cur.execute(
        "UPDATE cancellations SET reservation_id=%s, reason=%s, cancelled_at=%s WHERE id=%s",
        (payload.reservation_id, payload.reason, payload.cancelled_at, cancellation_id)
    )
    conn.commit(); cur.close(); conn.close()
    return CancellationOut(id=cancellation_id, **payload.dict())

@router.delete("/{cancellation_id}", status_code=status.HTTP_204_NO_CONTENT, responses={404: {"description": "Not found"}})
def delete_cancellation(cancellation_id: int):
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id FROM cancellations WHERE id=%s", (cancellation_id,))
    if not cur.fetchone():
        cur.close(); conn.close()
        raise HTTPException(status_code=404, detail="Cancellation not found")
    cur.execute("DELETE FROM cancellations WHERE id=%s", (cancellation_id,))
    conn.commit(); cur.close(); conn.close()
    return None
