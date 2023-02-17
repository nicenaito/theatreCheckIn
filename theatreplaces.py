import requests
import json
from django.conf import settings

def current_place():
    """
    現在地の緯度経度を取得する。

    Returns:
        int: 現在地の緯度、経度
    """    
    geo_request_url = "https://get.geojs.io/v1/ip/geo.json"
    geo_data = requests.get(geo_request_url).json()
    # print(geo_data['latitude'])
    # print(geo_data['longitude'])
    return geo_data["latitude"], geo_data["longitude"]


def get_movie_theatre(latitude, longitude):
    """
    現在地の緯度、経度をインプットとして、付近の映画館リストを返す。

    Args:
        latitude (int): 現在地の緯度
        longitude (int): 現在地の経度
    """
    
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + latitude + "," + longitude + "&radius=2000&type=movie_theater&key=" + settings.API_MAP
    # print(url)
    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    json_dict = response.json()

    movie_theatre = []

    if json_dict["status"] == "OK":
        for theatre in json_dict["results"]:
            movie_theatre.append((theatre["name"],theatre["name"]))
        # print(movie_theatre)
        
    return movie_theatre

if __name__ == "__main__":
    latitude, longitude = current_place()
    get_movie_theatre(latitude, longitude)