# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 12:12:23 2021

@author: i-achag
"""
import time 
import numpy as np

from Import import Import 
from Geometrical_points import Geometrical_points
from Plot import Plot
from math import  isnan

t0=time.time()

################################### Initialise this variables ###########################################
OFFSET_cm=0.5
datapath="C:/Temp/Not_For_Deep_Learning"
List_ROI=["Coeur","Sein G","Carbon Fiber","Paroi G","External"]
#########################################################################################################

# Take into account the difference of Name 
List_Of_ROI=[]
for i in List_ROI:
    List_Of_ROI.append(i.replace(" ","-"))
print(List_Of_ROI)


importer=Import(datapath,List_Of_ROI)

# importer.Save_masks_in_path()

List_Patient=importer.list_patient_path()
print(List_Patient)

#Loop on all patients
for y in List_Patient:
    t1=time.time()
    print('\n')
    print("Calculating data from Id : ",y,' ...')

    
    Geometric=Geometrical_points(List_ROI[1])
    
    

    img_sein , position_sein = importer.return_positions(y,List_Of_ROI[1]) or importer.return_positions(y,List_Of_ROI[3])

    img_coeur , position_coeur = importer.return_positions(y,List_Of_ROI[0]) 

    position_CouchSurface = importer.return_positions(y,List_Of_ROI[2])[1]
    
    mini, maxi, slice_barycenter = Geometric.limite_z(position_coeur,position_sein)
    
    volume_voxel= Geometric.volume(img_coeur, img_sein)
     
    List_angle , List_Anneau_x_slice_barycenter , List_Anneau_y_slice_barycenter , List_Couch_x_slice_barycenter , List_Couch_y_slice_barycenter  = [], [], [], [], []
    
    count=0
    count_pixel=0
    
#Loop on each slices
    for z in range (mini, maxi, 1):
        List_coeur_x , List_coeur_y , List_sein_x , List_sein_y , List_point = [] , [] , [] , [] , []   
        
        
        List_angle, position_coeur_slice_z, position_sein_slice_z, ConditionA, Xa, Ya, ConditionB, Xb, Yb, count_pixel  = Geometric.Select_Slice_And_Define_Angle(img_coeur, img_sein, position_coeur, position_sein, z, count_pixel, OFFSET_cm, List_angle)
        
        
        x=np.linspace(0,img_coeur.shape[0],1000)
        
#Check number of points in the slice and return False if Breast is not present        
        if ConditionA == True and ConditionB==True:
            
            m,p=Geometric.droite_directrice(Xa, Ya, Xb, Yb)
            
            for i in position_coeur_slice_z:
                List_coeur_x.append(i[0])
                List_coeur_y.append(i[1])
                if Geometric.point_au_dessus_droite(i[0], i[1], m, p)==True:
                    count=count+1
                    
            for j in position_sein_slice_z:
                List_sein_x.append(j[0])
                List_sein_y.append(j[1])
                
    List_angle=[x for x in List_angle if isnan(x) == False]            
                
###################################################### Display plot #################################################################################################################          
            # Plotter=Plot(List_coeur_x,List_coeur_y,List_sein_x,List_sein_y,x,y,z,m,p,slice_barycenter,List_Couch_x_slice_barycenter,List_Couch_y_slice_barycenter,position_CouchSurface)
            
            # Plotter.plot(Geometric.f,Geometric.Anneau_and_Couch,Geometric.size,Geometric.Verification_barycentre_table,img_coeur,img_sein)
#########################################################################################################################################################################################

############################### Display volume intersecting from minimal slice to current slice ##############################################################
 
           # print ("Le volume intersecté depuis la Slice " , mini+1 , "à ", z-1, "est : ", count * volume_voxel, "cm3")
           # print ("Le volume intersecté depuis la Slice " , mini+1 , "à ", z-1, "est : ", count * volume_voxel, "cm3")

##############################################################################################################################################################

#################################### Information display for each patient ######################################################################################    
    t2=time.time()
    print('\n')
    print ("Total volume intersecting tangential line shifted from:  ", OFFSET_cm,"is" ,  count*volume_voxel , "cm3")
    # print("\n")   
    # print("Le volume de coeur pour vérifier est : ",count_pixel*volume_voxel)
    print("\n")
    print("Gantry statistics:  \n \t moyen est  : ", np.mean(List_angle), " \n \t mininum est : ", np.min(List_angle), " \n \t maximum est : ", np.max(List_angle))
    print("\n")
    print("Done for patient Id n°" , y , 'in',t2-t1, "  secondes")
####################################################################################################################################################

t3=time.time()
print("All patient data are displayed in :", t3-t0, "secondes")
