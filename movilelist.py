import requests
import json

def get_now_playing_movie_list():
    
    json_file = open('../settings.json', 'r')
    json_data = json.load(json_file)

    url = "https://api.themoviedb.org/3/movie/now_playing?api_key=" + json_data["API_MOVIE"] + "&language=ja&region=jp"
    print(url)
    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    json_dict = response.json()
    
    movie_list = []
    pub_date_list = {}
    
    if json_dict["total_results"] > 0:
        movies = json_dict["results"]
        for movie in movies:
            movie_list.append( (movie["id"], movie["title"]))
            pub_date_list[movie["id"]] = movie["release_date"]
        print(movie_list)
        
    return movie_list, pub_date_list, movies
        
if __name__ == "__main__":
    get_now_playing_movie_list()