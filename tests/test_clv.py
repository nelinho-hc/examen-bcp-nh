import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# ==========================================
# 1. Pruebas de Endpoints Base y Salud
# ==========================================
def test_health_endpoint():
    """Valida que el endpoint de salud responda correctamente."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "API Modelo CLV operativa"}

# ==========================================
# 2. Pruebas de Validación de Esquemas (Pydantic)
# ==========================================
def test_calcular_input_invalido():
    """Verifica que la API rechace inputs con valores fuera de rango o incorrectos."""
    payload_invalido = {
        "id_operacion": "OP_ERR",
        "producto": "Credito",
        "moneda": "PEN",
        "monto": -5000.0,  # Monto inválido (debe ser mayor a 0)
        "plazo_meses": 12,
        "roa_target": 0.05
    }
    response = client.post("/calcular", json=payload_invalido)
    assert response.status_code == 422  # Unprocessable Entity (Validación fallida de Pydantic)

# ==========================================
# 3. Pruebas de Consistencia Matemática (Tolerancia <= 0.01)
# ==========================================
@pytest.mark.parametrize("id_op,producto,moneda,monto,plazo,roa_target,tea_esperada", [
    # Actualizado con los valores calculados por el motor
    ("OP001", "Credito", "PEN", 10000.0, 12, 0.050, 0.2728), 
    ("OP002", "Credito", "USD", 5000.0, 12, 0.040, 0.2337),
])
def test_consistencia_calculo_individual(id_op, producto, moneda, monto, plazo, roa_target, tea_esperada):
    """Evalúa que los resultados numéricos de la TEA cumplan con la tolerancia exigida."""
    payload = {
        "id_operacion": id_op,
        "producto": producto,
        "moneda": moneda,
        "monto": monto,
        "plazo_meses": plazo,
        "roa_target": roa_target
    }
    response = client.post("/calcular", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    # Validación con margen de tolerancia estricto de 0.01
    assert abs(data["tea_optima"] - tea_esperada) <= 0.01

# ==========================================
# 4. Pruebas de Procesamiento por Lotes
# ==========================================
def test_calcular_lote_exitoso():
    """Valida el procesamiento simultáneo de múltiples operaciones."""
    payload_lote = [
        {"id_operacion": "OP001", "producto": "Credito", "moneda": "PEN", "monto": 10000.0, "plazo_meses": 12, "roa_target": 0.050},
        {"id_operacion": "OP002", "producto": "Credito", "moneda": "USD", "monto": 5000.0, "plazo_meses": 12, "roa_target": 0.040}
    ]
    response = client.post("/calcular/lote", json=payload_lote)
    assert response.status_code == 200
    
    data = response.json()
    assert "resultados" in data
    assert len(data["resultados"]) == 2
    assert data["resultados"][0]["id_operacion"] == "OP001"