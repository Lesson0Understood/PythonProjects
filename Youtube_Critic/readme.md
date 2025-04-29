# YouTube Transcript Critic

This Python script searches YouTube for videos based on user-defined queries and genres, fetches their transcripts, and uses the Google Gemini AI model to analyze and critique the textual content of the transcripts for each channel found.

## What it Does

1.  **Searches YouTube:** Finds videos based on search terms and genres you provide.
2.  **Fetches Transcripts:** Downloads available English transcripts for the found videos.
3.  **Groups by Channel:** Organizes videos and their transcripts by the YouTube channel they belong to.
4.  **Combines Transcripts:** Creates a single text file containing all fetched transcripts for a specific channel.
5.  **AI Analysis:** Sends the combined transcript text to Google Gemini for analysis based on criteria like clarity, engagement, authenticity, and structure.
6.  **Saves Results:** Stores the combined transcripts (`.txt`) and the AI's critique (`.json`) in separate directories.

## Features

*   Interactive input for search queries and genres.
*   Uses YouTube Data API v3 for searching.
*   Leverages `youtube-transcript-api` for efficient transcript fetching.
*   Integrates with Google Gemini for content analysis (configurable model).
*   Outputs structured JSON critiques from the AI.
*   Handles potential errors during API calls and transcript fetching gracefully.
*   Organizes output files neatly by channel name.

## Requirements

*   Python 3.x
*   Google Account with:
    *   YouTube Data API v3 Key
    *   Google Generative AI (Gemini) API Key
*   Required Python libraries (install via `requirements.txt`)

## Setup

1.  **Clone the Repository:**
    ```bash
    git clone <your-repository-url>
    cd <repository-directory>
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set API Keys:**
    *   **Crucial:** You MUST set your API keys as environment variables *before* running the script.
    *   **Linux/macOS:**
        ```bash
        export YOUTUBE_API_KEY="YOUR_YOUTUBE_API_KEY"
        export GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
        ```
    *   **Windows (Command Prompt):**
        ```bash
        set YOUTUBE_API_KEY=YOUR_YOUTUBE_API_KEY
        set GEMINI_API_KEY=YOUR_GEMINI_API_KEY
        ```
    *   **Windows (PowerShell):**
        ```powershell
        $env:YOUTUBE_API_KEY="YOUR_YOUTUBE_API_KEY"
        $env:GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
        ```
    *   Alternatively, consider using a `.env` file and a library like `python-dotenv` if you prefer (requires modifying `config.py`).

## Configuration (Optional)

You can adjust settings in `config.py`:

*   `MAX_RESULTS_PER_QUERY`: How many videos to fetch per search query/genre pair.
*   `TRANSCRIPT_DIR`, `CRITIQUE_DIR`: Names for the output directories.
*   `GENERATION_CONFIG`: Parameters for the Gemini AI (temperature, max tokens, etc.).
*   `AI_MODEL_NAME`: Which Gemini model to use (e.g., `gemini-1.5-flash`, `gemini-pro`).
*   `TRANSCRIPT_LANGUAGES`: Preferred language codes for transcripts.

## How to Run

1.  Make sure your API keys are set as environment variables.
2.  Navigate to the project directory in your terminal.
3.  Run the main script:
    ```bash
    python main.py
    ```
4.  The script will prompt you to enter search queries one by one. Type `exit` when done.
5.  It will then prompt you for video genres. Type `exit` when done.
6.  The script will then search YouTube, process channels, fetch transcripts, perform AI analysis, and save the results. Watch the console for progress and any warnings/errors.

## Output

*   **Transcripts:** Combined transcripts for each channel are saved as `.txt` files in the `Transcripts/` directory (or as specified in `config.py`).
*   **Critiques:** AI analysis results are saved as `.json` files in the `Critiques/` directory (or as specified in `config.py`). If the AI fails to return valid JSON, an error file (`_critique_ERROR.txt`) might be generated instead.

File names are based on the sanitized channel names.
