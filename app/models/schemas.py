from pydantic import BaseModel, Field
from typing import List

class OperacionInput(BaseModel):
    id_operacion: str = Field(..., description="ID único de la operación")
    producto: str = Field(..., description="Tipo de producto (ej. Credito, Leasing)")
    moneda: str = Field(..., description="Moneda de la operación (PEN, USD)")
    monto: float = Field(..., gt=0, description="Monto de la operación")
    plazo_meses: int = Field(..., gt=0, description="Plazo en meses")
    roa_target: float = Field(..., description="ROA objetivo esperado")

class OperacionOutput(BaseModel):
    # Se prioriza el orden: identificadores y tipo primero, seguido de las métricas clave
    id_operacion: str
    producto: str
    tea_optima: float
    clv_final: float
    roa_alcanzado: float

class LoteOutput(BaseModel):
    resultados: List[OperacionOutput]