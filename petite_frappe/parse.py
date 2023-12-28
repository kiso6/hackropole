#!/usr/bin/python3
import pandas as pd
import numpy as np


lol = pd.read_csv(open("petite_frappe_2.txt","r+"),sep=" ")
otput=open("otp.txt","a+")
otput.write(str(np.array(lol.iloc[:,2])))
