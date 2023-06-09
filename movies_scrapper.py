import requests
from bs4 import BeautifulSoup as bs
import csv, json
import sys, time

## NUMBER OF MOVIES = m<<NUMBER OF MOVIES>>
## YEAR = y<<YEAR>>
## FILE NAME = n<<FILENAME>>
## FILE TYPE = csv OR json

""" SET INITIAL CONFIGURATION """
conf = {
    "MODE":"MULTIPLE",
    "NUMBER OF MOVIES":100,
    "STANDARD_MOVIES_PER_PAGE":50,
    "PER_PAGE_LIST":[],
    "MOVIE_LINK":"https://www.imdb.com/search/title/?release_date=2022-01-01,2022-12-31&sort=boxoffice_gross_us,desc&start=",
    "MOVIES":[],
    "OUT_FILE_EXISTS":False,
    "ARGS_LIST":[],
    "FILE_NAME":"hollywood_movie",
    "FILE_TYPE":"CSV",
    "YEAR":"2022",
}


class ImdbMoviesScrapper:
    
    def __init__(self, num_of_movies=None, year=None):
        if len(sys.argv) > 1:
            args_list = [a.replace("'", "").strip() for a in str(sys.argv).strip("[").strip("]").split(",")]
            conf["ARGS_LIST"].extend(args_list[1:])
            for arg in args_list[1:]:
                if arg.startswith("m"):
                    try:
                        conf["NUMBER OF MOVIES"] = int(arg.replace("m", ""))
                    except:
                        pass
                elif arg.startswith("n"):
                    conf["FILE_NAME"] = arg[1:]
                elif arg.startswith("y"):
                    try:
                        conf["YEAR"] = str(int(arg.replace("y", "")))
                    except:
                        pass
                elif arg == 'csv':
                    conf["FILE_TYPE"] = "CSV"
                elif arg == 'json':
                    conf["FILE_TYPE"] = "JSON"
                elif arg == 's':
                    conf['MODE'] = "SINGLE"
                elif arg == 'm':
                    conf['MODE'] = "MULTIPLE"

        if not num_of_movies:
            self.num_of_movies = conf["NUMBER OF MOVIES"]
        else:
            self.num_of_movies = num_of_movies
        
        if not year:
            self.year = conf["YEAR"]
        else:
            self.year = year

        count = 1
        while self.num_of_movies > 2:
            count = count + 1
            self.num_of_movies = self.num_of_movies - 50
            conf["PER_PAGE_LIST"].append(self.num_of_movies + 1)
            conf["PER_PAGE_LIST"] = sorted(conf["PER_PAGE_LIST"])


    def get_per_page(self):
        count = 1
        while self.num_of_movies > 2:
            count = count + 1
            self.num_of_movies = self.num_of_movies - 50
            conf["PER_PAGE_LIST"].append(self.num_of_movies + 1)
            conf["PER_PAGE_LIST"] = sorted(conf["PER_PAGE_LIST"])


    """ PAGE SCRAPPING """
    def movies_scrapper(self, movies_url):
        req = requests.get(movies_url).content
        res = bs(req, "html.parser")
        lister_list = res.find("div", {"class":"lister-list"})
        lister_items = lister_list.find_all("div", {"class":"lister-item"})
        movies_data = []
        for item in lister_items:
            movie = {}
            content = item.find("div", {"class":"lister-item-content"})
            movie['title'] = content.find("h3").find("a").text.strip()
            movie['link'] = f'https://www.imdb.com{content.find("h3").find("a").get("href").strip()}'

            try:
                movie['certificate'] = content.find("span", {"class":"certificate"}).text.strip()
            except:
                movie['certificate'] = "N/A"

            try:
                movie['runtime'] = content.find("span", {"class":"runtime"}).text.strip()
            except:
                movie['runtime'] = "N/A"
            
            try:
                movie['genre'] = content.find("span", {"class":"genre"}).text.strip().split(",")
            except:
                movie['genre'] = "N/A"
            
            
            ratings_bar = content.find("div", {"class":"ratings-bar"})

            try:
                movie['rating'] = ratings_bar.find("div", {"class":"ratings-imdb-rating"}).find("strong").text.strip()
            except:
                movie['rating'] = "N/A"

            try:
                movie['metascore'] = ratings_bar.find("div", {"class":"ratings-metascore"}).find("span", {"class":"metascore"}).text.strip()
            except:
                movie['metascore'] = "N/A"
            
            try:
                votes_gross = content.find("p", {"class":"sort-num_votes-visible"}).text.strip()
                if "|" in votes_gross:
                    movie['votes'] = votes_gross.split("|")[0].replace("Votes:", "").replace("," , "").strip()
                    try:
                        movie['gross'] = votes_gross.split("|")[1].replace("Gross:", "").replace(" \n", "")

                        if movie['gross'].startswith("$") and movie['gross'].endswith("M"):
                            g = movie['gross'].replace("$", "").replace("M", "")
                            movie['gross'] = float(g) * 1000000
                    except:
                        movie['gross'] = "N/A"
                else:
                    if votes_gross.startswith("Votes"):
                        movie['votes'] = votes_gross.replace("Votes:", "").replace("," , "").strip()
                        movie['gross'] = "N/A"
                    elif votes_gross.startswith("Gross"):
                        movie['votes'] = "N/A"
                        try:
                            movie['gross'] = votes_gross.replace("Gross:", "").replace(" \n", "")
                            if movie['gross'].startswith("$") and movie['gross'].endswith("M"):
                                g = movie['gross'].replace("$", "").replace("M", "")
                                movie['gross'] = float(g) * 1000000
                        except:
                            movie['gross'] = "N/A"
                    else:
                        movie['votes'] = "N/A"
                        movie['gross'] = "N/A"
            except:
                movie['votes'] = "N/A"
                movie['gross'] = "N/A"

            

            try:
                movie['storyline'] = ratings_bar.find_next_sibling('p').text.strip()
            except:
                movie['storyline'] = "N/A"

            try:
                cast = ratings_bar.find_next_sibling('p').find_next_sibling('p').text.strip()
            except:
                cast = ""
            
            if cast != "" and "|" in cast:
                movie['director'] = cast.split("|")[0].replace("Director:", "").strip().split(",")
            
                try:
                    movie['stars'] = [c.replace(" \n", "") for c in cast.split("|")[1].replace("Stars:", "").strip().split(",")]
                except:
                    movie['stars'] = "N/A"
            else:
                if cast.startswith("Director"):
                    movie['director'] = cast.replace("Director:", "").strip().split(",")
                elif cast.startswith("Stars:"):
                    movie['stars'] = [c.replace(" \n", "") for c in cast.replace("Stars:", "").strip().split(",")]
                    
            movies_data.append(movie)
        return movies_data
    
    
    """ CSV WRITER """
    def csv_writer(self, filename, data):
        if not conf["OUT_FILE_EXISTS"]:
            with open(filename, mode='w') as csv_file:
                self.fieldnames = []
                for k,v in data[0].items():
                    self.fieldnames.append(k)
                writer = csv.DictWriter(csv_file, fieldnames=self.fieldnames)
                writer.writeheader()
                for item in data:
                    writer.writerow(item)
            conf["OUT_FILE_EXISTS"] = True
        else:
            with open(filename, mode='a') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=self.fieldnames)
                writer.writeheader()
                for item in data:
                    writer.writerow(item)


    """ JSON WRITER """
    def json_writer(self, filename, data):
        if not conf["OUT_FILE_EXISTS"]:
            with open(f"{filename}.json", "w") as final:
                json.dump(data, final)
            conf["OUT_FILE_EXISTS"] = True
        else:
            with open(f"{filename}.json", "rw") as final:
                final_data = final.loads.extend(data)
                json.dump(final_data, final)



    """ GET SCRAPPED DATE INTO CSV FILE """
    def to_csv(self, mode=None):
        for page in conf["PER_PAGE_LIST"]:
            movies_url = f'{conf["MOVIE_LINK"]}{page}'.replace("2022", self.year)
            self.scraped_movies = self.movies_scrapper(movies_url=movies_url)
            conf["MOVIES"].extend(self.scraped_movies)

            self.filename=f'{conf["FILE_NAME"]}.csv'

            if not mode:
                mode = conf['MODE']
            if mode == "SINGLE":
                self.csv_writer(filename=self.filename, data=self.scraped_movies)
        if not mode:
            mode = conf['MODE']
        if mode.upper() == "MULTIPLE":
            self.csv_writer(filename=self.filename, data=conf["MOVIES"])

        print(f'Completed : {len(conf["MOVIES"])} Movies Scrapped to {self.filename}')


    """ GET SCRAPPED DATE INTO JSON FILE """
    def to_json(self, mode=None):
        for page in conf["PER_PAGE_LIST"]:
            movies_url = f'{conf["MOVIE_LINK"]}{page}'
            self.scraped_movies = self.movies_scrapper(movies_url=movies_url)
            conf["MOVIES"].extend(self.scraped_movies)
            
            self.filename=f'{conf["FILE_NAME"]}'

            if not mode:
                mode = conf['MODE']

            if mode.upper() == "SINGLE":
                self.json_writer(filename=self.filename, data=self.scraped_movies)

        if not mode:
            mode = conf['MODE']
        if mode.upper() == "MULTIPLE":
            self.json_writer(filename=self.filename, data=conf["MOVIES"])

        print(f'Completed : {len(conf["MOVIES"])} Movies Scrapped to {self.filename}.json')



x = ImdbMoviesScrapper()

if conf["FILE_TYPE"] == "CSV":
    x.to_csv()
else:
    x.to_json()
