import pandas as pd
import sqlite3
import mechanicalsoup
import itertools


#creating a browser object
browser = mechanicalsoup.StatefulBrowser()
browser.open('https://en.wikipedia.org/wiki/List_of_highest_mountains_on_Earth')

#extract data from the table
td = browser.page.find_all('td')

#extract only the text of the element td and th
table_data = [value.text.replace('\n','') for value in td]
#print(table_data.index('1'))
table_data = table_data[4:]
#print(table_data)

#create column header
Columns_header = ['Rank','Mountain_Name(s)', 'Height_(m)', 'Height_(ft)',
                  'Prominence_(m)', 'Prominence_(ft)', 'Range', 'Coordinates','Parent_Mountain','First_Ascent',
                  'Successes_before_2004', 'Failures_before_2004', 'Countries']
#print(len(Columns_header))

#
d = dict()
for idx, key in enumerate(Columns_header):
    d[key] = table_data[idx:][::13]

#print(dict(itertools.islice(d.items(),2)))
#print(d)

#converting dictiomary to Pandas Data Frame and
df = pd.DataFrame(d)
#print(df)

#exporting to csv
df.to_csv('Mountain table.csv')

#creating a database and a cursor

conn = sqlite3.connect('Mountains_db.sqlite')
cur = conn.cursor()


#creatind SQL Table

cur.execute('Drop table if exists Mountains')
cur.execute('''Create Table Mountains('Rank','Mountain_Name(s)', 'Height_(m)', 'Height_(ft)',
                  'Prominence_(m)', 'Prominence_(ft)', 'Range', 'Coordinates','Parent_Mountain','First_Ascent',
                  'Successes_before_2004', 'Failures_before_2004', 'Countries')''')

#inserting into table

for i in range(len(df)):
    cur.execute('insert into Mountains values (?,?,?,?,?,?,?,?,?,?,?,?,?)',df.iloc[i])

conn.commit()

conn.close()