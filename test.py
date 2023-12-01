import requests
from bs4 import BeautifulSoup
import threading
import pymongo

class News:
    """
    A class to represent news.

    ...

    Attributes
    ----------
    url : str
        url of the news
    header : str
        header of the news
    summary : str
        summary of the news
    text : str
        content of the news
    img_url_list : list
        list of image urls in the news
    publish_date : datetime
        publish date of the news
    update_date : datetime
        update date of the news
    """
    def __init__(self, url, header, summary, text, img_url_list, publish_date, update_date):
        self.url = url
        self.header = header
        self.summary = summary
        self.text = text
        self.img_url_list = img_url_list
        self.publish_date = publish_date
        self.update_date = update_date

class NewsController:
    """
    A class to represent news scraper.

    ...

    Attributes
    ----------
    base_url : str
        base url of the news website
    news_data : list
        list of news data
    
        
    Methods
    -------

    get_data(url)
        Gets news data from given url.
    append_tasks(page_count)
        Appends tasks to thread list.
    get_haber_detay(news_url)
        Gets news detail from given news url.
    get_data()
        Returns news data.


    """
    def __init__(self, base_url):
        self.base_url = base_url
        self.news_data = []

    def get_data(self, url):
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            news_list = soup.find_all('article', class_='col-12')

            for new in news_list:
                new_link = new.find('a')
                if new_link:
                    new_url = new_link.get('href')
                    if new_url:
                        self.get_haber_detay(new_url)
        except requests.exceptions.Timeout:
            print("Connection Timeouted.")
        except requests.exceptions.ConnectionError:
            print("Connection Error Occured.")


    def append_tasks(self, page_count):
        threads = []
        for page_number in range(1, page_count + 1):
            url = f"{self.base_url}/page/{page_number}/"
            thread = threading.Thread(target=self.get_data, args=(url,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    def get_haber_detay(self, news_url):
        response = requests.get(news_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        header = soup.find('h1', class_='single_title').text.strip()
        summary = soup.find('h2', class_='single_excerpt').text.strip()
        text = soup.find('div', class_='yazi_icerik').text.strip()
        img_url_list = [img['src'] for img in soup.find_all('img')]
        dates = soup.find('div', class_='yazibio').text.strip().split(' ')

        publish_date = dates[0]
        update_date = dates[2]

        news_data = News(url=news_url, header=header, summary=summary, text=text, img_url_list=img_url_list, publish_date=publish_date, update_date=update_date)
        self.news_data.append(news_data)

    def get_news(self):
        return self.news_data

if __name__ == "__main__":
    base_url = 'https://turkishnetworktimes.com/kategori/gundem'
    newsController = NewsController(base_url)
    newsController.append_tasks(page_count=50)

    news = newsController.get_news()
    for new in news:
        print(new.url, new.header, new.publish_date)
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["ayberk_deringoz"]
        collection = db["news"]
        collection.insert_one(new.__dict__)
        print("saved to db")




   