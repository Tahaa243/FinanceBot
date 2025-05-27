# finance_chatbot/app.py

import streamlit as st
import google.generativeai as genai
import os # For environment variables if not using Streamlit secrets directly for some reason

# --- Gemini API Configuration ---
# Attempt to get API key from Streamlit secrets first
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GEMINI_API_KEY)
except (KeyError, FileNotFoundError): # FileNotFoundError for local secrets.toml, KeyError for deployed without secrets set
    # Fallback to environment variable if secrets are not found (useful for some local setups)
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
    else:
        st.error("🔴 Gemini API Key not found. Please set it in Streamlit secrets or as an environment variable (GEMINI_API_KEY).")
        st.caption("To run locally, create a `.streamlit/secrets.toml` file with `GEMINI_API_KEY = 'YOUR_KEY_HERE'`.")
        st.stop()


# Model Configuration
generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

system_instruction = """You are an AI Finance Assistant. Your *only* function is to provide information and answer questions *strictly* related to the financial domain.
This includes, but is not limited to:
- Personal finance (e.g., budgeting, saving, debt management, credit scores, insurance)
- Investments (e.g., stocks, bonds, mutual funds, ETFs, real estate, cryptocurrency, NFTs, derivatives, venture capital, commodities) - you should discuss these topics factually, including their mechanisms, historical performance patterns, risks, and potential rewards, without giving specific financial advice to buy or sell.
- Cryptocurrency (e.g., Bitcoin, Ethereum, altcoins, blockchain technology, DeFi, CeFi, crypto wallets, crypto security, crypto exchanges, crypto scams, ICOs, IDOs, STOs)
- Money Management (e.g., banking products and services, loans, mortgages, interest rates, inflation)
- Businesses (e.g., entrepreneurship, business finance, financial statements, economics, market analysis, company valuations, startups, mergers and acquisitions)
- Financial Markets (e.g., stock exchanges, forex, derivatives markets, market trends, economic indicators, monetary policy, fiscal policy)
- Financial Scams (e.g., identification of various scam types like phishing, Ponzi schemes, pump and dump; prevention strategies; reporting mechanisms)
- Budgeting and Financial Planning (e.g., creating budgets, financial goals, retirement planning concepts, tax basics)
- General economic theories and principles.

You *must not* answer any questions or engage in any conversation outside of these financial topics. If a user asks a non-finance question, politely and firmly state that you can only discuss finance-related matters. Do not be drawn into off-topic conversation.
Do not provide specific financial, investment, or legal advice (e.g., "should I buy this stock?", "is this a good time to invest in crypto?", "tell me what to invest in for high returns"). Instead, provide general information, explain concepts, discuss different perspectives, and describe potential risks and benefits associated with financial products or strategies.
You are expected to discuss all aspects of these financial topics, including those that may be considered high-risk (such as speculative investments or volatile cryptocurrencies), from an informational and educational perspective. Your role is to inform, not to recommend or dissuade based on risk level without context.
Be concise, factual, and helpful within your designated financial domain.
If asked for real-time or live market prices, state that you do not have access to live data feeds but can provide general information about where such data might be found or discuss historical price movements if the information is part of your general knowledge.
"""

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}, # This should be set to not block discussions about financial risk if the discussion itself is not promoting illegal/harmful acts. The prompt will guide this.
]

try:
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash-latest", # Or your preferred Gemini model
        generation_config=generation_config,
        system_instruction=system_instruction,
        safety_settings=safety_settings
    )
except Exception as e:
    st.error(f"🔴 Error initializing Gemini Model: {e}")
    st.stop()

def get_finance_response(user_prompt, chat_history_internal):
    try:
        # Start a new chat session with the existing history for context
        convo = model.start_chat(history=chat_history_internal)
        convo.send_message(user_prompt)
        # The API automatically updates convo.history
        return convo.last.text, convo.history
    except Exception as e:
        st.error(f"🔴 Error getting response from Gemini: {e}")
        # Return the error message and the unchanged history
        return "Sorry, I encountered an error trying to respond. Please check the server logs or API key.", chat_history_internal

