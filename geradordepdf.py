import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
import io
from datetime import datetime
import textwrap
from PIL import Image
from reportlab.lib.utils import ImageReader

# Função para criar o PDF
def create_pdf(cliente, telefone, endereco, prazo_execucao, descricao_servico, forma_pagamento, valor_acordado, observacao, logo_data, title_image_data):
    buffer = io.BytesIO()
    
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Adicionar imagem ao cabeçalho
    if logo_data:
        logo_image = Image.open(io.BytesIO(logo_data))
        logo_image_buffer = io.BytesIO()
        logo_image.save(logo_image_buffer, format='PNG')
        logo_image_buffer.seek(0)
        logo_image_reader = ImageReader(logo_image_buffer)
        c.drawImage(logo_image_reader, 2*cm, height - 4*cm, width=4*cm, preserveAspectRatio=True, mask='auto')
    
    # Adicionar imagem acima do título
    if title_image_data:
        title_image = Image.open(io.BytesIO(title_image_data))
        title_image_buffer = io.BytesIO()
        title_image.save(title_image_buffer, format='PNG')
        title_image_buffer.seek(0)
        title_image_reader = ImageReader(title_image_buffer)
        c.drawImage(title_image_reader, (width - 8*cm) / 2, height - 8*cm, width=8*cm, preserveAspectRatio=True, mask='auto')

    # Centralizar título
    c.setFont("Helvetica-Bold", 16)
    title = "Orçamento de Demolição"
    c.drawCentredString(width / 2.0, height - 10*cm, title)
    
    # Informações do cliente e serviço
    c.setFont("Helvetica", 12)
    c.drawString(2*cm, height - 12*cm, f"Cliente: {cliente}")
    c.drawString(2*cm, height - 13*cm, f"Telefone: {telefone}")
    c.drawString(2*cm, height - 14*cm, f"Endereço: {endereco}")
    c.drawString(2*cm, height - 15*cm, f"Prazo de Execução: {prazo_execucao}")
    c.drawString(2*cm, height - 16*cm, f"Descrição do Serviço: {descricao_servico}")
    c.drawString(2*cm, height - 17*cm, f"Forma de Pagamento: {forma_pagamento}")
    c.drawString(2*cm, height - 18*cm, f"Valor Acordado: R${valor_acordado:,.2f}")
    c.drawString(2*cm, height - 19*cm, f"Observação: {observacao}")

    # Termos de acordo
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2*cm, height - 20*cm, "Termos de Acordo:")
    c.setFont("Helvetica", 10)
    terms = [
        "a) Serviços Prestados: O contratante concorda em realizar a demolição completa do imóvel conforme descrito na seção 1 deste documento.",
        "b) Alterações no Escopo: Qualquer alteração no escopo dos serviços acordados deverá ser comunicada por escrito e pode resultar em ajustes no preço e no prazo de execução.",
        "c) Pagamento: O cliente concorda em pagar o valor total estipulado neste orçamento de demolição, conforme descrito na seção VALOR, após a conclusão satisfatória dos serviços."
    ]
    
    y_position = height - 21*cm
    max_width = width - 4*cm  # Margem de 2 cm de cada lado
    for term in terms:
        wrapped_text = textwrap.wrap(term, width=100)  # Ajuste o valor de width conforme necessário
        for line in wrapped_text:
            c.drawString(2*cm, y_position, line)
            y_position -= 0.5*cm

    # Data e assinaturas
    c.drawString(2*cm, 6*cm, f"Data: {datetime.now().strftime('%d/%m/%Y')}")
    c.drawString(2*cm, 5*cm, "Cliente: ___________________________")
    c.drawString(2*cm, 4.5*cm, cliente)
    c.drawString(10*cm, 5*cm, "Herenildo Da Silva Souza: ___________________________")

    # Rodapé
    c.setFont("Helvetica", 8)
    c.drawString(2*cm, 1.5*cm, "Demolidora Genial - Documento gerado automaticamente")
    
    c.showPage()
    c.save()
    
    buffer.seek(0)
    return buffer

# Interface Streamlit
st.title('Gerador de Orçamentos de Demolição')

st.markdown("## Informações do Cliente")
cliente = st.text_input('Nome do Cliente')
telefone = st.text_input('Telefone')
endereco = st.text_area('Endereço')

st.markdown("## Detalhes do Serviço")
prazo_execucao = st.text_input('Prazo de Execução')
descricao_servico = st.text_area('Descrição do Serviço')
forma_pagamento = st.text_input('Forma de Pagamento')  # Alterado para input de texto
valor_acordado = st.number_input('Valor Acordado', format="%.2f")
observacao = st.text_area('Observação')

# Upload das imagens
logo_data = st.file_uploader("Upload do Logo", type=["jpg", "jpeg", "png"])
title_image_data = st.file_uploader("Upload da Imagem do Título", type=["jpg", "jpeg", "png"])

if st.button('Gerar PDF'):
    if logo_data:
        logo_data = logo_data.read()
    if title_image_data:
        title_image_data = title_image_data.read()
    
    pdf = create_pdf(cliente, telefone, endereco, prazo_execucao, descricao_servico, forma_pagamento, valor_acordado, observacao, logo_data, title_image_data)
    
    st.download_button(
        label="Baixar PDF",
        data=pdf,
        file_name=f"orcamento_{cliente}.pdf",
        mime="application/pdf"
    )
