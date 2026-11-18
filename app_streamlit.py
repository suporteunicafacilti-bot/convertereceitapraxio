import streamlit as st
import os

st.set_page_config(
    page_title="Sistema BGM - Substituição de Colunas",
    page_icon="📄",
    layout="centered"
)

st.title("📄 Sistema de Substituição de Colunas (TXT - BGM)")
st.markdown("Faça o upload do seu arquivo de texto original para realizar a substituição automática das colunas mantendo a estrutura original.")

with st.expander("ℹ️ Regras de Processamento"):
    st.markdown("- **Origem:** 6 caracteres imediatamente anteriores ao `*` final (colunas 234 a 239).")
    st.markdown("- **Destino:** Colunas 74 a 79 (base 1).")
    st.markdown("- **Preservação:** Coluna 80 e toda a estrutura, espaços e quebras de linha são mantidos intactos.")

uploaded_file = st.file_uploader("Selecione o arquivo TXT original", type=["txt"])

def processar_conteudo_bytes(conteudo_bytes):
    linhas_alteradas = 0
    linhas_ignoradas = 0
    resultado = []
    
    # Decodifica usando latin-1 para preservar caracteres especiais de ERPs
    linhas = conteudo_bytes.decode("latin-1").splitlines(keepends=True)
    
    for linha in linhas:
        quebra = "\r\n" if linha.endswith("\r\n") else "\n" if linha.endswith("\n") else ""
        conteudo = linha.rstrip("\r\n")
        
        DESTINO_INICIO, DESTINO_FIM = 74, 79
        ORIGEM_INICIO, ORIGEM_FIM   = 234, 239
        
        idx_dest_ini, idx_dest_fim = DESTINO_INICIO - 1, DESTINO_FIM
        idx_orig_ini, idx_orig_fim = ORIGEM_INICIO - 1, ORIGEM_FIM

        if len(conteudo) >= 239 and conteudo.endswith("*"):
            chars = list(conteudo)
            valor_origem = chars[-7:-1]
            chars[idx_dest_ini:idx_dest_fim] = valor_origem
            resultado.append("".join(chars) + quebra)
            linhas_alteradas += 1
        elif len(conteudo) >= ORIGEM_FIM:
            chars = list(conteudo)
            chars[idx_dest_ini:idx_dest_fim] = chars[idx_orig_ini:idx_orig_fim]
            resultado.append("".join(chars) + quebra)
            linhas_alteradas += 1
        else:
            resultado.append(conteudo + quebra)
            linhas_ignoradas += 1
            
    # Codifica de volta para latin-1
    return "".join(resultado).encode("latin-1"), linhas_alteradas, linhas_ignoradas

if uploaded_file is not None:
    st.success(f"Arquivo carregado com sucesso: **{uploaded_file.name}**")
    
    if st.button("🚀 Processar Arquivo", type="primary"):
        bytes_dados = uploaded_file.getvalue()
        bytes_saida, alteradas, ignoradas = processar_conteudo_bytes(bytes_dados)
        
        nome_base, ext = os.path.splitext(uploaded_file.name)
        nome_saida = f"{nome_base}_final{ext}"
        
        st.balloons()
        st.markdown("---")
        st.subheader("📊 Resumo do Processamento")
        col1, col2 = st.columns(2)
        col1.metric("Linhas Alteradas", alteradas)
        col2.metric("Linhas Mantidas Intactas", ignoradas)
        
        st.download_button(
            label="📥 Baixar Arquivo Processado",
            data=bytes_saida,
            file_name=nome_saida,
            mime="text/plain"
        )
