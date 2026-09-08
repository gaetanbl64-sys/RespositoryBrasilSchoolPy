import json

def import_json(path):
    expenses_archive = []
    try:
        with open(path, "r") as f:
            data = json.load(f)
            expenses_year = data.get("year", [])
            #number_year = len(expenses_year)
            #expenses_list = expenses_year[0].get("expenses", []))
            for item in expenses_year:
                new_list = [item] 
                expenses_archive.append(new_list)
    except FileNotFoundError:
        print("Fichier non trouvé.")
        #expenses_list = []
        expenses_archive = []
    #return expenses_list
    return expenses_archive