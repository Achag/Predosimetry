# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 09:06:19 2021

@author: i-achag
"""

from dicompylercore import dicomparser, dvh, dvhcalc
dp = dicomparser.DicomParser("C:/Temp/Temp/101339/RS1.2.752.243.1.1.20210315095609551.2000.71023.dcm")

# i.e. Get a dict of structure information
structures = dp.GetStructures()



# Access DVH data
# rtdose = dicomparser.DicomParser("C:/Temp/Not_For_Deep_Learning/101339/RD1.2.752.243.1.1.20210315112329612.3100.83646.dcm")
# heartdvh = dvh.DVH.from_dicom_dvh(rtdose.ds, 5)

# heartdvh.describe()
# Structure: Heart
# DVH Type:  cumulative, abs dose: Gy, abs volume: cm3
# Volume:    437.46 cm3
# Max Dose:  3.10 Gy
# Min Dose:  0.02 Gy
# Mean Dose: 0.64 Gy
# D100:      0.00 Gy
# D98:       0.03 Gy
# D95:       0.03 Gy
# D2cc:      2.93 Gy

# Calculate a DVH from DICOM RT data
calcdvh = dvhcalc.get_dvh("C:/Temp/Temp/101339/RS1.2.752.243.1.1.20210315095609551.2000.71023.dcm", "C:/Temp/Temp/101339/RD1.2.752.243.1.1.20210315112329612.3100.83646.dcm", 8)
print(calcdvh.max,calcdvh.min,calcdvh.D50)


# >>> calcdvh.max, calcdvh.min, calcdvh.D2cc
# (3.0899999999999999, 0.029999999999999999, dvh.DVHValue(2.96, 'Gy'))