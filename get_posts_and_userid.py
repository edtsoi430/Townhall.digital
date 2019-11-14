# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 21:52:51 2019

@author: Dominick
"""

import sqlite3
import random
import time
import PIL
#import nltk
#from nltk.stem.lancaster import LancasterStemmer
# word stemmer
#stemmer = LancasterStemmer()

from time import sleep
from facepy import GraphAPI
from io import BytesIO
from PIL import Image

import xlsxwriter

class extract_posts():
    def __init__(self, group_id, api_key):
        '''
        Initilize: Store the group's ID and the apikey associated with the group
        Facepy API key is key otherwisse, we can't scrap any data
        '''
        self.grp_id = group_id
        #the API key make sure to get this
        self.face_py = api_key
    
    def open_workbook(self, col_nmes, out_file):
        '''
        Opens an excel sheet and 1 sheetr for use. 
        I'm considering adding a way to add a second sheet
        
        Note: this function may act weird if it tries to read a comment 
        associate with your account.
        So if the account you have that has the facepy app associated with 
        it and you made a comment, there's no "Name" key when you look for the username
        of an account that facepy is associated with. 
        
        I've also made it so that comments are "indented" inter the post
        they're associated with. At most, we'll have two comment layers as that's Facebook's limit
        
        
        '''
        wb = xlsxwriter.Workbook(out_file)
        sheet1 = wb.add_worksheet()
        cnt = 0
        for i in col_nmes:
            sheet1.set_column(cnt,cnt,70)
            sheet1.write(0, cnt, i)
            cnt += 1
        return wb, sheet1
    
    def extract_posts(self, output_file):
        '''
        Extracts the posts
        '''
        #initilize graph 
        graph = GraphAPI(self.face_py)
        col_names = ["Poster", "Message", "Time"]
        #open a workbook
        wb, sheet1 = self.open_workbook(col_names, output_file)
        sheet1.set_column(3,3,70)
        sheet1.set_column(4,4,40)
        sheet1.set_column(5,5,40)
        
        #the group feed we're extracting from 
        x = graph.get(path = str(self.grp_id) + '/feed', page = False, retry = 3)
        cnt = 1
        for i in range(len(x['data'])):
            if("message" in x['data'][i].keys()):
                #the post we're extracting from
                y = graph.get(path = str(x['data'][i]["id"]) + "?fields=from", 
                              page = False, retry = 3)
                
                if "from" in y.keys():
                    name = (y["from"]["name"])
                else:
                    name = "(you)"
                sheet1.write(cnt, 0, name) 
                sheet1.write(cnt, 1, x['data'][i]['message']) 
                sheet1.write(cnt, 2, x['data'][i]['updated_time']) 
                
                #comments library
                comments = graph.get(path = str(x['data'][i]["id"]) + "?fields=comments", 
                              page = False, retry = 3)
                #checking if there are comments
                if "comments" in comments.keys():
                    for i in range(len(comments["comments"]["data"])):
                        cnt += 1
                        sheet1.write(cnt, 1, comments["comments"]["data"][i]["from"]["name"]) 
                        sheet1.write(cnt, 2, comments["comments"]["data"][i]['message']) 
                        sheet1.write(cnt, 3, comments["comments"]["data"][i]['created_time'])
                        comments_2nd_layer = graph.get(path = str(comments["comments"]["data"][i]["id"]) + "?fields=comments", 
                                  page = False, retry = 3)
                        
                        #checking of comments are in the comments. There are ony two layers
                        if "comments" in comments_2nd_layer.keys():
                            for i in range(len(comments_2nd_layer["comments"]["data"])):
                                cnt += 1
                                sheet1.write(cnt, 2, (comments_2nd_layer["comments"]["data"][i]["from"]["name"])) 
                                sheet1.write(cnt, 3, comments_2nd_layer["comments"]["data"][i]['message']) 
                                sheet1.write(cnt, 4, comments_2nd_layer["comments"]["data"][i]['created_time'])
                    
                cnt += 1
        #close workbook
        wb.close()
                
        