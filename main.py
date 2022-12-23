import requests as req
from pandas import DataFrame, read_sql, Timestamp
import datetime as dt
import time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from sqlalchemy import create_engine


RETRY_PERIOD = 60 * 60  # One hour hold between requests
HEADERS = {
    'User-Agent': UserAgent().chrome
}
URL_LIST = [
    'https://tass.ru/rss/v2.xml',
    'https://www.vedomosti.ru/rss/news',
    'https://lenta.ru/rss/'
]
# Categories generalized, to find unknown, check associated list new_categories
POSSIBLE_CATEGORIES = {
    'Спорт':
    'Спорт',
    'Россия и СНГ':
    'Россия, Бывший СССР, Моя страна, Новости партнеров, Москва',
    'Экономика и бизнес':
    'Экономика и бизнес, Бизнес, Экономика, Финансы, Недвижимость, Авто',
    'Происшествия':
    'Происшествия',
    'Медиа':
    'Медиа	Культура, Интернет и СМИ',
    'Наука и техника':
    'Наука и техника, Космос, Технологии',
    'Общество':
    'Общество, Забота о себе, Среда обитания, Из жизни, Ценности',
    'Мир':
    'Мир, Международная панорама, Путешествия',
    'Политика':
    'Политика, Силовые структуры',
    'Прочее':
    'Прочее'
}
# Update your database parameters
POSTGRES_USERNAME = 'docker'
POSTGRES_PASSWORD = 'docker'
POSTGRES_ADDRESS = 'localhost'
POSTGRES_PORT = '5432'  # Check port for availability
POSTGRES_DBNAME = 'test'
engine = create_engine(
    'postgresql://{username}:{password}@{ipaddress}:{port}/{dbname}'.format(
        username=POSTGRES_USERNAME,
        password=POSTGRES_PASSWORD,
        ipaddress=POSTGRES_ADDRESS,
        port=POSTGRES_PORT,
        dbname=POSTGRES_DBNAME
    )
)
# You may use autofilling from environment
'''.format(
        os.environ.get("POSTGRES_USER"),
        os.environ.get("POSTGRES_PASSWORD"),
        os.environ.get("POSTGRES_ADDRESS"),
        os.environ.get("POSTGRES_DATABASE"),
    )'''
connection = engine.connect()
# Collects all new unknown categories, that were found.
# Check it to update POSSIBLE_CATEGORIES dict if necessary.
new_categories = []


def category_generalizer(category):
    """Generalizes common categories"""
    for general, total in POSSIBLE_CATEGORIES.items():
        if category in total:
            return general
    new_categories.append(category)
    return POSSIBLE_CATEGORIES['Прочее']


def url_parse_news(url):
    """Parse news url and returns all posts found"""
    response = req.get(url, headers=HEADERS)
    response.encoding = 'utf-8'
    # If response not OK, returns empty list
    if response.status_code != 200:
        return []
    soup = BeautifulSoup(response.text, 'xml')
    return soup.find_all('item')


def date_cutter(date):
    """Cuts timezone and forms pandas Timestamp."""
    date_components = date.split(' ')
    sql_date_components = ' '.join(date_components[0:5])
    return Timestamp(
        dt.datetime.strptime(sql_date_components, "%a, %d %b %Y %H:%M:%S")
    )


def check_already_exist(article, df_articles, df_new_articles):
    """Check if article is already in database."""
    old_articles = df_articles.to_dict('records')
    new_articles = df_new_articles.to_dict('records')
    if article in old_articles or article in new_articles:
        return True
    return False


def main():
    """Collects data and saves to database"""
    timestamp = Timestamp(0)
    while True:
        # Loads articles from database
        df_articles = read_sql('articles', connection)
        # Frame for new uploaded articles
        df_new_articles = DataFrame(
            columns=["source", "title", "link", "pub_date", "category"]
        )
        for url in URL_LIST:
            for tag in url_parse_news(url):
                if date_cutter(tag.pubDate.text) > timestamp:
                    post = {
                        "source": url,
                        "title": tag.title.text,
                        "link": tag.link.text,
                        "pub_date": date_cutter(tag.pubDate.text),
                        "category": category_generalizer(tag.category.text)
                    }
                    if not check_already_exist(
                        post, df_articles,
                        df_new_articles
                    ):
                        df_new_articles = df_new_articles.append(
                            post,
                            ignore_index=True
                        )
        timestamp = Timestamp.now()
        df_new_articles.to_sql(
            "articles",
            connection,
            if_exists="append",
            index=False
        )
        time.sleep(RETRY_PERIOD)


main()
