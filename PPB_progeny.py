import pandas as pd
import numpy as np
from datetime import datetime

# Making the data frame from the csv file provided
df = pd.read_csv('5862.csv', low_memory = False) 
df.head()

print("\nv.1.2, 11/7/2024")
# Section to drop extra & uneeded columns
#df = df.drop(['Sibling','N_CANCER.DERIV_PRSN_AGE3','N_CANCER.OTH_Diagnosis Method','N_CANCER.TYPE','PRTRT.Oth Intent','PRTRT.Oth Procedure Validation'], axis = 1)
df = df.drop(['Sibling ID', 'PRTRT.Oth Intent', 'PRTRT.DERIV_PRSN_AGE', 'CANCER.OTH_Diagnosis Method', 'N_CANCER.OTH_Diagnosis Method', 'CANCER.DERIV_PRSN_AGE', 'N_CANCER.DERIV_PRSN_AGE', 'DEAD'], axis = 1)

# Section sorts the values based on id and cancer number
df.sort_values(["id", df.columns[16]], ascending = [True, True], inplace = True)

# Section creates new columns as placeholders for family_name, date_updated and BSI Columns: sample_id, seq_num, material_type, vial_status, date_flow_performed
df['sample_id'] = np.nan
df['seq_num'] = np.nan
df['material_type'] = np.nan
df['vial_status'] = np.nan
df['date_flow_performed'] = np.nan
df['date_updated'] = np.nan
df['family_name'] = np.nan
# The first 6 of empty columns added will not be needed in the FHH pedigree chart.

# Reorder columns based on index/iloc dues to same named columns that cannot be changed
df_reorder = df.iloc[:,[0,1,2,3,4,5,6,7,8,50,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,44,45,46,47,48,41,49,43,42]]
df_reorder.columns = ["family_id","id","father_id","mother_id","sex","deceased","date_of_birth","date_of_death","contact","family_name","last_name","first_name","multiple_birth_id","multiple_birth_type","spouse_number","spouse_id","number","age_at_diagnosis","behavior","date_of_diagnosis","estimated_age_at_diagnosis","cancer_diagnosis_method","icd_o_3_morphology","icd_o_3_site","laterality","dead_end","number","age_at_diagnosis","date_of_diagnosis","estimated_age_at_diagnosis","non_cancer_diagnosis_method","laterality","icd_10","dead_end","number","age_at_procedure","date_of_procedure","estimated_age_at_procedure","icd_9_cm","intent","laterality","procedure_validation","sample_id","seq_num","material_type","vial_status","date_flow_performed","vital_status","date_updated","type","legacy_id"]

# Section removes all Spouse Numbers != 1 that have no spouse_ids, or 0 as a placeholder, then replace spouse_number == 1 to 0 when spouse_id == 0, then drops all duplicated values. 
# All to preserve other column data that would otherwise be dropped
df_reorder["spouse_id"] = df_reorder["spouse_id"].fillna(0)
df_reorder = df_reorder.loc[~((df_reorder["spouse_number"] >= 2) & (df_reorder["spouse_id"] == 0))]
df_reorder.loc[(df_reorder["spouse_number"] == 1) & (df_reorder["spouse_id"] ==  0), "spouse_number"] =  0
df_reorder["spouse_number"] = df_reorder["spouse_number"].replace(0, np.nan)
df_reorder["spouse_id"] = df_reorder["spouse_id"].replace(0, np.nan)

df_reorder = df_reorder.drop_duplicates()

# Code to implement family_name, using the last_name of the proband
f_name = df_reorder.iloc[1,10]
df_reorder["family_name"] = df_reorder["family_name"].replace(np.nan, f_name)

# Code to implement deceased, if vital status is Alive or Unknown, return No. If vital_status is Dead, return Yes
df_reorder["deceased"] = df_reorder["deceased"].fillna(df_reorder["vital_status"] )
df_reorder["deceased"] = np.where(df_reorder["deceased"] == "Dead", "Yes", "No")

