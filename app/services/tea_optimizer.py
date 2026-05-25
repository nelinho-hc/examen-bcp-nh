from app.services.clv_engine import CLVEngine

class TEAOoptimizer:
    def __init__(self, engine: CLVEngine):
        self.engine = engine

    def buscar_tea_optima(self, producto: str, moneda: str, monto: float, plazo_meses: int, roa_target: float) -> dict:
        """
        Encuentra la TEA que iguala el ROA calculado con el ROA objetivo mediante Bisección.
        Límites de búsqueda: 0.1% a 150% (0.001 a 1.5).
        """
        tea_min = 0.001
        tea_max = 1.500
        tolerancia = 0.00001
        iteraciones_max = 50
        
        mejor_clv = 0.0
        tea_optima = 0.0
        
        for _ in range(iteraciones_max):
            tea_mid = (tea_min + tea_max) / 2.0
            
            # Evaluar el modelo con la TEA media
            resultado = self.engine.calcular_clv(producto, moneda, monto, plazo_meses, tea_mid)
            roa_calculado = resultado['roa']
            
            # Verificar si hemos alcanzado la convergencia
            if abs(roa_calculado - roa_target) <= tolerancia:
                tea_optima = tea_mid
                mejor_clv = resultado['clv']
                break
                
            # Ajustar los límites de bisección
            if roa_calculado < roa_target:
                # Si el ROA es menor al objetivo, necesitamos cobrar una TEA mayor
                tea_min = tea_mid
            else:
                # Si el ROA es mayor, podemos reducir la TEA
                tea_max = tea_mid
                
        # Guardar la última iteración si no converge exactamente por límite de iteraciones
        if tea_optima == 0.0:
            tea_optima = tea_mid
            mejor_clv = resultado['clv']

        # Salida estandarizada priorizando el orden de las métricas clave
        return {
            "tea_optima": round(tea_optima, 4),
            "clv_final": round(mejor_clv, 2),
            "roa_alcanzado": round(resultado['roa'], 4)
        }