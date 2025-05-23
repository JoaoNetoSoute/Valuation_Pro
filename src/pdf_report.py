from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import cm
import datetime
import tempfile
import os

def gerar_relatorio_pdf(ticker, valor_justo, wacc, df_fluxo, df_multiplos, path_imagem=None):
    buffer = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf = canvas.Canvas(buffer.name, pagesize=A4)
    largura, altura = A4

    pdf.setTitle(f"Valuation Report - {ticker}")
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(2 * cm, altura - 2 * cm, f"📊 Relatório de Valuation: {ticker.upper()}")
    
    pdf.setFont("Helvetica", 10)
    pdf.drawString(2 * cm, altura - 2.7 * cm, f"Data de Geração: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}")
    pdf.line(2 * cm, altura - 2.9 * cm, largura - 2 * cm, altura - 2.9 * cm)

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(2 * cm, altura - 4 * cm, "📌 Dados Principais:")
    pdf.setFont("Helvetica", 11)
    pdf.drawString(2.5 * cm, altura - 4.8 * cm, f"Valor Justo por Ação (DCF): US$ {valor_justo:.2f}")
    pdf.drawString(2.5 * cm, altura - 5.4 * cm, f"WACC Utilizado: {wacc:.2%}")

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(2 * cm, altura - 6.5 * cm, "📊 Múltiplos de Mercado:")
    y = altura - 7.3 * cm
    pdf.setFont("Helvetica", 10)
    for idx, row in df_multiplos.head(5).iterrows():
        texto = ", ".join([f"{col}: {row[col]}" for col in df_multiplos.columns])
        pdf.drawString(2.2 * cm, y, texto[:120])  # Evita texto muito longo
        y -= 0.6 * cm

    if path_imagem and os.path.exists(path_imagem):
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(2 * cm, y - 1 * cm, "📈 Benchmarking Visual:")
        pdf.drawImage(path_imagem, 2 * cm, y - 10 * cm, width=16 * cm, height=8 * cm)

    pdf.showPage()
    pdf.save()

    with open(buffer.name, "rb") as f:
        pdf_bytes = f.read()
    os.remove(buffer.name)
    return pdf_bytes
