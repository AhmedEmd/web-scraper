import streamlit as st
from scrape import (
    scrape_website,
    extract_body_content,
    clean_body_content,
    split_dom_content,
    process_content_with_ollama,
    generate_text_with_ollama
)
import ollama

def process_website(url, model, custom_prompt=None):
    with st.spinner("Scraping website..."):
        html_content = scrape_website(url)
    
    if html_content:
        body_content = extract_body_content(html_content)
        cleaned_content = clean_body_content(body_content)
        content_chunks = split_dom_content(cleaned_content)
        
        st.success("Website scraped successfully!")
        
        if model not in available_models:
            st.warning(f"Model '{model}' is not available. Please pull it first using 'ollama pull {model}'")
            st.stop()
        
        if custom_prompt:
            # Process the custom prompt
            full_prompt = f"Based on the following content:\n\n{cleaned_content}\n\nAnswer the following question: {custom_prompt}"
            with st.spinner("Processing your prompt..."):
                response = generate_text_with_ollama(full_prompt, model)
                if response:
                    st.subheader("Response to your prompt:")
                    st.write(response)
                else:
                    st.error("Failed to process your prompt")
        else:
            # Summarize each chunk
            for i, chunk in enumerate(content_chunks):
                with st.spinner(f"Processing chunk {i+1}..."):
                    summary = process_content_with_ollama(chunk, model)
                    if summary:
                        st.subheader(f"Summary of chunk {i+1}:")
                        st.write(summary)
                    else:
                        st.error(f"Failed to process chunk {i+1}")
    else:
        st.error("Failed to scrape the website.")

st.title("Web Scraper and Summarizer")

# Initialize session state
if 'show_prompt_input' not in st.session_state:
    st.session_state.show_prompt_input = False

url = st.text_input("Enter the website URL to scrape:")

# Add model selection
available_models = []
try:
    model_list = ollama.list()
    available_models = [m['name'] for m in model_list['models']]
except Exception as e:
    st.error(f"Failed to connect to Ollama: {e}")
    st.stop()

# Add a default option and combine with available models
model_options = ["Select a model"] + available_models

# Use selectbox for model selection
selected_model = st.selectbox("Select Ollama model", model_options)

# Create two columns for buttons
col1, col2 = st.columns(2)

# Button for Scrape and Summarize
if col1.button("Scrape and Summarize"):
    if not url:
        st.warning("Please enter a URL.")
    elif selected_model == "Select a model":
        st.warning("Please select a model.")
    else:
        st.session_state.show_prompt_input = False
        process_website(url, selected_model)

# Button for Scrape and Add Prompt
if col2.button("Scrape and Add Prompt"):
    if not url:
        st.warning("Please enter a URL.")
    elif selected_model == "Select a model":
        st.warning("Please select a model.")
    else:
        st.session_state.show_prompt_input = True
        html_content = scrape_website(url)
        if html_content:
            st.success("Website scraped successfully!")
        else:
            st.error("Failed to scrape the website.")

# Show prompt input if the state is True
if st.session_state.show_prompt_input:
    user_prompt = st.text_area("Enter your prompt or question about the scraped content:")
    if st.button("Process Prompt"):
        if user_prompt:
            process_website(url, selected_model, user_prompt)
        else:
            st.warning("Please enter a prompt before processing.")

# Update instructions for running Ollama
st.sidebar.title("Instructions")
st.sidebar.info(
    "1. Make sure Ollama is running locally on port 11434 before using this app. "
    "You can start Ollama by running the 'ollama serve' command in your terminal.\n\n"
    "2. If the model you want to use is not available in the dropdown, "
    "pull it using the command: 'ollama pull <model_name>' (e.g., 'ollama pull llama2') "
    "in your terminal, then restart this Streamlit app.\n\n"
    "3. If you encounter any issues, please check the Ollama documentation or restart the Ollama service."
)
