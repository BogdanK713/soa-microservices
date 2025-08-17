from fastapi import APIRouter, HTTPException
from app.models import (
    ReservationsPerMonthItem, RevenueByServiceItem,
    ReservationsByLocationItem, TopUserItem,
)
from collections import defaultdict
from datetime import datetime
from app import clients
import requests

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/reservations-per-month", response_model=list[ReservationsPerMonthItem])
def reservations_per_month():
    try:
        reservations = clients.list_reservations()
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"company-reservation-service error: {e}")
    buckets = defaultdict(int)
    for r in reservations:
        ds = r.get("date") or r.get("createdAt")
        if not ds: 
            continue
        try:
            d = datetime.fromisoformat(ds).date() if "T" in ds else datetime.strptime(ds, "%Y-%m-%d").date()
        except Exception:
            continue
        buckets[(d.year, d.month)] += 1
    return [{"year": y, "month": m, "total": total} for (y, m), total in sorted(buckets.items())]

@router.get("/revenue-by-service", response_model=list[RevenueByServiceItem])
def revenue_by_service():
    try:
        services = { s["id"]: s for s in clients.list_services() }
        reservations = clients.list_reservations()
        payments = clients.list_payments()
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"upstream error: {e}")

    paid_by_res = defaultdict(float)
    for p in payments:
        rid = p.get("reservation_id") or p.get("reservationId")
        amt = float(p.get("amount") or 0)
        if rid:
            paid_by_res[rid] += amt

    revenue_by_service_id = defaultdict(float)
    for r in reservations:
        rid = r.get("id")
        sid = r.get("service_id") or r.get("serviceId")
        if sid and rid in paid_by_res:
            revenue_by_service_id[sid] += paid_by_res[rid]

    out = []
    for sid, revenue in revenue_by_service_id.items():
        s = services.get(sid, {})
        out.append({
            "service_id": sid,
            "service_name": s.get("name", f"service_{sid}"),
            "revenue": round(revenue, 2),
        })
    out.sort(key=lambda x: x["revenue"], reverse=True)
    return out

@router.get("/reservations-by-location", response_model=list[ReservationsByLocationItem])
def reservations_by_location():
    try:
        locations = { l["id"]: l for l in clients.list_locations() }
        reservations = clients.list_reservations()
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"upstream error: {e}")

    counts = defaultdict(int)
    for r in reservations:
        lid = r.get("location_id") or r.get("locationId")
        if lid:
            counts[lid] += 1

    out = []
    for lid, total in counts.items():
        loc = locations.get(lid, {})
        out.append({
            "location_id": lid,
            "location_name": loc.get("name", f"location_{lid}"),
            "total": total
        })
    out.sort(key=lambda x: x["total"], reverse=True)
    return out

@router.get("/top-users", response_model=list[TopUserItem])
def top_users():
    # users možeš čitati i iz tvog lokalnog CRUD-a, ali za dosljednost:
    try:
        reservations = clients.list_reservations()
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"company-reservation-service error: {e}")

    by_user = defaultdict(int)
    for r in reservations:
        uid = r.get("user_id") or r.get("userId")
        if uid:
            by_user[int(uid)] += 1

    out = [{"user_id": uid, "total_reservations": total} for uid, total in by_user.items()]
    out.sort(key=lambda x: x["total_reservations"], reverse=True)
    return out
