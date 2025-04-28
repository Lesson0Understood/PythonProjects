# transcript_utils.py
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
import config # Import config to get language preferences

def get_transcript(video_id):
    """
    Fetches and returns the transcript text for a single video ID.
    Prioritizes languages specified in config.TRANSCRIPT_LANGUAGES.
    Returns None if no suitable transcript is found or an error occurs.
    """
    transcript_obj = None
    languages = config.TRANSCRIPT_LANGUAGES # Get preferred languages

    try:
        # List available transcripts
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        # Try finding a manually created transcript in preferred languages
        try:
            # print(f"    - Attempting manual transcript ({', '.join(languages)}) for {video_id}...")
            transcript_obj = transcript_list.find_manually_created_transcript(languages)
            # print(f"    - Found manual transcript for {video_id}")
        except NoTranscriptFound:
            # print(f"    - No manual transcript found in {', '.join(languages)}. Trying generated...")
            # Try finding a generated transcript in preferred languages
            try:
                transcript_obj = transcript_list.find_generated_transcript(languages)
                # print(f"    - Found generated transcript for {video_id}")
            except NoTranscriptFound:
                # print(f"    - WARNING: No transcript found in preferred languages ({', '.join(languages)}) for {video_id}.")
                return None # No suitable transcript found
            except Exception as e_gen:
                 print(f"    - WARNING: Error finding generated transcript for {video_id}: {e_gen}")
                 return None

    except TranscriptsDisabled:
        print(f"    - WARNING: Transcripts disabled for video {video_id}.")
        return None
    except Exception as e_list:
        # Covers errors during list_transcripts itself
        print(f"    - WARNING: Error listing transcripts for {video_id}: {e_list}")
        return None

    # --- Fetch and process the transcript data ---
    if transcript_obj:
        try:
            # print(f"    - Fetching transcript data for {video_id}...")
            transcript_data = transcript_obj.fetch()
            # print(f"    - Formatting transcript text for {video_id}...")

            text_segments = []
            for entry in transcript_data:
                 # Primarily expect objects with .text attribute now
                 if hasattr(entry, 'text'):
                     text_segments.append(entry.text)
                 elif isinstance(entry, dict) and 'text' in entry:
                     # Fallback for safety if format varies
                     text_segments.append(entry['text'])
                 # else: Optional: log entries without text

            full_text = " ".join(text_segments)
            # print(f"    - Successfully processed transcript for {video_id}")
            return full_text

        except AttributeError as e_attr:
             print(f"    - WARNING: Attribute error processing fetched transcript for {video_id}. Format issue? Error: {e_attr}")
             return None
        except Exception as e_fetch:
            print(f"    - WARNING: Error fetching/processing transcript content for {video_id}: {e_fetch}")
            return None

    # Should have returned None earlier if no transcript_obj was found
    return None

def format_combined_transcripts(channel_name, channel_id, video_texts):
    """Formats the collected video transcripts into a single string."""
    if not video_texts:
        return ""

    formatted_texts = [
        f"--- Video {index+1} ---\nVideo ID: {vid_id}\nVideo Title: {vid_title}\n\nTranscript:\n{text}\n\n"
        for index, (vid_id, vid_title, text) in enumerate(video_texts)
    ]
    header = f"Channel Name: {channel_name}\nChannel ID: {channel_id}\n\n--- Combined Transcripts ---\n\n"
    return header + "===\n".join(formatted_texts)