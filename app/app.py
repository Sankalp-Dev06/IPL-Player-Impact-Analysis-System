import streamlit as st

st.markdown("""
<style>
section[data-testid="stSidebar"] {
    background-color: #111827;
}
section[data-testid="stSidebar"] h2 {
    color: white;
}
section[data-testid="stSidebar"] .stMarkdown {
    color: #9CA3AF;
}
</style>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="IPL Impact Analytics",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---- Sidebar Branding ----
st.sidebar.markdown(
    """
    <div style='text-align: center; padding: 10px 0;'>
        <h2 style='margin-bottom:0;'>🏏 IPL Impact</h2>
        <p style='color: gray; font-size: 14px;'>Analytics System</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("---")

st.sidebar.caption("Navigate through analytics modules")

st.title("🏏 IPL Player Impact Analytics System")

st.markdown("""
### Context-Aware Performance Intelligence

This system evaluates IPL players using:

- Custom Impact Score  
- Consistency Index  
- Venue Intelligence  
- Team Defensive Strength  
- Rolling Form Analytics  
""")

st.markdown("---")
st.info("Use the sidebar to explore different analytics modules.")