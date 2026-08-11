"""
MADS v4.2 — Streamlit Demo
"""

import streamlit as st
from mads import MADSSystem

# Инициализация
@st.cache_resource
def init_mads():
    mads = MADSSystem()
    mads.initialize()
    return mads

st.set_page_config(page_title="MADS v4.2", page_icon="🛡️", layout="wide")

st.title("🛡️ MADS v4.2 — Adaptive Multi-Agent Immune Architecture")
st.caption("23 агента | 3 Гравитационных Кластера | Институт Права")

# Запуск MADS
if "mads" not in st.session_state:
    with st.spinner("Запуск MADS..."):
        st.session_state.mads = init_mads()
        st.session_state.messages = []
    st.success("MADS готов к работе!")

mads = st.session_state.mads

# Боковая панель — статус
with st.sidebar:
    st.header("📊 Статус системы")
    status = mads.get_status()
    st.metric("Запросов", status["queries_processed"])
    st.metric("Кожух", "🔒 АКТИВЕН" if status["shield_mode"] else "🟢 штатный")
    st.metric("Spider-Sense", status["spider_sense"]["mode"])
    st.metric("Карантин", f"{status['quarantine']['total_blocks']} блок.")
    st.metric("Культура", status["cultural_profile"]["region"] or "холодный старт")

    st.divider()
    st.header("🏗️ Архитектура")
    st.markdown("""
    **Кластер 1 — Защита (7)**  
    Safety, Warden, Consequence, Quarantine, Spider-Sense, Shield, ZeroTrust
    
    **Кластер 2 — Истина (10)**  
    Accuracy, FirstAid, Dialogue, Conservative, Modifier, Navigator, Socrates, Ethics, English, Russian
    
    **Кластер 3 — Контекст (5)**  
    ContextAgent, CulturalProfile, Dispatcher, Family, Sleep
    
    **Институт Права (1)**  
    LegalAgent
    """)

# Чат
st.header("💬 Диалог")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Введите запрос..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Обработка..."):
            result = mads.process_query(prompt)

        if result["status"] == "blocked":
            response = f"🚫 **ЗАБЛОКИРОВАНО**\n\n{result['reason']}"
        else:
            parts = []
            if "first_aid" in result:
                fa = result["first_aid"]
                parts.append(f"🏥 **First Aid:** {fa.get('field', '')}\n{fa.get('verified', '')}")
            if "english_language" in result:
                eng = result["english_language"]
                parts.append(f"🇬🇧 **English:** {eng.get('category', '')}\n{eng.get('explanation', '')}")
            if "russian_language" in result:
                rus = result["russian_language"]
                parts.append(f"🇷🇺 **Русский:** {rus.get('field', '')}\n{rus.get('explanation', '')}")
            if "ethics" in result:
                parts.append(f"⚖️ **Этика:** {result['ethics']}")
            if "legal" in result:
                parts.append(f"⚖️ **Право:** {result['legal']}")
            if "navigator" in result:
                nav = result["navigator"]
                parts.append(f"🧭 **Navigator:** {nav.get('status', '')}")
            if "family" in result:
                parts.append(f"👨‍👩‍👧‍👦 **Family:** обнаружены семейные маркеры")

            response = "\n\n".join(parts) if parts else "✅ Запрос обработан."

            activation = result.get("activation", {})
            if activation:
                cats = activation.get("categories", ["general"])
                agent_count = activation.get("agents_count", 0)
                response += f"\n\n---\n📊 Категории: {', '.join(cats)} | Агентов: {agent_count}/23"

        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})