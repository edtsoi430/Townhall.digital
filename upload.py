from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import csv
# Simple code to test out the functionality of Google Drive API. This code uploads a generic csv file to a user authenticated google drive.
g_login = GoogleAuth()
g_login.LocalWebserverAuth()
drive = GoogleDrive(g_login)

file_drive = drive.CreateFile({'title': "test.csv" })  
file_drive.SetContentFile("emails.csv") 
file_drive.Upload({'convert': True})
print("All files have been uploaded")

