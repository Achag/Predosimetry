# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 15:41:40 2021

@author: i-achag
"""


import numpy as np 
from iteration_utilities import duplicates
from iteration_utilities import unique_everseen
from math import acos, degrees

class Geometrical_points:
    def __init__(self,Name):
        self.Name=Name
    
    #Return the position of the minimum slice number between the lowest position of breast and heart
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
        # print("Mini = ", mini, "Maxi = ",maxi)
        return mini , maxi , slice_barycenter
    
    
    #Return the size in cm of a pixel
    def size(self,img_coeur,img_sein):
    
        if img_sein.shape == img_coeur.shape:
    
            hdr=img_coeur.header['pixdim']
            
            
            size_pixel=hdr[2]*0.1
            # print(img_coeur.shape[0]*size_pixel)
        return size_pixel
    

    #Return the volume of a voxel  
    def volume(self, img_coeur,img_sein):
    
        if img_sein.shape == img_coeur.shape:
            
            hdr=img_coeur.header['pixdim']
        
            volume_voxel=hdr[3]*hdr[1]*hdr[2]*0.001
        
        return volume_voxel
    
    #Return all the position of positions of the couch in the slice on which is defined the barycenter
    def Anneau_and_Couch(self,slice_barycenter,position_CouchSurface):
        # position_Anneau_slice_barycenter=[]
        position_CouchSurface_slice_barycenter=[]
        
        
        # for k in position_Anneau:
        #     if k[2]==slice_barycenter:
        #         position_Anneau_slice_barycenter.append(k)
        for p in position_CouchSurface:
            if p[2]==slice_barycenter:
                position_CouchSurface_slice_barycenter.append(p)
        return position_CouchSurface_slice_barycenter
    
    
    #Return positions of breast and heart for the ongoing slice z  
    def compare_imgs(self, img_coeur,img_sein,position_coeur,position_sein,z):
    
        if img_sein.shape == img_coeur.shape:
            position_coeur_slice_z=[]
            position_sein_slice_z=[]
            
            # tuple1 = [tuple(l) for l in position_coeur]
    
            # tuple2 = [tuple(l) for l in position_sein]
            
            # count=len(set(tuple1) & set(tuple2))

            for p in position_coeur:
                if p[2]==z:
                    position_coeur_slice_z.append(p)
                    
            for k in position_sein:
                if k[2]==z:
                    position_sein_slice_z.append(k)
                
                    
            return position_coeur_slice_z,position_sein_slice_z
    
    
    #Return line coefficient fitting the point A(Xa,Ya) and B(Xb,Yb)
    def droite_directrice(self,Xa,Ya,Xb,Yb):
        m=(Yb-Ya)/(Xb-Xa)
        p=Ya-m*Xa
        return m,p
    
    #Return True if the point (x,y) is above the line defined in droite_directrice
    def point_au_dessus_droite(self,x,y,m,p):

        return(y-(m*x+p)>0)
    
    #Find the top left position of a structure for the 'A' point and the point at the at the bottom right for the 'B' point
    def trouver_point(self,position, Name, offset_cm, img_coeur, img_sein):
        x_pos=[]
        y_pos=[]
        Condition=True
        offset_x_y_cm= offset_cm/(np.sqrt(2)*self.size(img_coeur,img_sein))
        
        
        if str(Name) == "A" : 
    
            for i in position:
                x_pos.append(i[0])
            if len(x_pos)!=0:
                xAmin=min(x_pos)
            else:
                Condition=False
                
            for j in position:
                if j[0]==xAmin:
                    y_pos.append(j[1])
            if len(y_pos)!=0:
                yAmin=min(y_pos)
                return Condition, xAmin-offset_x_y_cm, yAmin-offset_x_y_cm
            else:
                Condition=False
                return Condition, 1000, 1000
        
        if str(Name)=='B'  :
            for i in position:
                y_pos.append(i[1])
            if len(y_pos)!=0:
                yAmin=min(y_pos)
            else:
                Condition=False
                
            for j in position:
                if j[1]==yAmin:
                    x_pos.append(j[0])
            if len(x_pos)!=0:
                xAmin=min(x_pos)
                return Condition, xAmin-offset_x_y_cm, yAmin-offset_x_y_cm
            
            else:
                Condition=False
                return(Condition,1000,1000)
    
    #function used to create the ordinates of the line
    def f(self,x,m,p):
        return m * x + p
    
    # Return coordinates of the barycenter taking into account the ring diameter
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
    
    
    # Return all the variable needed to plot out Heart, Breast, line,barycenter point and the table 
    def Select_Slice_And_Define_Angle(self, img_coeur, img_sein, position_coeur, position_sein, z, count_pixel, OFFSET_cm, List_angle ):
        
        position_coeur_slice_z,position_sein_slice_z = self.compare_imgs(img_coeur,img_sein,position_coeur,position_sein,z)
    
        count_pixel=count_pixel + len(position_coeur_slice_z)
        
        ConditionA,Xa,Ya=self.trouver_point(position_sein_slice_z,'A',OFFSET_cm, img_coeur, img_sein)
        ConditionB,Xb,Yb=self.trouver_point(position_sein_slice_z,'B',OFFSET_cm, img_coeur, img_sein)
        
        if np.sqrt(np.abs(Ya-Yb)**2+np.abs(Xb-Xa)**2) !=0:
            cosangle=np.abs(Xb-Xa)/np.sqrt(np.abs(Ya-Yb)**2+np.abs(Xb-Xa)**2)
            angle= 270 + degrees(acos(cosangle))
            List_angle.append(angle)

        return List_angle, position_coeur_slice_z, position_sein_slice_z, ConditionA, Xa, Ya, ConditionB, Xb, Yb, count_pixel