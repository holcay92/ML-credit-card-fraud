# -*- coding: utf-8 -*-
"""ML.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BYbBnFEHWmStrJ59r97UZJNucvXa1hVL
"""

# Commented out IPython magic to ensure Python compatibility.
# Import libraries
from scipy import stats
import os
import random
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.tree import DecisionTreeRegressor
import xgboost as xgb
from sklearn.model_selection import GridSearchCV
from sklearn.cluster import KMeans
from matplotlib.patches import Patch
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, precision_score, recall_score, f1_score, roc_curve, auc
from sklearn.model_selection import cross_val_score
import seaborn as sn
import seaborn as sns
from sklearn.impute import SimpleImputer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

# from sklearn.decomposition import PCA
# %matplotlib inline
np.set_printoptions(suppress=True)

df = pd.read_csv('/content/buyukVeri.csv')

df.info()

df['OCCUPATION_TYPE'].fillna('UNKNOWN', inplace=True)
df['OWN_CAR_AGE'].fillna(1000, inplace=True)

df['APARTMENTS_AVG'].fillna(0, inplace=True)
df['BASEMENTAREA_AVG'].fillna(0, inplace=True)
df['YEARS_BEGINEXPLUATATION_AVG'].fillna(0, inplace=True)
df['YEARS_BUILD_AVG'].fillna(0, inplace=True)
df['COMMONAREA_AVG'].fillna(0, inplace=True)
df['ELEVATORS_AVG'].fillna(0, inplace=True)
df['ENTRANCES_AVG'].fillna(0, inplace=True)
df['FLOORSMAX_AVG'].fillna(0, inplace=True)
df['FLOORSMIN_AVG'].fillna(0, inplace=True)
df['LANDAREA_AVG'].fillna(0, inplace=True)
df['LIVINGAPARTMENTS_AVG'].fillna(0, inplace=True)
df['LIVINGAREA_AVG'].fillna(0, inplace=True)

df['NONLIVINGAPARTMENTS_AVG'].fillna(0, inplace=True)
df['NONLIVINGAREA_AVG'].fillna(0, inplace=True)
df['APARTMENTS_MODE'].fillna(0, inplace=True)
df['BASEMENTAREA_MODE'].fillna(0, inplace=True)
df['YEARS_BEGINEXPLUATATION_MODE'].fillna(0, inplace=True)
df['YEARS_BUILD_MODE'].fillna(0, inplace=True)
df['COMMONAREA_MODE'].fillna(0, inplace=True)

df['ELEVATORS_MODE'].fillna(0, inplace=True)
df['ENTRANCES_MODE'].fillna(0, inplace=True)
df['FLOORSMAX_MODE'].fillna(0, inplace=True)
df['FLOORSMIN_MODE'].fillna(0, inplace=True)
df['LANDAREA_MODE'].fillna(0, inplace=True)
df['LIVINGAPARTMENTS_MODE'].fillna(0, inplace=True)

df['LIVINGAREA_MODE'].fillna(0, inplace=True)
df['NONLIVINGAPARTMENTS_MODE'].fillna(0, inplace=True)
df['NONLIVINGAREA_MODE'].fillna(0, inplace=True)
df['APARTMENTS_MEDI'].fillna(0, inplace=True)
df['BASEMENTAREA_MEDI'].fillna(0, inplace=True)
df['YEARS_BEGINEXPLUATATION_MEDI'].fillna(0, inplace=True)
df['YEARS_BUILD_MEDI'].fillna(0, inplace=True)
df['COMMONAREA_MEDI'].fillna(0, inplace=True)
df['ELEVATORS_MEDI'].fillna(0, inplace=True)

df['FLOORSMAX_MEDI'].fillna(0, inplace=True)
df['FLOORSMIN_MEDI'].fillna(0, inplace=True)
df['LANDAREA_MEDI'].fillna(0, inplace=True)
df['LIVINGAPARTMENTS_MEDI'].fillna(0, inplace=True)
df['LIVINGAREA_MEDI'].fillna(0, inplace=True)
df['NONLIVINGAPARTMENTS_MEDI'].fillna(0, inplace=True)

df['NONLIVINGAREA_MEDI'].fillna(0, inplace=True)

df['FONDKAPREMONT_MODE'].fillna('UNKNOWN', inplace=True)
df['HOUSETYPE_MODE'].fillna('UNKNOWN', inplace=True)
df['TOTALAREA_MODE'].fillna(0, inplace=True)
df['WALLSMATERIAL_MODE'].fillna('UNKNOWN', inplace=True)


df['EMERGENCYSTATE_MODE'].fillna('UNKNOWN', inplace=True)

df.head()

# listing the null values columns having more than 30%
emptycol=df.isnull().sum()
emptycol=emptycol[emptycol.values>(0.7*len(emptycol))]
print("empty col and rmeove len = ", len(emptycol))

emptycol = list(emptycol[emptycol.values>=0.3].index)
df.drop(labels=emptycol,axis=1,inplace=True)
print("remaining  table col len = ", len(df.columns))

