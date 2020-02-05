## UCL Community of Practice: Christmas Songs

### Outline

Source christmas songs and lyrics data from the Spotify and Genius APIs using Python. Create an
interesting visualisation. 

### Data Collection Pipeline

The data colelction pipeline for this project collects song information from all official
Spotify Christmas playlists using the Spotify API and then scraped the associated song lyrics
from Genius.com

CSVs are crated for each playlist and a combined file of all the songs created. The lyrics are also
stored seperately as text only for later analysis and visualisation.

#### Collecting Spotify Christmas Songs

A connection to the Spotify API was establised using the Spotipy python library with authentication
keys generated from the Spotify developer's portal:

```python
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

cid = ''
secret = ''
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
```

The cid and secret variables can be replaced with a user's own keys.



<img src="tree.png?raw=true"/>