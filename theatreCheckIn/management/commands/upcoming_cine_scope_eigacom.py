import requests
from bs4 import BeautifulSoup
import re
import datetime
from datetime import date, timedelta
import logging
import urllib.request, urllib.error

# Initializing logger
logger = logging.getLogger(__name__)

# 指定したURLのHTMLを取得
def get_html(url):
    response = requests.get(url)
    logger.debug("Response data: " + response.text)
    return response.text


# 指定したHTMLから映画詳細ページのURLを取得
def parse_movie_url(html):
    soup = BeautifulSoup(html, "html.parser")
    
    now_playing = soup.find_all("section")

    # リンク先に/movie/Tが含まれるものを取得
    movies = now_playing[1].find_all(href=re.compile("/movie/\d+/$"), class_="btn small")
    movie_url_list = []
    for movie in movies:
        # URLを絶対パスに変換し、リストに追加
        movie_url_list.append("https://eiga.com" + movie.attrs["href"])
    
    logger.debug("movie_url_list: " + str(movie_url_list))
    return movie_url_list


# 映画詳細ページのHTMLから作品情報を取得
def parse_movie_detail(html, movie_url):
    soup = BeautifulSoup(html, "html.parser")

    movie_dict = {}
    
    # シネマトゥデイの映画IDを取得
    movie_id = movie_url.split("/")[-2]
    logger.debug("Movie id: " + movie_id)
    movie_dict["movie_id"] = movie_id

    # 作品名を取得
    title_tag = soup.find("h1", itemprop="name", class_="page-title")
    title = title_tag.contents[0]
    logger.debug("Movie title: " + title)
    movie_dict["title"] = title

    # 公開日を取得
    pub_date_tag = soup.find("strong", itemprop="datePublished")
    # print(pub_date_tag)
    # YYYY年MM月DD日の形式からdatetime型に変換
    s_format = "%Y-%m-%d"
    # pub_date_str = pub_date_tag.contents[1].strip().replace("公開", "")
    if pub_date_tag is not None:
        pub_date = datetime.datetime.now()
        try:
            pub_date = datetime.datetime.strptime(pub_date_tag.attrs['content'], s_format)
        except:
            s_format = "%Y"
            pub_date = datetime.datetime.strptime(pub_date_tag.attrs['content'], s_format)
    else:
        pub_date = None
    
    logger.debug("Release date: " + str(pub_date))
    movie_dict["pub_date"] = pub_date
    # print(pub_date)

    # 映画のあらすじを取得
    description_tag = soup.find("p", itemprop="description")
    # print(description_tag)
    if description_tag is not None:
        description = description_tag.contents[0]
    else:
        description = ""
    logger.debug("Movie description: " + description)
    movie_dict["description"] = description

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
    logger.debug("Next target date: " + str(next_target_date))

    return next_target_date

# 指定したURLが存在するかチェック
def check_url_alive(url):
    try:
        f = urllib.request.urlopen(url)
        print ("OK:" + url )
        f.close()
        return True
    except:
        print ("NotFound:" + url)
        return False 

# 次のページが存在するかチェック
def has_next_page(html):
    soup = BeautifulSoup(html, "html.parser")
    # print(html)
    try:
        # 作品名を取得
        next_page_tag = soup.find("a", class_="next icon-after")
        print(next_page_tag)
        next_page = next_page_tag.attrs["href"]
        logger.info("Has Next Page: " + next_page)
        return True
    except:
        print ("Next page is not found")
        return False

# 公開中映画のリスト作成
def make_playing_movie_list():
    url = "https://eiga.com/now/"

    # 今週の映画情報を取得
    html = get_html(url)
    movie_url_list = parse_movie_url(html)

    movie_list = []

    for movie_url in movie_url_list:
        html_detail = get_html(movie_url)
        # print(html)
        movie_list.append(parse_movie_detail(html_detail, movie_url))

    # 翌週以降の映画情報を取得
    is_next_url = True
    
    now_page_num = 2;

    while is_next_url == True:
        next_url = "https://eiga.com/now/all/release/" + str(now_page_num)
        print(next_url)
        # is_next_url = check_url_alive(next_url)
        
        html = get_html(next_url)
        movie_url_list = parse_movie_url(html)

        for movie_url in movie_url_list:
            html_detail = get_html(movie_url)
            movie_list.append(parse_movie_detail(html_detail, movie_url))
        
        now_page_num = now_page_num + 1
        
        is_next_url = has_next_page(html)
        
        if is_next_url == False:
            print("Next url is not found.")
            break

    print(len(movie_list))
    return movie_list


# メイン処理
if __name__ == "__main__":
    playing_movie_list = make_playing_movie_list()
