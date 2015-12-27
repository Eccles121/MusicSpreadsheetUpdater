import json
import os
import pwd
from oauth2client.client import SignedJwtAssertionCredentials


class Credentials:
    mac_user = pwd.getpwuid(os.getuid())[0]
    __jsonPath = '/Users/{0}/Documents/spreadsheet_update_credentials.json'.format(mac_user)
    __json_key = json.load(open(__jsonPath))
    __google_user_email = __json_key['client_email']
    __google_user_password = __json_key['private_key']
    __scope = ['https://spreadsheets.google.com/feeds']
    spreadsheet_credentials = SignedJwtAssertionCredentials(__google_user_email, __google_user_password.encode(), __scope)


class DB_Paths:
    __proclaim_data_folder = r"/Users/{0}/Library/Application Support/Proclaim/Data".format(Credentials.mac_user)
    __subfolder_items = [dir for dir in os.listdir(__proclaim_data_folder) if dir != '.DS_Store']
    __l_proclaim_db_files = [os.path.join(__proclaim_data_folder, subfolder, 'PresentationManager', 'PresentationManager.db') for subfolder in __subfolder_items]
    __l_proclaim_db_files.sort(key=os.path.getmtime)

    # sort arranges low to high, reverse to put most recent first
    __l_proclaim_db_files.reverse()

    presentation_manager_db_path = __l_proclaim_db_files[0]


class Spreadsheet:
    spreadsheet_name = 'new'