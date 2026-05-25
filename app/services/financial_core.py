import numpy as np

class FinancialCore:
    def __init__(self, data_loader):
        """Inyectar el DataLoader optimizado para consultas."""
        self.dl = data_loader

    # ==========================================
    # 1. Módulo de Amortización Francesa
    # ==========================================
    @staticmethod
    def calcular_cuota(monto: float, tem: float, plazo_meses: int) -> float:
        """
        Calcular la cuota constante (Amortización Francesa).
        """
        if tem <= 0:
            return monto / plazo_meses
        # Fórmula matemática estándar para anualidades
        cuota = monto * (tem * (1 + tem)**plazo_meses) / ((1 + tem)**plazo_meses - 1)
        return cuota

    @staticmethod
    def generar_saldos(monto: float, cuota: float, tem: float, plazo_meses: int) -> list:
        """Generar el cronograma de saldos remanentes mes a mes."""
        saldos = [monto] # Mes 0
        saldo_actual = monto
        for _ in range(plazo_meses):
            interes = saldo_actual * tem
            amortizacion = cuota - interes
            saldo_actual -= amortizacion
            # Se usa max(0, ...) para evitar saldos negativos residuales por precisión flotante
            saldos.append(max(0, saldo_actual)) 
        return saldos

    # ==========================================
    # 2. Módulo de Interpolación de Tasas
    # ==========================================
    def interpolar_tasa_fondeo(self, producto: str, moneda: str, plazo_dias: int) -> float:
        """
        Usa np.interp para una interpolación lineal extremadamente rápida en C.
        Reemplaza la ineficiente manipulación de DataFrames dentro de bucles.
        """
        curva = self.dl.get_curva_tasas(producto, moneda)
        if not curva:
            return 0.0
        
        # Separar la lista de tuplas en vectores X (plazos) e Y (tasas)
        plazos_x = [punto[0] for punto in curva]
        tasas_y = [punto[1] for punto in curva]
        
        # np.interp maneja automáticamente los límites y la interpolación
        tasa_interpolada = np.interp(plazo_dias, plazos_x, tasas_y)
        return float(tasa_interpolada)

    # ==========================================
    # 3. Módulo de Probabilidad de Supervivencia
    # ==========================================
    def calcular_supervivencia(self, producto: str, plazo_meses: int) -> list:
        """
        Calcular la curva de supervivencia acumulada.
        S(t) = S(t-1) * (1 - PD_marginal_t)
        """
        supervivencia = [1.0] # La probabilidad de sobrevivir en el mes 0 es 100%
        sup_actual = 1.0
        
        for mes in range(1, plazo_meses + 1):
            pd_marginal = self.dl.get_pd_marginal(producto, mes)
            sup_actual *= (1 - pd_marginal)
            supervivencia.append(sup_actual)
            
        return supervivencia