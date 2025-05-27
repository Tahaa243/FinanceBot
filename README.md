# AI Finance Assistant Chatbot 💰

This is an AI-powered chatbot specializing in finance-related topics. It's built using Google's Gemini API for natural language understanding and generation, and Streamlit for the interactive user interface. The chatbot is designed to only answer questions related to finance, money management, crypto, investments, businesses, finance scams, and market prices/shares.

## ✨ Features

* **Finance Focused**: Strictly answers questions within the financial domain.
* **Gemini Powered**: Utilizes the Gemini API for intelligent responses.
* **Interactive UI**: Built with Streamlit for a user-friendly chat experience.
* **Light Themed**: Custom white, light green, and yellow color scheme.
* **Responsive Design**: Adapts to both PC and mobile screens.
* **Bottom Prompt Bar**: Chat input is conveniently located at the bottom.
* **Enter to Submit**: Prompts are sent by pressing Enter.
* **(Optional) Flask Deployment**: Can be embedded within a Flask application using an iframe.

## 🛠️ Setup and Installation

### Prerequisites

* Python 3.8 or higher
* `pip` (Python package installer)
* A Gemini API Key from Google AI Studio.

### Steps

1.  **Clone the repository (or download the files):**
    ```bash
    # If it's a git repository:
    # git clone <repository_url>
    # cd finance_chatbot
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On macOS/Linux:
    source venv/bin/activate
    # On Windows:
    # venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure your Gemini API Key:**
    * Create a directory named `.streamlit` inside the `finance_chatbot` directory if it doesn't exist.
    * Inside `.streamlit`, create a file named `secrets.toml`.
    * Add your Gemini API key to `secrets.toml` like this:
        ```toml
        GEMINI_API_KEY = "YOUR_ACTUAL_GEMINI_API_KEY_HERE"
        ```
    * **Important**: Replace `"YOUR_ACTUAL_GEMINI_API_KEY_HERE"` with your real key. Add `.streamlit/secrets.toml` to your `.gitignore` file to avoid committing your key.

## 🚀 Running the Application

You have two main ways to run the application:

### 1. Directly with Streamlit (Recommended for development & Streamlit Cloud)

Navigate to the `finance_chatbot` directory in your terminal and run:
```bash
streamlit run app.py