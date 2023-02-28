from django.core.management.base import BaseCommand
from theatreCheckIn.models import Movies
from django.conf import settings
import requests
from django.utils import timezone

class Command(BaseCommand):
    def handle(self, *args, **options):
        url = "https://api.themoviedb.org/3/movie/now_playing?api_key=" + settings.API_MOVIE + "&language=ja&region=jp"
        total_pages = self.getNumberOfResults(url)
        
        if total_pages > 0:
            movies_dict = []
            movies_dict = self.makeNowPlayingMoviesDict(url+"&page=", total_pages, movies_dict)
            
            now_playing_movie_id_list = []
            
            for movie_list in movies_dict:
                for data in movie_list["results"]:
                    now_playing_movie_id_list.append(data["id"])
                    try:
                        Movies.objects.get(pk=data["id"])
                        # print("Not saved!")
                        
                    except (KeyError, Movies.DoesNotExist):
                        register_movie = Movies(
                        movie_id=data["id"],
                        movie_title=data["title"],
                        pub_date=data["release_date"],
                        original_title=data["original_title"],
                        poster_path=data["poster_path"],
                        original_language=data["original_language"],
                        overview=data["overview"],
                        )
                        register_movie.save()
                        print("Saved!")
            
            registered_movies = Movies.objects.values_list('movie_id', flat=True)
            
            # DBに登録されている映画が公開中映画APIのレスポンスに含まれていない場合、公開中フラグをFalseにする。
            for query_result in registered_movies:
                if query_result not in now_playing_movie_id_list:
                    selected_movie = Movies.objects.get(pk=query_result)
                    if selected_movie <= timezone.now():
                        selected_movie.now_playing = False
                        selected_movie.updated_datetime = timezone.now()
                        selected_movie.save()
                        print("Saved!")
                    
    def getNumberOfResults(self, base_url):
        payload = {}
        headers = {}

        response = requests.request("GET", base_url, headers=headers, data=payload)

        json_dict = response.json()
        
        total_pages = json_dict["total_pages"]
        
        return total_pages
    
    def makeNowPlayingMoviesDict(self, base_url, number_of_results, movies_dict):
        i = 1
        while i <= number_of_results:
        # for i in range(1, number_of_results):
            url = base_url + str(i)
            payload = {}
            headers = {}

            response = requests.request("GET", url, headers=headers, data=payload)

            movies_dict.append(response.json())
            
            i += 1
            	
        return movies_dict