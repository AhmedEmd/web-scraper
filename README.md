# Web Scraper and Summarizer

This application is a web scraper and summarizer that uses Streamlit for the interface and Ollama for text processing.

## Setup and Installation

1. Open your terminal and navigate to the directory where you want to clone the project.

2. Clone this repository to your local machine:
   ```
   git clone https://github.com/AhmedEmd/web-scraper.git
   cd web-scraper
   ```

3. Create a virtual environment:
   ```
   python -m venv venv
   ```

4. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```

5. Create a `requirements.txt` file in the project root directory with the following content:
   ```
   streamlit
   selenium
   webdriver_manager
   beautifulsoup4
   ollama
   ```

6. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```

7. Install Ollama by following the instructions at [Ollama's official website](https://ollama.ai/).

8. After installing Ollama, pull an LLM model. For example, to pull the llama2 model:
   ```
   ollama pull llama2
   ```

## Running the Application

1. Make sure Ollama is running locally on port 11434 before using this app. Start Ollama by running:
   ```
   ollama serve
   ```

2. If the model you want to use is not available in the dropdown when you run the app, pull it using the command:
   ```
   ollama pull <model_name>
   ```
   For example: `ollama pull llama2`
   Then restart the Streamlit app.

3. If you encounter any issues, please check the Ollama documentation or restart the Ollama service.

## Directory Structure

Your project directory should look like this:

```
web-scraper-summarizer/
│
├── main.py
├── scrape.py
├── requirements.txt
└── README.md
```

## Running the Project

After completing all the setup steps, you can run the project using:

```
streamlit run main.py
```

This will start the Streamlit app, and you should be able to access it through your web browser.

## Deactivating the Virtual Environment

When you're done working on the project, you can deactivate the virtual environment by running:

```
deactivate
```

This will return you to your global Python environment.