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


def main():
    data = pd.read_csv('genre-data.csv', index_col=0)
    data = data[['given-genre', 'popularity_scores']]

    # genre_count = data['given-genre'].value_counts()

    # enoughGenres = genre_count[genre_count > 100]
    # enoughGenres = enoughGenres.index.values

    # print(enoughGenres)
    # data = data[data['given-genre'].isin(enoughGenres)]
    groups = data.groupby('given-genre')
    genres = data['given-genre'].unique()

    dfs = []
    dictionary = {
    }
    for genre in genres:
        s = groups.get_group(genre)
        # dfs.append(s['popularity_scores'])
        dictionary[genre] = s['popularity_scores']

    # print(dfs)
    g1 = data[data['given-genre'] == 'pop']['popularity_scores']
    g2 = data[data['given-genre'] == 'rap']['popularity_scores']

    # print('variance test')
    # compute lenene test for each genre in the data
    binary = np.zeros((len(genres), len(genres)))
    for genre in genres:
        for genre2 in genres:
            if genre != genre2:
                g = data[data['given-genre'] == genre]['popularity_scores']
                g2 = data[data['given-genre'] == genre2]['popularity_scores']
                pvalue = stats.levene(g, g2).pvalue
                binary[genres == genre, genres == genre2] = pvalue < 0.05

    plt.figure()
    plt.title('Levene Test, blue = significant difference in variance')
    sns.heatmap(binary, xticklabels=genres,
                yticklabels=genres, cmap='Blues', annot=False)
    plt.tight_layout()
    plt.savefig('levene-genre.png')
    plt.close()

    # anova = stats.f_oneway(*dfs)
    # print(anova.pvalue)

    # if anova.pvalue < 0.05:
    #     print('there is a difference')
    # else:
    #     print('there is no difference')

    melt = pd.melt(data)

    byGenre = pd.DataFrame(dictionary)
    melt = pd.melt(byGenre).dropna()

    posthoc = pairwise_tukeyhsd(melt['value'], melt['variable'], alpha=0.05)
    # print(posthoc)

    plt.figure()
    posthoc.plot_simultaneous()
    plt.savefig('tukey.png')
    plt.close()

    plt.figure()
    ax = sns.histplot(data=data, x='popularity_scores',
                      hue='given-genre', multiple='dodge', shrink=0.8, bins=10)
    sns.move_legend(
        ax, "lower center",
        bbox_to_anchor=(.5, 1), ncol=5, title=None, frameon=False, borderaxespad=0.
    )
    plt.tight_layout()
    # g.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig('hist.png')
    plt.close()

    plt.figure()

    plt.title('Boxplot of Popularity Scores by Genre with more than 100 songs')
    ax = sns.boxplot(x='given-genre', y='popularity_scores', data=data, order=data.groupby(
        'given-genre').mean().sort_values('popularity_scores', ascending=False).index)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90,
                       horizontalalignment='right')

    plt.tight_layout()
    plt.savefig('boxplot.png')
    plt.close()

    plt.figure()

    plt.title('Pie Chart of Genres with more than 100 songs')
    genre_count = data['given-genre'].value_counts()
    # labels with count and name
    labels = [f'{genre_count[i]} {i}' for i in genre_count.index]

        
    plt.pie(genre_count, labels=labels, autopct='%1.0f%%')
    plt.tight_layout()
    plt.savefig('pie.png')
    plt.close()

 # chi square test
    data['popularity'] = pd.cut(x=data['popularity_scores'], bins=[
                                  0, 50, 75, 100], labels=['low', 'medium', 'high'])
    chi = data[['given-genre', 'popularity']]
    contingency = pd.crosstab(chi['given-genre'], chi['popularity'])
    # print(contingency)
    chi2, p, dof, expected = stats.chi2_contingency(contingency)
    print(p)
    # convert to non sciencitific notation of expected values
    expected = np.array(expected, dtype=int)
    # print(expected)

    # plot expected values
    plt.figure()
    plt.title('Expected Values')
    sns.heatmap(expected, xticklabels=contingency.columns, yticklabels=contingency.index, annot=True, fmt='d', annot_kws={"size": 8})
    plt.tight_layout()
    # text size
   
    plt.savefig('expected.png')
    plt.close()
    


   

if __name__ == '__main__':
    main()
