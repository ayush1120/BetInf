import os
import csv
import json
from stoned.settings import BASE_DIR
import datetime
backup_path = os.path.join(BASE_DIR, "backup")

def dump_bet(row, match_id):
    if not os.path.exists(backup_path):
        try:
            os.mkdir(backup_path)
        except OSError as error:
            raise error
    folder_name = "match" + str(match_id)
    folder_path = os.path.join(backup_path, folder_name)
    file_path = os.path.join(folder_path, "bets.csv")
    head = ['datetime', 'phone_no', 'match_pk', 'match_id', 'team', 'amount', 'payout']
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
        with open(file_path, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(head)
    
    dt = str(datetime.datetime.now().time())
    data = [dt]
    data.extend(row)
    print(data)
    with open(file_path, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(data)