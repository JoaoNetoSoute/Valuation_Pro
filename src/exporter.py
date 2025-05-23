import pandas as pd
from io import BytesIO

def exportar_para_excel(fluxo_df: pd.DataFrame, df_sensibilidade: pd.DataFrame, valor_justo: float) -> BytesIO:
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        # Aba 1: Fluxo de Caixa
        fluxo_df.to_excel(writer, sheet_name='Fluxo de Caixa', index=False)

        # Aba 2: Sensibilidade
        df_sensibilidade.to_excel(writer, sheet_name='Sensibilidade')

        # Aba 3: Resumo
        resumo_df = pd.DataFrame({
            'Métrica': ['Valor Justo por Ação'],
            'Valor': [valor_justo]
        })
        resumo_df.to_excel(writer, sheet_name='Resumo', index=False)

    buffer.seek(0)
    return buffer
