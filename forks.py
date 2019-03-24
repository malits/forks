import bs4 as bs
import urllib.request
import spotipy
import spotipy.util as util
import sys
import datetime as date

#TODO check update, confirm if a playlist contains a track
username = sys.argv[1]
playlist_id = sys.argv[2]
client_id = sys.argv[3]
client_secret = sys.argv[4]

#@Source Leigh Murray on Medium
token = util.prompt_for_user_token(username, scope='playlist-modify-private,playlist-modify-public', \
    client_id=client_id, client_secret=client_secret, redirect_uri='https://localhost:8080')

site = "https://pitchfork.com/reviews/best/albums/"

sauce = urllib.request.urlopen(site).read()
soup = bs.BeautifulSoup(sauce, 'html.parser')
spotify = spotipy.Spotify(auth=token)

to_search = []
albums = []

#@Source stackOverflow
for review in soup.findAll("div", {"class": "review__title"}):
     found_artist, found_title = review.find("li"), review.find("h2")
     to_search.append({"artist": found_artist.text, "title": found_title.text})


for item in to_search:
    spotify_artist = spotify.search(q=item["artist"] + " " \
        + item["title"], limit=1, type="album")
    if spotify_artist['albums']['items']:
        #pprint.pprint(spotify_artist['albums']['items'][0]['uri'])
        uri = spotify_artist['albums']['items'][0]['uri']
        albums.append(uri)

to_add = []

for album in albums:
    tracks = spotify.album_tracks(album)
    for track in tracks['items']:
        id = [track['id']]
        to_add.extend(id)

spotify.user_playlist_replace_tracks(username, playlist_id, to_add[:99])
spotify.user_playlist_add_tracks(username, playlist_id, to_add[99:])
