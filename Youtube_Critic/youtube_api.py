from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def build_youtube_client(api_key):
    """Builds and returns the YouTube API service object."""
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        print("YouTube API client initialized successfully.")
        return youtube

    except Exception as e:
        print(f"FATAL: Failed to initialize YouTube API client: {e}")
        raise SystemExit(f"Could not build YouTube client: {e}")


def search_videos(youtube_client, queries, genres, max_results):
    """Searches YouTube and groups videos by channel."""
    print("Starting YouTube search...")
    videos_by_creator = {}
    processed_video_ids = set() # Avoid duplicate video entries

    for query in queries:
        for genre in genres:
            search_term = f"{query} {genre}"
            print(f"  Searching for: '{search_term}' (Max results: {max_results})")
            try:
                search_response = youtube_client.search().list(
                    q=search_term,
                    part='snippet',
                    type='video',
                    maxResults=max_results
                ).execute()

                items = search_response.get('items', [])
                print(f"    Found {len(items)} potential items for '{search_term}'.")

                for item in items:
                    if item['id']['kind'] != 'youtube#video':
                         continue # Ensures it's actually a video result

                    video_id = item['id']['videoId']
                    # Skip if video already processed from another query/genre
                    if video_id in processed_video_ids:
                        continue

                    channel_id = item['snippet'].get('channelId')
                    channel_title = item['snippet'].get('channelTitle', 'Unknown Channel')
                    video_title = item['snippet'].get('title', 'Unknown Title')

                    if not channel_id:
                        print(f"WARNING: Skipping video {video_id} ('{video_title}') - Missing channel ID.")
                        continue

                    if channel_id not in videos_by_creator:
                        videos_by_creator[channel_id] = {
                            'creator_name': channel_title,
                            'videos': []
                        }
                        # If the channel title was initially unknown, update it if a later video has it
                    elif videos_by_creator[channel_id]['creator_name'] == 'Unknown Channel' and channel_title != 'Unknown Channel':
                         videos_by_creator[channel_id]['creator_name'] = channel_title


                    videos_by_creator[channel_id]['videos'].append({
                        'video_id': video_id,
                        'title': video_title,
                        'query': query, # Keep track of how the video was found
                        'genre': genre
                    })
                    processed_video_ids.add(video_id)

            except HttpError as e:
                print(f"  ERROR during YouTube API search for '{search_term}': {e}")
                if e.resp.status == 403:
                     print("  FATAL: Received 403 Forbidden error. Check API key permissions or quota.")
                     raise SystemExit("YouTube API Forbidden Error") # Stop execution
            except Exception as e:
                print(f"  An unexpected error occurred during search for '{search_term}': {e}")

    found_count = len(videos_by_creator)
    total_videos = sum(len(data['videos']) for data in videos_by_creator.values())
    print(f"\nSearch finished. Found {total_videos} unique videos from {found_count} unique channels.")
    return videos_by_creator