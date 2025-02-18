import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

engine = create_engine('sqlite:///employees.db')

def load_data():
    employees = pd.read_sql('SELECT * FROM Employees', engine)
    salaries = pd.read_sql('SELECT * FROM Salaries', engine)
    forecasts = pd.read_sql('SELECT * FROM Forecasts', engine)
    data = pd.merge(employees, salaries, on='employee_id')
    data = pd.merge(data, forecasts, on='employee_id', how='left')
    return data

data = load_data()

def statistical_analysis(data):
    stats = data[['base_salary', 'bonus', 'indexation']].describe()
    print(stats)
    return stats

stats = statistical_analysis(data)

def predict_indexation(data):
    data['years_at_company'] = data['hire_date'].apply(lambda x: 2024 - x.year)
    X = data[['age', 'base_salary', 'years_at_company']]
    y = data['predicted_indexation'].fillna(data['indexation'])
    
    model = LinearRegression()
    model.fit(X, y)
    data['predicted_indexation'] = model.predict(X)
    
    mse = np.mean((data['predicted_indexation'] - y) ** 2)
    print(f"Mean Squared Error: {mse}")
    return model, mse

model, mse = predict_indexation(data)

def cluster_employees(data, n_clusters=3):
    features = data[['base_salary', 'bonus', 'age']]
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    data['cluster'] = kmeans.fit_predict(features)
    return data, kmeans

data, kmeans = cluster_employees(data)

def visualize_clusters(data):
    plt.figure(figsize=(10,6))
    sns.scatterplot(x='age', y='base_salary', hue='cluster', data=data, palette='viridis')
    plt.title('Кластеризация сотрудников по возрасту и базовой зарплате')
    plt.xlabel('Возраст')
    plt.ylabel('Базовая зарплата')
    plt.savefig('clusters.png')
    plt.close()

visualize_clusters(data)