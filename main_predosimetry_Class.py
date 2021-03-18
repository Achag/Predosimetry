# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 12:12:23 2021

@author: i-achag
"""
import time 
from Import import Import 
from Geometrical_points import Geometrical_points

importera=Import("C:/Temp/Not_For_Deep_Learning",["Coeur","Sein G","Carbon Fiber","Paroi G","External"])


# #Génération des masks de la liste renseignée 
# importera.Save_masks_in_path()


# # Print tout les nii et rs présents  
# nii , rs = importera.read_nii_file()

patient_Number_exemple="305322"
path_read_nii=importera.select_specific_file(patient_Number_exemple)
print(path_read_nii)


# # Affiche les Ids Patient dans le path référencé 
# List_Patient=importera.list_patient_path()

t1=time.time()
List_imgs , List_positions=importera.return_positions()
t2=time.time()
print(t2-t1)
# # Montre les listes des images importés et la liste des positions des différentes structures renseignés 
# print(List_imgs,positions)

# Vérifie que la longeur de List_imgs et poisitions est similaire 
# print(len(List_imgs),len(List_positions))

# i=importera.find_i("Sein G")
# print(i)
# # ##########################################################################################################


# Geometric=Geometrical_points("Sein G")
# img_Sein , position_Sein = Geometric.Attribute_Name(i,List_imgs,List_positions)

# print(img_Sein,position_Sein)