df = df.drop(['SK_ID_CURR'],axis=1)
df.info()
df.head()

print("Current Dimensions: ", df.shape)

# Veri kümesindeki kategorik sütun isimleri listesi
categorical_column_names = [
    'NAME_CONTRACT_TYPE','CODE_GENDER','FLAG_OWN_CAR','FLAG_OWN_REALTY',
    'NAME_INCOME_TYPE','NAME_EDUCATION_TYPE','NAME_FAMILY_STATUS','NAME_HOUSING_TYPE',
    'WEEKDAY_APPR_PROCESS_START'
    ,'ORGANIZATION_TYPE'
    ,'FONDKAPREMONT_MODE'
    ,'HOUSETYPE_MODE'
    ,'WALLSMATERIAL_MODE'
    ,'EMERGENCYSTATE_MODE'
    ,'OCCUPATION_TYPE'

]

non_categorical_column_names = df.columns.difference(categorical_column_names).tolist()


# ColumnTransformer
transformers = [('encoder', OneHotEncoder(), categorical_column_names)]
ct = ColumnTransformer(transformers=transformers, remainder='passthrough')

X_encoded = ct.fit_transform(df)

# One-hot encoding sonrası sütun isimleri
encoded_column_names = ct.named_transformers_['encoder'].get_feature_names_out(categorical_column_names)
columns_after_encoding = list(encoded_column_names) + df.columns.difference(categorical_column_names).tolist()

df_encoded = pd.DataFrame(X_encoded, columns=columns_after_encoding)

df_encoded.head()

print("Current Dimensions: ", df_encoded.shape)

"""# Detecting the outliers calculating Z score for each row"""

z = np.abs(stats.zscore(df_encoded))
print(z)

sns.boxplot(df_encoded['AMT_CREDIT'])

"""# Detecting the outliers with z score"""

z = np.abs(stats.zscore(df_encoded['AMT_CREDIT']))
print(z)

df_encoded = df_encoded.dropna()

X = df_encoded.iloc[:, 1:].values
y = df_encoded.iloc[:, 0].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

X_train_df = pd.DataFrame(X_train, columns=df_encoded.columns[1:])
X_test_df = pd.DataFrame(X_test, columns=df_encoded.columns[1:])

selected_columns = ['AMT_ANNUITY', 'AMT_CREDIT',  'AMT_INCOME_TOTAL',
                    'CNT_CHILDREN', 'CNT_FAM_MEMBERS', 'DAYS_BIRTH', 'DAYS_EMPLOYED',
                    'DAYS_ID_PUBLISH', 'DAYS_LAST_PHONE_CHANGE', 'DAYS_REGISTRATION',

                    'HOUR_APPR_PROCESS_START',
                    'REGION_POPULATION_RELATIVE']

scaler = StandardScaler()

X_train_df[selected_columns] = scaler.fit_transform(X_train_df[selected_columns])
X_test_df[selected_columns] = scaler.transform(X_test_df[selected_columns])



results = []

def evaluate_model(name, model, X_train, y_train, X_test, y_test):

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    # Model performance
    print(f"\nModel: {name}")
    print(f"Accuracy: {accuracy_score(y_test, y_pred)}")

    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 5))
    sn.heatmap(cm, annot=True, fmt="d", cmap="Blues")
    plt.title(f'Confusion Matrix - {name}')
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.show()

    # error metrics
    print(classification_report(y_test, y_pred))

    # Precision, Recall, F1-Score
    precision = precision_score(y_test, y_pred, average='weighted')
    recall = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')

    print(f"Precision: {precision}")
    print(f"Recall: {recall}")
    print(f"F1-Score: {f1}")

    # ROC ve AUC
    y_prob = model.predict_proba(X_test)[:, 1]
    fpr, tpr, thresholds = roc_curve(y_test, y_prob)
    auc_value = auc(fpr, tpr)

    print(f"AUC: {auc_value}")

    # Cross-Validation
    cv_scores = cross_val_score(model, X_train, y_train, cv=5)
    print(f"Cross-Validation Scores: {cv_scores}")
    print(f"Mean CV Score: {np.mean(cv_scores)}")

    results.append({
        "Model": name,
        "Accuracy": accuracy_score(y_test, y_pred),
        "Precision": precision,
        "Recall": recall,
        "F1-Score": f1,
        "AUC": auc_value,
        "Mean CV Score": np.mean(cv_scores)
    })

evaluate_model("Naive Bayes", GaussianNB(var_smoothing=1e-8), X_train_df, y_train, X_test_df, y_test)

evaluate_model("Random Forest", RandomForestClassifier(random_state=0,max_depth=5), X_train_df, y_train, X_test_df, y_test)

evaluate_model("KNN", KNeighborsClassifier(n_neighbors = 5, metric = 'minkowski', p = 2), X_train_df, y_train, X_test_df, y_test)

results_df = pd.DataFrame(results)

print(results_df)

