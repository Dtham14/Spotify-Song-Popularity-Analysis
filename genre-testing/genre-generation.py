import numpy as np
import pandas as pd
import math
import os
from scipy import stats
import matplotlib.pyplot as plt
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import re
import seaborn as sns
sns.set()

def hexbin(x, y, color, **kwargs):
    cmap = sns.light_palette(color, as_cmap=True)
    
    extent = [0,1,0,100]
    if(x.name == 'loudness'):
        extent = [-60, 0, 0, 100]

    if(x.name == 'tempo'):
        extent =[0, 200, 0, 100] 

    if(x.name == 'duration_ms'):
        # extent =[0, 4500000, 0, 100] 
        extent =[0, 4500000/10, 0, 100] 

    plt.hexbin(x, y, cmap=cmap, gridsize=15,extent=extent, **kwargs)


def main():
    songs_data = pd.read_csv('../data/playlists-v4-final.csv')
    # songs_data['genre'] = songs_data['genre'].astype('category')
    # print(songs_data)

    numeric_columns = ['danceability', 'energy', 'loudness', 'speechiness',
                       'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
                       'duration_ms',
                       'popularity_scores']

    regex = r'(k-pop|filmi|acoustic|corrido|bollywood|electro swing|cumbia|edm|instrumental|funk|blues|country|lo-fi|punk|folk|jazz|trap|soundtrack|reggae|salsa|bass|rap|soul|anime|ambient|metal|hip hop|country|classical|alt z|rock|r&b|rnb|indie|pop|disco|latin|alternative)'
    # genres_data = songs_data['genre'].str.extract(regex,re.IGNORECASE, expand=False)
    all_genres_data = songs_data['genre'].str.extractall(regex, re.IGNORECASE)
    all_genres_data = all_genres_data.rename(columns={0: 'given-genre'})
    # print("total: ", songs_data['genre'].count())
    # nonempty = genres_data[~genres_data.isnull()]
    # empty = songs_data['genre'][genres_data.isnull()].dropna()
    # notEmpty = genres_data[~genres_data.isnull()]
    # notEmpty.to_csv('cleaned_genres.csv')
    # print("count of extracted genres: ", notEmpty.count())
    # print(notEmpty.value_counts())

    # print(all_genres_data.value_counts())
    all_genres_data = all_genres_data.reset_index().set_index('level_0')[
        'given-genre']
    joined = songs_data.join(all_genres_data, how='inner')
    # joined['given-genre']= joined['given-genre'].fillna('other')

    # creates csv for ml-test
    # joined.to_csv('genre-data.csv')

    genre_count = joined['given-genre'].value_counts()
    

    enoughGenres = genre_count[genre_count > 100]
    enoughGenres = enoughGenres.index.values

    print(enoughGenres)
    data = joined[joined['given-genre'].isin(enoughGenres)]

    data.to_csv('genre-data.csv')
    


    # generated_genres = all_genres_data.drop_duplicates().values
    # print(generated_genres)
    ##################################


    for feature in numeric_columns:
        
        plt.figure()
        g = sns.FacetGrid(data=data, col='given-genre', col_wrap=6)
        g.map(hexbin, feature,'popularity_scores')
        plt.savefig('../images/{}.png'.format(feature))
        plt.close()
        pass

    # mean = joined.groupby('given-genre').mean()
    # print(mean.sort_values('popularity_scores', ascending=False))

    # # chi square test
    # joined['popularity'] = pd.cut(x=joined['popularity_scores'], bins=[
    #                               0, 50, 75, 100], labels=['low', 'medium', 'high'])
    # chi = joined[['given-genre', 'popularity']]
    # contingency = pd.crosstab(chi['given-genre'], chi['popularity'])
    # # print(contingency)
    # chi2, p, dof, expected = stats.chi2_contingency(contingency)
    # print(p)
    # print(expected)


if __name__ == '__main__':
    main()
