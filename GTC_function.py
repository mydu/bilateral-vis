import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import networkx as nx
from sklearn.cluster import KMeans

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
        #list_trade = np.transpose(list_trade)
        G = nx.Graph()
        nodes = []
        for row in list_trade:
            nodes.append(row[0])
            nodes.append(row[1])
            G.add_edge(row[0],row[1],weight = row[2])
        nodes = set(nodes)
        G.add_nodes_from(nodes)
        return G
    
    
def spectral_clustering(dim_spec, n_cluster, graph):
    """
    return the prediction of kmeans model of the spectral clustering
    """

    cluster_km = KMeans(n_clusters = n_cluster)
    features_spectre = nx.spectral_layout(graph,dim = dim_spec)
    cluster_km.fit(features_spectre.values())
    return cluster_km.predict(features_spectre.values())
        
    
