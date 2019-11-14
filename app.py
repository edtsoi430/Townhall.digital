from flask import Flask, render_template, request, send_file
from io import TextIOWrapper
from tkinter import *  
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.common.keys import Keys
# PyDrive to upload files to Google Drive using Google Drive API
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import csv
import cgi
import os
import datetime
#---------------------Dominick's Libraries-----------------------------
from response_getter import response
from get_posts_and_userid import extract_posts
#---------------------------------------------------------

# Log in to user account and create a closed facebook group with custom name. Still under development.
option = Options()
form = cgi.FieldStorage()
option.add_argument("--disable-infobars")
option.add_argument("start-maximized")
option.add_argument("--disable-extensions")

# Pass the argument 1 to allow and 2 to block
option.add_experimental_option("prefs", { 
    "profile.default_content_setting_values.notifications": 1 
})

def create_group(usr_in, pwd_in, group_name_in, emails_in):
    driver = webdriver.Chrome(chrome_options=option)
    driver.get('https://www.facebook.com/login') 
    sleep(2) 
    username_box = driver.find_element_by_id('email') 
    username_box.send_keys(usr_in) 
    sleep(2) 

    password_box = driver.find_element_by_id('pass') 
    password_box.send_keys(pwd_in) 
    
    login_box = driver.find_element_by_id('loginbutton') 
    login_box.click() 

    group_button = driver.find_element_by_id('navItem_1434659290104689')
    group_button.click()
    sleep(2)

    create_group_btn = driver.find_element_by_xpath("//button[contains(@class,'mfclru0v oshhggmv hf30pyar lq84ybu9 bdao358l _4jy0 _4jy4 _4jy1 _51sy selected _42ft')]")
    create_group_btn.click()
    sleep(3)

    group_name_box = driver.find_element_by_xpath("//input[contains(@class,'inputtext pls _29br')]")
    group_name_box.send_keys(group_name_in)
    sleep(3)
    submit_btn = driver.find_element_by_xpath("//button[contains(@class,'_42ft _4jy0 layerConfirm _29bh uiOverlayButton _4jy3 _4jy1 selected _51sy')]")
    submit_btn.click()

    sleep(5)
    add_people_box = driver.find_element_by_xpath("//input[contains(@class,'inputtext textInput')]")
    sleep(1)
    for e in emails_in:
        add_people_box.send_keys(e)
        sleep(2)
        add_people_box.click()
    return render_template('index.html')

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/foo', methods=['GET', 'POST'])
def foo():
    if request.method == "POST":
        emails = []
        f = TextIOWrapper(request.files["emails_in"], encoding='utf-8 ', errors='replace')
        usr = request.form["fb-id"]
        pwd = request.form["fb-pw"]
        group_name = request.form["group-name"]
        for row in csv.reader(f):
            emails.append(row[0])
        g_login = GoogleAuth()
        g_login.LocalWebserverAuth()
        drive = GoogleDrive(g_login)
        f_name = group_name + ".csv"
        file_drive = drive.CreateFile({'title': f_name })   
        with open(f_name, 'w') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow(['Date Created', datetime.datetime.now().strftime("%Y-%m-%d %H:%M")])
            filewriter.writerow(['Master Account ID', usr])
            filewriter.writerow(['Master Account PW', pwd])
            filewriter.writerow("")
            filewriter.writerow(['Invited Members to the Group: '])
            for e in emails:
                filewriter.writerow([e])
        file_drive.SetContentFile(f_name)
        os.remove(f_name)
        file_drive.Upload({'convert': True})
    return create_group(usr, pwd, group_name, emails)

@app.route('/getComments', methods=['GET', 'POST'])
def getComments():
    f_name = "posts-test.xlsx"
    api_key = "EAAGalcf1NI4BACoAzGCbIgaLxo57YvNZCFyBVPwi5f6d1GfKWCaaC7U5HDFNi4XuqjLGMO1AQgw6YDrK1icqBS98MCAZBZBjlem1GdKU28SdhZBn81IJw1izUKbeySiDW3FuRKnLqXEQWKHb8hmIh95A8RFUFxfWwZASVc8QAfgZDZD"
    extract = extract_posts(310752336321637, api_key)
    extract.extract_posts(f_name)
    return send_file(f_name, as_attachment=True)

if __name__ == "__main__": 
    app.run(debug=True)
