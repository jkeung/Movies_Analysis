from sys import argv
import datetime as dt
import requests
from bs4 import BeautifulSoup
import dateutil.parser as parse
import urlparse
import os
import pickle
import re
import time

OUTPUTDIR = 'output'
FILENAMETEMPLATE = 'movie_dictionary'

def create_dir(directory):
    #Check to see if directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_soup_from_url(url):
    '''
    Takes url and returns bs4.BeautifulSoup class. If the soup already exists
    locally, it will load from file, otherwise it will pull from a url. It will
    also create a directory structure (in the current working directory) based on the url.
    
    Ex: 'http://www.boxofficemojo.com/movies/?id=ateam.htm'
        Creates: /data/www.boxofficemojo.com/movies/ateam.htm
    
    Args:
        url (string)
    Returns:
        soup (bs4.BeautifulSoup): 
    '''
    
    parsed_url = urlparse.urlparse(url)
    path = []
    for item in parsed_url:
        for x in item.split():
            path.append(x.replace('/', ''))
    outfile = path[-1]
    outfile = outfile[outfile.find('=') + 1:]
    outpath = 'data/' + '/'.join(path[1:-1])
    out_pathfile = os.path.join(outpath, outfile)

    #Check to see if directory exists
    create_dir(outpath)

    #Check to see if file exists
    try:
        soup = pickle.load(open('{}'.format(out_pathfile), 'rb'))
    except:
        #If doesn't exist, try to get soup from page
        try:
            soup = BeautifulSoup(requests.get(url).text, 'lxml')
            pickle.dump(soup, open('{}'.format(out_pathfile), 'wb'))
        except:
            pass

    return soup

def get_title(soup):
    
    '''
    Function to get movie title from the Box Office Mojo individual movie site's soup.
    
    Args:
        soup (BeautifulSoup): The beautiful soup that is obtained from requests.get(url)
    Returns: 
        title (string): A string of the title of the movie
    
    '''
    try:
        index = soup.title.text.find(' - Box Office Mojo')
        title = str(soup.title.text[:index])
        return title
    except:
        return 'N/A'


def get_domestic_gross(soup):
    
    '''
    Function to get total domestic gross from the Box Office Mojo individual movie site's soup.
    
    Args:
        soup (BeautifulSoup): The beautiful soup that is obtained from requests.get(url)
    Returns: 
        number (float): A float of the domestic gross of the movie
    
    '''  
    try:
        number = soup.find_all(text='Domestic:')[0].parent.parent.parent.td.next_sibling.next_sibling.b.text
        number = float(number.replace(',','').replace('$',''))
        return number
    except:
        return 'N/A'

def get_distributor(soup):
    
    '''
    Function to get total domestic gross from the Box Office Mojo individual movie site's soup.
    
    Args:
        soup (BeautifulSoup): The beautiful soup that is obtained from requests.get(url)
    Returns: 
        word (string): The distributor of the movie
    
    '''  
    try:
        word = soup.find(text = 'Distributor: ').next_sibling.text
        return str(word)
    except:
        return 'N/A'

def get_genre(soup):
    
    '''
    Function to get genre from the Box Office Mojo individual movie site's soup.
    
    Args:
        soup (BeautifulSoup): The beautiful soup that is obtained from requests.get(url)
    Returns: 
        genre (string): The genre of the movie
    
    '''  
    try:
        genre = str(soup.find(text = 'Genre: ').next_sibling.text)
        return genre
    except:
        return 'N/A'

def get_runtime(soup):
    
    '''
    Function to get total movie time in minutes from the Box Office Mojo individual movie site's soup.
    
    Args:
        soup (BeautifulSoup): The beautiful soup that is obtained from requests.get(url)
    Returns: 
        runtime (int): The runtime of the movie
    
    '''  
    try:
        time = soup.find(text = 'Runtime: ').next_sibling.text
        if time.find('hrs.') > 0 and time.find('min.') > 0:
            hours = int(time[:time.find('hrs.')])
            minutes = int(time[time.find('min.') - 3:time.find('min.')])
            runtime = (hours*60) + minutes
            return runtime
        else:
            return None
    except:
        return 'N/A'

