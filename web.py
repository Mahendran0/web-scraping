import requests, openpyxl
from bs4 import BeautifulSoup

excel = openpyxl.Workbook()
sheet = excel.active
sheet.title = "Movie List"
sheet.append(['Rank', 'Movie Name', 'Release Year', 'Rating'])

try:
    response = requests.get("https://www.imdb.com/india/top-rated-tamil-movies/")
    soup = BeautifulSoup(response.text, 'html.parser')
    # print(soup)
    movies = soup.find('tbody', class_='lister-list').find_all('tr')
    # print(movies)

    for movie in movies:
        # print(movies)
        rank = movie.find('td', class_='titleColumn').get_text(strip=True).split('.')[0]
        movie_name = movie.find('td', class_='titleColumn').a.text
        year = movie.find('td', class_='titleColumn').span.text.replace(')', "")
        year = year.replace('(', "")
        rate = movie.find('td', class_='ratingColumn').strong.text
        # print(rank, movie_name, year, rate)
        sheet.append([rank, movie_name, year, rate])


except Exception as e:
    print(e)
excel.save("movie.xlsx")
