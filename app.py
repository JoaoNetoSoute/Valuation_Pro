import streamlit as st
from src.dcf import calcular_vpl_dcf
from src.wacc import calcular_wacc
from src.sensitivity import analise_sensibilidade
from src.exporter import exportar_para_excel
from src.comparables import obter_multiplicadores, interpretar_multiplicadores
from src.valuation_summary import gerar_resumo_valuation, gerar_comparativo_valores
from src.pdf_report import gerar_relatorio_pdf
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import tempfile

st.set_page_config(page_title="Valuation Pro", layout="centered")
st.title("📊 Valuation Pro - DCF & Comparables")

st.sidebar.header("🔍 Parâmetros de Avaliação")
ticker = st.sidebar.text_input("Código da Ação (ex: AAPL, PETR4.SA)", value="AAPL")
risk_free = st.sidebar.number_input("Taxa Livre de Risco (rf)", value=0.04)
market_return = st.sidebar.number_input("Retorno Esperado do Mercado (rm)", value=0.10)
desconto = st.sidebar.slider("Taxa de Desconto (%)", 5.0, 15.0, 10.0)
crescimento_perpetuo = st.sidebar.slider("Crescimento Perpétuo (%)", 0.0, 5.0, 2.0)
anos = st.sidebar.slider("Anos de Projeção", 3, 10, 5)

if st.sidebar.button("Calcular Valuation"):
    with st.spinner("🔄 Coletando dados e calculando..."):
        try:
            wacc = calcular_wacc(ticker, risk_free, market_return)
            resultado = calcular_vpl_dcf(ticker, wacc, crescimento_perpetuo, anos)

            st.subheader("💰 Resultado do Valuation DCF")
            st.metric(label="Valor Justo por Ação (DCF)", value=f"US$ {resultado['valor_justo']:.2f}")
            st.write(f"WACC Utilizado: **{wacc:.2%}**")
            st.markdown("---")

            st.subheader("📈 Projeções de Fluxo de Caixa")
            st.dataframe(resultado['fluxo'])

            st.markdown("---")
            st.subheader("🎯 Análise de Sensibilidade")
            st.write("Valor justo variando a taxa de desconto (WACC) e crescimento perpétuo (g)")

            df_sens = analise_sensibilidade(ticker, risk_free, market_return, anos)
            st.dataframe(df_sens)

            st.write("🔍 Mapa de Calor (Heatmap)")
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.heatmap(df_sens.astype(float), annot=True, fmt=".2f", cmap="YlGnBu", ax=ax)
            st.pyplot(fig)

            st.markdown("---")
            st.subheader("📊 Múltiplos de Mercado (Comparables)")
            df_multiplos = obter_multiplicadores(ticker)
            st.dataframe(df_multiplos)
            interpretacao = interpretar_multiplicadores(df_multiplos)
            st.markdown(interpretacao)

            st.markdown("---")
            st.subheader("📋 Resumo do Valuation")
            df_resumo = gerar_resumo_valuation(ticker, resultado['valor_justo'], df_multiplos)
            st.dataframe(df_resumo)

            st.subheader("📊 Benchmarking Visual")
            df_comparativo = gerar_comparativo_valores(
                ticker,
                resultado['valor_justo'],
                df_multiplos["Valor Justo (Multiplo)"].mean() if "Valor Justo (Multiplo)" in df_multiplos.columns else None
            )
            fig2, ax2 = plt.subplots()
            sns.barplot(data=df_comparativo, x="Método", y="Valor Estimado", palette="viridis", ax=ax2)
            ax2.set_title("Comparação de Métodos de Valuation")

            temp_img = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
            fig2.savefig(temp_img.name, format="png")
            st.pyplot(fig2)

            st.markdown("---")
            st.subheader("⬇️ Exportar Resultados")
            buffer = exportar_para_excel(resultado['fluxo'], df_sens, resultado['valor_justo'])
            st.download_button(
                label="📥 Baixar Excel",
                data=buffer,
                file_name=f"valuation_{ticker}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

            st.markdown("### 🧾 Gerar Relatório em PDF")
            pdf_bytes = gerar_relatorio_pdf(ticker, resultado['valor_justo'], wacc, resultado['fluxo'], df_multiplos, temp_img.name)
            st.download_button(
                label="📄 Baixar PDF do Relatório",
                data=pdf_bytes,
                file_name=f"relatorio_valuation_{ticker}.pdf",
                mime="application/pdf"
            )

        except Exception as e:
            st.error(f"Erro ao calcular valuation: {e}")
else:
    st.info("Insira um código de ação e clique em 'Calcular Valuation'.")
