# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 11:35:41 2021

@author: i-achag
"""
from dataset import Dataset 
import nibabel as nib
import numpy as np 
import os 


class Import:
    
    def __init__(self, path,List_Nom ):
        self.path=path
        self.List_Nom=List_Nom
        self.Function=Dataset(self.path,"OUTPUT",self.List_Nom)
        self.File_Ext_nii=r".nii"
        self.File_Ext_rs=r".dcm"
        
        
        
        self.List_Final_nii , self.List_Final_rs = self.read_nii_file()
        
    # Save masks thanks to dataset.py from git of Brou Boni Kevin
    def Save_masks_in_path(self):
        self.Function.make_png()
    
    #Return the list of the patient included in the path 
    def list_patient_path(self):
        List_Patient=[]
        print("Patient Id's are :")
        for y in os.listdir(self.path):
            List_Patient.append(y)
        return List_Patient
    
    #Select the file with the Patient number name 
    def select_specific_file(self,patient_Number):
        for y in os.listdir(self.path):
            if y == patient_Number:
                path_read_nii=self.path+"/"+y
        return path_read_nii
    
    def find_i(self, Name):
        for i in range(len(self.List_Nom)):
            if self.List_Nom[i] == Name:
                return i 
        
    
    def read_nii_file(self):
        List_Final_nii=[]
        List_Final_rs=[]
        for y in os.listdir(self.path):
            specific_path=self.select_specific_file(y)
            # print("Id Patient : ",y)
            Fichiers=[os.path.join(specific_path+"/"+"/output", _) for _ in os.listdir(specific_path+"/"+"/output") if _.endswith(self.File_Ext_nii)]
            List_Final_nii=List_Final_nii+Fichiers

            Datapath_RS=[os.path.join(self.path+"/"+y, _) for _ in os.listdir(self.path+"/"+y) if  _.endswith(self.File_Ext_rs) ]
            
            for j in Datapath_RS:
                if "RS" in j:
                    List_Final_rs.append(j)
                    
            # path=self.path+'/'+y+'/'
            
            
        return List_Final_nii , List_Final_rs
        
    def return_positions(self,patient_id,Nom):
        path=self.path+ "/" + str(patient_id) + "/output"

        for m in os.listdir(path):
            for i in self.List_Nom:
                if 'mask_'+i.replace(" ","-") in m and Nom in m :
                    img_=nib.load(path+'/'+m)
                    List_position=list((np.argwhere( np.fliplr(np.asarray(img_.get_fdata(dtype=np.float32))) ==1)))

                    return  img_ , List_position
   
        
        