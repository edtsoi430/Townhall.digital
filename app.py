from flask import Flask, render_template, request
import csv
from tkinter import *  
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.common.keys import Keys
import cgi

# Log in to user account and create a closed facebook group with custom name. Still under development.

usr, pwd = " ", " "
group_name = "Townhall.Digital"
f_name = ""
option = Options()
form = cgi.FieldStorage()
# Disable notifications
option.add_argument("--disable-infobars")
option.add_argument("start-maximized")
option.add_argument("--disable-extensions")

# Pass the argument 1 to allow and 2 to block
option.add_experimental_option("prefs", { 
    "profile.default_content_setting_values.notifications": 1 
})


def create_group(usr_in, pwd_in, group_name_in, emails_in):
    driver = webdriver.Chrome(chrome_options=option)
    driver.get('https://www.facebook.com/') 
    sleep(1) 
    username_box = driver.find_element_by_id('email') 
    username_box.send_keys(usr_in) 
    sleep(1) 
    
    password_box = driver.find_element_by_id('pass') 
    password_box.send_keys(pwd_in) 
    
    login_box = driver.find_element_by_id('loginbutton') 
    login_box.click() 

    group_button = driver.find_element_by_id('navItem_1434659290104689')
    group_button.click()
    sleep(1)

    create_group_btn = driver.find_element_by_xpath("//button[contains(@class,'mfclru0v oshhggmv hf30pyar lq84ybu9 bdao358l _4jy0 _4jy4 _4jy1 _51sy selected _42ft')]")
    create_group_btn.click()
    sleep(3)

    group_name_box = driver.find_element_by_xpath("//input[contains(@class,'inputtext pls _29br')]")
    group_name_box.send_keys(group_name_in)
    sleep(3)

    add_people_box = driver.find_element_by_xpath("//input[contains(@class,'inputtext textInput')]")

    with open(emails_in) as f:
        reader = csv.reader(f)
        for row in reader:
            add_people_box.send_keys(row[0])
            sleep(1)
            add_people_box.send_keys(Keys.RETURN)
            sleep(1)
    
    submit_btn = driver.find_element_by_xpath("//button[contains(@class,'_42ft _4jy0 layerConfirm _29bh uiOverlayButton _4jy3 _4jy1 selected _51sy')]")
    # submit_btn.click()
    return ""

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/foo', methods=['GET', 'POST'])
def foo():
    if request.method == "POST":
        f_name = request.files["emails"].name + ".csv"
        usr = request.form["fb-id"]
        pwd = request.form["fb-pw"]
        group_name = request.form["group-name"]
    return create_group(usr, pwd, group_name, f_name)


if __name__ == "__main__": 
    app.run(debug=True)