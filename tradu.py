import streamlit as st
import fitz  # PyMuPDF
from deep_translator import GoogleTranslator
import io
import re

class PDFTranslator:
    def __init__(self):
        self.supported_languages = {
            'Português': 'pt',
            'Inglês': 'en',
            'Espanhol': 'es',
            'Francês': 'fr',
            'Alemão': 'de',
            'Italiano': 'it'
        }

    def translate_pdf(self, pdf_file, target_lang):
        # Criar um objeto PDF da entrada
        doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
        # Criar um novo documento para a tradução
        new_doc = fitz.open()
        translator = GoogleTranslator(source='auto', target=target_lang)

        # Processar cada página
        for page_num in range(len(doc)):
            # Obter a página original
            page = doc[page_num]
            
            # Copiar a página para manter layout, imagens e formatação
            new_page = new_doc.new_page(width=page.rect.width,
                                      height=page.rect.height)
            
            # Copiar o conteúdo original para a nova página
            new_page.show_pdf_page(new_page.rect, doc, page_num)
            
            # Extrair blocos de texto
            blocks = page.get_text("blocks")
            
            # Para cada bloco de texto na página
            for block in blocks:
                if block[6] == 0:  # Se for um bloco de texto
                    rect = fitz.Rect(block[:4])
                    text = block[4]
                    
                    # Traduzir o texto
                    try:
                        translated_text = translator.translate(text)
                        
                        # Criar um novo bloco de texto com o conteúdo traduzido
                        # Primeiro, limpar a área original
                        new_page.draw_rect(rect, color=None, fill=(1, 1, 1))
                        
                        # Inserir o texto traduzido
                        new_page.insert_text(
                            rect.tl,  # Posição superior esquerda do retângulo
                            translated_text,
                            fontsize=10,  # Ajuste conforme necessário
                            color=(0, 0, 0)
                        )
                    except Exception as e:
                        st.warning(f"Erro ao traduzir bloco: {str(e)}")
                        continue

        # Obter o PDF traduzido como bytes
        pdf_bytes = new_doc.tobytes()
        
        # Fechar os documentos
        doc.close()
        new_doc.close()
        
        return pdf_bytes

    def clean_filename(self, filename):
        return re.sub(r'[<>:"/\\|?*]', '', filename)

def main():
    st.set_page_config(page_title="PDF Translator", layout="wide")
    
    st.title("📚 Tradutor de PDF")
    st.markdown("### Traduza seus documentos PDF mantendo a estrutura original")
    
    translator = PDFTranslator()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Upload do PDF")
        pdf_file = st.file_uploader("Escolha um arquivo PDF", type=['pdf'])
        
        target_language = st.selectbox(
            "Selecione o idioma de destino",
            list(translator.supported_languages.keys())
        )
        
        if st.button("Traduzir"):
            if pdf_file is not None:
                with st.spinner("Traduzindo o documento... Isso pode levar alguns minutos."):
                    try:
                        # Traduzir o PDF
                        target_lang_code = translator.supported_languages[target_language]
                        translated_pdf = translator.translate_pdf(pdf_file, target_lang_code)
                        
                        st.success("Tradução concluída!")
                        
                        # Criar nome do arquivo traduzido
                        original_filename = pdf_file.name
                        translated_filename = f"traduzido_{original_filename}"
                        
                        # Botão de download
                        st.download_button(
                            label="Download do PDF traduzido",
                            data=translated_pdf,
                            file_name=translated_filename,
                            mime="application/pdf"
                        )
                            
                    except Exception as e:
                        st.error(f"Erro ao processar o PDF: {str(e)}")
            else:
                st.warning("Por favor, faça upload de um arquivo PDF primeiro.")

    st.markdown("---")
    st.markdown("""
    ### Como usar:
    1. Faça upload do seu arquivo PDF
    2. Selecione o idioma de destino
    3. Clique em "Traduzir"
    4. Baixe o PDF traduzido
    
    ### Observações:
    - A estrutura original do PDF será mantida (formatação, imagens, layout)
    - O processo pode levar alguns minutos dependendo do tamanho do documento
    - Alguns elementos complexos podem requerer ajustes manuais
    """)

if __name__ == "__main__":
    main()
