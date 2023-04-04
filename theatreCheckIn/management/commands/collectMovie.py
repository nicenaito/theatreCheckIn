
# Importing necessary libraries and modules
from django.core.management.base import BaseCommand
from theatreCheckIn.models import Movies
from django.conf import settings
import requests
from django.utils import timezone
import logging

# Initializing logger
logger = logging.getLogger(__name__)

# Defining a custom Django management command
class Command(BaseCommand):
    
    # Function to handle the command when it is run
    def handle(self, *args, **options):
        
        # Logging 'collectMovie' start
        logger.info("collectMovie start")
        
        # Requesting the now playing movies API
        url = "https://api.themoviedb.org/3/movie/now_playing?api_key=" + settings.API_MOVIE + "&language=ja&region=jp"
        total_pages = self.getNumberOfResults(url)
        
        # If there are pages of results, make a dictionary of all now playing movies from the response
        if total_pages > 0:
            logger.info("Total page of the response: " + str(total_pages))
            movies_dict = []
            movies_dict = self.makeNowPlayingMoviesDict(url+"&page=", total_pages, movies_dict)
            
            # Make a list of ids of movies currently playing in theatres
            now_playing_movie_id_list = []
            for movie_list in movies_dict:
                for data in movie_list["results"]:
                    now_playing_movie_id_list.append(data["id"])
                    
                    # Check if the movie is already present in the database. If yes, update its attributes.
                    try:
                        movie = Movies.objects.get(pk=data["id"])
                        if movie.overview == "" and data["overview"] != "":
                            movie.overview = data["overview"]
                            movie.updated_datetime = timezone.now()
                            movie.save()
                            logger.info("あらすじを登録しました。")
                            
                        logger.info("The movie has been on DB. Title: " + movie.movie_title)
                        
                    # If the movie is not already present in the database, create a new entry with its attributes
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
            
            # Make a list of ids of all movies present in the database 
            registered_movies = Movies.objects.values_list('movie_id', flat=True)
            
            # For each movie in the database, if it is not currently playing, update its status to False.
            for query_result in registered_movies:
                if query_result not in now_playing_movie_id_list:
                    selected_movie = Movies.objects.get(pk=query_result)
                    if selected_movie.now_playing == True and selected_movie.pub_date < timezone.now().date():
                        selected_movie.now_playing = False
                        selected_movie.updated_datetime = timezone.now()
                        selected_movie.save()
                        logger.info("The flag of 'now playing' for the movie has been updated to False. Title: " + selected_movie.movie_title)
                        
        # Logging 'collectMovie' end
        logger.info("collectMovie end")
                    
    # Helper function to return the number of pages in the API response
    def getNumberOfResults(self, base_url):
        logger.info("getNumberOfResults start")
        payload = {}
        headers = {}

        # Request the API and convert the response to a dictionary
        logger.info("API Request")
        response = requests.request("GET", base_url, headers=headers, data=payload)
        logger.info("API Response recieved")
        json_dict = response.json()
        
        # Get the number of pages in the response
        total_pages = json_dict["total_pages"]
        
        logger.info("getNumberOfResults end")
        
        return total_pages
    
    # Helper function to retrieve and compile a dictionary of all now playing movies from the API response
    def makeNowPlayingMoviesDict(self, base_url, number_of_results, movies_dict):
        logger.info("makeNowPlayingMoviesDict start")
        i = 1
        while i <= number_of_results:
            logger.debug("Getting page = " + str(i))
            url = base_url + str(i)
            payload = {}
            headers = {}

            # Request the API and convert the response to a dictionary
            logger.info("API Request")
            response = requests.request("GET", url, headers=headers, data=payload)
            logger.debug("Response: " + str(response.json()))
            logger.info("API Response recieved")

            # Append the results to the movie dictionary
            movies_dict.append(response.json())
            logger.debug("Dictionary is made: " + str(movies_dict))
            logger.debug("Done getting page = " + str(i))
            
            i += 1
                
        logger.info("makeNowPlayingMoviesDict end")
        return movies_dict
