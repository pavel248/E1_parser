from Modules.parser import *
import numpy as np #pip install numpy
import matplotlib.pyplot as plt
import pandas as pd


most_commented_articles = get_most_commented_articles_urls()
list1 = [0] * 24
list2 = [0] * 48
for article_url in most_commented_articles:
    soup = BeautifulSoup(get_page_source(article_url), 'html.parser')
    get_number_of_comm_regarding_astrotime(soup, list1)
    get_number_of_comm_regarding_time_from_post(soup,list2)


with open('stat1.csv', 'w', newline='') as csvfile:
    fieldnames = ['hour', 'count']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for i in range(24):
        writer.writerow({"hour":i, "count":list1[i]})

with open('stat2.csv', 'w', newline='') as csvfile:
    fieldnames = ['hour', 'count']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for i in range(48):
        writer.writerow({"hour": i, "count": list2[i]})




data = pd.read_csv("stat1.csv")
hour = data['hour']
count = data['count']
aboba = [str(i) for i in range(24)]
plt.bar(hour, count, tick_label=aboba)
plt.show()

data2 = pd.read_csv("stat2.csv")
hour2 = data2['hour']
count2 = data2['count']
aboba2 = [str(i) for i in range(48)]
plt.bar(hour2, count2, tick_label=aboba2)
plt.show()


