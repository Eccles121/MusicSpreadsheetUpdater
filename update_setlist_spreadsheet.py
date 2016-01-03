from processcredentials import DB_Paths
from processcredentials import Credentials
from processcredentials import Spreadsheet
from datetime import datetime
import gspread
import time
import sqlite3

class Presentation:
    def __init__(self, str_db_path):
        self.__sqlite_connection = sqlite3.connect(str_db_path)
        self.__cursor = self.__sqlite_connection.cursor()

    def get_all_service_items(self):
        presentation_table_query = 'SELECT p.lastviewedutc, p.title, s.title, s.serviceitemkind, p.presentationid ' \
                                   'FROM serviceitems s left join presentations p ' \
                                   'WHERE s.presentationid = p.presentationid'

        self.__cursor.execute(presentation_table_query)
        return list(self.__cursor)

    def get_latest_service_items(self):
        l_results = self.get_all_service_items()
        last_viewed_item_date = l_results[len(l_results)-1][0].split('t')[0]
        return [result for result in l_results if last_viewed_item_date in str(result[0])]

    def get_latest_songs(self):
        l_latest_items = self.get_latest_service_items()
        return [item for item in l_latest_items if item[3] == PresentationType.lyrics]


class PresentationType:
    lyrics = 'SongLyrics'

def get_leader_name():
    day = datetime.today().day

    if day >= 1 and day <= 7:
        leader = 'Week 1'
    elif day > 7 and day <= 14:
        leader = 'Week 2'
    elif day > 14 and day <= 21:
        leader = 'Week 3'
    elif day > 21 and day <= 28:
        leader = 'Week 4'
    else:
        leader = 'Week 5'

    return leader


def update_spreadsheet(spreadsheet_name, l_row_to_add):
    gc = gspread.authorize(Credentials.spreadsheet_credentials)
    sheet = gc.open(spreadsheet_name).sheet1
    print 'Spreadsheet "{0}" open. Inserting row...'.format(spreadsheet_name)

    print 'latest date on spreadsheet:{0}'.format(sheet.cell(1,2).value)
    print 'date to insert:{0}'.format(l_row_to_add[1])

    if sheet.cell(1,2).value == l_row_to_add[1]:
        print 'Spreadsheet up to date'
    else:
        sheet.insert_row(l_row_to_add, 1)
        print 'Set list row inserted'

#for logging purposes. Historically runs ~ 3 min
start_time = time.time()

pres = Presentation(DB_Paths.presentation_manager_db_path)

print pres.get_all_service_items()

l_last_songs = pres.get_latest_songs()
pres_date = l_last_songs[0][0].split('T')[0]

# split pres_date to reorder all pretty-like
l_pres_date = pres_date.split('-')
pres_date = "{0}/{1}/{2}".format(l_pres_date[1].lstrip('0'), l_pres_date[2].lstrip('0'), l_pres_date[0])
l_last_song_titles = [song[2] for song in l_last_songs]

leader_and_date = [get_leader_name(), pres_date]
row_to_add = leader_and_date + l_last_song_titles

update_spreadsheet(Spreadsheet.spreadsheet_name, row_to_add)

print '-- run time:{0} --'.format(time.time() - start_time)


