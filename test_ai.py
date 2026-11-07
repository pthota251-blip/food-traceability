"""
Automated Integration Tests for Phase 3: AI Vision & Predictive Risk Engine
"""
import io
import numpy as np
from PIL import Image
from fastapi.testclient import TestClient
from app.main import app

def create_synthetic_fresh_image() -> bytes:
    """Creates an in-memory image resembling fresh vibrant green produce."""
    img = Image.new("RGB", (256, 256), color=(34, 139, 34))  # Forest Green
    # Add subtle natural texture
    arr = np.array(img)
    noise = np.random.randint(-10, 10, arr.shape, dtype=np.int16)
    arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
    res_img = Image.fromarray(arr)
    buf = io.BytesIO()
    res_img.save(buf, format="JPEG")
    return buf.getvalue()


def create_synthetic_spoiled_image() -> bytes:
    """Creates an in-memory image with dark necrotic lesions and ashen mold patches."""
    img = Image.new("RGB", (256, 256), color=(100, 110, 90))
    arr = np.array(img)
    # Add dark necrotic rot patches
    arr[60:140, 60:140] = [20, 20, 25]
    # Add ashen gray fungal fuzz
    arr[140:200, 120:200] = [120, 125, 130]
    # Add abnormal blue-cyan rot
    arr[40:80, 150:210] = [30, 80, 160]
    res_img = Image.fromarray(arr)
    buf = io.BytesIO()
    res_img.save(buf, format="JPEG")
    return buf.getvalue()


def test_ai_pipeline():
    with TestClient(app) as client:
        print("\n--- 1. Testing AI Computer Vision: Fresh Sample Scan ---")
        fresh_bytes = create_synthetic_fresh_image()
        res_fresh = client.post(
            "/api/v1/ai/inspect-image",
            files={"image": ("fresh_apple.jpg", fresh_bytes, "image/jpeg")},
            data={"food_category": "produce"}
        )
        assert res_fresh.status_code == 200, f"Fresh scan failed: {res_fresh.text}"
        fresh_data = res_fresh.json()
        print(f"Fresh Scan Result: Score={fresh_data['visual_spoilage_score']}, Contaminant='{fresh_data['detected_contaminant']}', Safe={fresh_data['is_safe']}")
        assert fresh_data["is_safe"] is True
        assert fresh_data["visual_spoilage_score"] < 25.0

        print("\n--- 2. Testing AI Computer Vision: Spoilage & Fungal Mold Scan on Batch ---")
        # Get target batch 1 (LOT-2026-FARM-001)
        b_res = client.get("/api/v1/batches/verify/LOT-2026-FARM-001")
        batch_id = b_res.json()["id"]

        spoiled_bytes = create_synthetic_spoiled_image()
        res_spoiled = client.post(
            "/api/v1/ai/inspect-image",
            files={"image": ("spoiled_produce.jpg", spoiled_bytes, "image/jpeg")},
            data={"batch_id": str(batch_id), "food_category": "produce"}
        )
        assert res_spoiled.status_code == 200, f"Spoiled scan failed: {res_spoiled.text}"
        spoiled_data = res_spoiled.json()
        print(f"Spoiled Scan Result: Score={spoiled_data['visual_spoilage_score']}, Contaminant='{spoiled_data['detected_contaminant']}', Safe={spoiled_data['is_safe']}")
        assert spoiled_data["is_safe"] is False
        assert spoiled_data["visual_spoilage_score"] >= 35.0
        assert spoiled_data["annotated_image_url"] is not None
        print(f"Annotated Overlay Generated: {spoiled_data['annotated_image_url']}")

        print("\n--- 3. Testing Predictive Multi-Factor Risk Scorer ---")
        risk_res = client.get(f"/api/v1/ai/batch-risk/{batch_id}")
        assert risk_res.status_code == 200, f"Risk query failed: {risk_res.text}"
        risk_data = risk_res.json()
        print(f"Batch Risk: Score={risk_data['composite_risk_score']}/100, Tier={risk_data['risk_tier']}")
        print(f"Breakdown: Thermal={risk_data['factor_breakdown']['thermal_iot_score']}, Visual={risk_data['factor_breakdown']['visual_spoilage_score']}, Reports={risk_data['factor_breakdown']['incident_velocity_score']}")
        assert "composite_risk_score" in risk_data
        assert "factor_breakdown" in risk_data

        print("\n--- 4. Testing Sensory Anomaly Simulation (Hackathon Mode) ---")
        sim_res = client.post(
            f"/api/v1/ai/simulate-anomaly/{batch_id}",
            data={"anomaly_type": "COLD_CHAIN_SPIKE", "severity_level": "17.8"}
        )
        assert sim_res.status_code == 200, f"Simulation failed: {sim_res.text}"
        sim_data = sim_res.json()
        print(f"Simulation Result: Anomaly Injected -> New Status: {sim_data['new_status']}, New Risk Score: {sim_data['new_risk_score']}")
        assert sim_data["new_risk_score"] > 40.0

        print("\n=======================================================")
        print("ALL 4 AI ENGINE TESTS PASSED WITH 100% SUCCESS!")
        print("=======================================================\n")

if __name__ == "__main__":
    test_ai_pipeline()

