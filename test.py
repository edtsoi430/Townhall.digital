# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 14:55:47 2019

@author: Dominick
"""
from response_getter import response
from get_posts_and_userid import extract_posts

def response_get_tests():
    '''
    Serious of ways to see if response_getter is working right
    '''
    rep = response("test.xlsx")
    print(rep.get_options())
    reps = rep.get_responses('opium') 
    print("Result from getting the query")
    print(reps) #list of all responses for this query 
    print(reps[0][1]) #response 1
    print(reps[0][2]) #reponse 1's ID
    rep.increment_id(reps[0][0], 'opium')
    reps = rep.get_responses('opium')
    print("After incrementing")
    print(reps[0][2])#reponse 1's ID after incrementing
    print("Before addition")
    reps = rep.get_responses('opium')
    print(reps)
    rep.add_response("opium", "Opium has been used across history by many medical professionals to great effect", "Billy")
    reps = rep.get_responses('opium')
    print(reps)
    print(rep.options)
    rep.save_responses('out.xlsx')
    print("Loading from the saved file \n")
    rep = response("out.xlsx")
    reps = rep.get_responses('opium')
    print(reps)
    print(rep.options)
    
def get_responses():
    '''
    Testing to see if we can get the desired responses. Make sure not to call this 
    too often as facepy will ratelimit you and you'll lose access for an hour
    '''
    api_key = "EAAGalcf1NI4BACoAzGCbIgaLxo57YvNZCFyBVPwi5f6d1GfKWCaaC7U5HDFNi4XuqjLGMO1AQgw6YDrK1icqBS98MCAZBZBjlem1GdKU28SdhZBn81IJw1izUKbeySiDW3FuRKnLqXEQWKHb8hmIh95A8RFUFxfWwZASVc8QAfgZDZD"
    extract = extract_posts(310752336321637, api_key)
    extract.extract_posts("posts.xlsx")
    
def main():
    get_responses()
    
    
    
if __name__ == '__main__':
    main()