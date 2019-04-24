import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

class YTapi:

    scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

    def getViewCount(yt_id):
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        #os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        DEVELOPER_KEY = "AIzaSyDmyWkyolg4wqglm6HVed3-7zxuui9aVSU"

        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey = DEVELOPER_KEY)

        request = youtube.videos().list(
            part="statistics, snippet",
            id=yt_id
        )
        response = request.execute()

        #print('Views: {}'.format(response['items'][0]['statistics']['viewCount']))
        return [int(response['items'][0]['statistics']['viewCount']), response['items'][0]['snippet']['thumbnails']['high']['url']]


'''
    def updateViews():
        for v in Video.objects.all():
            v.view_count=getViewCount(v.yt_video_id)

        def getVideos():
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "client_secret_258237979915-3n6lkfh4k79pk9gr2u2r4bug6t2f381t.apps.googleusercontent.com.json"

        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_console()
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        request = youtube.search().list(
            part="snippet",
            channelId="UCOmHUn--16B90oW2L6FRR3A",
            maxResults=10,
            q="intitle:m/v",
            type="video"
        )
        response = request.execute()

        print(response)
'''