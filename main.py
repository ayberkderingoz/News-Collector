import asyncio
import requests
from bs4 import BeautifulSoup
from datetime import datetime

class HaberCekici:
    def __init__(self, base_url):
        self.base_url = base_url
        self.haberler = []

    async def veri_cek(self, session, page_count):
        tasks = []
        async with session:
            for sayfa_numarasi in range(1, page_count + 1):
                url = f"{self.base_url}/page/{sayfa_numarasi}/"
                tasks.append(asyncio.create_task(self.get_haberler(session, url)))
            await asyncio.gather(*tasks)

    async def get_haberler(self, session, url):
        async with session.get(url) as response:
            soup = BeautifulSoup(await response.text(), 'html.parser')
            haber_listesi = soup.find_all('article', class_='post')

            tasks = []
            for haber in haber_listesi:
                haber_url = haber.find('a')['href']
                tasks.append(asyncio.create_task(self.get_haber_detay(session, haber_url)))
            await asyncio.gather(*tasks)

    async def get_haber_detay(self, session, haber_url):
        async with session.get(haber_url) as response:
            haber_soup = BeautifulSoup(await response.text(), 'html.parser')
            header = haber_soup.find('h1', class_='entry-title').text.strip()
            summary = haber_soup.find('div', class_='entry-content').find('strong').text.strip()
            text = haber_soup.find('div', class_='entry-content').text.strip()
            img_url_list = [img['src'] for img in haber_soup.find_all('img')]
            publish_date = datetime.strptime(haber_soup.find('time', class_='entry-date')['datetime'], '%Y-%m-%dT%H:%M:%S%z').strftime('%Y-%m-%d')
            update_date = datetime.strptime(haber_soup.find('time', class_='updated')['datetime'], '%Y-%m-%dT%H:%M:%S%z').strftime('%Y-%m-%d')

            haber_verisi = {
                'url': haber_url,
                'header': header,
                'summary': summary,
                'text': text,
                'img_url_list': img_url_list,
                'publish_date': publish_date,
                'update_date': update_date
            }
            self.haberler.append(haber_verisi)

    def verileri_getir(self):
        return self.haberler

async def main():
    base_url = 'https://turkishnetworktimes.com/kategori/gundem'
    haber_cekici = HaberCekici(base_url)

    async with requests.Session() as session:
        await haber_cekici.veri_cek(session, page_count=50)

    haberler = haber_cekici.verileri_getir()
    for haber in haberler:
        print(haber)
        # Burada MongoDB'ye veri ekleme işlemleri yapılabilir

if __name__ == "__main__":
    asyncio.run(main())
