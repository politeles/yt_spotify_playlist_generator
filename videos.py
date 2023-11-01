# Get the api from youtube data api v3
import os
import argparse
import googleapiclient.discovery
import json



# Get channel id from channel name:
def get_channel_id(api_key, channel_name):
    youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=api_key)

    # Search for the channel based on the channel name

    search_response = youtube.search().list(
        q=channel_name,
        type='channel',
        part='id,snippet',
        maxResults=1,
    ).execute()
    print(search_response)
    # Get the channel ID from the search response
    channel_id = search_response['items'][0]['id']['channelId']
    return channel_id


# get the list of uploaded videos from channel id
def get_channel_videos(api_key, channel_id):
    youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=api_key)

    channel_response = youtube.channels().list(
        id=channel_id,
        part='contentDetails',
        maxResults=1,
    ).execute()

    # get the uploades playlist id from the channel
    playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

  
    # Fetch the videos from the channel
    videos = []
    next_page_token = None
    while True:
        playlist_response = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=200,
            pageToken=next_page_token
        ).execute()

        videos.extend(playlist_response['items'])

        next_page_token = playlist_response.get('nextPageToken')
        if not next_page_token:
            break

    return videos


# get channel videos from channel name
def get_channel_videos_from_name(api_key, channel_name):
    # call get channel id function
    channel_id = get_channel_id(api_key, channel_name)
    # call get channel videos function
    videos = get_channel_videos(api_key, channel_id)
    return videos


# store channel videos and titles in a json file
def store_channel_videos(channel_name, videos):
    channel_videos = {}
    channel_videos[channel_name] = []

    for video in videos:
        video_title = video['snippet']['title']
        video_id = video['snippet']['resourceId']['videoId']
        video_upload_date = video['snippet']['publishedAt']

        channel_videos[channel_name].append({'title': video_title, 'id': video_id, 'upload_date': video_upload_date})


    with open(channel_name+'-videos.json', 'w', encoding='utf-8') as f:
        json.dump(channel_videos, f, ensure_ascii=False, indent=4)



def main():
    parser = argparse.ArgumentParser(description='Fetch videos from a YouTube channel.')
    parser.add_argument('api_key', help='Your YouTube Data API v3 API key')
    parser.add_argument('channel_name', help='The name of the YouTube channel')
    args = parser.parse_args()

    api_key = args.api_key
    channel_name = args.channel_name

    videos = get_channel_videos_from_name(api_key, channel_name)
    store_channel_videos(channel_name, videos)

    for video in videos:
        video_title = video['snippet']['title']
        video_id = video['snippet']['resourceId']['videoId']
        print(f'{video_title}: https://www.youtube.com/watch?v={video_id}')

if __name__ == "__main__":
    main()
