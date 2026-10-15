import os
import streamlit as st
from google import genai

# Page configuration
st.set_page_config(page_title="ChazBot's Patented English to Nigerian Pidgin Auto-Translate Madness", page_icon="🇳🇬")

st.title("ChazBot's Patented English to Nigerian Pidgin Auto-Translate Madness")
st.write("Go nuts, it's authentic Nigerian Pidgin!")

# Retrieve the API key from environment / platform secrets
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("Missing GEMINI_API_KEY. Please set your API key in Streamlit Secrets.")
    st.stop()

# Initialize Gemini Client
client = genai.Client(api_key=api_key)

# Web Interface UI
english_text = st.text_area("English Text:", placeholder="Type something here, e.g., 'How are you doing today my friend?'")

if st.button("Translate to Pidgin", type="primary"):
    if english_text.strip():
        with st.spinner("Translating..."):
            try:
                # System instructions ensure authentic context-aware translation
                prompt = (
                    "You are an expert in Nigerian Pidgin English. Translate the provided English text "
                    "into natural, colloquial, and fluent Nigerian Pidgin. "
                    "Provide ONLY the translation, without any preamble, explanations, or quotes.\n\n"
                    f"English: {english_text}"
                )

                response = client.models.generate_content(
                    model='gemini-3.8-flash',
                    contents=prompt
                )

                st.subheader("Nigerian Pidgin:")
                st.success(response.text.strip())

            except Exception as e:
                st.error(f"Error during translation: {e}")
    else:
        st.warning("Please enter some English text to translate.")
