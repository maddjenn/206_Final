import sqlite3
from statistics import mean 

con = sqlite3.connect('FinalDatabase.db')
cur = con.cursor() 

cur.execute("SELECT * \
                FROM generalData \
                INNER JOIN hospitalData \
                ON generalData.date = hospitalData.date \
                WHERE generalData.date = hospitalData.date \
                ORDER BY generalData.date ASC")
rows = cur.fetchall()

general_data = {}
hospital_data = {}
hosp_per_pos_list = []
gen_per_pos_list = []
for row in rows:
    per_pos = (row[2]/row[6]) * 100
    general_data[row[0]] = per_pos
    gen_per_pos_list.append(per_pos) 
    per_pos = (row[12]/row[14]) * 100
    hospital_data[row[0]] = per_pos
    hosp_per_pos_list.append(per_pos) 

# General Data Printings 
with open('CovidAPI_calculations.txt', 'w') as f:
        # Print information 
        f.write("Using information gathered from a public COVID-19, we consolidated data on COVID-19 cases per day for 420 days preceding 03/07/2021.\n")
        f.write("Here are some statistics gathered using that data:\n\n")
        f.write(f'The average percent of positive test cases over the span of 420 days was {mean(gen_per_pos_list)}%.\n\n')
        f.write(f'The maximum percent of positive test cases over the span of 420 days was {max(gen_per_pos_list)}%.\n\n')
        f.write(f'The minimum percent of positive test cases over the span of 420 days was {min(gen_per_pos_list)}%.\n\n')
        f.write(f'The average percent of positive test cases over the span of {len(hospital_data)} days was {mean(hosp_per_pos_list)}%.\n\n')
        f.write(f'The maximum percent of positive test cases over the span of {len(hospital_data)} days was {max(hosp_per_pos_list)}%.\n\n')
        f.write(f'The minimum percent of positive test cases over the span of {len(hospital_data)} days was {min(hosp_per_pos_list)}%.\n\n')
        
    
