import csv
import json
import collections

def csv_to_json(csvFilePath, jsonFilePath):
    jsonDict = {}

    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.reader(csvf, delimiter=',')
        dPeople = collections.defaultdict(dict)
        d = collections.defaultdict(dict)


        for row in csvReader:
            # People
            dPeople[row[1]]['name'] = row[49]
            dPeople[row[1]]['father']= row[2]
            dPeople[row[1]]['mother']= row[3]
            
            # Demographics
            dPeople[row[4]]['gender'] = row[4] 

            # Cancer
            dPeople[row[20]]['code'] = row[20] # ICD_O_3
            dPeople[row[20]]['site'] = row[21] # ICD_O_3
            dPeople[row[20]]['morphology'] = row[20] # ICD_O_3
            dPeople[row[20]]['laterality'] = row[22]
            dPeople[row[20]]['behavior'] = row[16]
            dPeople[row[20]]['diagnosis_method'] = row[19]
            dPeople[row[20]]['age_of_diagnosis'] = row[15]
            dPeople[row[20]]['date_of_diagnosis'] = row[17]

            # Non-Cancer
            dPeople[row[30]]['code'] = row[30] # ICD 10
            dPeople[row[30]]['laterality'] = row[29]
            dPeople[row[30]]['diagnosis_method'] = row[28]
            dPeople[row[30]]['age_of_diagnosis'] = row[25]
            dPeople[row[30]]['date_of_diagnosis'] = row[26]

            # Procedure
            dPeople[row[36]]['code'] = row[36] # ICD 10
            dPeople[row[36]]['laterality'] = row[38]
            dPeople[row[36]]['age_at_procedure'] = row[33]
            dPeople[row[36]]['date_of_procedure'] = row[34]
            dPeople[row[36]]['intent'] = row[37]
            dPeople[row[36]]['procedure_validation'] = row[39]
        
        d['people'] = dPeople
            
    '''
        for frow in csvReader:
            if frow[1] in jsonDict:
                jsonDict[frow[1]]['name'] = frow[49]
                jsonDict[frow[1]]['father'] = frow[2]
                jsonDict[frow[1]]['mother'] = frow[3]
                
            else:
                jsonDict[frow[1]] = {'name': frow[49]}
                jsonDict[frow[1]] = {'father': frow[2]}
                jsonDict[frow[1]] = {'mother': frow[3]}
    '''
    
    with open(jsonFilePath, 'w', encoding = 'utf-8') as jsonf:
        jsonString = json.dumps(d, indent = 2)
        jsonf.write(jsonString)

csvFilePath = r'json_other.csv'
jsonFilePath = r'pedigree.json'
csv_to_json(csvFilePath, jsonFilePath)
print("\nPedigree JSON created\n")