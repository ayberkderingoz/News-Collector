import aiohttp
import asyncio
from bs4 import BeautifulSoup
from datetime import datetime

class HaberVerisi:
    def __init__(self, url, header, summary, text, img_url_list, publish_date, update_date):
        self.url = url
        self.header = header
        self.summary = summary
        self.text = text
        self.img_url_list = img_url_list
        self.publish_date = publish_date
        self.update_date = update_date


class HaberCekici:
    def __init__(self, base_url):
        self.base_url = base_url
        self.haber_verileri = []
        self.haberler = []

    async def _veri_cek(self, session, url):
        async with session.get(url) as response:
    
            content = await response.text(encoding='latin-1')
            soup = BeautifulSoup(content, 'html.parser',from_encoding="ISO-8859-9")
            haber_listesi = soup.find_all('div', class_='haber-post')

            tasks = []
        for haber in haber_listesi:
            haber_link = haber.find('a')
            if haber_link:
                haber_url = haber_link.get('href')
                if haber_url:
                    tasks.append(asyncio.create_task(self.get_haber_detay(session, haber_url)))

            await asyncio.gather(*tasks)

    async def veri_cek(self, page_count):
        await asyncio.sleep(5)
        async with aiohttp.ClientSession() as session:
            tasks = [self._veri_cek(session, f"{self.base_url}/page/{sayfa_numarasi}/") for sayfa_numarasi in range(1, page_count + 1)]
            await asyncio.gather(*tasks)

    async def get_haber_detay(self, session, haber_url):
        async with session.get(haber_url) as response:
            haber_soup = BeautifulSoup(await response.text(), 'html.parser')
            header = haber_soup.find('h1', class_='single_title').text.strip()
            summary = haber_soup.find('h2', class_='single_excerpt').text.strip()
            text = haber_soup.find('div', class_='yazi_icerik').text.strip()
            img_url_list = [img['src'] for img in haber_soup.find_all('img')]
            dates = haber_soup.find('div', class_='yazibio').text.strip().split(' ')

            publish_date = dates[0]
            update_date = dates[2]


            
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
        return self.haber_verileri

if __name__ == "__main__":
    base_url = 'https://turkishnetworktimes.com/kategori/gundem'
    haber_cekici = HaberCekici(base_url)
    asyncio.run(haber_cekici.veri_cek(page_count=50))

    haberler = haber_cekici.verileri_getir()
    for haber in haberler:
        print(haber.url, haber.header, haber.publish_date)
        # MongoDB'ye veri ekleme işlemleri yapılabilir
