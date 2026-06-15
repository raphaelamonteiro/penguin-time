from datetime import datetime
import streamlit as st

st.set_page_config(
    page_title="PenguinTime",
    page_icon="assets/favicon.ico",
    layout="centered"
)

def load_css():
    with open("src/styles/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()


if "running" not in st.session_state:
    st.session_state["running"] = False

if "duration" not in st.session_state:
    st.session_state["duration"] = None


st.title("PenguinTime")

col1, col2 = st.columns(2)

with col1:
    if st.button("▶️ Iniciar"):
        st.session_state["start_time"] = datetime.now()
        st.session_state["running"] = True
        st.success("Sessão iniciada!")

with col2:
    if st.button("⏹️ Parar"):
        if "start_time" in st.session_state:
            end_time = datetime.now()
            start_time = st.session_state["start_time"]

            st.session_state["duration"] = end_time - start_time
            st.session_state["running"] = False
            st.success("Sessão finalizada!")


st.divider()

if st.session_state["duration"]:
    st.write(f"⏱️ Tempo: {st.session_state['duration']}")

if st.session_state["running"]:
    st.write("🐧 Raul: você está focado agora!")
else:
    st.write("🐧 Raul: pronto quando você estiver.")