# from covidai.auth import authenticate_with_azure
# from covidai.common.database import SqlServerDatabaseEngine
# from covidai.common.experimental import get_and_format_data
import requests
import sqlite3
import os
import matplotlib.pyplot as plt     

def visualize():
    con = sqlite3.connect('FinalDatabase.db')
    cur = con.cursor() 

    cur.execute("SELECT * FROM YuGiOh")
    rows = cur.fetchall()
    types = {}
    for row in rows:
        if row[2] in types:
            types[row[2]] += 1
        else:
            types[row[2]] = 1
    type_list = []
    count_list = []
    for type in types.keys():
        type_list.append(type)
        count_list.append(types[type])
        # print("hosp: " + str(row[8]) + "total: " + str(row[14]) + '\n') 



    plt.bar(type_list, count_list)
    plt.title("Number of YuGiOh Cards per Type in Database")
    plt.xlabel("Types")
    plt.xticks(rotation = 90)
    plt.tick_params(axis='x', which='major', labelsize=3)
    plt.ylabel("Number of Cards")
    plt.savefig("YuGiOhAPI_Visualization_1.png")
    plt.show()


def calculate_and_visualize():
    con = sqlite3.connect('FinalDatabase.db')
    cur = con.cursor() 

    cur.execute("SELECT * FROM YuGiOh")
    rows = cur.fetchall()
    total = 0
    types = {}
    for row in rows:
        if row[2] in types:
            types[row[2]] += 1
        else:
            types[row[2]] = 1
    type_list = ["Spell Card", "Trap Card", "Monster"]
    count_list = [0, 0, 0]
    for type in types.keys():
        if(type == "Spell Card"):
            count_list[0] += 1
        elif(type == "Trap Card"):
            count_list[1] += 1
        else:
            count_list[2] += 1
        total += 1
        # print("hosp: " + str(row[8]) + "total: " + str(row[14]) + '\n') 
    for i in range(len(count_list)):
        count_list[i] = (count_list[i]/total) * 100


    plt.bar(type_list, count_list)
    plt.title("Percentage of Type Card in Total Number of Cards in Database")
    plt.xlabel("Types")
    plt.xticks(rotation = 90)
    plt.tick_params(axis='x', which='major', labelsize=3)
    plt.ylabel("Percentage of Total Cards")
    plt.savefig("YuGiOhAPI_Visualization_2.png")
    plt.show()


    with open('YuGiOhAPI_Calculations.txt', 'w') as f:
        # Print information 
        f.write("Using information gathered from a public YuGiOh API database, we calculated the division of card types in the database:\n")
        f.write(f'The percentage of Monster Cards out of the database totaled {count_list[2]}%.\n\n')
        f.write(f'The percentage of Spell Cards out of the database totaled {count_list[0]}%.\n\n')
        f.write(f'The percentage of Trap Cards out of the database totaled {count_list[1]}%.\n\n') 
        
    

     

def main():
    visualize()
    calculate_and_visualize()


main()