# modules/comparables.py

def valuation_por_multiplos(preco_lucro, lucro_liquido):
    """
    Calcula o valor justo de uma empresa com base no múltiplo Preço/Lucro (P/L)
    e o lucro líquido anual.

    Parâmetros:
    - preco_lucro (float): múltiplo P/L atual do mercado ou setor.
    - lucro_liquido (float): lucro líquido anual da empresa.

    Retorna:
    - float: valor justo estimado da empresa.
    """
    if preco_lucro is None or lucro_liquido is None:
        return None
    if preco_lucro <= 0 or lucro_liquido <= 0:
        return None
    return preco_lucro * lucro_liquido

