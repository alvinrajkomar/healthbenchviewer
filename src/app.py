import streamlit as st

# Set the page configuration
st.set_page_config(
    page_title="HealthBench Analysis",
    page_icon="🏥",
    layout="wide"
)

# Main app title
st.title("HealthBench Analysis")

# Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Main Analysis", "Penalty Only Dataset", "Data Explorer"])

# Load the appropriate page based on user selection
if page == "Home":
    st.write("Welcome to the HealthBench Analysis app. Use the sidebar to navigate to different sections.")
elif page == "Main Analysis":
    import pages.main_analysis
elif page == "Penalty Only Dataset":
    import pages.penalty_only_dataset
elif page == "Data Explorer":
    import pages.data_explorer 