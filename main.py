from Modules.parser import *
import numpy as np
import matplotlib.pyplot as plt

most_commented_articles = get_most_commented_articles_urls()
create_csv_comments1()
create_csv_comments2()
for article_url in most_commented_articles:

    users_urls = set()
    users_list = []
    comments_from_article = {}

    soup = BeautifulSoup(get_page_source(article_url), 'html.parser')

    create_dict_of_comments(soup, comments_from_article)

    write_csv_comments1(comments_from_article)

    get_users_urls(soup, users_urls)

    for user_url in users_urls:
        f2 = urllib.request.urlopen('https://www.e1.ru' + user_url)
        soup2 = BeautifulSoup(f2, 'html.parser')
        if soup2.find("h3", class_="_37lFf HCxDG _20h04") is not None:  # Проверка на заблоченого юзера
            continue
        user = User(get_name(soup2), get_time(soup2), [])
        get_users_comments(soup2, users_list, user_url, user)

    write_csv_comments2(users_list)
