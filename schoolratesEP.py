from flask import Flask, request, jsonify
import csv

app = Flask(__name__)



def schoolrateparser():
    
    # Create the hash table (dictionary)
    school_hash_table = {}

    # Open and read the CSV file
    with open("fan_daily_schools.csv", mode='r', newline='', encoding='utf-8') as csvfilea:
        reader1 = csv.reader(csvfilea)    
        next(reader1, None)  # Skip the header row
        
        for row in reader1:
            school_id = row[0].strip() 
            school_name = row[1].strip()  
            school_hash_table[school_id] = {"name": school_name,"clicks": 0,  "opens": 0} #nested dictionary with school name, clicks, and opens


    user_school_followings = {}

    # Open and read the CSV file
    with open("fan_daily_relationships.csv", mode='r', newline='', encoding='utf-8') as csvfileb:
        reader2 = csv.reader(csvfileb)
        next(reader2, None)  # Skip the header row
        
        for row in reader2:
            user_id = row[1].strip()  
            school_id = row[2].strip()  
            
            # If user_id is not already in the dictionary, add it with an empty set
            if user_id not in user_school_followings:
                user_school_followings[user_id] = set()
            user_school_followings[user_id].add(school_id)
            
    with open('fan_daily_engagement_events.csv') as file:
        for line in file:
                cols = line.split(',')
                try:
                    if cols[1].strip():  #only non-referred users follow schools
                      user_id = cols[1].strip()
                      for school_id in user_school_followings[user_id]:
                         if cols[2] == 'open':
                            school_hash_table[school_id]["opens"] += 1
                         elif cols[2] == 'click':
                            school_hash_table[school_id]["clicks"] += 1   # Print the updated school hash table
                except KeyError:                                                #most likely a header row
                    pass
    return school_hash_table

# Define an endpoint to get the results
@app.route('/school_data', methods=['GET'])
def get_school_data():
    data = schoolrateparser()
    return jsonify(data)
        
if __name__ == '__main__':
    app.run(debug=True)

