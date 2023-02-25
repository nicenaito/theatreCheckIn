import requests
from django.conf import settings

def get_now_playing_movie_list():
    
    # print(settings.API_MOVIE)

    url = "https://api.themoviedb.org/3/movie/now_playing?api_key=" + settings.API_MOVIE + "&language=ja&region=jp"
    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    json_dict = response.json()
    
    movie_list = []
    pub_date_list = {}
    
    if json_dict["total_results"] > 0:
        for i in range(1,json_dict["total_results"]):
            url = "https://api.themoviedb.org/3/movie/now_playing?api_key=" + settings.API_MOVIE + "&language=ja&region=jp&page=" + str(i) 
            payload={}
            headers = {}

            response = requests.request("GET", url, headers=headers, data=payload)

            json_dict = response.json()
            movies = json_dict["results"]
            for movie in movies:
                movie_list.append( (movie["id"], movie["title"]))
                pub_date_list[movie["id"]] = movie["release_date"]
    sorted_movie_list = sorted(movie_list, reverse=True)
    sorted_movie_list.insert(0,(0,"鑑賞した作品を選択してください。"))
    return sorted_movie_list, movies
        
if __name__ == "__main__":
    get_now_playing_movie_list()