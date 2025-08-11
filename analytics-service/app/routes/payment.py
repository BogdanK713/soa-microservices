from fastapi import APIRouter, HTTPException, status
from app.db import get_db_connection
from app.models import PaymentIn, PaymentOut

router = APIRouter(prefix="/payments", tags=["payments"])

@router.get("/", response_model=list[PaymentOut])
def list_payments():
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id, reservation_id, amount, method, paid_at FROM payments")
    rows = cur.fetchall()
    cur.close(); conn.close()
    return rows

@router.get("/{payment_id}", response_model=PaymentOut, responses={404: {"description": "Not found"}})
def get_payment(payment_id: int):
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id, reservation_id, amount, method, paid_at FROM payments WHERE id=%s", (payment_id,))
    row = cur.fetchone()
    cur.close(); conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Payment not found")
    return row

@router.post("/", response_model=PaymentOut, status_code=status.HTTP_201_CREATED,
             responses={400: {"description": "Bad request"}})
def create_payment(payload: PaymentIn):
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    try:
        cur.execute(
            "INSERT INTO payments (reservation_id, amount, method, paid_at) VALUES (%s, %s, %s, %s)",
            (payload.reservation_id, payload.amount, payload.method, payload.paid_at)
        )
        conn.commit(); new_id = cur.lastrowid
    except Exception as e:
        conn.rollback(); raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close(); conn.close()
    return PaymentOut(id=new_id, **payload.dict())

@router.put("/{payment_id}", response_model=PaymentOut, responses={404: {"description": "Not found"}})
def update_payment(payment_id: int, payload: PaymentIn):
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id FROM payments WHERE id=%s", (payment_id,))
    if not cur.fetchone():
        cur.close(); conn.close()
        raise HTTPException(status_code=404, detail="Payment not found")
    cur.execute(
        "UPDATE payments SET reservation_id=%s, amount=%s, method=%s, paid_at=%s WHERE id=%s",
        (payload.reservation_id, payload.amount, payload.method, payload.paid_at, payment_id)
    )
    conn.commit(); cur.close(); conn.close()
    return PaymentOut(id=payment_id, **payload.dict())

@router.delete("/{payment_id}", status_code=status.HTTP_204_NO_CONTENT, responses={404: {"description": "Not found"}})
def delete_payment(payment_id: int):
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id FROM payments WHERE id=%s", (payment_id,))
    if not cur.fetchone():
        cur.close(); conn.close()
        raise HTTPException(status_code=404, detail="Payment not found")
    cur.execute("DELETE FROM payments WHERE id=%s", (payment_id,))
    conn.commit(); cur.close(); conn.close()
    return None
