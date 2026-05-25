from fastapi import FastAPI, HTTPException
from typing import List
from app.models.schemas import OperacionInput, OperacionOutput, LoteOutput
from app.core.data_loader import DataLoaderOpt
from app.services.financial_core import FinancialCore
from app.services.clv_engine import CLVEngine
from app.services.tea_optimizer import TEAOoptimizer

app = FastAPI(
    title="API Modelo CLV - Pricing",
    description="API REST optimizada para cálculo de TEA basada en ROA target.",
    version="1.0.0"
)

# Inyección de dependencias estáticas (cargadas solo una vez al iniciar)
data_loader = DataLoaderOpt()
financial_core = FinancialCore(data_loader)
clv_engine = CLVEngine(financial_core)
tea_optimizer = TEAOoptimizer(clv_engine)

@app.get("/health", tags=["Health"])
def health_check():
    """Endpoint de salud para validar que el servicio está activo."""
    return {"status": "ok", "message": "API Modelo CLV operativa"}

@app.post("/calcular", response_model=OperacionOutput, tags=["Cálculo"])
def calcular_operacion(op: OperacionInput):
    """Calcula la TEA óptima y el CLV para una sola operación."""
    try:
        resultado = tea_optimizer.buscar_tea_optima(
            producto=op.producto,
            moneda=op.moneda,
            monto=op.monto,
            plazo_meses=op.plazo_meses,
            roa_target=op.roa_target
        )
        return OperacionOutput(
            id_operacion=op.id_operacion,
            producto=op.producto,
            tea_optima=resultado["tea_optima"],
            clv_final=resultado["clv_final"],
            roa_alcanzado=resultado["roa_alcanzado"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/calcular/lote", response_model=LoteOutput, tags=["Cálculo"])
def calcular_lote(operaciones: List[OperacionInput]):
    """Procesa un array de operaciones y devuelve los resultados en una sola ejecución."""
    resultados = []
    for op in operaciones:
        try:
            res = tea_optimizer.buscar_tea_optima(
                producto=op.producto,
                moneda=op.moneda,
                monto=op.monto,
                plazo_meses=op.plazo_meses,
                roa_target=op.roa_target
            )
            resultados.append(OperacionOutput(
                id_operacion=op.id_operacion,
                producto=op.producto,
                tea_optima=res["tea_optima"],
                clv_final=res["clv_final"],
                roa_alcanzado=res["roa_alcanzado"]
            ))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error en OP {op.id_operacion}: {str(e)}")
    
    return LoteOutput(resultados=resultados)