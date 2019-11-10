import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
# from yellowbrick.cluster import KElbowVisualizer
# import matplotlib.pyplot as plt
# import matplotlib

def run_clustering(df, k):
    X = df.values
    model = KMeans()
    kmeans = KMeans(n_clusters=k, random_state=0).fit(X)
    
    centers = kmeans.cluster_centers_
    label = list(kmeans.labels_)
    for i in range(len(label)):
        label[i] += 1
    
    return centers, label

def get_class_df(df, label, col_name):
    class_df = pd.DataFrame(label, index=df.index, columns=[col_name])
    return class_df

def get_center_df(df, centers, class_num):
    col = []
    for i in range(class_num):
        col.append('class{}'.format(i+1))
    
    return pd.DataFrame(centers, index=df.columns, columns=col)