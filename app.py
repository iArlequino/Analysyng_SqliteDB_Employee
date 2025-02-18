import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer

def load_data():
    engine = create_engine('sqlite:///employees.db')
    employees = pd.read_sql('SELECT * FROM Employees', engine)
    salaries = pd.read_sql('SELECT * FROM Salaries', engine)
    forecasts = pd.read_sql('SELECT * FROM Forecasts', engine)
    st.write("Загруженные данные (Employees):", employees)
    st.write("Загруженные данные (Salaries):", salaries)
    st.write("Загруженные данные (Forecasts):", forecasts)
    data = pd.merge(employees, salaries, on='employee_id', how='left')
    data = pd.merge(data, forecasts, on='employee_id', how='left')
    st.write("Объединенные данные:", data)
    return data

def main():
    st.title('Анализ данных о сотрудниках')

    data = load_data()

    imputer = SimpleImputer(strategy='mean')
    data[['age', 'base_salary']] = imputer.fit_transform(data[['age', 'base_salary']])
    
    kmeans = KMeans(n_clusters=2)
    data['cluster'] = kmeans.fit_predict(data[['age', 'base_salary']])
    
    st.header('Статистический обзор')
    st.write(data[['base_salary', 'bonus', 'indexation']].describe())

    st.subheader('Распределение базовых зарплат')
    fig, ax = plt.subplots()
    sns.histplot(data['base_salary'], bins=10, kde=True, ax=ax)
    st.pyplot(fig)

    st.subheader('Кластеризация сотрудников по зарплате и возрасту')
    fig2, ax2 = plt.subplots()
    sns.scatterplot(x='age', y='base_salary', hue='cluster', data=data, palette='viridis', ax=ax2)
    plt.title('Кластеры сотрудников')
    st.pyplot(fig2)

    st.header('Прогнозируемая индексация зарплат')
    st.write(data[['employee_id', 'first_name', 'last_name', 'predicted_indexation']])

    st.subheader('Прогнозируемая индексация по отделам')
    fig3, ax3 = plt.subplots(figsize=(10,6))
    sns.boxplot(x='department', y='predicted_indexation', data=data, ax=ax3)
    plt.title('Прогнозируемая индексация по отделам')
    st.pyplot(fig3)

if __name__ == '__main__':
    main()