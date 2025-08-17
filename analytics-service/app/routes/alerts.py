from fastapi import APIRouter, HTTPException
from app.models import AlertIn, AlertOut
import os, json, mysql.connector, mysql.connector.pooling

router = APIRouter(prefix="/alerts", tags=["alerts"])

POOL = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="alt_pool",
    pool_size=5,
    host=os.getenv("DB_HOST","analytics-mysql"),
    user=os.getenv("DB_USER","root"),
    password=os.getenv("DB_PASSWORD","root"),
    database=os.getenv("DB_NAME","reservation_service_db"),
    autocommit=True,
)

def conn():
    return POOL.get_connection()

@router.get("/", response_model=list[AlertOut])
def list_alerts():
    with conn() as c:
        cur = c.cursor(dictionary=True)
        cur.execute("SELECT id, name, `condition`, enabled FROM alert ORDER BY id DESC")
        rows = cur.fetchall()
    for r in rows:
        if isinstance(r["condition"], (bytes, bytearray, str)):
            r["condition"] = json.loads(r["condition"])
    return rows

@router.get("/{alert_id}", response_model=AlertOut)
def get_alert(alert_id: int):
    with conn() as c:
        cur = c.cursor(dictionary=True)
        cur.execute("SELECT id, name, `condition`, enabled FROM alert WHERE id=%s", (alert_id,))
        row = cur.fetchone()
    if not row:
        raise HTTPException(404, "Alert not found")
    if isinstance(row["condition"], (bytes, bytearray, str)):
        row["condition"] = json.loads(row["condition"])
    return row

@router.post("/", response_model=AlertOut, status_code=201)
def create_alert(data: AlertIn):
    with conn() as c:
        cur = c.cursor()
        cur.execute(
            "INSERT INTO alert (name, `condition`, enabled) VALUES (%s, CAST(%s AS JSON), %s)",
            (data.name, json.dumps(data.condition), data.enabled),
        )
        new_id = cur.lastrowid
    return {"id": new_id, **data.dict(by_alias=True)}

@router.put("/{alert_id}", response_model=AlertOut)
def update_alert(alert_id: int, data: AlertIn):
    with conn() as c:
        cur = c.cursor()
        cur.execute("SELECT 1 FROM alert WHERE id=%s", (alert_id,))
        if not cur.fetchone():
            raise HTTPException(404, "Alert not found")
        cur.execute(
            "UPDATE alert SET name=%s, `condition`=CAST(%s AS JSON), enabled=%s WHERE id=%s",
            (data.name, json.dumps(data.condition), data.enabled, alert_id),
        )
    return {"id": alert_id, **data.dict(by_alias=True)}

@router.delete("/{alert_id}", status_code=204)
def delete_alert(alert_id: int):
    with conn() as c:
        cur = c.cursor()
        cur.execute("DELETE FROM alert WHERE id=%s", (alert_id,))
        if cur.rowcount == 0:
            raise HTTPException(404, "Alert not found")
    return None
