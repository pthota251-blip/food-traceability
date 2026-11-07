"""
Automated Integration Test for Phase 2 FastAPI Endpoints
"""
from fastapi.testclient import TestClient
from app.main import app

def test_full_pipeline():
    with TestClient(app) as client:
        print("\n--- 1. Testing System Health ---")
        res = client.get("/api/v1/health")
        assert res.status_code == 200, f"Health check failed: {res.text}"
        print("Health Check PASS:", res.json())

        print("\n--- 2. Testing Authentication (Login) ---")
        login_res = client.post("/api/v1/auth/login", json={
            "username_or_email": "admin",
            "password": "admin123"
        })
        assert login_res.status_code == 200, f"Login failed: {login_res.text}"
        token = login_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("Auth PASS: Logged in as Admin, received JWT token.")

        print("\n--- 3. Testing Public Batch Verification ---")
        verify_res = client.get("/api/v1/batches/verify/LOT-2026-FARM-001")
        assert verify_res.status_code == 200, f"Verification failed: {verify_res.text}"
        batch_data = verify_res.json()
        assert batch_data["batch_number"] == "LOT-2026-FARM-001"
        assert batch_data["is_ledger_valid"] is True
        assert len(batch_data["checkpoints"]) >= 4
        print(f"Verify PASS: '{batch_data['product_name']}' - Status: {batch_data['status']}, Ledger Valid: {batch_data['is_ledger_valid']}, Checkpoints: {len(batch_data['checkpoints'])}")

        print("\n--- 4. Testing Batch Creation with QR & Cryptographic Hash ---")
        new_batch_payload = {
            "product_name": "Organic Honey Crisp Apples",
            "category": "produce",
            "description": "Crisp sweet apples harvested in Yakima Valley",
            "origin_farm": "Yakima Valley Orchards",
            "origin_location": "Yakima, WA",
            "harvest_date": "2026-11-01T08:00:00",
            "expiration_date": "2026-12-15T00:00:00",
            "initial_quantity": 250.0,
            "unit": "bushels"
        }
        create_res = client.post("/api/v1/batches/", json=new_batch_payload, headers=headers)
        assert create_res.status_code == 201, f"Create batch failed: {create_res.text}"
        created_batch = create_res.json()
        new_batch_id = created_batch["id"]
        new_batch_code = created_batch["batch_number"]
        assert created_batch["provenance_hash"] is not None
        assert created_batch["qr_code_image_path"] is not None
        print(f"Batch Create PASS: Code={new_batch_code}, Hash={created_batch['provenance_hash'][:16]}..., QR={created_batch['qr_code_image_path']}")

        print("\n--- 5. Testing Checkpoint Logging with Cold-Chain Violation Detection ---")
        breach_checkpoint = {
            "batch_id": new_batch_id,
            "stage": "distribution",
            "location_name": "Highway 90 Transit Truck #55",
            "action": "Refrigerated transport in progress",
            "notes": "Ambient sensor alert triggered",
            "telemetry": {
                "temperature": 11.5,
                "humidity": 88.0,
                "min_allowed_temp": 1.0,
                "max_allowed_temp": 4.0
            }
        }
        cp_res = client.post("/api/v1/checkpoints/", json=breach_checkpoint, headers=headers)
        assert cp_res.status_code == 201, f"Checkpoint logging failed: {cp_res.text}"
        cp_data = cp_res.json()
        assert cp_data["status_flag"] == "COLD_CHAIN_EXCURSION"
        assert cp_data["telemetry"]["is_cold_chain_breached"] is True
        print(f"Cold-Chain Breach PASS: Temp={cp_data['telemetry']['temperature']}°C, Flag={cp_data['status_flag']}")

        print("\n--- 6. Testing Contamination Incident Reporting ---")
        report_data = {
            "batch_number": new_batch_code,
            "reporter_name": "Marcus Kane",
            "reporter_contact": "marcus@consumer.org",
            "symptom_type": "Visible Fungal Mold / Rot",
            "description": "Apples arrived with soft moldy lesions on bottom layer.",
            "purchase_location": "Wholesale Mart Bay Area",
            "severity": "HIGH"
        }
        report_res = client.post("/api/v1/reports/submit", data=report_data)
        assert report_res.status_code == 201, f"Report submission failed: {report_res.text}"
        rep = report_res.json()
        assert rep["ticket_number"].startswith("REP-")
        print(f"Report Submit PASS: Ticket={rep['ticket_number']}, Severity={rep['severity']}, Status={rep['status']}")

        print("\n=======================================================")
        print("ALL 6 INTEGRATION TESTS PASSED WITH 100% SUCCESS!")
        print("=======================================================\n")

if __name__ == "__main__":
    test_full_pipeline()
