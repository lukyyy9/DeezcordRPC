import requests
from winrt.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as MediaManager

async def get_media_info():
    sessions = await MediaManager.request_async()
    current_session = sessions.get_current_session()
    if current_session:
        media_properties = await current_session.try_get_media_properties_async()
        title = media_properties.title
        artist = media_properties.artist

        search_url = f"https://api.deezer.com/search?q=artist:\"{artist}\" track:\"{title}\""
        response = requests.get(search_url)
        if response.status_code == 200:
            data = response.json()
            if data['total'] > 0:  # If at least one match is found
                song = data['data'][0]  # Take the first matching song
                duration = song['duration']  # Get the song duration
                link = song['link'] # Get the song link
                # Use the duration as needed for the remaining time
                print(f"Found on Deezer: {title} by {artist}. Duration: {duration} seconds")
                return {"artist": artist, "title": title, "duration": duration, "link": link}
            else:
                print("Song not found on Deezer.")
        else:
            print("Error when querying the Deezer API.")
    else:
        return None