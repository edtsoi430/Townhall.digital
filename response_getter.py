# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 11:22:19 2019

@author: Dominick
"""

import uuid
import xlsxwriter
import xlrd
from datetime import datetime


class response():
    def __init__(self, file_nm):
        '''
        Initilizes the class. Only takes in a file name or the path to a file.
        Mainly takes an excel sheet and will organize it into a dictionary
        '''
        #f= open(file_nm, 'r')
        self.response = {}
        self.options = []
        wb = xlrd.open_workbook(file_nm)
        sheet = wb.sheet_by_index(0)
        for i in range(sheet.nrows):
            if i == 0:
                #ignore the first line
                continue
            #list is [id, reponse, number of times called, number of times called ever, times called, character]
            addition = [uuid.uuid4(), sheet.cell_value(i, 2), 0, sheet.cell_value(i, 4), sheet.cell_value(i, 5),  sheet.cell_value(i, 0)]
            #key is the subject
            key = str(sheet.cell_value(i, 1))
            if key not in self.response:
                self.response[key] = [addition]
                self.options.append(key)
            else:
                self.response[key].append(addition)
                
    def get_options(self):
        '''
        Get all the possible subjects yo choose from
        '''
        return self.options

         
    def get_responses(self, subject):
        '''
        Get all the responses for a given subject line and their associated data
        '''
        key = str(subject)
        if key not in self.response:
            return []
        else:
            return self.response[key]
            
    def increment_id (self, ID, subject):
        '''
        Increments the number of times used this session and ever.
        Use this when you use a response
        '''
        key = subject
        for i in self.response[key]:
            if i[0] == ID:
                i[2] += 1
                i[3] += 1
                i[4] += datetime.now().strftime("%d-%B-%Y %H:%M:%S") + ", "
                return
    
    def add_response(self, subject, resp, character):
        '''
        Adds a new response and subject and character
        '''
        key = subject
        #note to self, maybe make this a seperate function 
        addition = [uuid.uuid4(), resp, 0 , 0, "", character]
        if key not in self.response:
            self.response[key] = [addition]
            self.options.append(key)
        else:
            self.response[key].append(addition)
        
    def save_responses(self, out_file):
        '''
        places reponses into an excel sheet. Just give it a file path
        '''
        #open workbook
        wb = xlsxwriter.Workbook(out_file)
        sheet1 = wb.add_worksheet()
        sheet1.set_column(2,2,70)
        sheet1.set_column(5,5,40)
        sheet1.write(0, 0, "Character") 
        sheet1.write(0, 1, "Response Type") 
        sheet1.write(0, 2, "Response") 
        sheet1.write(0, 3, "Times Used Last Session") 
        sheet1.write(0, 4, "Times Used Total") 
        sheet1.write(0, 5, "Times of Use") 
        cnt = 1
        for key in self.options:
            for item in self.response[key]:
                sheet1.write(cnt, 0, item[5]) 
                sheet1.write(cnt, 1, key) 
                sheet1.write(cnt, 2, item[1]) 
                sheet1.write(cnt, 3, item[2]) 
                sheet1.write(cnt, 4, item[3]) 
                sheet1.write(cnt, 5, item[4]) 
                cnt += 1
        wb.close()
                


    