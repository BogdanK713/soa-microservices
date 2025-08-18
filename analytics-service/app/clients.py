# app/clients.py
import os, requests

# ----- Employee service -----
EMPLOYEE_BASE = os.getenv("EMPLOYEE_BASE_URL", "http://employee-service:8000")
EMPLOYEE_API_PREFIX = os.getenv("EMPLOYEE_API_PREFIX", "")  # e.g. "/api" or ""

# ----- Company/Reservation service (Vanja) -----
# NOTE: in docker-compose you already set COMPANY_BASE_URL to "http://company-service:8082/api"
COMPANY_BASE  = os.getenv("COMPANY_BASE_URL",  "http://company-service:8082/api")
COMPANY_API_PREFIX = os.getenv("COMPANY_API_PREFIX", "")    # usually empty because BASE already has /api

# Default company id for analytics aggregations
DEFAULT_COMPANY_ID = int(os.getenv("ANALYTICS_COMPANY_ID", "1"))


def _url(base, prefix, path):
    base = base.rstrip("/")
    pfx = (prefix or "").strip()
    if pfx and not pfx.startswith("/"):
        pfx = "/" + pfx
    return f"{base}{pfx}{path}"  # path MUST start with "/"


def _get_json(url, params=None):
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    return r.json()


# --- Employee service ---
def list_employees():
    # If FastAPI has a prefix (e.g. /api), set EMPLOYEE_API_PREFIX="/api"
    return _get_json(_url(EMPLOYEE_BASE, EMPLOYEE_API_PREFIX, "/employees"))


# --- Company / Reservation service (Vanja) ---
# IMPORTANT: Vanja's service does NOT have root GET /reservations or /services.
# Use the company-scoped endpoints here and keep the rest of your code unchanged.

def list_reservations_by_company(company_id: int):
    # GET /api/reservations/company/{company_id}
    return _get_json(_url(COMPANY_BASE, COMPANY_API_PREFIX, f"/reservations/company/{company_id}"))

def list_reservations():
    # Keep your old call sites working by routing to company-scoped endpoint.
    return list_reservations_by_company(DEFAULT_COMPANY_ID)

def list_services_by_company(company_id: int):
    # GET /api/services/company/{company_id}
    return _get_json(_url(COMPANY_BASE, COMPANY_API_PREFIX, f"/services/company/{company_id}"))

def list_services():
    # Keep your old call sites working by routing to company-scoped endpoint.
    return list_services_by_company(DEFAULT_COMPANY_ID)

# These stayed the same; they already point to valid resources in your app.
def list_payments():
    return _get_json(_url(COMPANY_BASE, COMPANY_API_PREFIX, "/payments"))

def list_cancellations():
    return _get_json(_url(COMPANY_BASE, COMPANY_API_PREFIX, "/cancellations"))

def list_locations():
    return _get_json(_url(COMPANY_BASE, COMPANY_API_PREFIX, "/locations"))
