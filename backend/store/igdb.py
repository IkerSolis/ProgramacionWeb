import requests
from decouple import config

CLIENT_ID = config('IGDB_CLIENT_ID')
CLIENT_SECRET = config('IGDB_CLIENT_SECRET')

def get_twitch_token():
    response = requests.post('https://id.twitch.tv/oauth2/token', params={
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'client_credentials'
    })
    return response.json()['access_token']

def search_games(query):
    token = get_twitch_token()
    response = requests.post(
        'https://api.igdb.com/v4/games',
        headers={
            'Client-ID': CLIENT_ID,
            'Authorization': f'Bearer {token}',
        },
        data=f'search "{query}"; fields name,summary,cover.url,genres.name,first_release_date; limit 10;'
    )
    return response.json()

def get_game_images(igdb_id):
    token = get_twitch_token()
    response = requests.post(
        'https://api.igdb.com/v4/screenshots',
        headers={
            'Client-ID': CLIENT_ID,
            'Authorization': f'Bearer {token}',
        },
        data=f'where game = {igdb_id}; fields url; limit 6;'
    )
    # The igdb urls come as t_thumb. We replace with t_screenshot_big for full size
    try:
        return [img['url'].replace('t_thumb', 't_screenshot_big') for img in response.json()]
    except Exception:
        return []