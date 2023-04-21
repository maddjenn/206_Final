import matplotlib.pyplot as plt
import sqlite3

con = sqlite3.connect('FinalDatabase.db')
cur = con.cursor() 

cur.execute("SELECT * \
                FROM generalData \
                INNER JOIN hospitalData \
                ON generalData.date = hospitalData.date \
                WHERE generalData.date = hospitalData.date \
                ORDER BY generalData.date ASC")
rows = cur.fetchall()
dates = []
positives = []
for row in rows:
    dates.append(str(row[0])[4:6] + '/' + str(row[0])[6:] + '/' + str(row[0])[:4])
    positives.append((row[8]/row[14]) * 100)
    # print("hosp: " + str(row[8]) + "total: " + str(row[14]) + '\n') 



plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True
plt.bar(dates, positives)
plt.title("Percent Hospitalized by COVID-19 Per Day")
plt.xlabel("Dates")
plt.xticks(rotation = 90)
plt.tick_params(axis='x', which='major', labelsize=3)
plt.ylabel("Percent Hospitalized (# Hospitalized / Number of Cases) per day")
plt.savefig("COVIDApi_Visualization.png")
plt.show()
