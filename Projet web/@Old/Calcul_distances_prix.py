#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 12:10:05 2020

@author: francoishervier
"""

import os, csv
import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist

# Load data
os.chdir("/Users/francoishervier/Documents/GitHub/Visulalisation/Projet web/Data Paris/Appartements")
df_apts = pd.DataFrame(pd.read_csv('Data_appartements_reprojete.csv', delimiter=',', dtype = str))
os.chdir("/Users/francoishervier/Documents/GitHub/Visulalisation/Projet web/Data Paris/Stations")
df_metro = pd.DataFrame(pd.read_excel('stations_data_clean.xlsx'))
df_apts.valeur_fonciere_vraie = df_apts.valeur_fonciere_vraie.str.replace(",", ".")
df_apts = df_apts.astype({'longitude': float, 'latitude': float, 'surface_reelle_bati': float, 'valeur_fonciere_vraie': float})

# calcul des prix au m2
df_apts["Prix_m2"]= df_apts.valeur_fonciere_vraie / df_apts.surface_reelle_bati

# transformation de la DB en tableaux numpy
apts = df_apts.to_numpy()
df_metro = df_metro.sort_values(by=['gares_id'],axis=0)
df_metro = df_metro.reset_index()
metros = df_metro.to_numpy()
metros_coord = metros[:,[7,8]]
apts_coord = apts[:,[28,29]]
apts_prix = apts[:,[30]]
            
# detection pour chaque station des appartements les plus proches (dans un rayon de dist_mean entre 2 stations)
dist_mean = 571
mat_distances = cdist(apts_coord, metros_coord, metric='euclidean')
mat_prix = np.nan * mat_distances
for i in range(len(mat_distances)): #par appartement
    for j in range(len(mat_distances[0])): #par station
        if mat_distances[i,j] < dist_mean: #si l'appartement se trouve à - de dist_mean, on rempli la matrice de prix avec le prix/m2 de l'apt
            mat_prix[i,j] = apts_prix[i]
        else:
            mat_distances[i,j] = np.nan
        
# Calcul des moyennes de prix par station de métro     
df_mat_prix = pd.DataFrame(mat_prix)
df_prix = df_mat_prix.mean()
df_prix = df_prix.to_frame()
df_prix = df_prix.rename(columns={0:'prix_moyen_par_gare'})

# Réassociation des numéros de ligne de gare avec les Id_gare
df_resultats = pd.concat([df_metro,df_prix], axis=1)

# sauvegarde de la db
df_resultats.to_csv('Data_metro_avec_prix.csv', sep=';', encoding = "utf-8-sig", index = False, decimal = ',', quoting=csv.QUOTE_ALL, quotechar='"')

#test

#df_resultats = df_resultats[0:1000]
#df_save = pd.DataFrame(distances)
#df_save.to_csv('distances.csv', sep=';', encoding = "utf-8-sig", index = False, decimal = ',', quoting=csv.QUOTE_ALL, quotechar='"')

