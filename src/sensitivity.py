import numpy as np
import pandas as pd
from src.dcf import calcular_vpl_dcf
from src.wacc import calcular_wacc

def analise_sensibilidade(ticker, rf, rm, anos, wacc_range=(0.08, 0.14, 0.01), g_range=(0.00, 0.05, 0.01)):
    """
    Realiza a análise de sensibilidade do valor justo variando WACC e crescimento perpétuo (g).
    """
    wacc_vals = np.arange(*wacc_range)
    g_vals = np.arange(*g_range)

    tabela = []

    for g in g_vals:
        linha = []
        for wacc in wacc_vals:
            try:
                resultado = calcular_vpl_dcf(ticker, wacc, g, anos)
                valor = resultado["valor_justo"]
            except:
                valor = np.nan  # Falha no cálculo
            linha.append(valor)
        tabela.append(linha)

    df = pd.DataFrame(tabela, index=[f"{g:.2%}" for g in g_vals], columns=[f"{w:.2%}" for w in wacc_vals])
    df.index.name = "Crescimento Perpétuo (g)"
    df.columns.name = "WACC"

    return df
