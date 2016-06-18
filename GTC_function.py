import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import networkx as nx
from sklearn.cluster import KMeans
from sklearn import preprocessing

# data importing
raw_data = pd.read_csv('data/trade_data.csv')

class Graph_GT:
    def __init__(self, year, raw_data = raw_data):
        """
        Initialization
        self.df is a pd.dataframe for the given year
        """

        self.year = year
        self.df = raw_data.loc[raw_data['Yr']==year]
 

    def country_list(self):
        """
        raw_date should be a pd.dataframe
        
        """
        country_list = set(list(self.df.Reporting_Entity_RIC_Name)\
                           +list(self.df.Partner_Entity_RIC_Name))
        country_list = sorted(list(country_list))
        return country_list
    
    
    def graph(self):
        """
        creat a nx.graph object(weighted & directed)
        of the trading data for the given year
        """
        
        list_trade = self.df.iloc[:,[2,5,7]].values
        list_trade_nanremoved = []
        for row in list_trade:
            if np.isnan(row[2]) == False:
                list_trade_nanremoved +=  [row]
        list_trade = np.array(list_trade_nanremoved)
        min_max_scaler = preprocessing.MinMaxScaler()
        
        list_trade[:,2] = min_max_scaler.fit_transform(list_trade[:,2])       
        #list_trade[:,2] = preprocessing.scale(list_trade[:,2])
        #list_trade = np.transpose(list_trade)
        G = nx.Graph()
        nodes = []
        for row in list_trade:
            #if np.isnan(row[2])==False:
            G.add_edge(row[0],row[1],weight = np.exp(-0.5*row[2]**2))
            nodes.append(row[0])
            nodes.append(row[1])
        nodes = set(nodes)
        G.add_nodes_from(nodes)
        return G
    
    
def spectral_clustering(dim_spec, n_cluster, graph):
    """
    return the prediction of kmeans model of the spectral clustering
    """

    cluster_km = KMeans(n_clusters = n_cluster,max_iter = 10000,tol = 0.00000001)
    features_spectre = nx.spectral_layout(graph,dim = dim_spec)
    cluster_km.fit(features_spectre.values())
    return cluster_km.predict(features_spectre.values())
        
    
