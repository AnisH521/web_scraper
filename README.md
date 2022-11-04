# web_scraper
A web scraper tool which uses BeautifulSoup

## Setup
To run this project, install these python library and toolkit:

```
$ pip install BeautifulSoup4
$ pip install lxml
```

## Instruction to use
* open your browser and goto IMDB's website and search movies by genre
* at page 1 setup view mode = Detailed and copy the url 
* then open your code editor and inside main function setup the url object from page 1
* url must be string and must end with '&start='
* after that setup number_of_movies object within same function with the number of movies information you want to extract
* then run the code and you will get desired number of movies information starting from page 1
* NOTE1 : you must start from first movie indexed '1.' on IMDB's website
* NOTE2 : if at page 1 url doesn't end with '&start=' then goto next page and come back to previous page i.e. page 1 and you will get required url
