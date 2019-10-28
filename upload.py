from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import csv
#Login to Google Drive and create drive object
g_login = GoogleAuth()
g_login.LocalWebserverAuth()
drive = GoogleDrive(g_login)

file_drive = drive.CreateFile({'title': "test.csv" })  
file_drive.SetContentFile("emails.csv") 
file_drive.Upload({'convert': True})
print("All files have been uploaded")

