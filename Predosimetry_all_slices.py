# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 17:48:37 2021

@author: i-achag
"""

from dataset import Dataset 
import nibabel as nib
import time
import numpy as np 
import os 
import pydicom as dcm
import shutil
from iteration_utilities import duplicates
from iteration_utilities import unique_everseen
import matplotlib.pyplot as plt
from math import acos, degrees, isnan
import scipy

 

# Function=Dataset("C:/Temp/Not_For_Deep_Learning","OUTPUT",["Coeur","Sein G","Carbon Fiber","Paroi G","External"])

# Function_0=Function.make_png()


def volume(img_coeur,img_sein):
    
    if img_sein.shape == img_coeur.shape:
        
        hdr=img_coeur.header['pixdim']
    
        volume_voxel=hdr[3]*hdr[1]*hdr[2]*0.001
    
    return volume_voxel

def size(img_coeur,img_sein):
    
    if img_sein.shape == img_coeur.shape:

        hdr=img_coeur.header['pixdim']
        
        
        size_pixel=hdr[2]*0.1
        # print(img_coeur.shape[0]*size_pixel)
    return size_pixel

def trouver_limite_z(position_coeur,position_sein):
    # position_coeur = np.argwhere(img_coeur.get_fdata(dtype=np.float32)==1)
    # position_sein = np.argwhere(img_sein.get_fdata(dtype=np.float32)==1)
  
    
    # position_coeur = np.argwhere( np.fliplr(np.rot90(np.asarray(img_coeur.get_fdata(dtype=np.float32)), 3)) ==1)
    # position_sein = np.argwhere( np.fliplr(np.rot90(np.asarray(img_sein.get_fdata(dtype=np.float32)), 3)) ==1)
    
    List_z_coeur=[]
    List_z_Sein=[]
    List_tot_z=[]
    
    for i in position_coeur:
        List_z_coeur.append(i[2])
        
    List_z_coeur=list(unique_everseen(duplicates(List_z_coeur)))
    
    mini_coeur=min(List_z_coeur)
    maxi_coeur=max(List_z_coeur)
    for j in position_sein:
        List_z_Sein.append(j[2])
        
    List_z_Sein=list(unique_everseen(duplicates(List_z_Sein)))
    
    slice_barycenter= int(np.ceil((np.min(List_z_Sein) + np.max(List_z_Sein)) / 2) )
    
    List_tot_z=List_z_Sein + List_z_coeur
    mini=np.min(List_tot_z)
    maxi= np.max(List_tot_z)
    
    return mini , maxi , slice_barycenter,mini_coeur,maxi_coeur

def Anneau_and_Couch(slice_barycenter,position_CouchSurface):
        # position_Anneau_slice_barycenter=[]
        position_CouchSurface_slice_barycenter=[]
        
        
        # for k in position_Anneau:
        #     if k[2]==slice_barycenter:
        #         position_Anneau_slice_barycenter.append(k)
        for p in position_CouchSurface:
            if p[2]==slice_barycenter:
                position_CouchSurface_slice_barycenter.append(p)
        return position_CouchSurface_slice_barycenter   

#Défini les positions x,y du coeur et du sein sur la coupe Z 

def compare_imgs(img_coeur,img_sein,position_coeur,position_sein,z):
    

    if img_sein.shape == img_coeur.shape:
        position_coeur_slice_z=[]
        position_sein_slice_z=[]

        
        # position_coeur = np.argwhere(img_coeur.get_fdata(dtype=np.float32)==1)
        # position_sein = np.argwhere(img_sein.get_fdata(dtype=np.float32)==1)
        
        # position_coeur = np.argwhere( np.fliplr(np.rot90(np.asarray(img_coeur.get_fdata(dtype=np.float32)), 3)) ==1)
        # position_sein = np.argwhere( np.fliplr(np.rot90(np.asarray(img_sein.get_fdata(dtype=np.float32)), 3)) ==1)
        
        
        # tuple1 = [tuple(l) for l in position_coeur]

        # tuple2 = [tuple(l) for l in position_sein]
        
        # count=len(set(tuple1) & set(tuple2))
        
        # hdr=img_coeur.header['pixdim']
        # print(count*hdr[2]*hdr[0]*hdr[1]*0.001,"cm^3")
        for p in position_coeur:
            if p[2]==z:
                position_coeur_slice_z.append(p)
                
        for k in position_sein:
            if k[2]==z:
                position_sein_slice_z.append(k)
            
                
        return position_coeur_slice_z,position_sein_slice_z


def droite_directrice(Xa,Ya,Xb,Yb):
    m=(Yb-Ya)/(Xb-Xa)
    p=Ya-m*Xa
    return m,p

def point_au_dessus_droite(x,y,m,p):

    return(y-(m*x+p)>0)

def trouver_point(position,Name,offset_cm):
    x_pos=[]
    y_pos=[]
    Condition=True
    offset_x_y_cm= offset_cm/(np.sqrt(2)*size(img_coeur,img_sein))
    
    
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
        
    if str(Name)=='C'  :
        for i in position:
            y_pos.append(i[1])
        if len(y_pos)!=0:
            yAmax=max(y_pos)
        else:
            Condition=False
            
        for j in position:
            if j[1]==yAmax:
                x_pos.append(j[0])
        if len(x_pos)!=0:
            xAmin=min(x_pos)
            return Condition, xAmin-offset_x_y_cm, yAmax-offset_x_y_cm
        
        else:
            Condition=False
            return(Condition,1000,1000)
        
        
def f(x,m,p):
    return m * x + p


def Verification_barycentre_table(x_barycenter,y_barycenter,List_Couch_x_slice_barycenter,List_Couch_y_slice_barycenter,size):
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
  
# def getPointList(contourDataset, dispNbPoints = False):
#     c1 = contourDataset.ContourData
#     nbpoints = int(contourDataset.NumberOfContourPoints)
#     if dispNbPoints: print("Nb of points in the structure on that slice:", nbpoints)
       
#     pointList = []
#     for i in range (0,nbpoints):
#         x1 = c1[(i*3)]
#         y1 = c1[(i*3)+1]
#         pointList.append((x1, y1))
       
#     return pointList
 

# class coordConverter:
    
#     def __init__(self, xorigin, yorigin, pixsizex, pixsizey, dimx, dimy):
#         self.xorigin = xorigin
#         self.yorigin = yorigin
#         self.pixsizex = pixsizex
#         self.pixsizey = pixsizey
#         self.dimx = dimx
#         self.dimy = dimy

#     def convertCoord(self, x, y):
#         newposx = int(round((x-self.xorigin)/self.pixsizex))
#         newposy = int(round((y-self.yorigin)/self.pixsizey))
#         return (newposx, newposy)
    
#     def converStructList(self, structList):
#         newPointList = []
#         for i in structList:
#             newposx = int(round((i[0]-self.xorigin)/self.pixsizex))
#             newposy = int(round((i[1]-self.yorigin)/self.pixsizey))
#             newPointList.append((newposx, newposy))
#         return newPointList

# def getCTdictionary(path):
    
#     # handles `/` missing
#     if path[-1] != '/': path += '/'
    
#     # gets the list of filenames:
#     fpaths = [path + f for f in os.listdir(path) if ('.dcm' in f or '.DCM' in f)]
    
#     # reads all files and creates dictionary
#     n = 0
#     CTdict = {}
#     for fpath in fpaths:
#         f = dcm.read_file(fpath)
#         if ('Modality' in dir(f))and(f.Modality=='CT'):
#             CTdict.update({f.SOPInstanceUID : fpath})
#             n += 1
            
            
#     if n==0: print('No CT file found in this directory.')
    
#     return CTdict


# def reads_CT_image_corresponding_slice_of_interest(x, y):
#         imgID, c_data,List_slice_RS,m_ROInb= SPECT_infos(x , y,data,'Coeur')
#         CTimg = dcm.read_file(getCTdictionary(path)[imgID])

 

#         m_CTxSpacing, m_CTySpacing = float(CTimg.PixelSpacing[0]), float(CTimg.PixelSpacing[1])
#         m_CTxOrigin, m_CTyOrigin, CTzOrigin = CTimg.ImagePositionPatient 
#         m_CTsizeX, m_CTsizeY = CTimg.Rows, CTimg.Columns
        
#         return CTimg, (m_CTxSpacing, m_CTySpacing), (m_CTxOrigin, m_CTyOrigin, CTzOrigin),(m_CTsizeX, m_CTsizeY)
    
    
# def SPECT_infos(x, y,data,Name):
#         ListName=[]
#         for i in data[0x3006,0x0080]:
#             ListName.append(i[0x3006,0x0085].value)
#         for j in range (len(ListName)):
#             if str(Name) in ListName[j]:
#                 m_ROInb=j
#         List_slice_RS=[data.ROIContourSequence[m_ROInb].ContourSequence]
#         c_data = data.ROIContourSequence[m_ROInb].ContourSequence[y]
#         imgID = c_data.ContourImageSequence[0].ReferencedSOPInstanceUID
#         return imgID, c_data,List_slice_RS,m_ROInb;    

# def display_CT_contour(pointList, m_CTxOrigin, m_CTyOrigin, m_CTxSpacing, m_CTySpacing, m_CTsizeX, m_CTsizeY):
#         cc1 = coordConverter(m_CTxOrigin, m_CTyOrigin, m_CTxSpacing, m_CTySpacing, m_CTsizeX, m_CTsizeY)
#         CT_pointList = cc1.converStructList(pointList)
#         return CT_pointList
    
# def getPointList(contourDataset, dispNbPoints = False):
#         c1 = contourDataset.ContourData
#         nbpoints = int(contourDataset.NumberOfContourPoints)
#         if dispNbPoints: print("Nb of points in the structure on that slice:", nbpoints)
   
#         pointList = []
#         for i in range (0,nbpoints):
#             x1 = c1[(i*3)]
#             y1 = c1[(i*3)+1]
#             pointList.append((x1, y1))
   
#         return pointList
     
List_Final=[]
datapath="C:/Temp/Not_For_Deep_Learning"
fileExt=r".nii"
print(os.listdir(datapath))

for y in os.listdir(datapath):
    print("Id Patient : ",y)
    Fichiers=[os.path.join(datapath+"/"+y+"/"+"/output", _) for _ in os.listdir(datapath+"/"+y+"/"+"/output") if _.endswith(fileExt)]
    List_Final=List_Final+Fichiers
    fileExt_RS=r".dcm"
    Datapath_RS=[os.path.join(datapath+"/"+y, _) for _ in os.listdir(datapath+"/"+y) if  _.endswith(fileExt_RS) ]
    for j in Datapath_RS:
        if "RS" in j:
            data=dcm.read_file(j)
            
    path=datapath+'/'+y+'/'
            
    t1=time.time()
    for m in List_Final:
        
        if 'mask_Coeur' in m:
            img_coeur=nib.load(m)
        if 'mask_Sein-G' or 'Paroi-G'in m:
            img_sein=nib.load(m)
            if 'Paroi-G' in m:
                print("Paroi!!")
        if 'mask_Carbon-Fiber' in m:
            img_couch=nib.load(m)

            
            
    position_coeur = np.argwhere( np.fliplr(np.asarray(img_coeur.get_fdata(dtype=np.float32))) ==1)
    position_sein = np.argwhere(np.fliplr(np.asarray(img_sein.get_fdata(dtype=np.float32))) ==1)
    position_CouchSurface = np.argwhere(np.fliplr(np.asarray(img_couch.get_fdata(dtype=np.float32))) ==1)    
    # position_Anneau = np.argwhere(np.fliplr(np.asarray(img_anneau.get_fdata(dtype=np.float32))) ==1)
    
       
    mini, maxi, slice_barycenter,mini_coeur,maxi_coeur = trouver_limite_z(position_coeur,position_sein)
    #Done
    volume_voxel= volume(img_coeur, img_sein)
    
    count=0
    
    List_angle=[]
    List_Anneau_x_slice_barycenter=[]
    List_Anneau_y_slice_barycenter=[]
    List_Couch_x_slice_barycenter=[]
    List_Couch_y_slice_barycenter=[]
    
    count_pixel=0
    
    # 
    
    for z in range (mini,maxi,1):
        List_coeur_x=[]
        List_coeur_y=[]
        List_sein_x=[]
        List_sein_y=[]
        List_point=[]
        
        position_coeur_slice_z,position_sein_slice_z = compare_imgs(img_coeur,img_sein,position_coeur,position_sein,z)
        count_pixel=count_pixel + len(position_coeur_slice_z)    
        
        OFFSET_cm=0.3
        
        ConditionA,Xa,Ya=trouver_point(position_sein_slice_z,'A',OFFSET_cm)
        ConditionB,Xb,Yb=trouver_point(position_sein_slice_z,'B',OFFSET_cm)
        
        
        try:
            cosangle=np.abs(Xb-Xa)/np.sqrt(np.abs(Ya-Yb)**2+np.abs(Xb-Xa)**2)
            angle= 270 + degrees(acos(cosangle))
            List_angle.append(angle)
        # print("Angle de la droite est " , angle)
        except:
            pass
        x=np.linspace(0,img_coeur.shape[0],1000)
        # print (ConditionA,"conditionA",ConditionB,"conditionB")
        
        
        if ConditionA == True and ConditionB==True:
            
            
            # if z-mini < maxi_coeur-mini_coeur and z-mini > 0:
                
            #     List_x_RS=[]
            #     List_y_RS=[]
            #     List_point_RS=np.zeros((512,512))
        
            #     imgID,c_data,List_slice_RS,m_ROInb=SPECT_infos(7, z-mini,data,'Coeur')
                
                
            #     pointList=getPointList(c_data)
            #     CTimg,CTspacing,CTorigin,CTsize=reads_CT_image_corresponding_slice_of_interest(m_ROInb, z-mini)
            #     CT_pointList=display_CT_contour(pointList, CTorigin[0], CTorigin[1], CTspacing[0], CTspacing[1], CTsize[0], CTsize[1])
                
            #     for i in CT_pointList:
            #         List_point.append([float(i[0]),float(i[1])])
            #     for i in List_point:
            #         List_point_RS[int(i[0])][int(i[1])]=1
    
            #     List_point=np.argwhere(np.flipud(np.fliplr(np.rot90(np.asarray(List_point_RS),3))) ==1)
                
            #     for i in List_point:
            #         List_x_RS.append(i[0])
            #         List_y_RS.append(i[1]) 
            
            
            m,p=droite_directrice(Xa, Ya, Xb, Yb)
            
            for i in position_coeur_slice_z:
                List_coeur_x.append(i[0])
                List_coeur_y.append(i[1])
                if point_au_dessus_droite(i[0], i[1], m, p)==True:
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
            





