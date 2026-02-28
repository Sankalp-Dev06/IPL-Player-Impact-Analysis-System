import streamlit as st

st.set_page_config(
    page_title="Impact Intelligence Hub",
    layout="wide"
)

st.title("🏏 IPL Impact Intelligence Hub")

st.markdown("### Context-Aware Performance Intelligence Platform")

st.markdown(
"""
This system evaluates IPL player performance using contextual analytics 
derived from ball-by-ball data.

Rather than relying solely on traditional statistics (runs, wickets), 
the platform introduces structured performance modeling including:
"""
)

st.markdown(
"""
- **Custom Impact Score**
- **Consistency Index (Coefficient of Variation)**
- **Rolling 5-Match Form Analytics**
- **Venue Intelligence Modeling**
- **Team Defensive Strength Analysis**
- **Head-to-Head Player Comparison**
"""
)

st.markdown("---")

# Impact Score Explanation Section
st.markdown("## 📊 Impact Score Interpretation")

st.markdown(
"""
| Impact Score Range | Performance Meaning |
|--------------------|--------------------|
| < 0                | Poor Performance |
| 0 – 20             | Below Average |
| 20 – 40            | Moderate Contributor |
| 40 – 70            | Strong Performer |
| 70 – 120           | Match Influencer |
| 120+               | Dominant Performance |
"""
)

st.markdown(
"""
These ranges are derived from the observed distribution of match-level impact scores 
across recent IPL seasons.
"""
)

st.markdown("---")

st.info("Use the sidebar to explore individual player analytics, form tracking, venue intelligence, and team defensive insights.")

st.markdown("---")

st.caption("Built using Python, SQL Server, and Streamlit | Context-Aware Sports Analytics")