def get_rating(soup):
    
    '''
    Function to get MPAA rating from the Box Office Mojo individual movie site's soup.
    
    Args:
        soup (BeautifulSoup): The beautiful soup that is obtained from requests.get(url)
    Returns: 
        rating (string): The rating of the movie
    
    '''  
    try:
        rating = str(soup.find(text = 'MPAA Rating: ').next_sibling.text)
        return rating
    except:
        return 'N/A'

def get_budget(soup):
    
    '''
    Function to get production budget (in millions)from the Box Office Mojo individual 
    movie site's soup.
    
    Args:
        soup (BeautifulSoup): The beautiful soup that is obtained from requests.get(url)
    Returns: 
        budget (string): The production budget of the movie
    
    '''  
    try:
        budget = str(soup.find(text = 'Production Budget: ').next_sibling.text)
        budget = int(budget[1:budget.find('million')])
        return budget
    except:
        return 'N/A'

def get_release_date(soup):
    
    '''
    Function to get release date from the Box Office Mojo individual movie site's soup.
    
    Args:
        soup (BeautifulSoup): The beautiful soup that is obtained from requests.get(url)
    Returns: 
        date (date): The release date of the movie
    
    ''' 
    try:
        date = soup.find(text = 'Release Date: ').next_sibling.text
        date = parse.parse(date, fuzzy = True).date()
        return date
    except:
        return 'N/A'


def get_directors(soup):
    
    '''
    Function to get directors from the Box Office Mojo individual movie site's soup.
    
    Args:
        soup (BeautifulSoup): The beautiful soup that is obtained from requests.get(url)
    Returns: 
        list: A list of director(s) of the movie
    
    '''
    fieldlist = []
    try:
        for x in soup.find_all(text='Director:')[0].parent.parent.parent.nextSibling.font:
            word = str(x.string)
            if word[0].isupper() and word != 'None':
                fieldlist.append(word)
        return fieldlist
    except:
        return 'N/A'

def get_writers(soup):
    
    '''
    Function to get writers from the Box Office Mojo individual movie site's soup.
    
    Args:
        soup (BeautifulSoup): The beautiful soup that is obtained from requests.get(url)
    Returns: 
        list: A list of writer(s) of the movie
    
    '''
    fieldlist = []
    try:
        for x in soup.find_all(text='Writers:')[0].parent.parent.parent.nextSibling.font:
            word = str(x.string)
            if word[0].isupper() and word != 'None':
                fieldlist.append(word)
        return fieldlist
    except:
        return 'N/A'

def get_actors(soup):
    
    '''
    Function to get actors from the Box Office Mojo individual movie site's soup.
    
    Args:
        soup (BeautifulSoup): The beautiful soup that is obtained from requests.get(url)
    Returns: 
        list: A list of actor(s) in the movie
    
    '''
    fieldlist = []
    try:
        for x in soup.find_all(text='Actors:')[0].parent.parent.parent.nextSibling.font:
            word = str(x.string)
            if word[0].isupper() and word != 'None':
                fieldlist.append(word)
        return fieldlist
    except:
        return 'N/A'

def get_producers(soup):
    
    '''
    Function to get producers from the Box Office Mojo individual movie site's soup.
    
    Args:
        soup (BeautifulSoup): The beautiful soup that is obtained from requests.get(url)
    Returns: 
        list: A list of producer(s) of the movie
    
    '''
    fieldlist = []
    try:
        for x in soup.find_all(text='Producers:')[0].parent.parent.parent.nextSibling.font:
            word = str(x.string)
            if word[0].isupper() and word != 'None':
                fieldlist.append(word)
        return fieldlist
    except:
        return 'N/A'

def get_composers(soup):
    
    '''
    Function to get composers from the Box Office Mojo individual movie site's soup.
    
    Args:
        soup (BeautifulSoup): The beautiful soup that is obtained from requests.get(url)
    Returns: 
        list: A list of writer(s) of the movie
    
    '''
    fieldlist = []
    try:
        for x in soup.find_all(text='Domestic Total Gross: ')[0].parent.parent.parent.nextSibling.font:
            word = str(x.string)
            if word[0].isupper() and word != 'None':
                fieldlist.append(word)
        return fieldlist
    except:
        return 'N/A'

