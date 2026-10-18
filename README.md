# Groq RAG Knowledge Assistant

A web-based Retrieval-Augmented Generation (RAG) chatbot built with
Flask, Python, scikit-learn, and the Groq API. It searches a local
knowledge database and uses an LLM to generate answers grounded in the
retrieved content.

## Features

-   Chat-style web interface
-   Retrieves relevant information from `database.json`
-   Uses TF-IDF and cosine similarity for document retrieval
-   Streams responses from the Groq API
-   Flask backend with HTML, CSS, and JavaScript frontend

## Project Structure

``` text
NLP_Lab/
├── app.py
├── llm.py
├── retrivel.py
├── main.py
├── database.json
├── requirements.txt
├── .env                 # Keep private; do not commit
├── .gitignore
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── script.js
```

## Requirements

-   Python 3.10 or a compatible supported Python version
-   A Groq API key
-   Git (optional, for version control)

## Run Locally

### 1. Open the project folder

``` bash
cd ~/NLP_Lab
```

### 2. Create and activate a virtual environment

If you already have `.venv`, activate it:

``` bash
source .venv/bin/activate
```

Otherwise, create one first:

``` bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

``` bash
python -m pip install -r requirements.txt
```

The `requirements.txt` file should include:

``` text
flask
groq
python-dotenv
scikit-learn
gunicorn
```

### 4. Configure the API key

Create a file named `.env` in the project root:

``` text
GROQ_API_KEY=your_actual_groq_api_key
```

Get an API key from [Groq Console](https://console.groq.com/keys).

**Security:** Never commit `.env` or publish your API key. If a key is
accidentally exposed, revoke it and create a replacement.

### 5. Start the app

``` bash
python app.py
```

Open <http://127.0.0.1:5000> in your browser.

Stop the development server with `Ctrl+C`.

## How It Works

1.  The user enters a question in the web interface.
2.  `app.py` receives the question and streams the response to the
    browser.
3.  `retrivel.py` searches `database.json` for relevant content using
    TF-IDF and cosine similarity.
4.  `llm.py` sends the question and retrieved context to the Groq
    chat-completions API.
5.  The generated response is streamed back to the web interface.

## Knowledge Database

The chatbot uses `database.json` as its knowledge source. Keep the file
in the project root and make sure its structure matches what
`retrivel.py` expects. After changing the database, restart the app if
needed.

## GitHub

Make sure `.gitignore` contains at least:

``` text
.env
.venv/
venv/
__pycache__/
*.py[cod]
```

Then initialize and push the project:

``` bash
git init
git add .
git status
git commit -m "Initial commit - Groq RAG chatbot"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

Before committing, check that `.env` is not staged. If Git reports that
`origin` already exists, update it instead:

``` bash
git remote set-url origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
```

If Git asks for an identity, configure it once:

``` bash
git config --global user.name "Your Name"
git config --global user.email "YOUR_GITHUB_EMAIL"
```

## Deploy on Render

1.  Push the project to GitHub.

2.  Sign in at [Render](https://render.com/).

3.  Create a **New Web Service** and connect the repository.

4.  Use these settings:

    -   **Build command:** `pip install -r requirements.txt`
    -   **Start command:** `gunicorn app:app`

5.  Add the environment variable in Render's service settings:

    -   **Key:** `GROQ_API_KEY`
    -   **Value:** your actual Groq API key

6.  Deploy and open the public URL Render provides.

Do not upload `.env` to GitHub. Configure secrets through the hosting
provider's environment-variable settings.

## Troubleshooting

-   **`ModuleNotFoundError`:** Activate `.venv`, then run
    `python -m pip install -r requirements.txt`.
-   **Missing API key:** Check that `.env` exists locally or
    `GROQ_API_KEY` is configured in Render.
-   **API/model error:** Check your Groq API key, account access, and
    the model name configured in `llm.py`.
-   **Deployment fails:** Read the service logs in Render and verify
    that `app.py` exposes a Flask variable named `app`.
-   **Empty or irrelevant answers:** Check that `database.json` contains
    useful content and matches the structure expected by `retrivel.py`.

## License

Add a license file if you intend to distribute or open-source this
project.
