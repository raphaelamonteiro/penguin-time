from datetime import datetime
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Penguin Time",
    page_icon="assets/favicon.ico",
    layout="wide"
)

def load_css():
    with open("src/styles/style.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Initialize session state
if "sessions" not in st.session_state:
    st.session_state.sessions = []

if "is_running" not in st.session_state:
    st.session_state.is_running = False

st.title("Penguin Time")

# Control section
col1, col2 = st.columns([2, 2])

with col1:
    task_name = st.text_input(
        "Task",
        placeholder="Example: Study Python"
    )

with col2:
    category = st.selectbox(
        "Category",
        ["Work", "Study", "Project", "Other"]
    )

# Main buttons
start_col, stop_col = st.columns(2)

with start_col:
    if st.button("Start", disabled=st.session_state.is_running):
        if task_name:
            st.session_state.current_task = {
                "name": task_name,
                "category": category,
                "start_time": datetime.now(),
                "start_time_text": datetime.now().strftime("%H:%M:%S")
            }

            st.session_state.is_running = True
            st.success(f"🐧 Started: {task_name}")

        else:
            st.warning("Please enter a task!")

with stop_col:
    if st.button("Stop", disabled=not st.session_state.is_running):

        end_time = datetime.now()

        duration = (
            end_time -
            st.session_state.current_task["start_time"]
        )

        st.session_state.sessions.append({
            "task": st.session_state.current_task["name"],
            "category": st.session_state.current_task["category"],
            "start": st.session_state.current_task["start_time_text"],
            "end": end_time.strftime("%H:%M:%S"),
            "duration_minutes": round(
                duration.total_seconds() / 60,
                1
            ),
            "timestamp": st.session_state.current_task["start_time"]
        })

        st.session_state.is_running = False

        st.success(
            f"Finished! Duration: "
            f"{duration.total_seconds()/60:.1f} minutes"
        )

# Penguin status
st.divider()

if st.session_state.is_running:
    current_task = st.session_state.current_task["name"]

    st.info(
        f"🐧 **Raul:** "
        f"Focused on '{current_task}'! 🚀"
    )
else:
    st.info(
        "🐧 **Raul:** "
        "Hello Raphs! Ready to start? Choose a task! 📚"
    )

# Today's sessions
st.divider()
st.subheader("📊 Today's Sessions")

if st.session_state.sessions:

    df = pd.DataFrame(st.session_state.sessions)
    df = df.sort_values("timestamp", ascending=False)

    display_df = df[
        ["task", "category", "start", "end", "duration_minutes"]
    ]

    display_df.columns = [
        "Task",
        "Category",
        "Start",
        "End",
        "Minutes"
    ]

    st.dataframe(display_df, use_container_width=True)

    total_minutes = df["duration_minutes"].sum()

    st.metric(
        "⏱️ Total Today",
        f"{total_minutes:.1f} minutes",
        f"{total_minutes/60:.1f} hours"
    )

else:
    st.caption("No sessions recorded today")