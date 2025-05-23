# src/wacc.py

import yfinance as yf

def calcular_wacc(ticker: str, rf: float = 0.04, rm: float = 0.10) -> float:
    """
    Calcula o WACC (Custo Médio Ponderado de Capital).

    rf: taxa livre de risco (Risk-free rate)
    rm: retorno esperado do mercado (Expected market return)
    """
    try:
        empresa = yf.Ticker(ticker)
        info = empresa.info

        beta = info.get('beta', 1.0)
        ke = rf + beta * (rm - rf)  # CAPM

        # Suposições simples para dívida
        kd = 0.08  # custo da dívida estimado
        taxa_imposto = 0.34  # imposto estimado (Brasil ou média global)

        # Estrutura de capital (estimativas simples se não houver dados reais)
        valor_mercado_acao = info.get('marketCap', 1e9)
        valor_divida = info.get('totalDebt', 1e8)
        total = valor_mercado_acao + valor_divida

        peso_acao = valor_mercado_acao / total
        peso_divida = valor_divida / total

        wacc = peso_acao * ke + peso_divida * kd * (1 - taxa_imposto)
        return round(wacc, 4)

    except Exception as e:
        print(f"Erro ao calcular WACC: {e}")
        return 0.10  # valor padrão em caso de falha


def calcular_custo_capital_proprio(beta: float, rf: float = 0.04, rm: float = 0.10) -> float:
    """
    Calcula o custo do capital próprio usando o modelo CAPM.
    """
    return round(rf + beta * (rm - rf), 4)
