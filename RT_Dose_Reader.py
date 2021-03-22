# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 09:06:19 2021

@author: i-achag
"""

from dicompylercore import dicomparser, dvh, dvhcalc
import os
import pydicom

List_ROI=['Coeur','Sein G']


datapath="C:/Temp/DIBH"

List_Of_ROI=[]
for i in List_ROI:
    List_Of_ROI.append(i.replace(" ","-"))



List_Patient=os.listdir("C:/Temp/DIBH")
List=[]
for y in List_Patient:
    List.append(y)
    print("Patient Id : ",y)
    Fichiers=[os.path.join(datapath+"/"+str(y)+'/DIBH/', _) for _ in os.listdir(datapath+"/"+str(y)+'/DIBH/') if _.endswith(r".dcm")]
    
    
    
    for i in Fichiers:
        if 'RD' in i:
            Fichier_RD=i
        if 'RS' in i:
            Fichier_RS=i
        if 'CT' in i:
            Fichier_CT=i
            
    ds = pydicom.read_file(Fichier_CT).PatientID

    dp = dicomparser.DicomParser(Fichier_RS)

    
    # i.e. Get a dict of structure information
    structures = dp.GetStructures()
    New_structures = []

    for j in List_ROI : 
        #print(j)
        try:
            for i in list(structures):
                
                if  j == structures[i]["name"]:

                    indice=i

                    calcdvh = dvhcalc.get_dvh(str(Fichier_RS), str(Fichier_RD), indice)
                    print('\n pour le  '+str(structures[i]["name"])+' : ' , '\n \t Dose max : ', calcdvh.max," \n \t Dose min : ",calcdvh.min, '\n \t D1cc : ',calcdvh.D1cc,'\n \t D50 ',calcdvh.D50)
                
                    
        except:
            pass
    
# print(indice_Sein_G,indice_Coeur)


#print(List)

# # Calculate a DVH from DICOM RT data
# calcdvh = dvhcalc.get_dvh(str(Fichier_RS), str(Fichier_RD), indice_Coeur)
# print('pour le coeur' ,calcdvh.max,calcdvh.min,calcdvh.D50)

# calcdvh = dvhcalc.get_dvh(str(Fichier_RS), str(Fichier_RD), indice_Sein_G)
# print('pour le sein G' , calcdvh.max,calcdvh.min,calcdvh.D50)


