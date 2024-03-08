import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import re
# Введите свои учетные данные для Spotify API
client_id = '7745aa6ebc7a4dd381f6c3d55c8a5922'
client_secret = 'c145b7fecddc4b158cb99262c6c7b196'

# Создаем объект авторизации
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

def get_playlist_data(playlist_id):

    # Получаем информацию о плейлисте

    playlist = sp.playlist(playlist_id=f'{playlist_id}')

    return {'playlist_name':playlist['name'], 'playlist_img':playlist['images'][0]['url'] }

def get_playlist(playlist_id):
    # Извлекаем ID плейлиста из URL


    # Получаем информацию о плейлисте

    playlist=sp.playlist_tracks(playlist_id=f'spotify:playlist:{playlist_id}')
    # Извлекаем артистов и названия песен
    artists_and_songs = []

    for track in playlist['items']:
        artists = ' '.join([artist['name'] for artist in track['track']['artists']])
        song_name = track['track']['name']
        artists_and_songs.append(f"{artists} – {song_name}")
    '''a = {}
    for track in playlist['items']:
        artists = ', '.join([artist['name'] for artist in track['track']['artists']])
        song_name = track['track']['name']
        a[f'{artists}'] = song_name'''
    return artists_and_songs



