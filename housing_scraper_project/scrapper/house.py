
#import libraries

import pandas as pd
import numpy as np
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import ssl
import tqdm

#header for metadata
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

#get all the urls to scrape from search url
def get_all_anchor_tags(url):
  page = requests.get(url, headers=headers)#, proxies=proxies)
  content = page.content
  soup = BeautifulSoup(content)
  link_list = []
  for tag in soup.find_all('a'):
    link = tag.get("href")
    searchd = "/in/buy/projects/page/"
    if link.find(searchd) != -1:
      new_link = "https://housing.com" + link
      link_list.append(new_link)
  return link_list

#Scrape the url
def extract_data(url):
  page = requests.get(url, headers=headers)#, proxies=proxies)
  content = page.content
  soup = BeautifulSoup(content)
  #print(soup)
  result = {}
  flat_data = soup.findAll('div',attrs={'class' : 'css-j2zgcq'})
  flat_type = flat_data[0].find('h1',attrs={'class':'css-10rvbm3'})
  if flat_type is not None:
    flat_type = flat_type.text
  else:
    flat_type = "Flat type not mentioned"
  result['Flat type'] = flat_type
  key = []
  value = []
  for data in soup.findAll('section',attrs={'class' : 'css-13dph6'}):
    for i in data.findAll('div',attrs={'class' : 'css-r74jsk'}):
      key.append(i.text)
    for j in data.findAll('div',attrs={'class' : 'css-3o6ku8'}):
      value.append(j.text)
  for i in range(0,4):
    result[key[i]] = value[i]
  #print(result)
  tables = soup.find_all("table")
  table = tables[0]
  tab_data = [[cell.text for cell in row.find_all(["th","td"])]
                          for row in table.find_all("tr")]
  for k in tab_data:
    result[k[0]] = k[1]
  #print(result)

  about = soup.find('div',attrs={'class' : 'css-1tetu0c'})
  #print(about.text)
  about_data = soup.find('div',attrs={'class' : 'about-text css-1d1e0rh'})
  #print(about_data.text)
  result[about.text] = about_data.text

  special_high = soup.find('div',attrs={'class' : "css-1o20zr1"})

  if special_high is not None:
    high = special_high.find('span',attrs={'class' : "css-xms1sc"}).text
    lis = []
    for i in special_high.findAll('div',attrs={'class' : "highlight css-1byt3mr"}):
      lis.append(i.text)
    result[high] = ",".join(lis)
  #print(result)
  new_dic = {}
  for k, v in result.items():
    lis=[]
    if v.find("}") != -1:
      lis.append(v.split("}")[-1])
    elif v.find("₹") != -1:
      lis.append(v.split("₹")[-1])
    else:
      lis.append(v)
    
    new_dic[k] = lis
  df = pd.DataFrame(new_dic)
  return df

def extract_image_urls(url):
  page = requests.get(url, headers=headers)#, proxies=proxies)
  content = page.content
  soup = BeautifulSoup(content)
  images = soup.find_all('img')
  images_list = []
  for image in images: 
    images_list.append(image['src'])
  return images_list
def download_images(img_list):
  count = 0
  for image in img_list:
    try:
      response = requests.get(image, stream=True)
      #print(response,image)
      img_format = image.split(".")[-1]
      remaining = image.split(".")[-2]
      realname = remaining.split("/")[-1]
      realname = realname + "_" + str(count)+"." + img_format
      # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
      count+=1
      with open(realname, "wb") as f:
          f.write(response.content)
    except:
      continue

#Write the data to the csv file
def write_to_file(dataframe):
  dataframe.to_csv('my_csv.csv', mode='w',header=True,index=False)

#merge the new and existing data in the csv file
def process_data_frame(df):
  try:
    old_df = pd.read_csv("my_csv.csv")
    new_df = old_df.append(df)
  except:
    new_df = df
  return new_df

#urls of the search page
#TODO
# Add your URLS to search in the url list
# Note : Don't forget to add a comma after each url
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
for url in url_list:
  # Ignore SSL certificate errors
  ctx = ssl.create_default_context()
  ctx.check_hostname = False
  ctx.verify_mode = ssl.CERT_NONE
  #get all the url from search result
  list_of_urls = get_all_anchor_tags(url)
  print(list_of_urls)
  for i in list_of_urls:
    try:
      df = extract_data(i)
      new_df = process_data_frame(df)
      write_to_file(new_df)
      #code to download images from the website
      #====
      # list_of_img_urls = extract_image_urls(i)
      # download_images(list_of_img_urls)
      #=====
    except:
      continue
#print the data
read_data = pd.read_csv("my_csv.csv");
read_data.head()
