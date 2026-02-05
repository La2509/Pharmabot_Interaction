import streamlit as st
import json
from openai import OpenAI

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="PharmaBot AI", page_icon="💊", layout="centered")

# --- FUNÇÕES ---

def analyze_interaction_ai(drug1, drug2, api_key):
    """
    Usa o GPT para detectar e classificar a interação farmacológica.
    Retorna um JSON estruturado com a gravidade e detalhes.
    """
    client = OpenAI(api_key=api_key)
    
    prompt = f"""
    Aja como um Farmacologista Clínico Sênior.
    Analise a interação entre: "{drug1}" e "{drug2}".
    
    Responda EXATAMENTE neste formato JSON (sem markdown):
    {{
        "tem_interacao": true/false,
        "gravidade": "Alta" | "Moderada" | "Leve" | "Nenhuma",
        "mecanismo": "Explicação técnica curta em PT-BR",
        "recomendacao": "Recomendação clínica para o paciente em PT-BR"
    }}
    
    Se não houver interação conhecida, "tem_interacao" deve ser false.
    Considere interações documentadas em bulas e literatura médica (Micromedex/UpToDate).
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", # Ou "gpt-4-turbo" para mais precisão
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            response_format={"type": "json_object"} # Garante que volta um JSON válido
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        st.error(f"Erro na análise: {e}")
        return None

# --- INTERFACE ---

st.title("💊 PharmaBot: Validador de Interações")
st.markdown("Detector de interações movido a **Inteligência Artificial** (Substituto do NIH RxNav).")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuração")
    # Tenta pegar a chave dos secrets ou input manual
    api_key = st.secrets.get("OPENAI_API_KEY")
    if not api_key:
        api_key = st.text_input("Cole sua OpenAI API Key", type="password")
    else:
        st.success("Chave de API detectada! ✅")

# Inputs
c1, c2 = st.columns(2)
with c1:
    d1 = st.text_input("Medicamento 1", "Varfarina")
with c2:
    d2 = st.text_input("Medicamento 2", "Aspirina")

if st.button("Analisar Interação", type="primary"):
    if not api_key:
        st.warning("Por favor, insira a chave da API.")
        st.stop()
        
    with st.spinner(f"Consultando base de conhecimento farmacêutico sobre {d1} + {d2}..."):
        result = analyze_interaction_ai(d1, d2, api_key)
        
        if result:
            # Lógica de Exibição baseada na Gravidade
            if result['tem_interacao']:
                
                # Cores dinâmicas baseadas na gravidade
                if result['gravidade'] in ["Alta", "Grave"]:
                    st.error(f"🚨 INTERAÇÃO {result['gravidade'].upper()} DETECTADA")
                elif result['gravidade'] == "Moderada":
                    st.warning(f"⚠️ INTERAÇÃO {result['gravidade'].upper()} DETECTADA")
                else:
                    st.info(f"ℹ️ INTERAÇÃO {result['gravidade'].upper()}")
                
                # Detalhes
                st.subheader("🧬 O que acontece?")
                st.write(result['mecanismo'])
                
                st.subheader("💡 Recomendação ao Paciente")
                st.write(result['recomendacao'])
                
                # Alerta específico para Varfarina+Aspirina (Exemplo de validação extra)
                if "sangramento" in result['mecanismo'].lower():
                    st.toast("Atenção: Risco de hemorragia detectado!", icon="🩸")
                    
            else:
                st.success(f"✅ Nenhuma interação farmacológica clinicamente significativa encontrada entre {d1} e {d2}.")
                st.caption("Nota: Sempre consulte seu médico. A IA baseia-se em literatura médica até 2023.")