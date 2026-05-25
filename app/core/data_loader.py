import pandas as pd
from app.core.config import settings

class DataLoaderOpt:
    def __init__(self):
        self.costos_dict = {}
        self.pd_dict = {}
        self.tasas_dict = {}
        self._cargar_datos()

    def _cargar_datos(self):
        """Carga los CSV y los transforma en diccionarios de acceso rápido."""
        
        # 1. Cargar y mapear Costos
        df_costos = pd.read_csv(settings.COSTOS_FILE)
        # Llave: (producto, moneda), Valor: (originacion_pct, mantenimiento_pct)
        for _, row in df_costos.iterrows():
            llave = (row['producto'], row['moneda'])
            self.costos_dict[llave] = {
                'originacion': row['costo_originacion_pct'],
                'mantenimiento': row['costo_mantenimiento_anual_pct']
            }

        # 2. Cargar y mapear Probabilidad de Default (PD)
        df_pd = pd.read_csv(settings.PD_FILE)
        # Llave: (producto, mes), Valor: pd_marginal
        for _, row in df_pd.iterrows():
            llave = (row['producto'], int(row['mes']))
            self.pd_dict[llave] = row['pd_marginal']

        # 3. Cargar y mapear Tasas de Transferencia
        df_tasas = pd.read_csv(settings.TASAS_FILE)
        # Llave: (producto, moneda), Valor: lista de tuplas (plazo_dias, tasa_anual)
        for _, row in df_tasas.iterrows():
            llave = (row['producto'], row['moneda'])
            if llave not in self.tasas_dict:
                self.tasas_dict[llave] = []
            self.tasas_dict[llave].append((int(row['plazo_dias']), row['tasa_anual']))
        
        # Ordenar las tasas por plazo para facilitar la interpolación posterior
        for llave in self.tasas_dict:
            self.tasas_dict[llave] = sorted(self.tasas_dict[llave], key=lambda x: x[0])

    def get_costos(self, producto: str, moneda: str) -> dict:
        # Retorna valores por defecto si no encuentra el cruce
        return self.costos_dict.get((producto, moneda), {'originacion': 0.02, 'mantenimiento': 0.02})

    def get_pd_marginal(self, producto: str, mes: int) -> float:
        return self.pd_dict.get((producto, mes), 0.0)

    def get_curva_tasas(self, producto: str, moneda: str) -> list:
        return self.tasas_dict.get((producto, moneda), [])