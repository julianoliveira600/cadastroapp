
import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Configurações da página
st.set_page_config(page_title="Cadastro de Clientes", page_icon="📋", layout="centered")

# Nome do arquivo local onde os dados serão armazenados
ARQUIVO_DADOS = "clientes_cadastrados.csv"

st.title("📋 Cadastro de Clientes")
st.write("Preencha os campos abaixo para registrar seus dados:")

# Formulário com limpeza automática após o envio
with st.form(key="form_cadastro", clear_on_submit=True):
    nome = st.text_input("Nome Completo *", placeholder="Ex: Maria Silva")
    email = st.text_input("E-mail *", placeholder="Ex: maria@email.com")
    
    col1, col2 = st.columns(2)
    with col1:
        telefone = st.text_input("Telefone / WhatsApp", placeholder="Ex: (43) 99999-9999")
    with col2:
        endereco = st.text_input("Endereço", placeholder="Ex: Rua das Flores, 123")
        
    enviado = st.form_submit_button("Salvar Cadastro", use_container_width=True)

if enviado:
    if not nome.strip() or not email.strip():
        st.error("⚠️ Os campos Nome e E-mail são obrigatórios.")
    else:
        novo_registro = pd.DataFrame([{
            "Data_Registro": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "Nome": nome.strip(),
            "Email": email.strip(),
            "Telefone": telefone.strip(),
            "Endereco": endereco.strip()
        }])
        
        # Gravação no CSV
        if os.path.exists(ARQUIVO_DADOS):
            df_existente = pd.read_csv(ARQUIVO_DADOS)
            df_atualizado = pd.concat([df_existente, novo_registro], ignore_index=True)
            df_atualizado.to_csv(ARQUIVO_DADOS, index=False)
        else:
            novo_registro.to_csv(ARQUIVO_DADOS, index=False)
            
        st.success(f"✅ Cadastro de {nome} salvo com sucesso!")

# Visualização da tabela e botão de download
if os.path.exists(ARQUIVO_DADOS):
    st.divider()
    st.subheader("📊 Registros Salvos")
    df = pd.read_csv(ARQUIVO_DADOS)
    st.dataframe(df, use_container_width=True)
    
    csv_bytes = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Baixar Planilha CSV",
        data=csv_bytes,
        file_name="clientes_cadastrados.csv",
        mime="text/csv"
    )