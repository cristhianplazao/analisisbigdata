# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 12:49:33 2020
@author: Miguel Fernandez""
"""
#nltk.download('punkt')
#nltk.download('stopwords')
#nltk.download('brown')
# importing required modules 
import tarfile
import re
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from collections import Counter
from functools import reduce
import sys
import operator
import json
class dataProcess():
    "Principal Constructor"
    def __init__(self,jsondata=None):
        self.__dict__ = json.loads(jsondata)#json file import
        self.tagfilter = "text";# tag validator
        self.maxvalues=3; #files max value permitted
        self.en_stops = set(stopwords.words('english'));
    
    "//Extract data from selected directory//"
    def __extract_data(self):
        result=dict();
        filenames=[];
        try:
            tar = tarfile.open(self.filetar, "r:gz")
    
            for names in self.listdata:
                filenames = filenames + [member for member in tar.getmembers() 
                             if names in str(member)]
            try:
                flag = 0 if len(filenames)>self.maxvalues else len(filenames);
                self.maxvalues/flag;
                for member in filenames:
                    content = tar.extractfile(member);
                    
                    soup = (((BeautifulSoup(str(content.read()),'lxml').
                              findAll(self.tagfilter))));#extract selected tag
                    
                    data =[[result for result in 
                            nltk.word_tokenize(re.sub('[^A-Za-z]+',' ',
                                                      re.sub("\s\s+"," ",
                                                             content.text.
                                                             replace(r'\n',"").lower()))) 
                            if not result in self.en_stops]
                           for content in soup];
                    #Cleaning process using lower case,regex, 
                    #tokenizer, stop word process.
                    test={member.name:data}
                    result.update(test);#Append data processed
                return result #Result data after extract and clean;
            except :
                sys.exit(1)
        except Exception as e:
            return e;
        
    "//Process data by results a point//"
    def __ae_point(self):
        data = self.__extract_data();
        keys=list(data.keys());
        result=[];
        for i in range(0,len(keys)):
            result.append([str(keys[i]),sum([len(member) 
                                             for member in list(data.values())[i]])])
            #result+=sum([len(member) for member in list(data.values())[i]])
        return dict(result)
    
    "//Process data by results b point//"
    def __be_point(self):
        result =Counter(reduce(lambda x,y: x+y,
                       reduce(lambda x,y: x+y,
                              list(self.__extract_data().values()))));
        return result;
    
    "//Process data by results c point//"
    def __cde_point(self):
        return dict([(k, v) for k, v in 
                self.__be_point().most_common(self.topvalue)])
     
    "//Process data by results g point//"       
    def __g_point(self):
        result=[];
        data = self.__extract_data()
        values = list(data.values());
        keys=list(data.keys());
        for i in range(0,len(keys)):
            tmp=dict(Counter(reduce(lambda x,y: x+y,values[i])))
            try:
                result.append([str(keys[i])+" word: "+
                               self.wordfilter,tmp[self.wordfilter]])   
            except:
                continue;
        data=max(self.__ae_point().items(), key=operator.itemgetter(1));
        
        result = dict([member for member in  result 
                       if max(map(lambda x: x[1], result)) in member])
        result.update({data[0]+" max words:":data[1]})
        return result
    
    "//Export json data for web app//"
    def __export_json(self,dictdata={}):
        result=dictdata;
        with open(self.output+'result'+str(self.point)+'.json', 'w') as fp:
            json.dump(result, fp);
    
    "//Process data by results a point//"
    def process_data(self):
        if self.point == 1:
            self.__export_json(self.__ae_point())
        elif self.point==2:
            self.__export_json(self.__be_point())
        elif self.point==3:
            self.__export_json(self.__cde_point())
        elif self.point==4:
            self.__export_json(self.__g_point())
        else:
            sys.exit(0)