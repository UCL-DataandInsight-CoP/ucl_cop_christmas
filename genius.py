import json
import lyricsgenius
import os

artist_name = "Backstreet Boys"
os.getcwd()
genius = lyricsgenius.Genius("jWTT2Hx299ISIx1cPlGmCPZnWXEnobCDc7p7gxCRUihRjwDDyId58x5npDQqSKmT")
artist = genius.search_artist(artist_name, max_songs=3, sort="title")

song = genius.search_song("All I Have to Give", artist.name)

artist.save_lyrics()

import pandas as pd
from pandas import Series, DataFrame
with open('Lyrics_BackstreetBoys.json') as json_data:
    data = json.load(json_data)
    #print(data.keys())

df = pd.DataFrame(
    [
        {
            'Song Title': item['title'],
            'Lyrics': item['lyrics']
        } 
        for item in data['songs'] if data['songs'] is not None
    ]
)


print(df.head())
df.to_csv('output.csv')