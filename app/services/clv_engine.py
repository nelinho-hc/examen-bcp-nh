from app.services.financial_core import FinancialCore

class CLVEngine:
    def __init__(self, core: FinancialCore):
        self.core = core

    def calcular_clv(self, producto: str, moneda: str, monto: float, plazo_meses: int, tea: float) -> dict:
        """
        Proyectar el flujo de caja del crédito y retorna el CLV y el ROA calculado.
        """
        # 1. Conversión de tasas
        tem = (1 + tea)**(1/12) - 1
        tasa_fondeo_anual = self.core.interpolar_tasa_fondeo(producto, moneda, plazo_meses * 30)
        tem_fondeo = (1 + tasa_fondeo_anual)**(1/12) - 1

        # 2. Generación de curvas base
        cuota = self.core.calcular_cuota(monto, tem, plazo_meses)
        saldos = self.core.generar_saldos(monto, cuota, tem, plazo_meses)
        supervivencia = self.core.calcular_supervivencia(producto, plazo_meses)
        
        # 3. Obtención de costos iniciales
        costos = self.core.dl.get_costos(producto, moneda)
        gasto_originacion = monto * costos['originacion']
        gasto_mantenimiento_mensual = monto * (costos['mantenimiento'] / 12)

        clv_acumulado = -gasto_originacion

        # 4. Proyección de flujos mensuales
        for mes in range(1, plazo_meses + 1):
            saldo_anterior = saldos[mes-1]
            
            # Ingresos y Egresos
            ingreso_financiero = saldo_anterior * tem
            costo_financiero = saldo_anterior * tem_fondeo
            margen_financiero = ingreso_financiero - costo_financiero
            
            # Pérdida Esperada (Probabilidad de Default Marginal * Saldo)
            pd_marginal = self.core.dl.get_pd_marginal(producto, mes)
            perdida_esperada = saldo_anterior * pd_marginal
            
            # Flujo Neto Ajustado por Supervivencia
            flujo_neto = margen_financiero - gasto_mantenimiento_mensual - perdida_esperada
            flujo_ajustado = flujo_neto * supervivencia[mes]
            
            # Descuento a Valor Presente (usando la tasa de fondeo como factor de descuento)
            factor_descuento = (1 + tem_fondeo)**mes
            flujo_descontado = flujo_ajustado / factor_descuento
            
            clv_acumulado += flujo_descontado

        # 5. Cálculo del ROA
        roa_calculado = clv_acumulado / monto

        return {
            "tea_evaluada": tea,
            "clv": round(clv_acumulado, 4),
            "roa": round(roa_calculado, 6)
        }