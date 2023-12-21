# scraper/urls.py

from django.urls import path
from . import views

# Your list of URLs
url_list = [
"https://housing.com/in/buy/searches/P3te34s1zvaong5td",
"https://housing.com/in/buy/searches/P2q1uwqz5uo79lvmy",
"https://housing.com/in/buy/searches/P6w6rzu8yq0jutxih",
"https://housing.com/in/buy/searches/P1el4pqs71cc8a4oq",
"https://housing.com/in/buy/searches/Presjxke82ehhai1",
"https://housing.com/in/buy/searches/P2p755bijb3w8veen",
"https://housing.com/in/buy/searches/P6mmiqcl6ho6er3oc",
"https://housing.com/in/buy/searches/E4ff9",
"https://housing.com/in/buy/searches/Pv26iopup2rxged3",
"https://housing.com/in/buy/searches/E4e7y",
"https://housing.com/in/buy/searches/E4di3",
"https://housing.com/in/buy/searches/P2hln47z1q71v8uqk"
"https://housing.com/in/buy/searches/P1jlgdrtnm1iwir8c",
"https://housing.com/in/buy/searches/P26nrckh1cj7f6fhh"
]

# Create URL patterns for each URL in the list
urlpatterns = [
    path(f'scrape/{i}/', views.scrape_property, {'url': url}, name=f'scrape_property_{i}')
    for i, url in enumerate(url_list)
]
