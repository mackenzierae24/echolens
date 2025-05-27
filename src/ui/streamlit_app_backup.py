"""
Main Streamlit Application for EchoLens
"""
import streamlit as st

def run_app():
    st.set_page_config(
        page_title="EchoLens",
        page_icon="🔍",
        layout="wide"
    )
    
    st.title("🔍 EchoLens")
    st.subheader("See what echoes through your words")
    
    st.info("🚧 EchoLens is under construction! Come back soon for linguistic analysis.")
    
    # Placeholder for main app functionality
    with st.container():
        st.write("### Coming Soon:")
        st.write("- Text analysis for ideological patterns")
        st.write("- Audio transcription support") 
        st.write("- Visual similarity reports")
        st.write("- Extensible dialect database")

if __name__ == "__main__":
    run_app()
