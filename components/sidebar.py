import streamlit as st
import time
def sidebar_ui():
    """Sidebar with mode and Quizzer sub-mode selectors, and core controls."""

    st.sidebar.image("assets/sgpa_logo.png", width=50)

    # API/info
    #st.sidebar.markdown("### API Model")

    # Mode selection
    st.sidebar.markdown("### 🧩 Choose Mode")
    mode = st.sidebar.selectbox(
        "Select a core function:",
        ["💡 Explainer", "📰 Summarizer", "🧩 Quizzer"],
        index=0
    )

    # Nested radio for Quizzer
    sub_mode = None
    if mode == "🧩 Quizzer":
        st.sidebar.markdown("### ✨ Quizzer Action")
        sub_mode = st.sidebar.selectbox(
            "Choose Quizzer action:",
            [
                "📝 Generate Questions",
                "📖 Solve Questions",
                "✅ Evaluate Answers"
            ],
            index=0
        )
    
    # Visuals toggle
    st.sidebar.markdown("### 📊 Visuals")
    if "include_visuals" not in st.session_state:
        st.session_state.include_visuals = False
    st.session_state.include_visuals = st.sidebar.checkbox(
        "Include visuals when helpful",
        value=st.session_state.include_visuals
    )

    # New chat button
    if st.sidebar.button("🆕 New Chat"):
        st.session_state.messages = []
        # Success message that auto-disappears after 2 seconds
        success_placeholder = st.sidebar.empty()
        with success_placeholder.container():
            st.success("Started a new chat!")
        time.sleep(2)
        success_placeholder.empty()

    st.sidebar.caption("✨ Adaptive Learning Tutor")

    return mode, sub_mode
