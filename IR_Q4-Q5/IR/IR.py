import csv 
import nltk
import textblob 

import sklearn
import pandas
from pandas import DataFrame, read_csv
import pandas as pd


def preprocess():
    # Load dataset from csv
    file = 'Book5.csv'
    data = pd.read_csv(file, encoding="ISO-8859-1")
    df = pd.DataFrame(data)
    df = df[["text","Categorize"]]
    peek = df.head(10)
    print(peek)
    #tweet = df["text"]
    
    #preprocessing 
    df["text"] = df["text"].str.replace('http\S+', ' ')
    df["text"] = df["text"].str.replace('[^\w\s]', ' ')
    df["text"] = df["text"].str.replace('\n', ' ')
    df["text"] = df["text"].str.replace('ã å â  â', ' ')
    df["text"] = df["text"].str.replace('ã â  â', ' ')

    df["text"] =df["text"].str.lower()
    print(df)
    print(",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,")
    df["text"] = df["text"].str.replace('rt', ' ')
    tweet = df["text"]
    print(tweet)
    

    from io import StringIO
    df = df[pd.notnull(df['text'])]
    df.columns = ['text', 'Categorize']
    df["category_id"] = df.Categorize.factorize()[0]
    category_id_df = df[['text', 'category_id']].drop_duplicates().sort_values('category_id') 
    category_to_id = dict(category_id_df.values) 
    id_to_category = dict(category_id_df[['category_id', 'text']].values)
    print("\n\n" + "-------------Ten rows of data for example purposes:-------------  ")
    #print(df.head(10)) # For 10 and debugging purposes
    print(df)
    print("\n\n")

    from sklearn import model_selection, preprocessing, linear_model, naive_bayes, metrics, svm

    # Visualization of data
    #import matplotlib.pyplot as plt
    #fig = plt.figure(figsize=(8,6))
    #df.groupby('Categorize').text.count().plot.bar(ylim=0)
    #plt.show()

    from sklearn.metrics import cohen_kappa_score
    from sklearn.metrics import confusion_matrix 
    from sklearn.grid_search import GridSearchCV
    from sklearn.svm import LinearSVC

    rater1 = ['Personal','Personal', 'News', 'News', 'Personal', 'Personal', 'News', 'News', 'Personal','Personal','Personal','News', 'News', 'Personal', 'News', 'Personal', 'News', 'Personal', 'Personal',
    'News','News','Personal','Personal','Personal','News','Personal', 'Personal','Score','Personal','News','News','News','News','News','News','News','Personal','News','News','Personal','Personal','Personal',
    'Personal','Personal','News','News','News','News','News','News','News','News','News','News','News','Personal','News','News','Personal','News','News','Personal',
    'Personal','Personal','Personal','News','News','Personal','Personal','Personal','News','News','Personal','Personal','Personal','News','News','News','News','Personal','Personal','News','Personal','News','News',
    'Personal','News','Personal','News','Personal','Personal','Personal','News','Personal','News','Personal','News','Personal','Personal','News','News','Personal','Personal','Personal','Personal','News','Personal','News','News','Personal',
    'Personal','News','Personal','Personal','Personal','News','Personal','Personal','Personal','News','News','News','Personal','News','News','News','News','News','News','Personal','Personal','Personal','News','News','Personal','Personal',
    'Personal','News','Personal','Personal','News','Personal','Personal','Personal','Personal','News','Personal','News','Personal','Personal','News','News','News','News',
    'News','Personal','News','Personal','News','Personal','Personal','News','News','Personal','Personal','News','News','News','News','News','Personal','Personal','Personal','News','News','Personal','Personal','Personal','News',
    'Personal','Personal','Personal','Personal','News','Personal','News','News','Personal','Personal','News','Personal','News','Personal','Personal','News','Personal','Personal','News','Personal','Personal','Personal',
    'News','Personal','Personal','News','News','Personal','Personal','Personal','Personal','Personal','News','Personal','News','News','News','News','Personal','Personal','Personal','Personal','News','Score','Personal','Personal',
    'Score','Personal','News','News','Personal','News','Personal','Personal','Personal','News','Personal','Personal','Personal','Personal','Personal','News','News','News','News','News','Personal','Personal','News','Personal','News','Personal','News','News','Personal','News',
    'News','News','News','News','News','News','Personal','Personal','Personal','News','News','News','Personal','Score','Personal','News','Personal','News','News','News','News','News','News','Personal','News','Personal','News','Personal',
    'Personal','Personal','Personal','Personal','Personal','News','Personal','News','News','News','News','News','News','Personal','Personal','Personal','Personal','News','Personal','Personal','Personal','Personal','Personal','Personal','News','Personal','Personal','Personal',
    'Personal','Personal','Personal','Personal','Personal','Personal','Personal','Personal','Personal','Personal','News','News','News','Personal','Personal','News','News','Personal','Personal','Personal','News','Personal','Personal','News','News',
    'News','News','News','Personal','Personal','News','News','News','News','Personal','Personal','Personal','News','Personal','Personal','Personal','Personal','Personal','Personal','News','News','News','Personal','Personal','Personal','News','Personal','News','Personal','News',
    'News','Personal','Personal','News','News','News','News','News','Personal','News','Personal','Personal','Personal','News','Personal','Personal','News','News','Personal','News','Personal','News','Personal','Personal','Personal','Personal','Personal','Personal','Personal',
    'Personal','Personal','Personal','Personal','News','News','News','News','News','Personal','News','Personal','News','News','Personal','News','Personal','News','Personal','Personal','Personal','Personal','Personal','News',
    'News','Personal','Personal','Personal','News','News','News','Personal','News','Personal','News','Personal','Personal','Personal','Personal','News','Personal','News','Personal','News','News','Personal','News','Personal','Personal',
    'Personal','News','Personal','News','News','Personal','News','Personal','Personal','Personal','Personal','Personal','News','Personal','News','Personal','Personal','Personal','Personal','Personal','News',
    'Personal','News','Personal','News','News','Personal','News','News','Personal','Personal','Personal','News','News','Personal','News','Score','Score','Personal','Score','News','Score','News','News','Score','News','News',
    'Score','News','News','News','News','News','Personal','Personal','Personal','News','News','Personal','Personal','News','News','Personal','News','News','Personal','Personal','News','News','Personal','News','News','News','News','News','Personal','Personal']

    rater2 = ['Personal','News','Personal','Personal','Personal','Personal','News','Personal','Personal','Personal','News','Personal','Personal','News','News','News','Personal','Personal','News','Personal','Personal','Personal','Personal',
'Personal','Personal','Personal','Personal','Personal','News','Personal','News','Personal','News','Personal','News','Personal','News','Personal','Personal','News','Personal','Personal','Personal','Personal','News',
'Personal','Personal','Personal','News','Personal','Personal','News','Personal','Personal','News','News','News','Personal','Personal','News','Personal','News','Personal','News','News','Personal','News','Personal',
'Personal','Personal','Personal','News','Personal','Personal','Personal','News','Personal','News','Personal','News','News','Personal','News','Personal','Personal','News','Personal','News','News','News',
'Personal','Personal','Personal','News','Personal','Score','Personal','News','News','News','News','News','Personal','Personal','News','Personal','News','Personal','Personal','News','Personal','Personal','Personal',
'News','Personal','Personal','Personal','Personal','Personal','Personal','Personal','Personal','Score','Personal','Personal','Personal','Personal','Personal','Personal','News','Personal','Personal','Personal',
'News','News','News','Personal','Personal','Personal','Personal','Personal','Personal','Personal','Personal','News','News','News','News','Personal','News','Personal','Personal','Personal','News','Personal','Personal','Personal','Personal',
'Personal','Personal','Personal','Personal','Personal','News','Personal','Personal','Personal','News','Personal','News','News','Personal','Personal','Personal','Personal','Personal','News','News','News','News','Personal','Personal','Personal','Personal','Personal','Personal',
'News','Personal','Personal','Personal','News','News','Personal','Personal','Personal','Personal','Personal','News','News','Personal','Personal','Personal','Personal','Personal','Personal','Personal','News','Personal','Personal','Personal',
'Personal','News','Personal','Personal','Personal','Personal','Personal','Personal','Personal','Personal','Personal','Personal','Personal','Personal','Personal','Personal','Personal','Personal','Personal','Personal',
'Personal','Personal','Personal','Personal','Personal','Personal','Personal','Personal','Personal','Personal','Personal','Personal','Personal','Personal','Personal',
'Personal','Personal','Personal','Personal','Personal','Personal','News','News','Personal','Personal','Personal','Personal','Personal','Personal','Personal','Personal','Personal','Personal','Personal','Personal','Personal',
'Personal','Personal','Personal','Personal','Personal','Personal','Personal','News','Personal','Personal','Personal','News','News','Personal','News','Personal','Personal','Personal','Personal','Personal','Personal','Personal','News','Personal','News','Personal','Personal',
'News','News','News','News','Personal','Personal','News','News','Personal','News','News','News','Personal','Personal','News','News','Personal','Personal','Personal','Personal','Personal','News','Personal','Personal','News',
'Personal','News','News','Personal','Personal','Personal','News','News','News','Personal','News','Personal','News','Personal','Personal','Personal','Personal','Personal','Personal','Personal','Personal','Personal','Personal',
'Personal','Personal','Personal','Personal','News','Personal','Personal','News','Personal','Personal','Personal','Personal','News','News','News','News','News','Personal','News','News','Personal','Personal','News','Personal','News','News',
'Personal','Personal','Personal','News','News','Personal','Personal','Personal','News','Personal','News','News','News','News','News','Personal','News','Personal','Personal','News','Personal','News','News','News','Personal',
'News','News','News','Personal','Personal','Personal','News','News','Personal','Personal','Personal','News','News','Personal','News','Personal','Personal','News','Personal',
'News','Personal','News','Personal','Personal','News','Personal','Personal','News','News','News','News','Personal','News','News','News','News','News','Personal','Personal','Personal','News',
'News','News','News','News','Personal','News','News','Personal','Personal','News','News','Personal','News','News','Personal','Personal','Personal','Personal','Personal','Personal','Personal','Personal','Personal','News',
'Personal','Personal','News','Personal','News','Personal','Personal','Personal','Personal','Personal','Personal','Personal','Personal','Personal','Personal','Personal','Personal','News','Personal','Personal','Personal','Personal',
'Personal','Personal','Personal','Personal','Personal','Personal','Personal','Personal','News','News','Personal','Personal','Personal','Personal','News','News','Personal','News','News','News','News','Personal','News','Personal',
'Personal','Personal','News','News','Personal','Personal','News','Personal','Personal','Personal','News','News','Personal','Personal','Personal','News','Personal','Personal']
    
    #kappa cohen score
    kappa = cohen_kappa_score(rater1,rater2)
    print(kappa)
    print(confusion_matrix(rater1,rater2))

    print("************************************************************")
    # Evaluate Algorithms
    from sklearn.model_selection import train_test_split 
    X_train, X_test, y_train, y_test = train_test_split(df.text, df['Categorize'] , test_size=0.1, random_state=0) # 20% test set 80% training set

    from sklearn.feature_extraction.text import TfidfVectorizer
    tfidf = TfidfVectorizer(sublinear_tf=True, min_df=5, norm='l2', encoding='latin-1', ngram_range=(1, 2), stop_words='english')
    X = tfidf.fit_transform(X_train).toarray() # Fit to convert words to int
    print("-------------Vector words found in one classifier:------------- ")
    print(tfidf.inverse_transform(X[1]))
    labels = y_train #df.category_id
    print("\n" + "-------------Numbers of features and description:-------------  ")
    print(X.shape)   
    print("\n\n")

    print("~~~~~~~~~~~~~~~~~~~Multinomial Classifier~~~~~~~~~~~~~~~")
    from sklearn.naive_bayes import MultinomialNB
    mnb = MultinomialNB()
    mnb1 = mnb.fit(X, y_train)
    print(mnb1) # MultinomialNB(alpha=1.0, class_prior=None, fit_prior=True)

    # Test one specific data
    #print("\n" + "-------------For one prediction:-------------" )
    #print(mnb.predict(tfidf.transform(["RT @IanCheeseman: #ManCity fans are wonderful. For many years they showed great loyalty when times were tough. Just because the glory daysâ€¦."])))
    
    # Extract tfidf features to test all data set.
    X_testtfidf = tfidf.transform(X_test) 
    pred = mnb.predict(X_testtfidf) # Change here for specific data
    #print("\n" + "-------------All prediction:---------------- ")
    #print(pred)

    from sklearn.metrics import accuracy_score, classification_report, confusion_matrix 
    predicted = mnb.predict(X_testtfidf)
    print(confusion_matrix(y_test,predicted))
    print(classification_report(y_test,predicted))
    print("\n" + "-------------Accuracy score:-------------  ")
    print(accuracy_score(y_test,predicted))
    print("\n\n")

    #print("~~~~~~~~~~~~~~~~~SVM~~~~~~~~~~~~~~~~~~~~~~~~~~")
    #X= df.text
    #y = df['Categorize']
    #from sklearn.model_selection import train_test_split  
    #X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20) 
    #tfidf = TfidfVectorizer(sublinear_tf=True, min_df=5, norm='l2', encoding='latin-1', ngram_range=(1, 2), stop_words='english')
    #X = tfidf.fit_transform(X_train)
    #print(X.shape)
    #print(y_train.shape)
    #from sklearn.svm import SVC  
    #svclassifier = SVC(kernel='linear')  
    #svclassifier.fit(X, y_train)
    #X_testtfidf = tfidf.transform(X_test)
    #y_pred = svclassifier.predict(X_testtfidf)
    #from sklearn.metrics import classification_report, confusion_matrix  
    #print(confusion_matrix(y_test,y_pred))   
    #print(classification_report(y_test,y_pred))
    #print("\n\n" + "-------------Accuracy score:-------------  ")
    #print(accuracy_score(y_test,y_pred))


    #  Compare Algorithms 
    from sklearn.linear_model import LogisticRegression
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.svm import LinearSVC
    from sklearn.model_selection import cross_val_score

    models = [RandomForestClassifier(n_estimators=200, max_depth=3, random_state=0),
              LinearSVC(),
              MultinomialNB(),
              LogisticRegression(random_state=0)
              ]
    CV = 5 
    cv_df = pd.DataFrame(index=range(CV * len(models)))
    entries = []
    for model in models:
          model_name = model.__class__.__name__
          accuracies = cross_val_score(model, X, labels, scoring='accuracy', cv=CV)
          for fold_idx, accuracy in enumerate(accuracies):
              entries.append((model_name, fold_idx, accuracy))
    cv_df = pd.DataFrame(entries, columns=['model_name', 'fold_idx', 'accuracy'])
    import seaborn as sns
    sns.boxplot(x='model_name', y='accuracy', data=cv_df)
    sns.stripplot(x='model_name', y='accuracy', data=cv_df, 
              size=8, jitter=True, edgecolor="gray", linewidth=2)
    #plt.show()
    print("\n\n" + "-------------Accuracy for four models:------------- ")
    print(cv_df.groupby('model_name').accuracy.mean())

    # Improve Accuracy  
    classifier = RandomForestClassifier(n_estimators=1000, random_state=0)  
    classifier.fit(X, y_train)

    # Evaluating the Model
    print("\n\n\n" + "-------------Models for evaluating and further accuracy:------------- ")
    y_pred = classifier.predict(X_testtfidf)
    print(confusion_matrix(y_test,y_pred))
    print(classification_report(y_test,y_pred))
    print(accuracy_score(y_test, y_pred))
    print("\n\n")


if __name__ == '__main__':

  preprocess()
