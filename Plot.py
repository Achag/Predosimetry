# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 09:24:25 2021

@author: i-achag
"""
import matplotlib.pyplot as plt 


class Plot:
    def __init__(self,List_coeur_x,List_coeur_y,List_sein_x,List_sein_y,x,y,z,m,p,slice_barycenter,List_Couch_x_slice_barycenter,List_Couch_y_slice_barycenter,position_CouchSurface):
        self.List_coeur_x = List_coeur_x
        self.List_coeur_y = List_coeur_y
        self.List_sein_x = List_sein_x
        self.List_sein_y = List_sein_y
        self.x = x
        self.y = y
        self.z = z
        self.m = m
        self.p  = p
        self.slice_barycenter = slice_barycenter
        self.List_Couch_x_slice_barycenter = List_Couch_x_slice_barycenter
        self.List_Couch_y_slice_barycenter = List_Couch_y_slice_barycenter
        self.position_CouchSurface = position_CouchSurface
    
    
    def plot(self,f,Anneau_and_Couch,size,Verification_barycentre_table,img_coeur,img_sein):
        
        plt.figure(self.z)
        # if z-mini < maxi_coeur-mini_coeur and z-mini > 0:
        #     plt.scatter(List_y_RS,List_x_RS,marker=".",color='blue')
    
        g1=plt.scatter(self.List_coeur_x,self.List_coeur_y, marker=".",color='red')
        g2=plt.scatter(self.List_sein_x,self.List_sein_y, marker=".",color='pink')
        plt.plot(self.x,f(self.x,self.m,self.p),color='red')
        plt.title("Image de la coupe "+str(self.z)+" Id Patient : "+ str(self.y))
        plt.xlabel("pixel en x ")
        plt.ylabel("pixel en y ")
        plt.legend([g1,g2], ['Heart', 'Breast'],loc = 'upper left', ncol = 2, scatterpoints = 1,frameon = True, markerscale = 2,borderpad = 0.5, labelspacing = 0.5)
    
    
    
        if self.z == self.slice_barycenter:
            position_CouchSurface_slice_barycenter = Anneau_and_Couch(self.slice_barycenter,self.position_CouchSurface)
            
    
            
            x_barycenter= sum(self.List_sein_x)/ len(self.List_sein_x)
            y_barycenter= sum(self.List_sein_y)/ len(self.List_sein_y)                        
            
            
            for j in position_CouchSurface_slice_barycenter:
                self.List_Couch_x_slice_barycenter.append(j[0])
                self.List_Couch_y_slice_barycenter.append(j[1])
            
            print("\n")
            print("On slice number "+str(self.slice_barycenter)+" : ")

            print("barycenter coordinates before verification are : (",x_barycenter*size(img_coeur,img_sein),",",y_barycenter*size(img_coeur,img_sein),") cm  ")
            
            g4=plt.scatter(x_barycenter,y_barycenter, marker="+")
    
            x_barycenter,y_barycenter=Verification_barycentre_table(x_barycenter,y_barycenter,self.List_Couch_x_slice_barycenter,self.List_Couch_y_slice_barycenter,size(img_coeur,img_sein))
            
            print("barycenter coordinates after verification are : (",x_barycenter*size(img_coeur,img_sein),",",y_barycenter*size(img_coeur,img_sein),")  cm  ")
    
            g5=plt.scatter(x_barycenter,y_barycenter, marker="+")
            
            
            
            g6=plt.scatter(self.List_Couch_x_slice_barycenter,self.List_Couch_y_slice_barycenter, marker=".")           
    
    
                
            plt.legend([g1,g2,g4,g5,g6], ['Heart', 'Breast','Barycenter non-adjusted', 'barycenter adjusted','Couch'],loc = 'upper left', ncol = 1, scatterpoints = 1,frameon = True, markerscale = 1,borderpad = 0.5, labelspacing = 0.5)
            
            
            
        plt.show()