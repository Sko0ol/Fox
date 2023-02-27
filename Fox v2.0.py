import requests
import os
from datetime import date, datetime
import sqlite3
import time

filename = "ExistingImageURLs.db"
conn = None

while conn is None:
    try:
        conn = sqlite3.connect(filename)
    except sqlite3.OperationalError as e:
        print(e)
        time.sleep(1)

cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS URLs(url TEXT)")

URL = "https://randomfox.ca/floof"

count = int(input("Wie viele Fuchsbilder willst du haben?\n> "))

for i in range(count):
    
    while True:
        response = requests.get(URL)
        img_url = response.json()['image']
        
        cur.execute("SELECT * FROM URLs WHERE url = ?", (img_url,))
        results = cur.fetchall()
        
        if len(results) == 0:
            break
        
    cur.execute("INSERT INTO URLs(url) VALUES(?)", (img_url,))
    conn.commit()
    
    current_date = date.today().strftime("%b-%d-%Y")
    current_time = datetime.now().strftime("%H:%M:%S")
    
    os.system(f"curl {img_url} --output img_{i + 1}_at_{current_date}.jpg")
    
conn.close()