from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import streamlit as st
import ollama

def scrape_website(website):
    print("Connecting to Scraping Browser...")
    
    # Setup ChromeDriver service and options
    service = Service(ChromeDriverManager().install())
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    try:
        # Initialize WebDriver
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(website)
        
        # Wait for the body to be present
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
        except TimeoutException:
            print("Timed out waiting for page to load")
            return None

        print("Navigated! Scraping page content...")
        html = driver.page_source
        return html
    except Exception as e:
        print(f"Error during scraping: {e}")
        return None
    finally:
        if 'driver' in locals():
            driver.quit()

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )
    return cleaned_content

def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]

# Add this new function at the end of the file
def generate_text_with_ollama(prompt, model="llama2"):
    try:
        response = ollama.generate(model=model, prompt=prompt)
        return response['response']
    except Exception as e:
        if "model not found" in str(e).lower():
            st.error(f"Model '{model}' not found. Please pull the model first using 'ollama pull {model}'")
        else:
            st.error(f"Error generating text with Ollama: {e}")
        return None

def process_content_with_ollama(content, model):
    prompt = f"Summarize the following content:\n\n{content}\n\nSummary:"
    summary = generate_text_with_ollama(prompt, model)
    return summary

# Remove the main function and __main__ block from scrape.py
