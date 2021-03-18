# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 15:41:40 2021

@author: i-achag
"""


import numpy as np 
from iteration_utilities import duplicates
from iteration_utilities import unique_everseen
from math import acos, degrees, isnan

class Geometrical_points:
    def __init__(self,Name):
        self.Name=Name
    
    # i correspond à l'indice de position pour le Name 
    def Attribute_Name (self , i , img , position):
        img_Name = img[i]
        position_Name = position[i]
        return img_Name , position_Name
    
    
    def limite_z(self,position_coeur,position_sein):
        List_z_coeur=[]
        List_z_Sein=[]
        List_tot_z=[]
        
        for i in position_coeur:
            List_z_coeur.append(i[2])

        for j in position_sein:
            List_z_Sein.append(j[2])
            
        List_z_coeur=list(unique_everseen(duplicates(List_z_coeur)))            
        List_z_Sein=list(unique_everseen(duplicates(List_z_Sein)))
        
        slice_barycenter= int(np.ceil((np.min(List_z_Sein) + np.max(List_z_Sein)) / 2) )
        
        List_tot_z= List_z_Sein + List_z_coeur
        mini=np.min(List_tot_z)
        maxi= np.max(List_tot_z)
        
        return mini , maxi , slice_barycenter
    
    def volume(self, img_coeur,img_sein):
    
        if img_sein.shape == img_coeur.shape:
            
            hdr=img_coeur.header['pixdim']
        
            volume_voxel=hdr[3]*hdr[1]*hdr[2]*0.001
        
        return volume_voxel
    
    def compare_imgs(self, img_coeur,img_sein,position_coeur,position_sein,z):
    
        if img_sein.shape == img_coeur.shape:
            position_coeur_slice_z=[]
            position_sein_slice_z=[]
            

            for p in position_coeur:
                if p[2]==z:
                    position_coeur_slice_z.append(p)
                    
            for k in position_sein:
                if k[2]==z:
                    position_sein_slice_z.append(k)
                
                    
            return position_coeur_slice_z,position_sein_slice_z
    
    def droite_directrice(self,Xa,Ya,Xb,Yb):
        m=(Yb-Ya)/(Xb-Xa)
        p=Ya-m*Xa
        return m,p
    
    
    def point_au_dessus_droite(self,x,y,m,p):

        return(y-(m*x+p)>0)
    

    def Verification_barycentre_table(self,x_barycenter,y_barycenter,List_Couch_x_slice_barycenter,List_Couch_y_slice_barycenter,size):
        xmin=min(List_Couch_x_slice_barycenter)
        ymin=min(List_Couch_y_slice_barycenter)
        ymax=max(List_Couch_y_slice_barycenter)
        
        point_haut=[xmin,ymax]
        point_bas=[xmin,ymin]
        
        if np.sqrt((point_haut[0]-x_barycenter)**2+(point_haut[1]-y_barycenter)**2)> 47.5/size:
            x_barycenter= x_barycenter - (np.sqrt((point_haut[0]-x_barycenter)**2+(point_haut[1]-y_barycenter)**2) - 45/size)/(np.sqrt(2))
            y_barycenter= y_barycenter - (np.sqrt((point_haut[0]-x_barycenter)**2+(point_haut[1]-y_barycenter)**2) - 45/size)/(np.sqrt(2))
            return x_barycenter,y_barycenter
        
        if np.sqrt((point_bas[0]-x_barycenter)**2+(point_bas[1]-y_barycenter)**2)> 47.5/size:
            x_barycenter= x_barycenter - (np.sqrt((point_bas[0]-x_barycenter)**2+(point_bas[1]-y_barycenter)**2) - 45/size)/(np.sqrt(2))
            y_barycenter= y_barycenter - (np.sqrt((point_bas[0]-x_barycenter)**2+(point_bas[1]-y_barycenter)**2) - 45/size)/(np.sqrt(2))
            return x_barycenter,y_barycenter
        else:
            return x_barycenter,y_barycenter
    
    
    def Select_Slice_And_Define_Anlge(self, img_coeur, img_sein, position_coeur, position_sein, z, count_pixel, OFFSET_cm, List_angle ):
        
        position_coeur_slice_z,position_sein_slice_z = self.compare_imgs(img_coeur,img_sein,position_coeur,position_sein,z)
    
        count_pixel=count_pixel + len(position_coeur_slice_z)
        
        ConditionA,Xa,Ya=self.trouver_point(position_sein_slice_z,'A',OFFSET_cm)
        ConditionB,Xb,Yb=self.trouver_point(position_sein_slice_z,'B',OFFSET_cm)
        
        try:
            cosangle=np.abs(Xb-Xa)/np.sqrt(np.abs(Ya-Yb)**2+np.abs(Xb-Xa)**2)
            angle= 270 + degrees(acos(cosangle))
            List_angle.append(angle)
        # print("Angle de la droite est " , angle)
        except:
            pass
        return List_angle, 