# --- Streamlit UI Configuration ---
st.set_page_config(
    layout="wide",
    page_title="AI Finance Assistant",
    page_icon="💰" # Favicon
)

# --- Theming and Styling (config.toml is primary, CSS for specifics) ---
# Custom CSS for prompt bar positioning, spacing, and chat message styling
st.markdown("""
<style>
    /* Main container adjustments for fixed input */
    .main .block-container {
        padding-bottom: 6rem; /* Ensure enough space for the fixed input bar */
    }

    /* Chat input container */
    .stChatInputContainer {
        position: fixed;
        bottom: 0px; /* Position at the very bottom */
        width: 100%; /* Occupy full width */
        padding: 10px 1rem 20px 1rem; /* Top, LR, Bottom padding; 1rem for side match */
        background-color: #FFFFFF; /* White background to match theme */
        border-top: 1px solid #EEEEEE; /* Subtle top border */
        box-shadow: 0 -2px 5px rgba(0,0,0,0.05); /* Slight shadow for depth */
        z-index: 999;
        left: 0; /* Ensure it aligns to the left correctly */
        right: 0; /* Ensure it aligns to the right correctly */
    }

    /* Make input field itself have a light touch */
    div[data-testid="stChatInput"] div[data-baseweb="input"] > div {
        background-color: #F0F2F6; /* Light grey for input field */
        border-radius: 8px;
    }

    /* Chat message styling */
    .stChatMessage {
        border-radius: 10px;
        padding: 0.75rem;
        margin-bottom: 0.5rem;
    }

    [data-testid="chatAvatarIcon-user"] {
        background-color: #90EE90; /* Light Green for user avatar */
        color: black;
    }
    div[data-testid="stChatMessageContent-user"] {
        background-color: #F0FFF0; /* Honeydew (very light green) for user message bubble */
        border-radius: 10px;
        padding: 0.75rem;
    }

    [data-testid="chatAvatarIcon-assistant"] {
        background-color: #FFFFE0; /* Light Yellow for assistant avatar */
        color: black;
    }
    div[data-testid="stChatMessageContent-assistant"] {
        background-color: #FFFACD; /* LemonChiffon (light yellow) for assistant message bubble */
        border-radius: 10px;
        padding: 0.75rem;
    }

    /* Ensure responsiveness: Adjust padding for smaller screens */
    @media (max-width: 640px) {
        .stChatInputContainer {
            padding: 10px 0.5rem 15px 0.5rem;
        }
        .main .block-container {
            padding-left: 0.5rem;
            padding-right: 0.5rem;
            padding-bottom: 5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

st.title("Finance Bot")
st.caption("Your friendly AI guide for finance")

# Initialize chat history in session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = [] # For displaying in Streamlit UI
if "gemini_history" not in st.session_state:
    # For maintaining history in the format Gemini API expects (parts with role and content)
    # Example: [{"role": "user", "parts": ["Hello"]}, {"role": "model", "parts": ["Hi there!"]}]
    st.session_state.gemini_history = []

# Display prior chat messages from Streamlit's perspective
for message in st.session_state.messages:
    with st.chat_message(message["role"]): # Use role for avatar
        st.markdown(message["content"])

# Chat input - st.chat_input handles Enter key submission automatically
if prompt := st.chat_input("Ask about finance...", key="finance_chat_input"):
    # Add user message to Streamlit display chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): # "user" for user avatar
        st.markdown(prompt)

    # Get response from Gemini, passing the current Gemini-formatted history
    with st.spinner("🤖 Thinking..."):
        response_text, updated_gemini_history = get_finance_response(prompt, st.session_state.gemini_history)
        st.session_state.gemini_history = updated_gemini_history # Update the history for next turn

    # Add assistant response to Streamlit display chat history
    st.session_state.messages.append({"role": "assistant", "content": response_text})
    with st.chat_message("assistant"): # "assistant" for bot avatar
        st.markdown(response_text)

    # Rerun to display the latest messages if needed, though st.chat_message should update automatically
    # st.rerun()