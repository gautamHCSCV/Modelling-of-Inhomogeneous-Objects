# -*- coding: utf-8 -*-
"""Clustering approach.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MzYHnre73brMbklACC0LjkgzKFDzbRfz
"""

!pip install catboost

import pandas as pd
import numpy as np
import os
import csv
from datetime import datetime
from catboost import CatBoostRegressor
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

import warnings
warnings.filterwarnings('ignore')

from google.colab import drive
drive.mount('/content/drive')

"""# Models Estimation"""

path = '/content/drive/MyDrive/Virtual env/z_inhomogenous_modeling/ecoflex_181221_rf_rd_data/'
path1 = '/content/drive/MyDrive/Virtual env/z_inhomogenous_modeling/x_y_data_all_points/'
train_path = '/content/drive/MyDrive/Virtual env/z_inhomogenous_modeling/percep_fbl_rf_rd_seperately_data/'

path2 = '/content/drive/MyDrive/Virtual env/z_inhomogenous_modeling/'
arr = np.array(pd.read_csv(path2+'x_y_value_for_all_points.csv', names = ['x','y']))
print(arr.shape)
arr[:5]

from sklearn.cluster import KMeans
k_values = range(1, 11)

# Perform k-means clustering for each k value
inertia_values = []
for k in k_values:
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(arr)
    inertia_values.append(kmeans.inertia_)

# Plot the inertia values against the number of clusters
plt.plot(k_values, inertia_values, 'bx-')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Inertia')
plt.title('Elbow Method for Optimal k')
plt.show()

kmeans = KMeans(n_clusters=5)
kmeans.fit(arr)
kmeans.cluster_centers_

from collections import defaultdict
d = defaultdict(lambda: [])
for i in range(200):
    label = kmeans.predict([arr[i]])[0]
    d[label].append(i)

for i in range(5):
    print(d[i])

from scipy.linalg import norm

def dist(i):
    at = -1
    mini = 10
    for j in range(len(d[i])):
        dis = ((arr[d[i][j]][0]- kmeans.cluster_centers_[i][0])**2 + (arr[d[i][j]][1]- kmeans.cluster_centers_[i][1])**2)**0.5
        if dis <mini:
            mini = dis 
            at = j
    print(f'{d[i][at]+1} is the master node of {i}th cluster')
    print(arr[d[i][at]], kmeans.cluster_centers_[i],'\n')
for i in range(5):
    dist(i)

"""# Training and Evaluation of Clusters"""

x1 = np.array(pd.read_csv(path+f'{162}_pos_ecoflex_181221_derivative_data.csv')) # fractional derivatives
y1 = np.array(pd.read_csv(path+f'{162}_force_ecoflex_181221_derivative_data.csv'))
rf = RandomForestRegressor()
rf.fit(x1,y1)

error = []
array = np.array(d[0])+1
for i in array:
    arr = np.array(pd.read_csv(path1+f'{i}_x_y_pos_vel_ecoflex_181221_data.csv'))[:,:2] # x and y values
    x2 = np.array(pd.read_csv(path+f'{i}_pos_ecoflex_181221_derivative_data.csv')) # fractional derivatives
    y1 = np.array(pd.read_csv(path+f'{i}_force_ecoflex_181221_derivative_data.csv'))
    y_pred = rf.predict(x2)
    statement = f'For point: {i}, Error: {mean_squared_error(y_pred, y1)**0.5}\n'
    #print(f'For point: {i}, Error: {mean_squared_error(y_pred, y1)**0.5}')
    error.append(mean_squared_error(y_pred, y1)**0.5)
    with open('results.txt','a') as f:
        f.write(statement)
print(sum(error)/len(error))
print(max(error), min(error))
total = error

x2 = np.array(pd.read_csv(path+f'{40}_pos_ecoflex_181221_derivative_data.csv')) # fractional derivatives
y1 = np.array(pd.read_csv(path+f'{40}_force_ecoflex_181221_derivative_data.csv'))
l = len(y1)
arr = np.array(pd.read_csv(path1+f'{40}_x_y_pos_vel_ecoflex_181221_data.csv'))[:l,:2] # x and y values
rf = RandomForestRegressor()
rf.fit(x2,y1)

error = []
array = np.array(d[1])+1
for i in array:
    arr = np.array(pd.read_csv(path1+f'{i}_x_y_pos_vel_ecoflex_181221_data.csv'))[:,:2] # x and y values
    x2 = np.array(pd.read_csv(path+f'{i}_pos_ecoflex_181221_derivative_data.csv')) # fractional derivatives
    y1 = np.array(pd.read_csv(path+f'{i}_force_ecoflex_181221_derivative_data.csv'))
    y_pred = rf.predict(x2)
    statement = f'For point: {i}, Error: {mean_squared_error(y_pred, y1)**0.5}\n'
    #print(f'For point: {i}, Error: {mean_squared_error(y_pred, y1)**0.5}')
    error.append(mean_squared_error(y_pred, y1)**0.5)
    with open('results.txt','a') as f:
        f.write(statement)
