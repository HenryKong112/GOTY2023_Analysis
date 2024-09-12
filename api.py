import os
import pandas as pd
import googleapiclient.discovery
from dotenv import load_dotenv

# YouTube API setup
load_dotenv()
DEVELOPER_KEY = os.getenv("DEVELOPER_KEY")
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"
youtube = googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, developerKey=DEVELOPER_KEY)

def get_replies(parent_id):  # Added video_id as an argument
    replies = []
    next_page_token = None

    while True:
        reply_request = youtube.comments().list(
            part="snippet",
            parentId=parent_id,
            textFormat="plainText",
            maxResults=100,
            pageToken=next_page_token
        )
        reply_response = reply_request.execute()

        for item in reply_response['items']:
            comment = item['snippet']
            replies.append([
                comment['authorDisplayName'],
                comment['parentId'],
                comment['publishedAt'],
                comment['likeCount'],
                comment['textDisplay'],
                item['id']
            ])

        next_page_token = reply_response.get('nextPageToken')
        if not next_page_token:
            break

    return replies

def fetch_comments(video_id):

    comments_list = []
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100
    )
    response = request.execute()
    while True:
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            comments_list.append([
                comment['authorDisplayName'],
                item['id'],
                comment['publishedAt'],
                comment['likeCount'],
                comment['textDisplay'],
            ])
        try:
            next_page_token = response['nextPageToken']
            
        except KeyError:
            break
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,
            pageToken=next_page_token
        )
        response = request.execute()
    return comments_list

# Fetch comments for a specific video
VIDEO_ID = "Zu2z5M4gmno"
comments = fetch_comments(VIDEO_ID)

# Get top comments
df_top_comment = pd.DataFrame(comments,columns=['Username','Comment_ID', 'PublishedAt', 'Like', 'Comment'])

# Get reply comments
id_list = df_top_comment["Comment_ID"].to_list()
reply_list=[]
for id in id_list:
    reply_get = get_replies(id)
    for i in range(len(reply_get)):
        one_reply = reply_get[i]
        reply_list.append(one_reply)
df_reply = pd.DataFrame(reply_list,columns=['Username','Parent_ID', 'PublishedAt', 'Like', 'Comment','Comment_ID'])

# Combine 2 dataframes to get all comments
df_combined = pd.concat([df_top_comment, df_reply], ignore_index=True)

