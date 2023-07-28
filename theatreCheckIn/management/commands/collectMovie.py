
# Importing necessary libraries and modules
from django.core.management.base import BaseCommand
from theatreCheckIn.models import Movies
import requests
import logging
from bs4 import BeautifulSoup
import re
import datetime
from datetime import timedelta

# Initializing logger
logger = logging.getLogger(__name__)

<<<<<<< HEAD
# Defining a custom Django management command
=======

>>>>>>> c657f5034509eb305de8b3f7dd15687c0e4750f3
class Command(BaseCommand):
    
    # Function to handle the command when it is run
    def handle(self, *args, **options):
        
        # Logging 'collectMovie' start
        logger.info("collectMovie start")
<<<<<<< HEAD
        
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
=======
        url = "https://www.cinematoday.jp/movie/release/"

        # 今週の映画情報を取得
        html = get_html(url)
        movie_url_list = parse_movie_url(html)

        movie_list = []

        for movie_url in movie_url_list:
            html = get_html(movie_url)
            movie_list.append(parse_movie_detail(html, movie_url))

        # print(movie_list)

        # 翌週以降の映画情報を取得
        is_next_url = True

        date = datetime.date.today()

        while is_next_url == True:
            next_url = url + get_next_date(date)
            is_next_url = check_url_alive(next_url)
            html = get_html(next_url)
            movie_url_list = parse_movie_url(html)

            for movie_url in movie_url_list:
                html = get_html(movie_url)
                movie_list.append(parse_movie_detail(html, movie_url))

            # 翌週の日付を取得
            td = timedelta(days=7)
            date = date + td
            # print(date)

        else:
            print("Next url is not found.")

        print(len(movie_list))

        # TODO: #1 DBへの登録処理を修正する
        for movie in movie_list:
            register_movie = Movies(
            movie_id=movie["movie_id"],
            movie_title=movie["title"],
            pub_date=movie["pub_date"],
            discription=movie["discription"],
            )
            register_movie.save()
            logger.info("The movie has been registered in DB. Title: " + movie["title"])

        logger.info("collectMovie end")
                    
        # 指定したURLのHTMLを取得
        def get_html(url):
            response = requests.get(url)
            # print(response.text)
            return response.text


        # 指定したHTMLから映画詳細ページのURLを取得
        def parse_movie_url(html):
            soup = BeautifulSoup(html, "html.parser")

            # リンク先に/movie/Tが含まれるものを取得
            movies = soup.find_all(href=re.compile("^/movie/T"))
            movie_url_list = []
            for movie in movies:
                # URLを絶対パスに変換し、リストに追加
                movie_url_list.append("https://www.cinematoday.jp/" + movie.attrs["href"])
            return movie_url_list


        # 映画詳細ページのHTMLから作品情報を取得
        def parse_movie_detail(html, movie_url):
            soup = BeautifulSoup(html, "html.parser")

            movie_dict = {}

            # シネマトゥデイの映画IDを取得
            movie_id = movie_url.split("/")[-1]
            # print(movie_id)
            movie_dict["movie_id"] = movie_id

            # 作品名を取得
            title_tag = soup.find("h1", itemprop="name")
            title = title_tag.contents[0]
            # print(title)
            movie_dict["title"] = title

            # 公開日を取得
            pub_date_tag = soup.find("span", class_="published")
            # print(pub_date.contents[1])
            # YYYY年MM月DD日の形式からdatetime型に変換
            s_format = "%Y年%m月%d日"
            pub_date_str = pub_date_tag.contents[1].strip().replace("公開", "")
            pub_date = datetime.datetime.strptime(pub_date_str, s_format)
            # print(pub_date)
            movie_dict["pub_date"] = pub_date

            # 映画のあらすじを取得
            description_tag = soup.find("p", itemprop="description")
            description = description_tag.contents[0]
            # print(description)
            movie_dict["description"] = description

            # TODO: #1 Implement getting movie summary
            # summary_tag = soup.find_all("section","")
            # print(summary_tag[1])

            # print(movie_dict)

            return movie_dict


        # 　翌週月曜日の日付を取得
        def get_next_date(date):
            # dateの曜日を取得
            weekday = date.weekday()
            # dateから指定した曜日までの加算日数を計算
            add_days = 7 - weekday
            # dateに加算
            next_target_date = date + datetime.timedelta(days=add_days)
            next_target_date = next_target_date.strftime("%Y%m%d")
            # print(next_target_date)

            return next_target_date


        # 指定したURLが存在するかチェック
        def check_url_alive(url):
            html = get_html(url)
            soup = BeautifulSoup(html, "html.parser")
            found_url = soup.find("meta", attrs={"property": "og:url"})
            current_url = found_url.get("content")
            print(url)
            # print(current_url)

            # metaタグのURLと指定したURLが一致するかチェック
            # 一致する場合はTrueを返す
            if url == current_url:
                return True
            else:
                return False
>>>>>>> c657f5034509eb305de8b3f7dd15687c0e4750f3
