'''
Created  by @deepanshubaghel
'''

from bs4 import BeautifulSoup
import requests
import pandas as pdc
import re
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

# setting the User-Agent header is important for web scraping to avoid detection and blocking by websites
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

url = 'https://www.imdb.com/chart/top/'
page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.content, "html.parser")

scraped_movies = soup.find_all('div', class_='ipc-title ipc-title--base ipc-title--title ipc-title-link-no-icon ipc-title--on-textPrimary sc-b0691f29-9 klOwFB cli-title')
movies = []
for movie in scraped_movies:
    movie = movie.get_text().replace('\n', "")
    movie = movie.strip(" ")
    movies.append(movie)

craped_ratings = soup.find_all('span', class_= 'sc-b0691f29-1 grHDBY')
ratings = []
for rating in scraped_ratings:
    rating = rating.get_text()[:3]
    ratings.append(rating)

scraped_voting = soup.find_all('span', class_= 'ipc-rating-star--voteCount')
votings = []
for voting in scraped_voting:
    voting = voting.get_text()[2:7:1].replace(')',"")
    voting = voting.replace('M','')
    voting = voting.replace('K','')
    votings.append(voting)

scraped_year = soup.find_all('span', class_= 'sc-b0691f29-8 ilsLEX cli-title-metadata-item')
years = []
for year in scraped_year:
    text = year.get_text()
    match = re.search(r'\b(19|20)\d{2}\b', text)
    if match:
        years.append(match.group())

data = pd.DataFrame()
data['Movie Names'] = movies
data['Ratings'] = ratings
data['Votings'] = votings
data['Release Year'] = years

data['Ratings'] = data['Ratings'].astype(float)
data['Votings'] = data['Votings'].astype(float)
data['Release Year'] = pd.to_numeric(data['Release Year'], errors='coerce')
data = data.dropna()
# data.to_csv('--path--', index=False)
# print("File saved successfully")
print(data.head())

#Distribution of Voting
plt.figure(figsize=(10, 6))
sns.histplot(data['Votings'], kde=True, color='black')
plt.title('Distribution of Votings')
plt.xlabel('Votings')
plt.ylabel('Frequency')
plt.show()

#Distribution Of Rating
fig = px.histogram(data, x='Ratings', nbins=100, range_x=[0,10], title='Distribution of Ratings')
fig.update_layout(xaxis_title='Ratings', yaxis_title='Frequency')
fig.show()

#MOvie by Release Year
fig = px.histogram(data, x='Release Year', nbins=100, title='Movies by Release Year')
fig.update_layout(title="Movies by Release Year",xaxis_title='Release Year', yaxis_title='Frequency')
fig.show()

# Interactive Scatter Plot of Ratings vs. Votings
fig = px.scatter(data, x='Ratings', y='Movie Names', title='Ratings vs. Votings')
fig.update_layout(xaxis_title='Ratings', yaxis_title='Movies')
fig.show()

# 3D Scatter Plot of Ratings vs. Votings vs. Release Year
fig = go.Figure(data=[go.Scatter3d(x=data['Ratings'], y=data['Movie Names'], z=data['Release Year'], mode='markers', 
                                   marker=dict(size=5, color='red', opacity=0.8))])
fig.update_layout(title='Ratings vs. Movie Name vs. Release Year', 
                  scene=dict(xaxis_title='Ratings', yaxis_title='Votings', zaxis_title='Release Year'))
fig.show()




