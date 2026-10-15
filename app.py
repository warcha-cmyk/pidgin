import os
import time
import streamlit as st
from google import genai

# Page configuration
st.set_page_config(page_title="Chazbot's Marvelous Pidgin Translator", page_icon="🇳🇬")

st.title("🇳🇬 Chazbot's Marvelous Patented English to Nigerian Pidgin Translator 🇳🇬")
st.write("Jan Pidgin App")

# Retrieve the API key from environment / platform secrets
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("Missing GEMINI_API_KEY. Please set your API key in Streamlit Secrets or your environment.")
    st.stop()

# Initialize Gemini Client
client = genai.Client(api_key=api_key)

# Web Interface UI
english_text = st.text_area("English Text:", placeholder="Type something here, e.g., 'Aren't my friends great for vibe coding me Nigerian Pidgin translating apps?'")

if st.button("Translate to Pidgin", type="primary"):
    if english_text.strip():
        with st.spinner("Translating... (this may take a moment if servers are busy)"):
            prompt = (
                "You are an expert in Nigerian Pidgin English. Translate the provided English text "
                "into natural, colloquial, and fluent Nigerian Pidgin. "
                "Provide ONLY the translation, without any preamble, explanations, or quotes.\n\n"
                f"English: {english_text}"
            )
            
            # Retry logic to handle temporary 503 high-demand spikes gracefully
            max_retries = 3
            success = False
            translation = ""
            
            for attempt in range(max_retries):
                try:
                    response = client.models.generate_content(
                        model='gemini-3.8-flash',
                        contents=prompt
                    )
                    translation = response.text.strip()
                    success = True
                    break
                except Exception as e:
                    if "503" in str(e) or "UNAVAILABLE" in str(e):
                        if attempt < max_retries - 1:
                            time.sleep(2 * (attempt + 1)) # Wait longer each try
                            continue
                    # If it's a different error or we ran out of retries, raise it
                    error_message = str(e)
                    break

            if success:
                st.subheader("Nigerian Pidgin:")
                st.success(translation)
            else:
                st.warning("Google's servers are experiencing high traffic right now (Error 503). Please wait a moment and try clicking translate again!")
    else:
        st.warning("Please enter some English text to translate.")
