def calcular_dcf(receita, margem, crescimento, wacc, anos):
    fluxos = []
    for i in range(anos):
        fcf = receita * (1 + crescimento) ** (i + 1) * margem
        fluxo_descontado = fcf / (1 + wacc) ** (i + 1)
        fluxos.append(fluxo_descontado)

    valor_terminal = fluxos[-1] * (1 + crescimento) / (wacc - crescimento)
    valor_terminal_presente = valor_terminal / (1 + wacc) ** anos

    valor_justo = sum(fluxos) + valor_terminal_presente
    return valor_justo
