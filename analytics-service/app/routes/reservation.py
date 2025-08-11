from fastapi import APIRouter, HTTPException, status
from app.db import get_db_connection
from app.models import ReservationIn, ReservationOut

router = APIRouter(prefix="/reservations", tags=["reservations"])

@router.get("/", response_model=list[ReservationOut])
def list_reservations():
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id, user_id, service_id, location_id, date FROM reservations")
    rows = cur.fetchall()
    cur.close(); conn.close()
    return rows

@router.get("/{reservation_id}", response_model=ReservationOut, responses={404: {"description": "Not found"}})
def get_reservation(reservation_id: int):
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id, user_id, service_id, location_id, date FROM reservations WHERE id=%s", (reservation_id,))
    row = cur.fetchone()
    cur.close(); conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return row

@router.post("/", response_model=ReservationOut, status_code=status.HTTP_201_CREATED,
             responses={400: {"description": "Bad request"}})
def create_reservation(payload: ReservationIn):
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    try:
        cur.execute(
            "INSERT INTO reservations (user_id, service_id, location_id, date) VALUES (%s, %s, %s, %s)",
            (payload.user_id, payload.service_id, payload.location_id, payload.date)
        )
        conn.commit(); new_id = cur.lastrowid
    except Exception as e:
        conn.rollback(); raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close(); conn.close()
    return ReservationOut(id=new_id, **payload.dict())

@router.put("/{reservation_id}", response_model=ReservationOut, responses={404: {"description": "Not found"}})
def update_reservation(reservation_id: int, payload: ReservationIn):
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id FROM reservations WHERE id=%s", (reservation_id,))
    if not cur.fetchone():
        cur.close(); conn.close()
        raise HTTPException(status_code=404, detail="Reservation not found")
    cur.execute(
        "UPDATE reservations SET user_id=%s, service_id=%s, location_id=%s, date=%s WHERE id=%s",
        (payload.user_id, payload.service_id, payload.location_id, payload.date, reservation_id)
    )
    conn.commit(); cur.close(); conn.close()
    return ReservationOut(id=reservation_id, **payload.dict())

@router.delete("/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT, responses={404: {"description": "Not found"}})
def delete_reservation(reservation_id: int):
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id FROM reservations WHERE id=%s", (reservation_id,))
    if not cur.fetchone():
        cur.close(); conn.close()
        raise HTTPException(status_code=404, detail="Reservation not found")
    cur.execute("DELETE FROM reservations WHERE id=%s", (reservation_id,))
    conn.commit(); cur.close(); conn.close()
    return None
