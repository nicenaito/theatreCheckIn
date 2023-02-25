from django.core.management.base import BaseCommand
from theatreCheckIn.models import Movies
from django.conf import settings
import requests

class Command(BaseCommand):
    def handle(self, *args, **options):
        url = "https://api.themoviedb.org/3/movie/now_playing?api_key=" + \
        settings.API_MOVIE + "&language=ja&region=jp"
        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        json_dict = response.json()

        if json_dict["total_results"] > 0:
            for i in range(1, json_dict["total_results"]):
                url = "https://api.themoviedb.org/3/movie/now_playing?api_key=" + \
                    settings.API_MOVIE + "&language=ja&region=jp&page=" + str(i)
                payload = {}
                headers = {}

                response = requests.request("GET", url, headers=headers, data=payload)

                json_dict = response.json()
                movies = json_dict["results"]
                for movie in movies:
                    try:
                        Movies.objects.get(pk=movie["id"])
                        print("Not saved!")
                        
                    except (KeyError, Movies.DoesNotExist):
                        register_movie = Movies(
                        movie_id=movie["id"],
                        movie_title=movie["title"],
                        pub_date=movie["release_date"],
                        original_title=movie["original_title"],
                        poster_path=movie["poster_path"],
                        original_language=movie["original_language"],
                        overview=movie["overview"],
                        )
                        register_movie.save()
                        print("Saved!")
