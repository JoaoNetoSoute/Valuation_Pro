def valuation_por_multiplos(preco_lucro, lucro_liquido):
    """
    Calcula o valor justo baseado em múltiplo P/L e lucro líquido anual.
    """
    if preco_lucro <= 0:
        return None
    return preco_lucro * lucro_liquido

