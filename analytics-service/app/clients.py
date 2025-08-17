# app/clients.py
import os, requests

EMPLOYEE_BASE = os.getenv("EMPLOYEE_BASE_URL", "http://employee-service:8000")
EMPLOYEE_API_PREFIX = os.getenv("EMPLOYEE_API_PREFIX", "")  # npr. "/api" ili ""

COMPANY_BASE  = os.getenv("COMPANY_BASE_URL",  "http://company-reservation-service:8082")
COMPANY_API_PREFIX = os.getenv("COMPANY_API_PREFIX", "")    # npr. "/api" ili ""

def _url(base, prefix, path):
    # garantuj jedno / između segmenata
    return f"{base.rstrip('/')}{prefix.rstrip('/')}{path}"

def _get_json(url, params=None):
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    return r.json()

# --- Employee service ---
def list_employees():
    # Ako FastAPI ima prefiks (npr. /api), postavi EMPLOYEE_API_PREFIX="/api"
    return _get_json(_url(EMPLOYEE_BASE, EMPLOYEE_API_PREFIX, "/employees"))

# --- Company reservation service ---
def list_reservations():
    return _get_json(_url(COMPANY_BASE, COMPANY_API_PREFIX, "/reservations"))

def list_payments():
    return _get_json(_url(COMPANY_BASE, COMPANY_API_PREFIX, "/payments"))

def list_cancellations():
    return _get_json(_url(COMPANY_BASE, COMPANY_API_PREFIX, "/cancellations"))

def list_locations():
    return _get_json(_url(COMPANY_BASE, COMPANY_API_PREFIX, "/locations"))

def list_services():
    return _get_json(_url(COMPANY_BASE, COMPANY_API_PREFIX, "/services"))
