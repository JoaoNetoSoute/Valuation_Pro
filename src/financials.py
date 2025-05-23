# src/financials.py

import yfinance as yf
import pandas as pd

def buscar_dados_financeiros(ticker_symbol):
    """
    Coleta os principais demonstrativos financeiros da empresa via yfinance.
    
    Args:
        ticker_symbol (str): Código da ação (ex: 'AAPL', 'PETR4.SA')
    
    Returns:
        dict: Contendo income statement, balance sheet e cashflow
    """
    try:
        empresa = yf.Ticker(ticker_symbol)

        df_income = empresa.financials.T
        df_balance = empresa.balance_sheet.T
        df_cashflow = empresa.cashflow.T

        # Removendo colunas totalmente vazias e preenchendo NaNs com zero
        df_income = df_income.dropna(axis=1, how='all').fillna(0)
        df_balance = df_balance.dropna(axis=1, how='all').fillna(0)
        df_cashflow = df_cashflow.dropna(axis=1, how='all').fillna(0)

        return {
            "income": df_income,
            "balance": df_balance,
            "cashflow": df_cashflow
        }

    except Exception as e:
        print(f"[ERRO] Falha ao buscar dados: {e}")
        return None
