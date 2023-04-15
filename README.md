# Imdb-Hollywood-Movies-Scrapper
This is a project that aims to Scrape Hollywood movies data for data analysis.

🚀 Features
🌐 Internet access for searches and information gathering
🔗 Access to popular websites and platforms
💾 Saves in CSV or JSON


📋 Requirements
environments : Python 3.8 or later

💾 Installation
Make sure you have all the requirements above, if not, install/get them.
Clone the repository: For this step you need Git installed, but you can just download the zip file instead by clicking the button at the top of this page ☝️
Navigate to the project directory: (Type this into your CMD window, you're aiming to navigate the CMD window to the repository you just downloaded)
Install the required dependencies: (Again, type this into your CMD window) : pip install -r requirements.txt

🔧 Usage
Run the movie_scrapper Python module in your terminal: (Type this into your CMD window)

python movie_scrapper.py

Passing Arguments:
  python movie_scrapper.py y2021 nfile_name m200 csv s
  
  To set Year of scapping, append y and year with no spaces e.g. y2023
  To set output filename append n and filename with no spaces e.g. nNew_File
  To set your desired number of movies append m and number of movies with no spaces e.g. m1000
  To set file format append either csv or json
  To set search mode append either s or m
    NB: s for single mode, data is saved to file as soon as received
        m for multiple mode, all scraped data is first accumulated before saved to file 
        
       
       
Run the movie_scrapper Python module in IDE Environment: (Type this into your IDE)
movie_scrapper = ImdbMoviesScrapper(num_of_movies=<YOUR DESIRED NUMBER OF MOVIES e.g 1000>, year=<DESIRED YEAR e.g. 2023>)

for CSV
movie_scrapper.to_csv(mode) 

for JSON
movie_scrapper.to_json(mode)
NB: mode = "single" for single mode, data is saved to file as soon as received
    mode = "multiple" for multiple mode, all scraped data is first accumulated before saved to file
    
