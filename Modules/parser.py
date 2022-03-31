from bs4 import BeautifulSoup
import urllib.request
import requests
import datetime
from datetime import datetime
import threading
from selenium import webdriver
import multiprocessing
import time
import csv
import re
from selenium.webdriver.common.by import By

months = {'янв': '01',
          'фев': '02',
          'мар': '03',
          'апр': '04',
          'мая': '05',
          'июн': '06',
          'июл': '07',
          'авг': '08',
          'сен': '09',
          'окт': '10',
          'ноя': '11',
          'дек': '12'}


class User:
    def __init__(self, name, time_since_registration, massive_of_comments):
        self.name = name
        self.timeSinceRegistration = time_since_registration
        self.massiveOfComments = massive_of_comments


class Comment:
    def __init__(self, content, rating, article_type):
        self.content = content
        self.rating = rating
        self.articleType = article_type


def get_most_commented_articles_urls():
    most_commented_news_urls = []
    for i in range(1, 250):
        all_news = 'https://www.e1.ru/text/?page=' + str(i)
        print(all_news)
        f = urllib.request.urlopen(all_news)
        soup = BeautifulSoup(f, 'html.parser')

        for link in soup.find_all(attrs={"data-test": "archive-record-item"}):
            if (link.find(attrs={'data-test': "record-stats-comments-count"}) != None):
                try:
                    if (int(link.find(attrs={'data-test': "record-stats-comments-count"}).text) >= 500):
                        most_commented_news_urls.append(
                            "https://www.e1.ru" + link.find(attrs={'data-test': "archive-record-header"}).get(
                                'href') + "comments/")
                        print(
                            "e1.ru" + link.find(attrs={'data-test': "archive-record-header"}).get('href') + "comments/")
                except:
                    most_commented_news_urls.append(
                        "https://www.e1.ru" + link.find(attrs={'data-test': "archive-record-header"}).get(
                            'href') + "comments/")
                    print("e1.ru" + link.find(attrs={'data-test': "archive-record-header"}).get('href') + "comments/")
    return most_commented_news_urls


def get_users_urls(soup, urls):
    for link in soup.find_all('a'):  # Parsing main page
        if type(link.get('href')) == str:
            if '/profile' in link.get('href'):
                urls.add(link.get('href'))  # _34R5A _1L80z


def get_time(soup2):
    registration_date = list(map(int, (soup2.find(class_="_34R5A _1L80z").text.split(':')[-1][1:].split('.'))))
    return datetime.date.today() - datetime.date(registration_date[2], registration_date[1], registration_date[0])


def get_name(soup2):
    return soup2.find("h3", class_="_37lFf HCxDG").text


def add_comment_to_user(user, link):
    content = link.find('p').text
    print(content)
    rating = int(link.find(class_='_3a3yB _36vB4').text[1:]) - int(link.find(class_='_3a3yB _2LFJP').text[1:])
    article_type = link.find("a").get("href")[6:].split('/')[0]
    comment = Comment(content, rating, article_type)
    user.massiveOfComments.append(comment)


def create_dict_of_comments(soup, comments_from_article):
    for link in soup.find_all(attrs={"data-test": "comment-item"}):
        name = link.find(attrs={"data-test": "comment-item__user-nickname"}).text
        comment = link.find(attrs={"data-test": "comment-item__text"}).text
        comments_from_article[name] = comment


def get_users_comments(soup2, users_list, url, user):
    for link in soup2.find_all(attrs={"data-test": "profile-comment-item"}):
        add_comment_to_user(user, link)
    if soup2.find(attrs={"data-test": "pagination-component"}) != None:
        for i in range(2, int((soup2.find_all(class_="_1sx3b")[-1].text)) + 1):
            f3 = urllib.request.urlopen('https://www.e1.ru' + url + '?page=' + str(i))
            soup3 = BeautifulSoup(f3, 'html.parser')
            threads = []
            for link in soup3.find_all(attrs={"data-test": "profile-comment-item"}):
                t = threading.Thread(target=add_comment_to_user, args=(user, link))
                threads.append(t)
                t.start()
            for t in threads:
                t.join()
            print("https://www.e1.ru" + url + "?page=" + str(i))
    users_list.append(user)


def write_csv_comments1(comments_from_article):
    with open('../comments.csv', 'w', newline='', encoding="utf-8") as csvfile:
        fieldnames1 = ['nickname', 'comment']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames1)
        for key, value in comments_from_article.items():
            writer.writerow({'nickname': key, 'comment': value})


def write_csv_comments2(users_list):
    with open('../comments2.csv', 'w', newline='') as csvfile:
        fieldnames2 = ['nickname', 'date_since_reg', 'comment', 'comment_rating', 'article_type']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames2)
        for user in users_list:
            for comment in user.massiveOfComments:
                writer.writerow({'nickname': user.name,
                                 'date_since_reg': user.timeSinceRegistration,
                                 'comment': comment.content,
                                 'comment_rating': comment.rating,
                                 'article_type': comment.articleType})


def get_page_source(url):
    browser = webdriver.Chrome()
    browser.get(url)
    answers_buttons = browser.find_elements(by=By.CSS_SELECTOR, value=".GcLi1")
    for button in answers_buttons:
        button.click()
        time.sleep(1)
        print("Кнопка прожата")
    try:
        show_more_btn = browser.find_element(by=By.XPATH,
                                             value="/html[1]/body[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div["
                                                   "3]/div[2]/div[ "
                                                   "1]/section[1]/div[2]/div[1]/div[2]/div[1]/button[1]")
        while show_more_btn is not None:
            show_more_btn = browser.find_element(by=By.XPATH,
                                                 value="/html[1]/body[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div["
                                                       "3]/div[2]/div[ "
                                                       "1]/section[1]/div[2]/div[1]/div[2]/div[1]/button[1]")
            show_more_btn.click()
    except:
        return browser.page_source
    browser.quit()


def get_number_of_comm_regarding_astrotime(soup, list):
    for link in soup.find_all(attrs={"itemprop": "commentTime"}):
        hour = int(str(link.text).split(' ')[-1].split(':')[0])
        list[hour] += 1


def get_number_of_comm_regarding_time_from_post(soup, list):
    date = soup.find(class_="_1mfwY")['datetime'].replace("T", " ").replace("-", "/")[2:]
    date_of_art = datetime.strptime(date, '%y/%m/%d %H:%M:%S')
    for link in soup.find_all(attrs={"itemprop": "commentTime"}):
        text = link.text.split(" ")
        date2 = text[2][2:] + "/" + months[text[1]] + "/" + text[0] + " " + text[-1] + ":00"
        date_of_comm = datetime.strptime(date2, '%y/%m/%d %H:%M:%S')
        try:
            list[int((str((date_of_comm - date_of_art)).split(':')[0]))] += 1
        except:
            continue

def create_csv_comments1():
    with open('../comments.csv', 'w', newline='', encoding="utf-8") as csvfile:
        fieldnames1 = ['nickname', 'comment']
        writer1 = csv.DictWriter(csvfile, fieldnames=fieldnames1)

        writer1.writeheader()
def create_csv_comments2():
    with open('../comments2.csv', 'w', newline='') as csvfile:
        fieldnames2 = ['nickname', 'date_since_reg', 'comment', 'comment_rating', 'article_type']
        writer2 = csv.DictWriter(csvfile, fieldnames=fieldnames2)

        writer2.writeheader()