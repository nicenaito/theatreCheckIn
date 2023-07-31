import requests
from bs4 import BeautifulSoup
import re
import datetime
from datetime import date, timedelta


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


# メイン処理
if __name__ == "__main__":
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
