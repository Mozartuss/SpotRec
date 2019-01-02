import spotipy
from spotipy import oauth2
from titlecase import titlecase


def generate_token():
    credentials = oauth2.SpotifyClientCredentials(
        client_id="bf02b103fc4f499d8b3a65a3ec8739cb",
        client_secret="689e7d33f9e24da39fe4e1a38b5ab5fe",
    )
    token = credentials.get_access_token()
    return token


def refresh_token():
    """ Refresh expired token"""
    global spotify
    new_token = generate_token()
    spotify = spotipy.Spotify(auth=new_token)


_token = generate_token()
spotify = spotipy.Spotify(auth=_token)


def generate_metadata(raw_song):
    """
    Fetch a song's metadata from Spotify.
    fetch track information directly if it is spotify link
    """
    print("[Spotipy]", _token)
    meta_tags = spotify.track(raw_song)

    artist = spotify.artist(meta_tags["artists"][0]["id"])
    album = spotify.album(meta_tags["album"]["id"])

    try:
        meta_tags[u"genre"] = titlecase(artist["genres"][0])
    except IndexError:
        meta_tags[u"genre"] = None
    try:
        meta_tags[u"copyright"] = album["copyrights"][0]["text"]
    except IndexError:
        meta_tags[u"copyright"] = None
    try:
        meta_tags[u"external_ids"][u"isrc"]
    except KeyError:
        meta_tags[u"external_ids"][u"isrc"] = None

    meta_tags[u"release_date"] = album["release_date"]
    meta_tags[u"publisher"] = album["label"]
    meta_tags[u"total_tracks"] = album["tracks"]["total"]
    meta_tags["year"], *_ = meta_tags["release_date"].split("-")
    return meta_tags

# Apple has specific tags - see mutagen docs -
# http://mutagen.readthedocs.io/en/latest/api/mp4.html
M4A_TAG_PRESET = {
    "album": "\xa9alb",
    "artist": "\xa9ART",
    "date": "\xa9day",
    "title": "\xa9nam",
    "year": "\xa9day",
    "originaldate": "purd",
    "comment": "\xa9cmt",
    "group": "\xa9grp",
    "writer": "\xa9wrt",
    "genre": "\xa9gen",
    "tracknumber": "trkn",
    "albumartist": "aART",
    "discnumber": "disk",
    "cpil": "cpil",
    "albumart": "covr",
    "copyright": "cprt",
    "tempo": "tmpo",
    "lyrics": "\xa9lyr",
    "comment": "\xa9cmt",
}

TAG_PRESET = {}
for key in M4A_TAG_PRESET.keys():
    TAG_PRESET[key] = key

