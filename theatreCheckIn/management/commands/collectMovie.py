from django.core.management.base import BaseCommand
from theatreCheckIn.models import Movies
from django.conf import settings
import requests
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    def handle(self, *args, **options):
        logger.info("collectMovie start")
        url = "https://api.themoviedb.org/3/movie/now_playing?api_key=" + settings.API_MOVIE + "&language=ja&region=jp"
        total_pages = self.getNumberOfResults(url)
        
        if total_pages > 0:
            logger.info("Total page of the response: " + str(total_pages))
            movies_dict = []
            movies_dict = self.makeNowPlayingMoviesDict(url+"&page=", total_pages, movies_dict)
            
            now_playing_movie_id_list = []
            
            for movie_list in movies_dict:
                for data in movie_list["results"]:
                    now_playing_movie_id_list.append(data["id"])
                    try:
                        movie = Movies.objects.get(pk=data["id"])
                        logger.info("The movie has been on DB. Title: " + movie.movie_title)
                        
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
                        logger.info("The movie has been registered in DB. Title: " + data["title"])
            
            registered_movies = Movies.objects.values_list('movie_id', flat=True)
            
            # DBに登録されている映画が公開中映画APIのレスポンスに含まれていない場合、公開中フラグをFalseにする。
            for query_result in registered_movies:
                if query_result not in now_playing_movie_id_list:
                    selected_movie = Movies.objects.get(pk=query_result)
                    if selected_movie.now_playing == True and selected_movie.pub_date < timezone.now().date():
                        selected_movie.now_playing = False
                        selected_movie.updated_datetime = timezone.now()
                        selected_movie.save()
                        logger.info("The flag of 'now playing' for the movie has been updated to False. Title: " + selected_movie.movie_title)
                        
        logger.info("collectMovie end")
                    
    def getNumberOfResults(self, base_url):
        logger.info("getNumberOfResults start")
        payload = {}
        headers = {}

        logger.info("API Request")
        response = requests.request("GET", base_url, headers=headers, data=payload)
        logger.info("API Response recieved")

        json_dict = response.json()
        
        total_pages = json_dict["total_pages"]
        
        logger.info("getNumberOfResults end")
        
        return total_pages
    
    def makeNowPlayingMoviesDict(self, base_url, number_of_results, movies_dict):
        logger.info("makeNowPlayingMoviesDict start")
        i = 1
        while i <= number_of_results:
        # for i in range(1, number_of_results):
        
            logger.debug("Getting page = " + str(i))
            url = base_url + str(i)
            payload = {}
            headers = {}

            logger.info("API Request")
            response = requests.request("GET", url, headers=headers, data=payload)
            logger.debug("Response: " + str(response.json()))
            logger.info("API Response recieved")

            movies_dict.append(response.json())
            logger.debug("Dictionary is made: " + str(movies_dict))
            logger.debug("Done getting page = " + str(i))
            
            i += 1
            	
        logger.info("makeNowPlayingMoviesDict end")
        return movies_dict