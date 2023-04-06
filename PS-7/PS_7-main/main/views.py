from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError

import requests
from bs4 import BeautifulSoup
import csv
import os


def main_page(request):
    return render(request, 'main\Main.html')

def model_page(request):
    if request.method == 'POST':

        postDict = request.POST.dict()
        keyWord = postDict.get('Key')

        HEADERS = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 OPR/92.0.0.0'
        }
        HOST = 'https://fabstore.ru'
        URL =  'https://fabstore.ru/catalog/kurtki'

        def get_html(url, params=''):
            r = requests.get(url, headers= HEADERS,params=params)
            return r

        def get_content(html):
            soup = BeautifulSoup(html, 'html.parser')
            items = soup.find_all('div', class_ ='product-card')
            clothes = []
            for item in items:
                if item.find('div', class_ ='product-card__title').get_text(strip =True) == keyWord:
                    clothes.append(
                        {
                            'name':item.find('div', class_ ='product-card__desc-line').get_text(strip =True),
                            'name_brand':item.find('div', class_ ='product-card__title').get_text(strip =True),
                            'link':HOST+item.find('a', class_='product-card__link').get('href'),
                            'img': HOST+ item.find('img', class_ ='product-card__pic').get('src')
                        }
                    )
            return clothes

        def parser():
            PAGENATTION = 5
            html = get_html(URL)
            if html.status_code == 200:
                cards = []
                for page in range(0,PAGENATTION):
                    print(f'Парсим страницу:{(round(page)+1)}')
                    html = get_html(URL, params = {'page': page})
                    cards.extend(get_content(html.text))
                print(cards)
            else:
                print("Сайт полёг!!!")
                cards = [{'name': '-', 'name_brand': 'Бренд не найден', 'link': '-', 'img': '-'}]
            if len(cards) == 0:
                cards = [{'name': '-', 'name_brand': 'Бренд не найден', 'link': '-', 'img': '-'}]
            return cards        

        answer = parser()

        r = requests.get(URL, headers=HEADERS)
        bs = BeautifulSoup(r.text, "lxml")


        # for i in range(len(all_links)):
        #     el = {'link': 'https://www.kinopoisk.ru/'+all_links[i]['href'], 'name': all_name[i].text, 'rating': all_rating[i].text}
        #     #print(el)
        #     if keyWord in all_name[i].text:
        #         answer.append(el)
        
        
        


    else:
        #print('GET')
        answer = [{'name': ''}]
    return render(request, 'main\Parser.html', {'answer': answer})

def contacts_page(request):
    return render(request, 'main\Contacts.html')

def gettedBadRequest(request, exception):
    return HttpResponseBadRequest(f"<h1>Упс... Что-то пошло не так</h1>")

def gettedServerError(request):
    return HttpResponseServerError(f"<h1>Упс... Что-то пошло не так. Уже чиним!</h1>")
