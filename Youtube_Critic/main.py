import os
import config              # Import all settings
import utils               # Import utility functions
import youtube_api         # Import YouTube functions
import transcript_utils    # Import Transcript functions
import ai_analyzer         # Import AI functions
import json                # Import json for potential loading/checking

def main():
    print("--- YouTube Transcript Critic ---")

    # --- Initial Checks and Setup ---
    if not config.YOUTUBE_API_KEY:
        raise ValueError("FATAL: YOUTUBE_API_KEY environment variable not set.")
    if not config.GEMINI_API_KEY:
        raise ValueError("FATAL: GEMINI_API_KEY environment variable not set.")

    utils.ensure_dir_exists(config.TRANSCRIPT_DIR)
    utils.ensure_dir_exists(config.CRITIQUE_DIR)

    # --- Initialize Services ---
    youtube = youtube_api.build_youtube_client(config.YOUTUBE_API_KEY)
    ai_analyzer.configure_genai(config.GEMINI_API_KEY)
    ai_model = ai_analyzer.build_genai_model()

    # --- Step 1: Search for Videos ---
    videos_by_creator = youtube_api.search_videos(
        youtube_client=youtube,
        queries=config.SEARCH_QUERIES,
        genres=config.VIDEO_GENRES,
        max_results=config.MAX_RESULTS_PER_QUERY
    )

    if not videos_by_creator:
        print("No videos found matching the criteria. Exiting.")
        return

    # --- Step 2 & 3: Process Each Channel ---
    print("\n--- Processing Channels ---")
    total_channels = len(videos_by_creator)
    processed_count = 0

    for channel_id, creator_data in videos_by_creator.items():
        processed_count += 1
        channel_name = creator_data['creator_name']
        sanitized_channel_name = utils.sanitize_filename(channel_name)

        print(f"\n[{processed_count}/{total_channels}] Processing Channel: '{channel_name}' (ID: {channel_id})")
        print("-" * 30)

        # --- Step 2a: Fetch Transcripts ---
        video_transcripts = []
        videos_to_process = creator_data['videos']
        print(f"  Fetching transcripts for {len(videos_to_process)} video(s)...")

        for i, video_info in enumerate(videos_to_process):
            video_id = video_info['video_id']
            video_title = video_info['title']
            print(f"    ({i+1}/{len(videos_to_process)}) Fetching: {video_id} ('{video_title[:50]}...')")
            transcript_text = transcript_utils.get_transcript(video_id)
            if transcript_text:
                video_transcripts.append((video_id, video_title, transcript_text))
                print(f"      -> Transcript found ({len(transcript_text)} chars).")

        if not video_transcripts:
            print(f"  No usable transcripts found for channel '{channel_name}'. Skipping analysis.")
            continue

        print(f"  Successfully obtained {len(video_transcripts)} transcripts for '{channel_name}'.")

        # --- Step 2b: Combine and Save Transcripts ---
        combined_transcript_text = transcript_utils.format_combined_transcripts(
            channel_name, channel_id, video_transcripts
        )
        transcript_filename = os.path.join(config.TRANSCRIPT_DIR, f"{sanitized_channel_name}_transcripts.txt")
        try:
            with open(transcript_filename, "w", encoding="utf-8") as f:
                f.write(combined_transcript_text)
            print(f"  Saved combined transcripts to: {transcript_filename}")
        except IOError as e:
            print(f"  ERROR saving transcript file {transcript_filename}: {e}")
            # continue # Optional: skip AI if saving fails

        # --- Step 3: Analyze with AI and Save Critique ---
        critique_json_text = ai_analyzer.analyze_transcripts(
            model=ai_model,
            channel_name=channel_name,
            combined_transcript_text=combined_transcript_text
        )

        # --- CHANGE FILE EXTENSION ---
        critique_filename = os.path.join(config.CRITIQUE_DIR, f"{sanitized_channel_name}_critique.json")
        # --- END OF CHANGE ---

        try:
            # Basic check: Is it JSON-like enough to save? (Starts with { or [)
            if critique_json_text.strip().startswith(("{", "[")):
                 # Save the raw JSON string returned by the AI
                 with open(critique_filename, "w", encoding="utf-8") as f:
                     f.write(critique_json_text)
                 print(f"  Saved AI critique JSON to: {critique_filename}")
            else:
                 # If it's not JSON-like (likely an error message string), save as .txt
                 error_filename = os.path.join(config.CRITIQUE_DIR, f"{sanitized_channel_name}_critique_ERROR.txt")
                 with open(error_filename, "w", encoding="utf-8") as f:
                     f.write("--- AI ANALYSIS FAILED TO RETURN JSON ---\n")
                     f.write(critique_json_text)
                 print(f"  ERROR: AI did not return expected JSON. Saved raw error output to: {error_filename}")

        except IOError as e:
            print(f"  ERROR saving critique file {critique_filename}: {e}")
        except Exception as e_main: # Catch other potential errors during file handling
             print(f"  UNEXPECTED ERROR during critique saving for '{channel_name}': {e_main}")


    print("\n--- Processing Complete ---")

if __name__ == '__main__':
    main()