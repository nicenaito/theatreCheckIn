
# Importing necessary libraries and modules
from django.core.management.base import BaseCommand
from theatreCheckIn.models import Movies
import requests
import logging
from bs4 import BeautifulSoup
import re
import datetime
from datetime import timedelta
from theatreCheckIn.management.commands import upcoming_cine_scope

# Initializing logger
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    
    # Function to handle the command when it is run
    def handle(self, *args, **options):
        
        # Logging 'collectMovie' start
        logger.info("collectMovie start")
        url = "https://www.cinematoday.jp/movie/release/"

        # 今週の映画情報を取得
        html = upcoming_cine_scope.get_html(url)
        movie_url_list = upcoming_cine_scope.parse_movie_url(html)
        logger.debug("The list of target url :" + str(movie_url_list))

        movie_list = []

        logger.info("Get current week movie information start")
        
        for movie_url in movie_url_list:
            html = upcoming_cine_scope.get_html(movie_url)
            movie_list.append(upcoming_cine_scope.parse_movie_detail(html, movie_url))

        logger.info("Get current week movie information end")
        # print(movie_list)

        logger.info("Get next and more week movie information start")
        
        # 翌週以降の映画情報を取得
        is_next_url = True

        date = datetime.date.today()

        while is_next_url == True:
            logger.debug("The target date :" + str(date))
            next_url = url + upcoming_cine_scope.get_next_date(date)
            is_next_url = upcoming_cine_scope.check_url_alive(next_url)
            html = upcoming_cine_scope.get_html(next_url)
            movie_url_list = upcoming_cine_scope.parse_movie_url(html)
            logger.debug("The list of target url :" + str(movie_url_list))

            for movie_url in movie_url_list:
                html = upcoming_cine_scope.get_html(movie_url)
                movie_list.append(upcoming_cine_scope.parse_movie_detail(html, movie_url))

            # 翌週の日付を取得
            td = timedelta(days=7)
            date = date + td
            # print(date)

        else:
            logger.info("Next url is not found.")

        logger.info("Get next and more week movie information end")
        logger.debug("The number of movies :" + str(len(movie_list)))

        # TODO: #1 DBへの登録処理を修正する
        for movie in movie_list:
            
            # Get the current movie information from DB
            current_movie = Movies.objects.filter(movie_id=movie["movie_id"])
            
            # Register the movie information to DB
            register_movie = Movies(
            movie_id=movie["movie_id"],
            movie_title=movie["title"],
            pub_date=movie["pub_date"],
            description=movie["description"],
            )
            
            logger.info("The movie exists: " + str(current_movie.exists()))
            
            # If the movie information exists in DB and the description is the same, skip the registration
            if current_movie.exists():
                logger.debug("Specified movie id :" + current_movie[0].movie_id)
                if current_movie[0].description == movie["description"]:
                    logger.info("The movie has already been registered in DB. ID: " + movie["movie_id"] + " Title: " + movie["title"])
                    continue
                # If the movie information exists in DB and the description is different, update the updated_datetime
                else:
                    # Keep the created_datetime. updated_datetime will be updated to current time as default value.
                    register_movie.created_datetime = current_movie[0].created_datetime
                    logger.info("created_datetime is not changed and updated_datetime will be changed to current time. ")
            
            register_movie.save()
            logger.info("The movie has been registered in DB. Title: " + movie["title"])

        logger.info("collectMovie end")

