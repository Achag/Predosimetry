# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 12:12:23 2021

@author: i-achag
"""
import time 
import numpy as np

from Import import Import 
from Geometrical_points import Geometrical_points

# importera=Import("C:/Temp/Not_For_Deep_Learning",["Coeur","Sein G","Carbon Fiber","Paroi G","External"])


# # #Génération des masks de la liste renseignée 
# # importera.Save_masks_in_path()


# # # Print tout les nii et rs présents  
# # nii , rs = importera.read_nii_file()

# patient_Number_exemple="305322"
# path_read_nii=importera.select_specific_file(patient_Number_exemple)
# print(path_read_nii)


# # # Affiche les Ids Patient dans le path référencé 
# # List_Patient=importera.list_patient_path()

# t1=time.time()
# List_imgs , List_positions=importera.return_positions()
# t2=time.time()
# print(t2-t1)
# # # Montre les listes des images importés et la liste des positions des différentes structures renseignés 
# # print(List_imgs,positions)

# # Vérifie que la longeur de List_imgs et poisitions est similaire 
# # print(len(List_imgs),len(List_positions))

# # i=importera.find_i("Sein G")
# # print(i)
# # ##########################################################################################################


# Geometric=Geometrical_points("Sein G")
# img_Sein , position_Sein = Geometric.Attribute_Name(i , List_imgs , List_positions)

# print(img_Sein,position_Sein)


################################################################################################################
################################################################################################################
################################################################################################################

importer=Import("C:/Temp/Not_For_Deep_Learning",["Coeur","Sein G","Carbon Fiber","Paroi G","External"])
Geometric=Geometrical_points("Sein G")

OFFSET_cm=3


List_imgs , List_positions=importer.return_positions()

img_sein , position_sein = Geometric.Attribute_Name(0, List_imgs , List_positions)
img_coeur , position_coeur = Geometric.Attribute_Name(1 , List_imgs , List_positions ) or Geometric.Attribute_Name(3 , List_imgs , List_positions )
position_CouchSurface = Geometric.Attribute_Name(2 , List_imgs , List_positions)[1]

mini, maxi, slice_barycenter = Geometric.limite_z(position_coeur,position_sein)

volume_voxel= Geometric.volume(img_coeur, img_sein)
 
List_angle , List_Anneau_x_slice_barycenter , List_Anneau_y_slice_barycenter , List_Couch_x_slice_barycenter , List_Couch_y_slice_barycenter  = [], [], [], [], []

count=0
count_pixel=0

for z in range (mini, maxi, 1):
    List_coeur_x , List_coeur_y , List_sein_x , List_sein_y , List_point = [] , [] , [] , [] , []   
    

    List_angle, , , , ,  = Select_Slice_And_Define_Angle()
    
    x=np.linspace(0,img_coeur.shape[0],1000)
    
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
            
        
   
                
        plt.figure(z)
        # if z-mini < maxi_coeur-mini_coeur and z-mini > 0:
        #     plt.scatter(List_y_RS,List_x_RS,marker=".",color='blue')

        g1=plt.scatter(List_coeur_x,List_coeur_y, marker=".",color='red')
        g2=plt.scatter(List_sein_x,List_sein_y, marker=".",color='pink')
        g3=plt.plot(x,f(x,m,p),color='red')
        plt.title("Image de la coupe "+str(z)+" Id Patient : "+ str(y))
        plt.xlabel("pixel en x ")
        plt.ylabel("pixel en y ")
        plt.legend([g1,g2], ['Coeur', 'sein'],loc = 'upper left', ncol = 2, scatterpoints = 1,frameon = True, markerscale = 2,borderpad = 0.5, labelspacing = 0.5)



        if z == slice_barycenter:
            position_CouchSurface_slice_barycenter = Anneau_and_Couch(slice_barycenter,position_CouchSurface)
            

            
            x_barycenter= sum(List_sein_x)/ len(List_sein_x)
            y_barycenter= sum(List_sein_y)/ len(List_sein_y)                        
            
            
            for j in position_CouchSurface_slice_barycenter:
                List_Couch_x_slice_barycenter.append(j[0])
                List_Couch_y_slice_barycenter.append(j[1])
            
            print("\n")
            print("Sur la coupe "+str(slice_barycenter)+" : ")
            
            print("\n")
            
            print("les coordonnées du barycentre avant vérification sont : (",x_barycenter*size(img_coeur,img_sein),",",y_barycenter*size(img_coeur,img_sein),") en cm  ")
            
            g4=plt.scatter(x_barycenter,y_barycenter, marker="+")

            x_barycenter,y_barycenter=Verification_barycentre_table(x_barycenter,y_barycenter,List_Couch_x_slice_barycenter,List_Couch_y_slice_barycenter,size(img_coeur,img_sein))
            
            print("\n")
            print("les coordonnées du barycentre après vérification sont : (",x_barycenter*size(img_coeur,img_sein),",",y_barycenter*size(img_coeur,img_sein),")  en cm  ")

            g5=plt.scatter(x_barycenter,y_barycenter, marker="+")
            
            
            # Xm=(min(List_Anneau_x_slice_barycenter)+max(List_Anneau_x_slice_barycenter))/2
            # Ym=(min(List_Anneau_y_slice_barycenter)+max(List_Anneau_y_slice_barycenter))/2

            
            # offset_x=x_barycenter-Xm
            # offset_y=y_barycenter-Ym
            
            # List_Anneau_x_slice_barycenter=list(np.array(List_Anneau_x_slice_barycenter)+offset_x)
            # List_Anneau_y_slice_barycenter=list(np.array(List_Anneau_y_slice_barycenter)+offset_y)
           
            
            # plt.scatter(List_Anneau_x_slice_barycenter,List_Anneau_x_slice_barycenter, marker=".")
            
            # plt.Circle((x_barycenter, y_barycenter), 45/size(img_coeur,img_sein) ,fill=False)
            # plt.subplots()
            
            
            g6=plt.scatter(List_Couch_x_slice_barycenter,List_Couch_y_slice_barycenter, marker=".")           
    
            # plt.scatter(Xm,Ym, marker="+" )
                
            plt.legend([g1,g2,g4,g5,g6], ['Coeur', 'sein','Barycentre avant optimisation', 'barycentre ajusté','Table de Traitement'],loc = 'upper left', ncol = 1, scatterpoints = 1,frameon = True, markerscale = 1,borderpad = 0.5, labelspacing = 0.5)
            
            
            
        plt.show()
        
        
        
    # print ("Le volume intersecté depuis la Slice " , mini+1 , "à ", z-1, "est : ", count * volume_voxel, "cm3")
    # print("\n")

t2=time.time()

print('\n')

print ("Le volume de coeur intersectant la tangente est  :  ", count*volume_voxel , "cm3")

print("\n")  

print("Le volume de coeur pour vérifier est : ",count_pixel*volume_voxel)


List_angle=[x for x in List_angle if isnan(x) == False]


print("\n")

print("Statistique gantry:  \n \t moyen est  : ", np.mean(List_angle), " \n \t mininum est : ", np.min(List_angle), " \n \t maximum est : ", np.max(List_angle))
print("\n")

print("Le temps de calcul est de:",t2-t1, "  secondes")

