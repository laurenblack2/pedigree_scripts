import csv
import json
import collections

def first_pass_make_pedigree(csvReader):
    print ("Starting First Pass\n")
    people = collections.defaultdict(dict)

# We are going to have to iterate over this several times.
# First lets get all the people and the pedigree structure in place

    next(csvReader) # throws out the header line
    for row in csvReader:
        # People
        id = row[1]

        # There are multi (many) lines for the same person, we only care about the first for now
        if (not (id in people)):
            people[id]['name'] = row[49]
            people[id]['father']= row[2]
            people[id]['mother']= row[3]
            people[id]['partners'] = [];
            people[id]['demographics']= {}
            people[id]['demographics']['gender'] = row[4]
            people[id]['diseases'] = {}
            people[id]['procedures'] = {}


            print (people[id]['name'] + "\n")

    return people

def second_pass_get_cancers(csvReader, people):
    print ("Starting Second Pass\n")
    next(csvReader) # throws out the header line
    for row in csvReader:
        id = row[1]
        if (row[20]):
            code = row[20]
            site = row[21]

            morphology = row[20] # ICD_O_3
            laterality = row[22]
            behavior = row[16]
            diagnosis_method = row[19]
            age_of_diagnosis = row[15]
            date_of_diagnosis = row[17]

            print (id + " Cancer [" + code + "] Site: [" + site + "] morphology [" + morphology + "] laterality [" + laterality + "]"
                + " behavior [" + behavior + "] method [" + diagnosis_method + "] age [" + age_of_diagnosis + "] date [" + date_of_diagnosis + "]")

            people[id]['diseases'][code] = {}
            people[id]['diseases'][code]["shorthand"] = code;
            people[id]['diseases'][code]["site"] = site;
            people[id]['diseases'][code]["morphology"] = morphology;
            people[id]['diseases'][code]["laterality"] = laterality;
            people[id]['diseases'][code]["behavior"] = behavior;
            people[id]['diseases'][code]["diagnosis_method"] = diagnosis_method;
            people[id]['diseases'][code]["age_of_diagnosis"] = age_of_diagnosis;
            people[id]['diseases'][code]["date_of_diagnosis"] = date_of_diagnosis;

def third_pass_get_noncancers(csvReader, people):
    print ("Starting Third Pass\n")
    next(csvReader) # throws out the header line
    for row in csvReader:
        id = row[1]
        if (row[30]):
            code = row[30]
            laterality = row[29]
            diagnosis_method = row[28]
            age_of_diagnosis = row[25]
            date_of_diagnosis = row[26]

            print (id + " NonCancer [" + code + "] laterality [" + laterality + "]"
                + " method [" + diagnosis_method + "] age [" + age_of_diagnosis + "] date [" + date_of_diagnosis + "]")

            people[id]['diseases'][code] = {}
            people[id]['diseases'][code]["shorthand"] = code;
            people[id]['diseases'][code]["laterality"] = laterality;
            people[id]['diseases'][code]["diagnosis_method"] = diagnosis_method;
            people[id]['diseases'][code]["age_of_diagnosis"] = age_of_diagnosis;
            people[id]['diseases'][code]["date_of_diagnosis"] = date_of_diagnosis;

def fourth_pass_get_procedures(csvReader, people):
    print ("Starting Fourth Pass\n")
    next(csvReader) # throws out the header line
    for row in csvReader:
        id = row[1]
        if (row[36]):
            code = row[36]
            laterality = row[38]
            age_at_procedure = row[33]
            date_of_procedure = row[34]
            intent = row[37]
            procedure_validation = row[39]


            print (id + " Procedure [" + code + "] laterality [" + laterality + "]"
                + " age [" + age_at_procedure + "] date [" + date_of_procedure + "] intent [" + intent + "] validation [" + procedure_validation + "]")

            people[id]['procedures'][code] = {}
            people[id]['procedures'][code]["shorthand"] = code;
            people[id]['procedures'][code]["laterality"] = laterality;
            people[id]['procedures'][code]["age_at_procedure"] = age_at_procedure;
            people[id]['procedures'][code]["date_of_procedure"] = date_of_procedure;
            people[id]['procedures'][code]["intent"] = intent;
            people[id]['procedures'][code]["procedure_validation"] = procedure_validation;


def build_json_file(people, jsonFilePath):
    d = collections.defaultdict(dict)

    d['proband'] = "5983-01-001"
    d['people'] = people
    jsonString = json.dumps(d, indent = 2)
#    print (jsonString);

    with open(jsonFilePath, 'w', encoding = 'utf-8') as jsonf:
        jsonString = json.dumps(d, indent = 2)
        jsonf.write(jsonString)

def process_csv (csvFilePath):
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.reader(csvf, delimiter=',')
        people = first_pass_make_pedigree(csvReader)
        csvf.seek(0) # reset to the beginning of the file
        csvReader = csv.reader(csvf, delimiter=',')
        second_pass_get_cancers(csvReader, people)
        csvf.seek(0) # reset to the beginning of the file
        csvReader = csv.reader(csvf, delimiter=',')
        third_pass_get_noncancers(csvReader, people)
        csvf.seek(0) # reset to the beginning of the file
        csvReader = csv.reader(csvf, delimiter=',')
        fourth_pass_get_procedures(csvReader, people)
    return people


# Main Function is here

csvFilePath = r'json_other.csv'
jsonFilePath = r'pedigree_test.json'
people = process_csv(csvFilePath)
build_json_file(people, jsonFilePath)
print("\nPedigree JSON created\n")
