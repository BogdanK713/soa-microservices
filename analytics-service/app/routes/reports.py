from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.models import ReportIn, ReportOut
import os, json, mysql.connector, mysql.connector.pooling

router = APIRouter(prefix="/reports", tags=["reports"])

POOL = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="rep_pool",
    pool_size=5,
    host=os.getenv("DB_HOST","analytics-mysql"),
    user=os.getenv("DB_USER","root"),
    password=os.getenv("DB_PASSWORD","root"),
    database=os.getenv("DB_NAME","reservation_service_db"),
    autocommit=True,
)

def conn():
    return POOL.get_connection()

@router.get("/", response_model=list[ReportOut])
def list_reports():
    with conn() as c:
        cur = c.cursor(dictionary=True)
        cur.execute("SELECT id, name, query, schedule_cron FROM report ORDER BY id DESC")
        rows = cur.fetchall()
    for r in rows:
        if isinstance(r["query"], (bytes, bytearray, str)):
            r["query"] = json.loads(r["query"])
    return rows

@router.get("/{report_id}", response_model=ReportOut)
def get_report(report_id: int):
    with conn() as c:
        cur = c.cursor(dictionary=True)
        cur.execute("SELECT id, name, query, schedule_cron FROM report WHERE id=%s", (report_id,))
        row = cur.fetchone()
    if not row:
        raise HTTPException(404, "Report not found")
    if isinstance(row["query"], (bytes, bytearray, str)):
        row["query"] = json.loads(row["query"])
    return row

@router.post("/", response_model=ReportOut, status_code=201)
def create_report(data: ReportIn):
    with conn() as c:
        cur = c.cursor()
        cur.execute(
            "INSERT INTO report (name, query, schedule_cron) VALUES (%s, CAST(%s AS JSON), %s)",
            (data.name, json.dumps(data.query), data.schedule_cron),
        )
        new_id = cur.lastrowid
    return {"id": new_id, **data.dict()}

@router.put("/{report_id}", response_model=ReportOut)
def update_report(report_id: int, data: ReportIn):
    with conn() as c:
        cur = c.cursor()
        cur.execute("SELECT 1 FROM report WHERE id=%s", (report_id,))
        if not cur.fetchone():
            raise HTTPException(404, "Report not found")
        cur.execute(
            "UPDATE report SET name=%s, query=CAST(%s AS JSON), schedule_cron=%s WHERE id=%s",
            (data.name, json.dumps(data.query), data.schedule_cron, report_id),
        )
    return {"id": report_id, **data.dict()}

@router.delete("/{report_id}", status_code=204)
def delete_report(report_id: int):
    with conn() as c:
        cur = c.cursor()
        cur.execute("DELETE FROM report WHERE id=%s", (report_id,))
        if cur.rowcount == 0:
            raise HTTPException(404, "Report not found")
    return None
