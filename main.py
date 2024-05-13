import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint

date = input("Type the date you want to create Playlist: ")
BILLBOARD_URL = f"https://www.billboard.com/charts/hot-100/{date}"
CLIENT_ID = "CLIENT_ID"
CLIENT_SECRET = "CLIENT_SECRET"

response = requests.get(BILLBOARD_URL)
billboard_html = response.text
soup = BeautifulSoup(billboard_html, "html.parser")
songs_tags = soup.select(selector="li ul li h3")
songs_list = [tag.string.strip() for tag in songs_tags]
print(songs_list)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt",
        username="Abhay Dixit"
    )

)
user_id = sp.current_user()["id"]
song_uris = []
year = date.split("-")[0]
for song in songs_list:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)

    try:
        uri = result["tracks"]["items"][0]['uri']
        song_uris.append(uri)
    except IndexError:
        print(f"'{song}' Is Not Available on Spotify. Skipped")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard {len(song_uris)}", public=False)
print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)

