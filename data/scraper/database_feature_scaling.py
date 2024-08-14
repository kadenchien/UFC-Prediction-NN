import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler
from IPython.display import display


df = pd.read_csv('/Users/kevinliu/Desktop/UFC-Prediction-NN/data/raw/mens_fighters_database.csv')

#replace all numerical NA values with the mean of that column
imputer = SimpleImputer(strategy='mean')
numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns
df[numerical_columns] = imputer.fit_transform(df[numerical_columns])

#one-hot encode the fighting style
df = pd.get_dummies(df, columns=['Style'], prefix='Style', drop_first=True)


#normalize all of the columnx
scaler = MinMaxScaler()

# Select only the numerical columns
numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns

# Fit the scaler to the data and transform it
df[numerical_columns] = scaler.fit_transform(df[numerical_columns])
display(df)