# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 12:41:44 2020
@author: Miguel Fernández
"""
from process_data_class import dataProcess as dp
import json
import sys
def main():
    with open('C:/projects/laboratorio_1/jsonref.json') as f:
        jsondata2 = str(json.load(f)).replace("'",'"')
    obj= dp(jsondata2)
    obj.process_data()
    print ("The script has the name %s" % (len(sys.argv[0])))
           
if __name__ == "__main__":
    main()