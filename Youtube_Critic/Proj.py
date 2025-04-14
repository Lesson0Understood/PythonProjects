from youtube_transcript_api import YouTubeTranscriptApi
from googleapiclient.discovery import build

# Replace 'YOUR_API_KEY' with your actual API key from Google Cloud
API_KEY = 'AIzaSyDUbnu5dtuOyXxNbmUjmdUYIhdMEnHI7yY'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'


def search_videos_and_group_by_creator(queries, genres,max_results):
    """
    Searches for videos based on queries and genres and groups the results by creator.

    Args:
        queries: A list of search queries.
        genres: A list of video categories or genres (can be keywords).

    Returns:
        A dictionary where keys are creator channel IDs and values are lists of
        dictionaries, each containing 'video_id', 'query', and 'genre'.
    """
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)
    videos_by_creator = {}

    for query in queries:
        for genre in genres:
            search_term = f"{query} {genre}"  # Combine query and genre for search
            try:
                search_response = youtube.search().list(
                    q=search_term,
                    part='snippet',
                    type='video',
                    maxResults=max_results  # Adjust as needed
                ).execute()

                for search_result in search_response.get('items', []):
                    if search_result['id']['kind'] == 'youtube#video':
                        video_id = search_result['id']['videoId']
                        channel_id = search_result['snippet']['channelId']
                        channel_title = search_result['snippet']['channelTitle'] # You can use title if needed

                        if channel_id not in videos_by_creator:
                            videos_by_creator[channel_id] = {
                                'creator': channel_title,
                                'videos': []
                            }

                        videos_by_creator[channel_id]['videos'].append({
                            'video_id': video_id,
                            'query': query,
                            'genre': genre
                        })
            except Exception as e:
                print(f"An error occurred during search for '{search_term}': {e}")

    return videos_by_creator

if __name__ == '__main__':
    search_queries = ["understanding neural network, math intution"]
    video_genres = ["deep learning"]

    grouped_videos = search_videos_and_group_by_creator(search_queries, video_genres,100)

    for creator_id, creator_data in grouped_videos.items():

        # gather all video transcriptions
        video_texts = []
        for video in creator_data["videos"]:
            try:
                transcript = YouTubeTranscriptApi.get_transcript(video["video_id"])
                text = " ".join([entry['text'] for entry in transcript])
            except:
                print(f"No text for video {video['video_id']} for {creator_data['creator']}")
                continue

            video_texts.append((video["video_id"],text))
        final_texts = [f"Video {index+1}\n\nID: {vid[0]}\n\n{vid[1]}\n\n\n\n" for index, vid in enumerate(video_texts)]
        full_text = "\nEnd of video\n".join(final_texts)
        
        # create file for creator
        with open(f"Reports/{creator_data['creator']}","w",encoding="utf-8") as f:
            f.write(f"""
Channel Name: {creator_data['creator']}

Videos:

{full_text}

""")
            
    print("Deep Search Finished Successfully.")
            