def get_movie_dictionary(url, d = {}):  

    '''
    Function to create or append to a dictionary from the Box Office Mojo individual movie page.

    Args:
        url (string): The url of the Box Office Mojo individual movie page
        Ex: 'http://www.boxofficemojo.com/movies/?id=ateam.htm'
    Returns: 
        d (dictionary): A dictionary of the movie

    '''
    #Get soup from url locally or from Box Office Mojo directly
    soup = get_soup_from_url(url)
    
    #Get movie information
    title = get_title(soup)
    genre = get_genre(soup)
    gross = get_domestic_gross(soup)
    release_date = get_release_date(soup)
    runtime = get_runtime(soup)
    budget = get_budget(soup)
    rating = get_rating(soup)
    distributor = get_distributor(soup)
    directors = get_directors(soup)
    actors = get_actors(soup)
    writers = get_writers(soup)
    producers = get_producers(soup)
    
    #Update dictionary
    d.setdefault(title, {}).update({'genre':genre})
    d.setdefault(title, {}).update({'gross':gross})
    d.setdefault(title, {}).update({'date':release_date})
    d.setdefault(title, {}).update({'runtime':runtime})
    d.setdefault(title, {}).update({'budget':budget})
    d.setdefault(title, {}).update({'rating':rating})
    d.setdefault(title, {}).update({'distributor':distributor})
    d.setdefault(title, {}).update({'directors':directors})
    d.setdefault(title, {}).update({'actors':actors})
    d.setdefault(title, {}).update({'writers':writers})
    d.setdefault(title, {}).update({'producers':producers})
    
    return d

def get_movie_url_list(letter):

    '''
    Function to get a list of urls of all movies that begin with a particular letter from the 
    Box Office Mojo individual movie page.

    Args:
        letter (string): The letter to pull for movies on the Box Office Mojo A-Z listing page.
        Ex: 'http://www.boxofficemojo.com/movies/alphabetical.htm?letter={letter}&p=.htm'
    Returns: 
        url_list2 (list): A list of urls for movies that start with letter.

    '''

    #Create a dictionary for the number of sublinks per letter
    link_dict = {'#':1, 'A':10, 'B':8, 'C':7, 'D':6, 'E':7, 'F':6, 'G':7, 'H':6, 'I':6,       \
                'J':4, 'K':4, 'L':5, 'M':6, 'N':5, 'O':5, 'P':7, 'Q':1, 'R':6, 'S':13, 'T':8, \
                'U':2, 'V':3, 'W':6, 'X':1, 'Y':2, 'Z':2}
    
    base = 'http://www.boxofficemojo.com/'

    url_list1 = ['http://www.boxofficemojo.com/movies/alphabetical.htm?letter={0}&page={1}&p=.htm'.format(letter, num) \
                for num in range(1, link_dict[letter] + 1) ]
    url_list2 = []

    for url_1 in url_list1:
        soupin = BeautifulSoup(requests.get(url_1).text, 'lxml')
        movie_list_table = soupin.find(text = 'ALPHABETICAL INDEX').parent.parent.parent.parent.parent.parent
        movie_list = movie_list_table.find_all('a', href=re.compile('^/movies/\?id='))
        for movie in movie_list:
            url_list2.append(base + movie['href'])

    return url_list2

def update_movie_dictionary(file, url_list):

    '''
    Function to create/load a dictionary if exists and update with movie information.

    Args:
        letter (string): The letter to pull for movies on the Box Office Mojo A-Z listing page.
        url_list (list): A list of urls for individual moviepages on the Box Office Mojo

    Returns: 
        url_list2 (list): A list of urls for movies that start with letter.

    '''

    try:
        d = pickle.load(open('{}'.format(file), 'rb'))
    except:
        d = {}

    for url in url_list:
        d.update(get_movie_dictionary(url, d))
        pickle.dump(d, open('{}'.format(file), 'wb'))



def main():

    script, letter = argv
    start_time = time.time()

    create_dir(OUTPUTDIR)

    url_list = get_movie_url_list(letter)
    output_path = os.path.join(OUTPUTDIR, '{0}_{1}.p'.format(FILENAMETEMPLATE, letter))
    update_movie_dictionary(output_path, url_list)

    print ("--- %s seconds ---\n") % (time.time() - start_time)
    print ("Dictionary created successfully!")

if __name__ == '__main__':
    main()