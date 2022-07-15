import requests, openpyxl
from bs4 import BeautifulSoup
import pandas as pd
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="movie",
)
cursor = mydb.cursor()


def web_scrap():
    excel = openpyxl.Workbook()
    sheet = excel.active
    sheet.title = "Movie List"
    sheet.append(['Rank', 'Movie Name', 'Release Year', 'Rating'])

    df = pd.read_excel('movies.xlsx')
    print(df)

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

    except Exception as e:
        print(e)
    excel.save("movies.xlsx")


def excel_db(file):
    try:
        wb = openpyxl.load_workbook(file)
        ws = wb.active
        sh1 = wb['Movie List']
        ro = sh1.max_row
        print(ro)

        data = []
        for row in ws.iter_rows(min_row=2, max_row=ro, values_only=True):
            data.append(row)
        print(data)
        sql = "INSERT INTO `movie_tittle` (rank, movie_name, release_year, rating) " \
              "VALUES(%s, %s, %s, %s)"

        cursor.executemany(sql, data)
        mydb.commit()
        print("Successfully Imported")

        mydb.close()
    except Exception as e:
        print(e)


file_path = "movie.xlsx"
excel_db(file_path)
