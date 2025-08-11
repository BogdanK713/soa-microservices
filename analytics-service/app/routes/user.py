from fastapi import APIRouter, HTTPException, status
from app.db import get_db_connection
from app.models import UserIn, UserOut

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=list[UserOut])
def list_users():
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id, name, email FROM users")
    rows = cur.fetchall()
    cur.close(); conn.close()
    return rows

@router.get("/{user_id}", response_model=UserOut, responses={404: {"description": "Not found"}})
def get_user(user_id: int):
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id, name, email FROM users WHERE id=%s", (user_id,))
    row = cur.fetchone()
    cur.close(); conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="User not found")
    return row

@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED,
             responses={400: {"description": "Bad request"}})
def create_user(payload: UserIn):
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    try:
        cur.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (payload.name, payload.email))
        conn.commit(); new_id = cur.lastrowid
    except Exception as e:
        conn.rollback(); raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close(); conn.close()
    return UserOut(id=new_id, **payload.dict())

@router.put("/{user_id}", response_model=UserOut, responses={404: {"description": "Not found"}})
def update_user(user_id: int, payload: UserIn):
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id FROM users WHERE id=%s", (user_id,))
    if not cur.fetchone():
        cur.close(); conn.close()
        raise HTTPException(status_code=404, detail="User not found")
    cur.execute("UPDATE users SET name=%s, email=%s WHERE id=%s", (payload.name, payload.email, user_id))
    conn.commit(); cur.close(); conn.close()
    return UserOut(id=user_id, **payload.dict())

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, responses={404: {"description": "Not found"}})
def delete_user(user_id: int):
    conn = get_db_connection(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id FROM users WHERE id=%s", (user_id,))
    if not cur.fetchone():
        cur.close(); conn.close()
        raise HTTPException(status_code=404, detail="User not found")
    cur.execute("DELETE FROM users WHERE id=%s", (user_id,))
    conn.commit(); cur.close(); conn.close()
    return None