print(sum(error)/len(error))
print(max(error), min(error))
total += error

x2 = np.array(pd.read_csv(path+f'{52}_pos_ecoflex_181221_derivative_data.csv')) # fractional derivatives
y1 = np.array(pd.read_csv(path+f'{52}_force_ecoflex_181221_derivative_data.csv'))
l = len(y1)
arr = np.array(pd.read_csv(path1+f'{52}_x_y_pos_vel_ecoflex_181221_data.csv'))[:l,:2] # x and y values
rf = RandomForestRegressor()
rf.fit(x2,y1)

error = []
array = np.array(d[2])+1
for i in array:
    arr = np.array(pd.read_csv(path1+f'{i}_x_y_pos_vel_ecoflex_181221_data.csv'))[:,:2] # x and y values
    x2 = np.array(pd.read_csv(path+f'{i}_pos_ecoflex_181221_derivative_data.csv')) # fractional derivatives
    y1 = np.array(pd.read_csv(path+f'{i}_force_ecoflex_181221_derivative_data.csv'))
    y_pred = rf.predict(x2)
    statement = f'For point: {i}, Error: {mean_squared_error(y_pred, y1)**0.5}\n'
    #print(f'For point: {i}, Error: {mean_squared_error(y_pred, y1)**0.5}')
    error.append(mean_squared_error(y_pred, y1)**0.5)
    with open('results.txt','a') as f:
        f.write(statement)
print(sum(error)/len(error))
print(max(error), min(error))
total += error

x2 = np.array(pd.read_csv(path+f'{45}_pos_ecoflex_181221_derivative_data.csv')) # fractional derivatives
y1 = np.array(pd.read_csv(path+f'{45}_force_ecoflex_181221_derivative_data.csv'))
l = len(y1)
arr = np.array(pd.read_csv(path1+f'{45}_x_y_pos_vel_ecoflex_181221_data.csv'))[:l,:2] # x and y values
rf = RandomForestRegressor()
rf.fit(x2,y1)

error = []
array = np.array(d[3])+1
for i in array:
    arr = np.array(pd.read_csv(path1+f'{i}_x_y_pos_vel_ecoflex_181221_data.csv'))[:,:2] # x and y values
    x2 = np.array(pd.read_csv(path+f'{i}_pos_ecoflex_181221_derivative_data.csv')) # fractional derivatives
    y1 = np.array(pd.read_csv(path+f'{i}_force_ecoflex_181221_derivative_data.csv'))
    y_pred = rf.predict(x2)
    statement = f'For point: {i}, Error: {mean_squared_error(y_pred, y1)**0.5}\n'
    #print(f'For point: {i}, Error: {mean_squared_error(y_pred, y1)**0.5}')
    error.append(mean_squared_error(y_pred, y1)**0.5)
    with open('results.txt','a') as f:
        f.write(statement)
print(sum(error)/len(error))
print(max(error), min(error))
total += error

x2 = np.array(pd.read_csv(path+f'{147}_pos_ecoflex_181221_derivative_data.csv')) # fractional derivatives
y1 = np.array(pd.read_csv(path+f'{147}_force_ecoflex_181221_derivative_data.csv'))
l = len(y1)
arr = np.array(pd.read_csv(path1+f'{147}_x_y_pos_vel_ecoflex_181221_data.csv'))[:l,:2] # x and y values
rf = RandomForestRegressor()
rf.fit(x2,y1)

error = []
array = np.array(d[4])+1
for i in array:
    arr = np.array(pd.read_csv(path1+f'{i}_x_y_pos_vel_ecoflex_181221_data.csv'))[:,:2] # x and y values
    x2 = np.array(pd.read_csv(path+f'{i}_pos_ecoflex_181221_derivative_data.csv')) # fractional derivatives
    y1 = np.array(pd.read_csv(path+f'{i}_force_ecoflex_181221_derivative_data.csv'))
    y_pred = rf.predict(x2)
    statement = f'For point: {i}, Error: {mean_squared_error(y_pred, y1)**0.5}\n'
    #print(f'For point: {i}, Error: {mean_squared_error(y_pred, y1)**0.5}')
    error.append(mean_squared_error(y_pred, y1)**0.5)
    with open('results.txt','a') as f:
        f.write(statement)
print(sum(error)/len(error))
print(max(error), min(error))
total += error

print('Mean:', np.mean(np.array(total)))
print('Std:', np.std(np.array(total)))
