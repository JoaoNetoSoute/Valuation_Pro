def gerar_resumo(ticker, valor_justo, wacc, crescimento, anos, comparables_interp):
    resumo = f"""
📘 **Resumo do Valuation - {ticker.upper()}**

🔹 O valuation foi realizado utilizando o método do **Fluxo de Caixa Descontado (DCF)**, com um horizonte de projeção de **{anos} anos**, uma taxa de desconto (**WACC**) de **{wacc:.2%}** e uma taxa de crescimento perpétuo de **{crescimento:.2%}**.

💵 O **valor justo por ação estimado** é de **US$ {valor_justo:.2f}**, o que serve como referência para análise de investimento com base no fluxo de caixa futuro.

📊 **Múltiplos de mercado** (P/L, EV/EBITDA, etc.) também foram analisados como abordagem complementar ao DCF. Abaixo segue a interpretação dos múltiplos:

{comparables_interp}

📈 Também foi realizada uma **análise de sensibilidade**, variando o WACC e o crescimento perpétuo, para entender como essas variáveis impactam o valor justo.

🧠 Com base nesses dados, o investidor pode tomar decisões mais fundamentadas, considerando tanto o valuation absoluto (DCF) quanto relativo (múltiplos).
"""
    return resumo
