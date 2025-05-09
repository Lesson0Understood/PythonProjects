import os

# --- API Keys ---
# Set these as environment variables before running
YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

# --- YouTube Search Parameters ---
SEARCH_QUERIES = ["understanding neural network", "math intuition deep learning"]
VIDEO_GENRES = ["tutorial", "explanation"]
MAX_RESULTS_PER_QUERY = 5 # Adjust depending on the gemini model

# --- Output Directories ---
TRANSCRIPT_DIR = "Transcripts"
CRITIQUE_DIR = "Critiques"

# --- Gemini Model Configuration ---
GENERATION_CONFIG = {
  "temperature": 0.7, # Slightly lower temp for more deterministic JSON structure
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "application/json", # Request JSON output
}
AI_MODEL_NAME = "gemini-1.5-flash" # Change depending on accuracy needed

# --- Transcript Settings ---
TRANSCRIPT_LANGUAGES = ['en'] # Prioritize English transcripts