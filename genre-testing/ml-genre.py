import numpy as np
import pandas as pd
from sklearn.metrics import classification_report
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import make_pipeline
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

from sklearn.neural_network import MLPClassifier
import seaborn as sns
sns.set()

def main():
    data = pd.read_csv('genre-data.csv', index_col=0)

    # count = data.value_counts('given-genre')
    # print(count)
    # count = count[count > 100]
    # enoughData = count.index.values

    # only use data genres that have more than 100 data points
    # data = data[data['given-genre'].isin(enoughData)]
    y = data['given-genre']
    X = data.drop(['given-genre', 'genre','key', 'mode', 'id', 'song_title', 'popularity_scores', 'time_signature'], axis=1)
    
    print(X.columns.values)
    X_train, X_valid, y_train, y_valid = train_test_split(X,y, test_size=0.15)
    print(X_train.shape, X_valid.shape)
    # KN 
    model = make_pipeline(
        # StandardScaler(),
        MinMaxScaler(),
        KNeighborsClassifier(10)
    )
    model.fit(X=X_train, y=y_train)

    print('KNeighborsClassifier')
    y_predicted = model.predict(X_valid)
    # print(classification_report(y_valid, y_predicted))
    print(model.score(X=X_train, y=y_train))
    print(model.score(X=X_valid, y=y_valid))
    kn_report = classification_report(y_valid, y_predicted, output_dict=True)


    # RF
    model = make_pipeline(
        MinMaxScaler(), 
        RandomForestClassifier(n_estimators=150, max_depth=100, min_samples_split=20)
    )
    model.fit(X=X_train, y=y_train)

    print('RandomForestClassifier')
    y_predicted = model.predict(X_valid)
    # print(classification_report(y_valid, y_predicted))
    print(model.score(X=X_train, y=y_train))
    print(model.score(X=X_valid, y=y_valid))
    rf_report = classification_report(y_valid, y_predicted, output_dict=True)


    # MLP
    model = make_pipeline(
        MinMaxScaler(),
        MLPClassifier(solver='lbfgs', hidden_layer_sizes=(100, 50))
    )
    model.fit(X=X_train, y=y_train)

    print('MLPClassifier')
    y_predicted = model.predict(X_valid)
    # print(classification_report(y_valid, y_predicted))
    print(model.score(X=X_train, y=y_train))
    print(model.score(X=X_valid, y=y_valid))
    mlp_report = classification_report(y_valid, y_predicted, output_dict=True)


    # X_valid['ml'] = y_predicted
    # ids = X_valid['ml']
    # # valid['genre'] = y_predicted
    
    # valid = pd.merge(data, ids, left_index=True, right_index=True)
    # valid['result'] = valid['given-genre'] == valid['ml']
    # valid = valid[['song_title','genre', 'given-genre', 'ml', 'result']]
    # valid.to_csv('valid.csv')

    # plot the report
    kn = pd.DataFrame(kn_report).transpose()
    rf = pd.DataFrame(rf_report).transpose()
    mlp = pd.DataFrame(mlp_report).transpose()

    precision = pd.concat([kn['precision'], rf['precision'], mlp['precision']], axis=1)
    precision.columns = ['KNeighborsClassifier', 'RandomForestClassifier', 'MLPClassifier']
    plt.figure()

    
    precision.plot.bar()
    plt.title('Precision of Machine Learning Models on Validation Set')
    plt.xlabel('Genre')
    plt.ylim(0, 1)
    plt.ylabel('Precision')
    plt.tight_layout()
    plt.savefig('precision.png')

    recall = pd.concat([kn['recall'], rf['recall'], mlp['recall']], axis=1)
    recall.columns = ['KNeighborsClassifier', 'RandomForestClassifier', 'MLPClassifier']
    plt.figure()

    recall.plot.bar()
    plt.title('Recall of Machine Learning Models on Validation Set')
    plt.xlabel('Genre')
    plt.ylim(0, 1)
    plt.ylabel('Recall')
    plt.tight_layout()
    plt.savefig('recall.png')


    f1 = pd.concat([kn['f1-score'], rf['f1-score'], mlp['f1-score']], axis=1)
    f1.columns = ['KNeighborsClassifier', 'RandomForestClassifier', 'MLPClassifier']
    plt.figure()
    
    
    f1.plot.bar()
    plt.title('F1 Score of Machine Learning Models on Validation Set')
    plt.xlabel('Genre')
    plt.ylim(0, 1)
    plt.ylabel('F1 Score')
    plt.tight_layout()
    plt.savefig('f1.png')


   

    



   
    

if __name__ == '__main__':
    main()
    