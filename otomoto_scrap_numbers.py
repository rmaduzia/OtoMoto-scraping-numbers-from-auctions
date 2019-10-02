import requests
from bs4 import BeautifulSoup
import re


class otomoto_numbers_scrapping():
    def __init__(self, main_url):
        self.main_url = main_url
        self.get_all_main_pages(main_url)

        for i in all_pages_to_scrap:

            self.get_all_auctions_links_in_page(i)
        for j in auctions_links:
            self.get_auction_id(j)

        for k in auctions_id:
            self.get_auction_numbers(str(k)[2:-2])

        for j in range(0,len(auctions_links)):
            auctions_data.append(str(auctions_links[j])+str(auctions_id[j])+str(auctions_numbers[j]))

        self.export_data_to_csv(auctions_data)

    def get_all_main_pages(self, url):
        counter = 2
        if "search" in url:
            already_url = url + "&page="
            all_pages_to_scrap.append(url)

            while requests.get(already_url + str(counter), allow_redirects=False).status_code == 200:
                all_pages_to_scrap.append(already_url + str(counter))
                counter += 1

        else:
            already_url = url + "?page="
            all_pages_to_scrap.append(url)
            while requests.get(already_url + str(counter), allow_redirects=False).status_code == 200:
                all_pages_to_scrap.append(already_url + str(counter))
                counter += 1

    def get_all_auctions_links_in_page(self, link):
        req = requests.get(link)
        soup = BeautifulSoup(req.content, 'html.parser')
        for link in soup.find_all(class_="offer-title__link"):
            auctions_links.append(link.get('href'))

    def get_auction_id(self, auctions_list):
        auctions_id.append(re.findall("ID(.+?).html", auctions_list))

    def get_auction_numbers(self, auction_id):
        temp=[]
        phone_url = 'https://www.otomoto.pl/ajax/misc/contact/all_phones/' + auction_id
        r = requests.get(phone_url)
        json_phone_numbers = r.json()

        if len(json_phone_numbers) == 1:
            auctions_numbers.append(json_phone_numbers[0]["number"])
        else:
            for i in range(0, len(json_phone_numbers)):
                temp += [json_phone_numbers[i]["number"]]
            auctions_numbers.append(temp)

    def export_data_to_csv(self, body):
        f = open("Auctions_Data.txt", "a")
        for i in range(0,len(body)):
            f.write(body[i]+'\n')


if __name__ == "__main__":
    global all_pages_to_scrap
    global auctions_links
    global auctions_id
    global auctions_numbers
    global auctions_data

    auctions_links = []
    all_pages_to_scrap = []
    auctions_id = []
    auctions_numbers = []
    auctions_data = []

    test_url='https://www.otomoto.pl/osobowe/aixam/a721/?search%5Bfilter_float_price%3Ato%5D=20000&search%5Bfilter_enum_fuel_type%5D%5B0%5D=diesel&search%5Bfilter_enum_fuel_type%5D%5B1%5D=petrol-cng&search%5Bbrand_program_id%5D%5B0%5D=&search%5Bcountry%5D='
    kl = otomoto_numbers_scrapping(test_url)