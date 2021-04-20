#################################
##### Name: Dylan Coakley   #####
##### Uniqname: dcoakley    #####
#################################
################################################################################

from bs4 import BeautifulSoup
import requests
import json

WIKI = "https://en.wikipedia.org"

def build_city_dict():
   ''' Make a of dictionary of city data from 'https://en.wikipedia.org/wiki/
   List_of_United_States_cities_by_population'"

    Parameters
    ----------
    None

    Returns
    -------
    dict
        key is the url and the data is a list of information for a city.
    '''
   list_of_cities = '/wiki/List_of_United_States_cities_by_population'

   url = WIKI + list_of_cities

   cache = open_cache('cache.json')

   if url in cache:
        print('Using cache')
        return(cache[url])

   else:
      response = requests.get(url)
      soup = BeautifulSoup(response.text, 'html.parser')
      #print(soup)

      page_data = soup.find('div', class_='mw-parser-output')
      #print(cities_data)
      #table_data = page_data.find('tbody')
      #print(table_data)


      city_info = page_data.find_all('tr')[20:120] #Learned about this method of limiting on a scrape here: https://stackoverflow.com/questions/18966368/python-beautifulsoup-scrape-tables
      #print(city_info)

      title = []
      url = []
      pop2019 = []
      size = []
      density = []

      for i in city_info:
         j = i.find('a')
         title.append(j['title'])
         url.append(j['href'])

         k = i.find_all('td')[3]
         for tags in k:
            tags = tags.replace(',', '')
            pop2019.append(int(tags[:-1]))

         l = i.find_all('td')[-5]
         for tags in l:
            tags = tags[:5]
            tags = tags.strip()
            tags = tags.replace(',', '')
            size.append(float(tags))

         m = i.find_all('td')[-3]
         for tags in m:
            tags = tags.replace(',', '')
            tags = tags.replace('/sq\xa0mi\n', '')
            density.append(int(tags))

      dicts = {'title':title, 'url':url, 'pop':pop2019, 'size':size, 'dens':density}
      print(dicts)

      #thcdict = {url: title}
      #return thcdict

      
      #


def open_cache(cache_file):
    '''Opens the cache file if it exists and loads the JSON into
    the CACHE_DICT dictionary.
    if the cache file doesn't exist, creates a new cache dictionary

    Parameters
    ----------
    cache_file: str
        The cache filename

    Returns
    -------
    The opened cache: dict
    '''
    try:
        cache_file = open(cache_file, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

def save_cache(cache_file, cache_dict):
    ''' Saves the current state of the cache to disk

    Parameters
    ----------
    cache_file: str
        The cache filename

    cache_dict: dict
        The dictionary to save

    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(cache_file,"w")
    fw.write(dumped_json_cache)
    fw.close()


if __name__ == "__main__":
   build_city_dict()