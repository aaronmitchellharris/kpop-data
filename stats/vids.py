
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors


def vidResults(groupName):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyDmyWkyolg4wqglm6HVed3-7zxuui9aVSU"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    request = youtube.search().list(
        part="snippet",
        channelId="UCOmHUn--16B90oW2L6FRR3A",
        maxResults=10,
        q="intitle:m/v|mv|"+groupName,
        type="video"
    )
    response = request.execute()

    print(response)