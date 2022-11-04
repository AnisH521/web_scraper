# Import Necessary Libraries
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
from typing import List, Dict

def movie_scraper(movie: str) -> Dict:

    '''
    creates a dictionary movie_content.

    finds information of a movies such as name, release year etc and stores it in movie_content.

    Returns movie_content contains information about a single movie.
    '''

    movie_content = {}

    movie_content['movie_name'] = movie.find('a').get_text()
    
    try:
        movie_content['movie_release_year'] = movie.find('span', class_ = 'lister-item-year text-muted unbold').contents[0][1:5]
    except:
        movie_content['movie_release_year'] = None
        
    try:
        movie_content['movie_runtime'] = movie.find('span', class_ = 'runtime').contents[0][0:3]
    except:
        movie_content['movie_runtime'] = None
        
    try:
        movie_content['movie_genre'] = movie.find('span', class_ = 'genre').contents[0].strip()
    except:
        movie_content['movie_genre'] = None

    try:
        imdb_rate_block = movie.find('div', class_ = "inline-block ratings-imdb-rating")
        for rate in imdb_rate_block.find('strong'):
            movie_content['imdb_rate'] = rate
    except:
        movie_content['imdb_rate'] = None

    try:
        movie_content['movie_meta_score'] = movie.find_all('div', class_ = "inline-block ratings-metascore")[0].get_text().split()[0]
    except:
        movie_content['movie_meta_score'] = None
        
    try:
        for item in movie.find_all('p', class_="sort-num_votes-visible"):
            movie_content['movie_gross_val'] = item.find_all('span', {'name':'nv'})[1].get_text()
    except:
        movie_content['movie_gross_val'] = None
        
    try:
        movie_content['movie_votes'] = movie.find('span', {'name':'nv'}).get('data-value')
    except:
        movie_content['movie_votes'] = None
    
    return movie_content


def page_scraper(link: str) -> List:

    '''
    scraps an entire page.

    creates a list named movies_list.

    stores information of the movie within movies_list.

    each movie's information is a dictionary type object returned by movie_scraper.

    returns movies_list.
    '''

    movies_list = []
    
    headers = {'Accept-Language': 'en-US,en;q=0.5'} 
    source = requests.get(link, headers = headers).text
    soup = BeautifulSoup(source,'lxml')
    
    for movie in soup.find_all('div', class_ = 'lister-item-content'):
        movies_list.append(movie_scraper(movie))
    
    return movies_list 


def full_scraper(link: str, final_movie_index: int) -> List:

    '''
    scrap movies from IMDB's website upto a certain index starting from page 1.

    receives url of the page to start scraping.

    receives last movie's index upto which user wants to scrap.

    returns a list of dictionaries contains information about movies.
    '''
    
    source = requests.get(link).text
    soup = BeautifulSoup(source,'lxml')
    
    initial_url = link
    initial_movie_index = int(soup.find("div", {"class":"nav"})
                              .find("div", {"class": "desc"})
                              .contents[1]
                              .get_text()
                              .split("-")[0])
    
    current_movie_index = initial_movie_index
                       
    m_list = []
    
    while current_movie_index < final_movie_index:
        
        current_url = initial_url + str(current_movie_index)
    
        m_list.extend(page_scraper(current_url))
        
        current_movie_index += 50
        
        time.sleep(20)
        
    return m_list  

# main function
def main() -> None:
    
    url = 'https://www.imdb.com/search/title/?title_type=feature&num_votes=25000,&genres=comedy&start='
    number_of_movies = 100
    
    movies_list = full_scraper(url, number_of_movies)
    df = pd.DataFrame(movies_list)
    df.to_csv('movies.csv', index = False)

# uses special variable
if __name__ == "__main__":
    main() 