# Section for changing Datatypes for quicker script checking, dropping the float (0.0) value for int (0)
df_reorder.iloc[:,14] = df_reorder.iloc[:,14].astype('Int64')
df_reorder.iloc[:,16] = df_reorder.iloc[:,16].astype('Int64')
df_reorder.iloc[:,18] = df_reorder.iloc[:,18].astype('Int64')
df_reorder.iloc[:,21] = df_reorder.iloc[:,21].astype('Int64')
df_reorder.iloc[:,22] = df_reorder.iloc[:,22].astype('Int64')
df_reorder.iloc[:,24] = df_reorder.iloc[:,24].astype('Int64')
df_reorder.iloc[:,26] = df_reorder.iloc[:,26].astype('Int64')
df_reorder.iloc[:,30] = df_reorder.iloc[:,30].astype('Int64')
df_reorder.iloc[:,31] = df_reorder.iloc[:,31].astype('Int64')
df_reorder.iloc[:,34] = df_reorder.iloc[:,34].astype('Int64')
df_reorder.iloc[:,39] = df_reorder.iloc[:,39].astype('Int64')
df_reorder.iloc[:,40] = df_reorder.iloc[:,40].astype('Int64')
df_reorder.iloc[:,41] = df_reorder.iloc[:,41].astype('Int64')


# Datetime fixes: remove time, change date format and remove leading zeros in dates
'''
df_reorder["date_of_birth"] = pd.to_datetime(df_reorder["date_of_birth"]).dt.date
df_reorder["date_of_birth"] = pd.to_datetime(df_reorder["date_of_birth"]).dt.strftime("%#m/%#d/%Y")
df_reorder["date_of_death"] = pd.to_datetime(df_reorder["date_of_death"]).dt.date
df_reorder["date_of_death"] = pd.to_datetime(df_reorder["date_of_death"]).dt.strftime("%#m/%#d/%Y")
df_reorder.iloc[:,19] = pd.to_datetime(df_reorder.iloc[:,19]).dt.date
df_reorder.iloc[:,19] = pd.to_datetime(df_reorder.iloc[:,19]).dt.strftime("%#m/%#d/%Y")
df_reorder.iloc[:,28] = pd.to_datetime(df_reorder.iloc[:,28]).dt.date
df_reorder.iloc[:,28] = pd.to_datetime(df_reorder.iloc[:,28]).dt.strftime("%#m/%#d/%Y")
df_reorder["date_of_procedure"] = pd.to_datetime(df_reorder["date_of_procedure"]).dt.date
df_reorder["date_of_procedure"] = pd.to_datetime(df_reorder["date_of_procedure"]).dt.strftime("%#m/%#d/%Y")
'''

dtyping = df_reorder.dtypes
#print(dtyping)

# Rename columns only for csv to json converter
df_reorder.columns.values[16]= "cancer_number" 
df_reorder.columns.values[26]= "non_cancer_number" 
df_reorder.columns.values[34]= "procedure_number" 


df_reorder.columns.values[17]= "age_at_diag_cancer" 
df_reorder.columns.values[27]= "age_at_diag_non_cancer" 


df_reorder.columns.values[19]= "date_of_diag_cancer" 
df_reorder.columns.values[28]= "date_of_diag_non_cancer" 


df_reorder.columns.values[25]= "dead_end_cancer" 
df_reorder.columns.values[33]= "dead_end_non_cancer" 

df_reorder.columns.values[24]= "laterality_cancer" 
df_reorder.columns.values[31]= "laterality_non_cancer" 
df_reorder.columns.values[40]= "laterality_procedures" 

# Adding a column "name" for combining first name and last name
df_reorder['name'] = df_reorder['first_name'].astype(str) + ' ' + df_reorder['last_name'].astype(str)
flname_drop = ['first_name', 'last_name'] 
df_reorder = df_reorder.drop(columns = flname_drop)
# Removes the columns of first_name & last_name

# Section that renames columns and exports the new CSV file 
#df_reorder.columns = ["family_id","id","father_id","mother_id","sex","deceased","date_of_birth","date_of_death","contact","family_name","last_name","first_name","multiple_birth_id","multiple_birth_type","spouse_number","spouse_id","number","age_at_diagnosis","behavior","date_of_diagnosis","estimated_age_at_diagnosis","cancer_diagnosis_method","icd_o_3_morphology","icd_o_3_site","laterality","dead_end","number","age_at_diagnosis","date_of_diagnosis","estimated_age_at_diagnosis","non_cancer_diagnosis_method","laterality","icd_10","dead_end","number","age_at_procedure","date_of_procedure","estimated_age_at_procedure","icd_9_cm","intent","laterality","procedure_validation","sample_id","seq_num","material_type","vial_status","date_flow_performed","vital_status","date_updated","type","legacy_id"]
df_reorder.to_csv('5983_1.csv', index = False)
print("\nNew Progeny CSV created\n")