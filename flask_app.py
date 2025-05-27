# finance_chatbot/flask_app.py

from flask import Flask, render_template
import subprocess
import atexit
import os
import signal

app = Flask(__name__)

streamlit_process = None

def start_streamlit():
    global streamlit_process
    # Command to run Streamlit.
    # Using "server.headless=true" is good practice when running it as a background process.
    # "server.enableCORS=false" might be needed depending on your exact setup,
    # but often not necessary when just iframing from the same domain or localhost.
    # "server.port" ensures Streamlit uses a specific port.
    cmd = [
        "streamlit", "run", "app.py",
        "--server.port", "8501",
        "--server.headless", "true"
    ]
    # Start the Streamlit process
    # Use Popen for non-blocking execution.
    # Store the process object to be able to terminate it later.
    # On Windows, you might need creationflags=subprocess.CREATE_NEW_PROCESS_GROUP for proper termination.
    if os.name == 'nt': # Windows
        streamlit_process = subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
    else: # POSIX (Linux, macOS)
        streamlit_process = subprocess.Popen(cmd, preexec_fn=os.setsid) # Start in a new session
    print(f"Streamlit process started with PID: {streamlit_process.pid} on port 8501")

def stop_streamlit():
    global streamlit_process
    if streamlit_process:
        print(f"Stopping Streamlit process with PID: {streamlit_process.pid}...")
        try:
            if os.name == 'nt': # Windows
                subprocess.call(['taskkill', '/F', '/T', '/PID', str(streamlit_process.pid)])
            else: # POSIX
                os.killpg(os.getpgid(streamlit_process.pid), signal.SIGTERM) # Send SIGTERM to the process group
            streamlit_process.wait(timeout=5) # Wait for the process to terminate
            print("Streamlit process terminated.")
        except subprocess.TimeoutExpired:
            print("Streamlit process did not terminate in time, attempting to kill.")
            if os.name == 'nt':
                 subprocess.call(['taskkill', '/F', '/T', '/PID', str(streamlit_process.pid)]) # Force kill
            else:
                os.killpg(os.getpgid(streamlit_process.pid), signal.SIGKILL) # Send SIGKILL
            print("Streamlit process force killed.")
        except Exception as e:
            print(f"Error stopping Streamlit process: {e}")
        streamlit_process = None

@app.route('/')
def index():
    # Renders the index.html template which contains the iframe.
    # The iframe will point to where the Streamlit app is running.
    return render_template('index.html', streamlit_url="http://localhost:8501")

if __name__ == '__main__':
    # Start Streamlit when Flask starts
    start_streamlit()
    # Register stop_streamlit to be called when Flask exits
    atexit.register(stop_streamlit)
    # Run the Flask app. Use a different port than Streamlit.
    app.run(debug=True, port=5000, host="0.0.0.0")