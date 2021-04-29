#################################
##### Name: Dylan Coakley   #####
##### Uniqname: dcoakley    #####
#################################


from bs4 import BeautifulSoup
import requests
import json
import time
import pandas as pd
import numpy as np
import random as random
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon
from matplotlib.path import Path
import secrets as secrets


WIKI = "https://en.wikipedia.org"
CENSUS_KEY = secrets.CENSUS_KEY


def build_city_dict():
    ''' Make a of dictionary of city data from 'https://en.wikipedia.org/wiki/
    List_of_United_States_cities_by_population'"

    Parameters
    ----------
    None

    Returns
    -------
    dict
        returns a dictionary of city information scraped from wikipedia.
    '''
    list_of_cities = '/wiki/List_of_United_States_cities_by_population'

    cities_url = WIKI + list_of_cities

    cache = open_cache('cache.json')

    if cities_url in cache:
        print('Using cache')
        return(cache[cities_url])

    else:
        response = requests.get(cities_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        page_data = soup.find('div', class_='mw-parser-output')

        city_info = page_data.find_all('tr')[20:120] #Learned about this method of limiting on a scrape here: https://stackoverflow.com/questions/18966368/python-beautifulsoup-scrape-tables

        title = []
        url = []
        pop2019 = []
        size = []
        density = []
        state = []

        for i in city_info:
            j = i.find('a')
            if ',' in j['title']:
                x = j['title'].split(',', 1)[0]
                title.append(x)
            else:
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

            z = i.find_all('td')[2]
            state.append(z.text[1:-1])

        url2 = WIKI + '/wiki/List_of_U.S._state_and_territory_abbreviations'
        response2 = requests.get(url2)
        soup2 = BeautifulSoup(response2.text, 'html.parser')

        state_data = soup2.find('div', class_='mw-parser-output')
        state_table = state_data.find('tbody')

        state_names_abbr = state_table.find_all('tr')[12:63]

        state_names = []
        abbreviations = []
        for n in state_names_abbr:

            o = n.find_all('td')[0]
            state_names.append(o.text[1:])

            p = n.find_all('td')[3]
            abbreviations.append(p.text)

        state_abbr_dict = {state_names[i]: abbreviations[i] for i in range(51)}

        abbr_coll = []
        for states in state:
            for key in state_abbr_dict:
                if states == key:
                    abbr_coll.append(state_abbr_dict[key])

        dicts = {'name':title, 'state':state, 'abbr':abbr_coll, 'Population':pop2019, 'Size in Square Miles':size, 'Population Density (People per Square Mile)':density, 'url':url}
        cache = {cities_url: dicts}
        save_cache('cities_data.json', cache)
        return dicts


def crawl_city_info(city_dict):
    '''Crawls wikipedia city pages and pulls introductory paragraphs on the city.
    
    Parameters
    ----------
    The city information dictionary.

    Returns
    -------
    A list of text on the city

    '''
    cache = open_cache('paragraphs.json')

    if 'city paragraph' in cache:
        print('Using cache')
        return(cache['city paragraph'])

    else:
        wiki_city_url = city_dict['url']


        city_info = []
        for x in wiki_city_url:
            city_url= WIKI+x
            response = requests.get(city_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            if x=='/wiki/Los_Angeles' or x=='/wiki/Louisville,_Kentucky' or x=='/wiki/New_Orleans' or x=='/wiki/Chicago':
                parent=soup.find('div', class_='mw-parser-output')
                child = parent.find_all('p')[2]
                child=child.text
                child=child.replace('(\xa0m', ' meters')
                child=child.replace('\xa0million', ' million')
                child=child.replace('\xa0billion', ' billion')
                child=child.replace('xa0[', ' [')
                child=child.replace('xa0km', ' km')
                child=child.replace('xa0km2', ' km2')
                child=child.replace('xa0ha', ' hectares')
                child=child.replace('xa0mi', 'mi')
                child=child.replace('\xa0', '')
                child=child.replace('\n', '')
                child=child.replace('(listen)', '')
                child=child.replace('[a]', '')
                city_info.append(child)
                for i in range(30):
                    child=child.replace(f'[{i}]', '')
            elif x=='/wiki/San_Francisco':
                parent=soup.find('div', class_='mw-parser-output')
                child = parent.find_all('p')[3]
                child=child.text
                child=child.replace('(\xa0m', ' meters')
                child=child.replace('\xa0million', ' million')
                child=child.replace('\xa0billion', ' billion')
                child=child.replace('xa0[', ' [')
                child=child.replace('xa0km', ' km')
                child=child.replace('xa0km2', ' km2')
                child=child.replace('xa0ha', ' hectares')
                child=child.replace('xa0mi', 'mi')
                child=child.replace('\xa0', '')
                child=child.replace('\n', '')
                child=child.replace('(listen)', '')
                child=child.replace('[a]', '')
                for i in range(30):
                    child=child.replace(f'[{i}]', '')
                city_info.append(child)
            else:
                print(f'Fetching from {city_url}')
                parent = soup.find('body')
                child = parent.find_all('p')[1]
                child=child.text
                child=child.replace('(784\xa0km2)', 'or 784 square kilometers')
                child=child.replace('\xa0million', ' million')
                child=child.replace('\xa0billion', ' billion')
                child=child.replace('xa0[', ' [')
                child=child.replace('xa0km', ' km')
                child=child.replace('xa0km2', ' km2')
                child=child.replace('xa0ha', ' hectares')
                child=child.replace('xa0mi', 'mi')
                child=child.replace('\xa0', '')
                child=child.replace('\n', '')
                child=child.replace('(listen)', '')
                child=child.replace('[a]', '')
                for i in range(30):
                    child=child.replace(f'[{i}]', '')
                city_info.append(child)

        cache = {'city paragraph': city_info}
        save_cache('paragraphs.json', cache)

        return city_info


def get_redline_map(city, state_abbr):
    ''' Gets redline map data from the richmond website

    Parameters
    ----------
    City name, two letter state abbreviation

    Returns
    -------
    Dictionary of geo data from historic US redlining
    '''
    richmond_url ='http://dsl.richmond.edu/panorama/redlining/static/downloads/geojson/'

    cache = open_cache('redline_maps.json')

    if city in cache:
        print('Using cache')
        return(cache[city])

    else:
        corr_city = city.replace(' ', '')
        corr_city = corr_city.replace('Saint', 'St')
        corr_city = corr_city.replace('St.', 'St')

        year = 1930
        mapdata = {}


        while year < 1946:
            print(f'Checking {city} for redlining data in {year}AD')
            data = requests.get(richmond_url+state_abbr+corr_city+str(year)+'.geojson')
            year+=1
            if year ==1945 and data.status_code == 404:
                cache[city] = f'{city} does not have redlining data available from http://dsl.richmond.edu/panorama/redlining/static/downloads/geojson/'
                cache_dict = cache
                save_cache('redline_maps.json', cache_dict)
                return mapdata
                break
            elif data.status_code == 404 and year > 1944:
                continue
            elif year == 1944:
                new_data = requests.get(richmond_url+state_abbr+corr_city+'19XX.geojson')
                if new_data.status_code == 200:
                    cache[city] = new_data.json()
                    cache_dict = cache
                    save_cache('redline_maps.json', cache_dict)
                    return cache[city]
                    break
                else:
                    cache[city] = f'{city} does not have redlining data available from http://dsl.richmond.edu/panorama/redlining/static/downloads/geojson/'
                    cache_dict = cache
                    save_cache('redline_maps.json', cache_dict)
                    return mapdata
                    break
            elif data.status_code == 200:
                cache[city] = data.json()
                cache_dict = cache
                save_cache('redline_maps.json', cache_dict)
                return cache[city]
                break


def make_redline_map(map_data, city):
    '''Makes the redlining map from geodata.

    Paramaters
    ----------
    the map data dictionary from, the city name

    Returns
    -------
    Dictionary of redlining map data
    '''
    range_ = len(map_data['features'])
    holc_grades = [map_data['features'][i]['properties']['holc_grade'] for i in range(range_)]

    color_collector = []
    for x in holc_grades:
        if x == 'A':
            color_collector.append('darkgreen')
        elif x == 'B':
            color_collector.append('cornflowerblue')
        elif x == 'C':
            color_collector.append('gold')
        else:
            color_collector.append('maroon')

    thisDict ={
    "Coordinates": [map_data['features'][i]['geometry']['coordinates'][0][0] for i in range(range_)],
    "Holc_Grade": [map_data['features'][i]['properties']['holc_grade'] for i in range(range_)],
    "Holc_Color": color_collector,
    "name": [i for i in range(range_)]
    }

    districts = []
    for i in range(range_):
        districts.append(Polygon(thisDict['Coordinates'][i], ec='black', fc=thisDict['Holc_Color'][i]))

    fig, ax = plt.subplots()

    for u in districts:
        ax.add_patch(u)

    ax.autoscale(enable=True)
    #plt.rcParams["figure.figsize"] = (15,15)
    plt.title(label=f'{city} Redlining Map')
    plt.show()
    return(thisDict)
    #Some of this code is reused from HW4


def dict_to_pd_df(city_data):
    ''' Takes in a dictionary and returns a pandas dataframe of the same data
    
    Parameters
    ----------
    Dictionary of scraped city data

    Returns
    -------
    Dataframe of scraped city data
    '''
    df = pd.DataFrame.from_dict(city_data)
    return(df)


def summary_stats(df):
    ''' Takes in a dataframe and returns the summary statistics of that dataframe

    Parameters
    ----------
    None

    Returns
    -------
    None
    '''
    print(df.describe())


def histo(df, input):
    ''' Takes in a dataframe and the input of the requestor, spits out a histogram of city data
    
    Parameters
    ----------
    dataframe and input

    Returns
    -------
    None
    '''
    
    if input == 1:
        df.hist(column = 'Population')
        plt.title('Histogram of U.S. Cities by Population')
        plt.show()
    elif input == 2:
        df.hist(column = 'Size in Square Miles')
        plt.title('Histogram of U.S. Cities by Size in Square Miles')
        plt.show()
    elif input == 3 :
        df.hist(column = 'Population Density (People per Square Mile)')
        plt.title('Histogram of U.S. Cities by Population per Square Mile')
        plt.show()
    else:
        print('Please input 1, 2, or 3 to show the distribution of either population, size or population density')
        time.sleep(1)


def get_min_max(city_data):
    ''' Takes in a map data and gives the maximum of each set of coordinates to set the grid making

    Parameters
    ----------
    Map data dictionary
    
    Returns
    -------
    Minimum and maximum X, Y for the map to be made
    '''
    latitudes = []
    longitudes = []

    for x in city_data['Coordinates']:
        for coords in x:
            #print(coords[0])
            latitudes.append(coords[0])
            longitudes.append(coords[1])

    minmax = []

    latmin = min(latitudes)
    latmax = max(latitudes)
    lonmin = min(longitudes)
    lonmax = max(longitudes)

    minmax.append(latmin)
    minmax.append(latmax)
    minmax.append(lonmin)
    minmax.append(lonmax)
    #print(minmax)
    return(minmax)


def make_grid(city_data, boundaries, city):
    ''' Takes in a dictionary, the limits of the map, and the city name and puts out a coordinate
    for each district of the redlined data

    Parameters
    ----------
    map data dictionary, boundaries for map, city name
    
    Returns
    -------
    coordinate for each district
    '''
    cache = open_cache('grid.json')
    #print(cache)

    if city in cache:
        print('Using cache')
        return(cache[city])

    else:
        xmin = boundaries[0]
        xmax = boundaries[1]
        ymin = boundaries[-2]
        ymax = boundaries[-1]

        xgrid = np.arange(xmin,xmax,.0001)
        ygrid = np.arange(ymin,ymax, .0001)


        census_points = []
        xmesh, ymesh = np.meshgrid(xgrid,ygrid)
        points = np.vstack((xmesh.flatten(),ymesh.flatten())).T
        range_ = len(city_data['Holc_Grade'])

        random.seed(33)
        for x in range(range_):
            p = Path(city_data['Coordinates'][x])
            grid = p.contains_points(points)
            #print([random.choice(np.where(grid)[0])])
            census_points.append(points[random.choice(np.where(grid)[0])])
            print(f'Making district coordinates step {x+1}(This step will likely take a while, particularly if the city has a large area)')

        census = []

        a = 1
        for i in range(range_):
            new_info = requests.get('https://geo.fcc.gov/api/census/area?lat='+(str(census_points[i][1]))+'&lon='+(str(census_points[i][0]))+'&format=json')
            census.append(new_info.json())
            print(f'Pulling census district coordinates step {a}')
            a+=1

        y = []
        for i in range(range_):
            a = census[i]['results'][0]['block_fips']
            b = a[2:11]
            y.append(b)

        state = census[i]['results'][0]['block_fips'][:2]

        y.append(state)
        #print(y[-1])
        cache[city] = y
        #print(cache)
        save_cache('grid.json', cache)
        return(cache[city])


def make_income_map(city_data, grid, city):
    ''' Takes in a dictionary the coordinates for the polygons and the city name and makes
    a map of income according to those polygons

    Parameters
    ----------
    dictionary of map data, list of coordinates, city name

    Returns
    -------
    None

    '''  
    y = grid

    cache = open_cache('income.json')

    if city in cache:
        print('Using cache')
        wage_info = cache[city]

    else:
        print('Fetching census Data')
        tract_info = requests.get(f'https://api.census.gov/data/2015/acs/acs5?get=NAME,B19013_001E&for=tract:*&in=state:{y[-1]}&key={CENSUS_KEY}')
        info = tract_info.json()
        cache[city] = info
        save_cache('income.json', cache)
        wage_info = cache[city]

    #print(wage_info)

    med_inc = []

    y.pop()
    #print(y)

    for x in y:
        #print(x)
        #print(x[3:])
        for inc in wage_info:
            #print(inc[-2])
            if x[:3] == inc[-2] and x[3:] == inc[-1]:
                med_inc.append(int(inc[-4]))

    #print(med_inc)


    Q1 = np.percentile(med_inc, 25, interpolation='midpoint')
    Q2 = np.percentile(med_inc, 50, interpolation='midpoint')
    Q3 = np.percentile(med_inc, 75, interpolation='midpoint')

    ordered_inc_col = []

    for inc in med_inc:
        if inc <= Q1:
            ordered_inc_col.append('mintcream')
        elif inc > Q1 and inc <= Q2:
            ordered_inc_col.append('lightgreen')
        elif inc > Q2 and inc <= Q3:
            ordered_inc_col.append('forestgreen')
        else:
            ordered_inc_col.append('seagreen')
    
    polygons = []
    range_ = len(y)
    
    for i in range(range_):
        polygons.append(Polygon(city_data['Coordinates'][i], ec=city_data['Holc_Color'][i], fc=ordered_inc_col[i]))

    fig, ax = plt.subplots()

    for u in polygons:
        ax.add_patch(u)

    ax.autoscale(enable=True)
    #plt.rcParams["figure.figsize"] = (15,15)
    plt.title(label=f'Effect of Redlining on wages Map')
    plt.show()


def make_travel_time_to_work_map(city_data, grid, city):
    ''' Takes in a dictionary the coordinates for the polygons and the city name and makes
    a map of travel time to work according to those polygons
    
    Parameters
    ----------
    dictionary of map data, list of coordinates, city name
    
    Returns
    -------
    None

    '''    
    y = grid
    
    cache = open_cache('travel.json')

    #print(y)
    if city in cache:
        print('Using cache')
        travel_info = cache[city]
    
    else:
        print('Fetching census Data')
        tract_info = requests.get(f'https://api.census.gov/data/2015/acs/acs5?get=NAME,B08303_001E&for=tract:*&in=state:{y[-1]}&key={CENSUS_KEY}')
        #print(tract_info)
        info = tract_info.json()
        cache[city] = info
        save_cache('travel.json', cache)
        travel_info = cache[city]

    #print(wage_info)

    med_inc = []

    y.pop()

    for x in y:
        for inc in travel_info:
            if x[:3] == inc[-2] and x[3:] == inc[-1]:
                med_inc.append(int(inc[-4]))

    Q1 = np.percentile(med_inc, 25, interpolation='midpoint')
    Q2 = np.percentile(med_inc, 50, interpolation='midpoint')
    Q3 = np.percentile(med_inc, 75, interpolation='midpoint')

    ordered_inc_col = []

    for inc in med_inc:
        if inc <= Q1:
            ordered_inc_col.append('seashell')
        elif inc > Q1 and inc <= Q2:
            ordered_inc_col.append('salmon')
        elif inc > Q2 and inc <= Q3:
            ordered_inc_col.append('orangered')
        else:
            ordered_inc_col.append('darkred')
    
    polygons = []
    range_ = len(y)
    
    for i in range(range_):
        polygons.append(Polygon(city_data['Coordinates'][i], ec=city_data['Holc_Color'][i], fc=ordered_inc_col[i]))

    fig, ax = plt.subplots()

    for u in polygons:
        ax.add_patch(u)

    ax.autoscale(enable=True)

    plt.title(label=f'Comparison of historic Redlining to currenton Travel Time to Work Map')
    plt.show()


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


def main():
    city_dict = build_city_dict()
    print('Please select from the following choices or print "exit" to leave:')
    print('1. Aggregate Largest U.S. Cities Data')
    print('2. Individual City Data')
    input1 = input(':').lower()
    if input1 == 'exit':
        print('Bye!')
    else:
        while True:
            try:
                if input1 == '1':
                    df = dict_to_pd_df(city_dict)
                    print('Please select from the following choices or enter "back" to return to the initial level of the program')
                    print('1. Summary statistics for 100 largest cities by population in the United States')
                    print('2. Histograms of 100 largest cities in the United States by population, size, and population density')
                    input2 = input(':').lower()
                    try:
                        if input2=='exit':
                            print('Bye!')
                            break
                        elif input2 =='back':
                            time.sleep(1)
                            print('')
                            print('Please select from the following choices or print "exit" to leave:')
                            print('1. Aggregate Largest U.S. Cities Data')
                            print('2. Individual City Data')
                            input1 = input(':').lower()
                            continue
                        elif input2=='1':
                            summary_stats(df)
                            time.sleep(1)
                            print('')
                            continue
                        elif input2=='2':
                            histo(df, 1)
                            histo(df, 2)
                            histo(df, 3)
                            time.sleep(1)
                            print('')
                        else:
                            print('Error invalid input, please enter 1, 2, exit or back')
                            time.sleep(1)
                            print('')
                            continue
                    except:
                        pass
                elif input1 == '2':
                    city_p = crawl_city_info(city_dict)
                    i = 0
                    j = 0
                    print('Please select the city you would like to see data on:')
                    for x in city_dict['name']:
                        i+=1
                        print(f'{i}. {x}, {city_dict["state"][j]}')
                        j+=1
                    input2a = input(':').lower()
                    try:
                        if input2a=='exit':
                            print('Bye!')
                            break
                        elif input2a =='back':
                            time.sleep(1)
                            print('')
                            print('Please select from the following choices or print "exit" to leave:')
                            print('1. Aggregate Largest U.S. Cities Data')
                            print('2. Individual City Data')
                            input1 = input(':').lower()
                        elif input2a == '1':
                            print(city_p[0])
                            print('')
                            print('New York is a special case as the five boroughs are basically cities unto themselves.')
                            print('Please select from the list of NYC borroughs to see NYC data by borrough')
                            print('1. Bronx')
                            print('2. Brooklyn')
                            print('3. Manhattan')
                            print('4. Queens')
                            print('5. Staten Island')
                            bor = ['Bronx', 'Brooklyn', 'Manhattan', 'Queens', 'StatenIsland']
                            input3b = input(':').lower()
                            x = int(input3b)-1
                            try:
                                while True:
                                    city_redline_map_data = get_redline_map(bor[x], 'NY')
                                    map_data = make_redline_map(city_redline_map_data, bor[x])
                                    boundaries = get_min_max(map_data)
                                    grid = make_grid(map_data, boundaries, bor[x])
                                    print('Pease select from the following options as to what visualization you would like to generate')
                                    print('1. Income data for redlined districts')
                                    print('2. Commute time for redlined districts')
                                    input3a = input(':').lower()
                                    while True:
                                        try:
                                            if input3a =='exit':
                                                print('Bye!')
                                                break
                                            elif input3a =='back':
                                                print('Pease select from the following options as to what visualization you would like to generate')
                                                print('1. Income data for redlined districts')
                                                print('2. Commute time for redlined districts')
                                                input3a = input(':').lower()
                                            elif input3a == '1':
                                                print('In this visualization income is split into quartiles where lighter green is the lowest income quartile and dark green is the top income quartile. Additionally, the edge colors for the polygons correspond to the historic redlining code that was used on that district')
                                                make_income_map(map_data, grid, bor[x])
                                                print('Pease select from the following options as to what visualization you would like to generate')
                                                print('1. Income data for redlined districts')
                                                print('2. Commute time for redlined districts')
                                                input3a = input(':').lower()
                                            elif input3a == '2':
                                                print('In this visualization travel time to work is split into quartiles where lighter red corresponds to shorter commutes and darker red corresponds to longer commutes. Additionally, the edge colors for the polygons correspond to the historic redlining code that was used on that district')
                                                make_travel_time_to_work_map(map_data, grid, bor[x])
                                                print('Pease select from the following options as to what visualization you would like to generate')
                                                print('1. Income data for redlined districts')
                                                print('2. Commute time for redlined districts')
                                                input3a = input(':').lower()
                                            else:
                                                print('Error invalid input, please enter 1, 2, exit or back')
                                                time.sleep(1)
                                                print('')
                                                print('Pease select from the following options as to what visualization you would like to generate')
                                                print('1. Income data for redlined districts')
                                                print('2. Commute time for redlined districts')
                                                input3a = input(':').lower()
                                        except KeyError:
                                            print('Invalid input, please enter a 1 or 2, exit or back')
                                            continue
                            except KeyError:
                                print('Invalid input, please enter a digit between 1 and 5, exit or back')
                                continue
                        elif int(input2a) in range(2, 101):
                            x = int(input2a) -1
                            print(city_p[x])
                            print('')
                            print('The redline map for this city will appear in an external window that needs to be closed in order to continue the program')
                            try:
                                city_redline_map_data = get_redline_map(city_dict['name'][x], city_dict['abbr'][x])
                                map_data = make_redline_map(city_redline_map_data, city_dict['name'][x])
                                boundaries = get_min_max(map_data)
                                grid = make_grid(map_data, boundaries, city_dict['name'][x])
                                print('Pease select from the following options as to what visualization you would like to generate')
                                print('1. Income data for redlined districts')
                                print('2. Commute time for redlined districts')
                                while True:
                                    try:
                                        input3a = input(':').lower()
                                        if input3a =='exit':
                                            print('Bye!')
                                            break
                                        elif input3a =='back':
                                            print('Please select the city you would like to see data on:')
                                            for x in city_dict['name']:
                                                i+=1
                                                print(f'{i}. {x}, {city_dict["state"][j]}')
                                                j+=1
                                            input2a = input(':').lower()
                                        elif input3a == '1':
                                            print('In this visualization income is split into quartiles where lighter green is the lowest income quartile and dark green is the top income quartile. Additionally, the edge colors for the polygons correspond to the historic redlining code that was used on that district')
                                            make_income_map(map_data, grid, city_dict['name'][x])
                                            print('Pease select from the following options as to what visualization you would like to generate')
                                            print('1. Income data for redlined districts')
                                            print('2. Commute time for redlined districts')
                                            #input3a = input(':').lower()
                                            #if input3a =='1':
                                                # try:
                                                #     make_travel_time_to_work_map(map_data, grid, city_dict['name'][x])
                                                # except TypeError:
                                                #     print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
                                        elif input3a == '2':
                                            print('In this visualization travel time to work is split into quartiles where lighter red corresponds to shorter commutes and darker red corresponds to longer commutes. Additionally, the edge colors for the polygons correspond to the historic redlining code that was used on that district')
                                            make_travel_time_to_work_map(map_data, grid, city_dict['name'][x])
                                            print('Pease select from the following options as to what visualization you would like to generate')
                                            print('1. Income data for redlined districts')
                                            print('2. Commute time for redlined districts')
                                            #input3a = input(':').lower()
                                        else:
                                            print('Error invalid input, please enter 1, 2, exit or back')
                                            time.sleep(1)
                                            print('')
                                            print('Pease select from the following options as to what visualization you would like to generate')
                                            print('1. Income data for redlined districts')
                                            print('2. Commute time for redlined districts')
                                            input3a = input(':').lower()
                                    except KeyError:
                                        pass
                            except KeyError:
                                print('Apologies but your selection does not appear to have redline data. Please make a new selection')
                                print('')
                                print('')
                                print('')
                                time.sleep(4)
                                continue
                            except TypeError:
                                print('Apologies but your selection does not appear to have redline data. Please make a new selection')
                                print('')
                                print('')
                                print('')
                                time.sleep(4)
                                continue
                    except:
                        pass
                else:
                    print('Error invalid input')
                    time.sleep(1)
                    print('')
                    print('Please select from the following choices or print "exit" to leave:')
                    print('1. Aggregate Largest U.S. Cities Data')
                    print('2. Individual City Data')
                    input1 = input(':').lower()
                    continue
            except:
                pass


if __name__ == "__main__":
    main()