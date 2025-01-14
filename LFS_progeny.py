import pandas as pd
import numpy as np
from datetime import datetime

# Making the data frame from the csv file provided
file_in = 'Files//05129.csv'
output_file = 'Files//05129_scrubbed.csv'

df = pd.read_csv(file_in, low_memory = False) 
df.head()

print("\nv.1.3, 1/14/2025")
# Section to drop extra & uneeded columns
df = df.drop(['Sibling', 'CANCER.DERIV_PRSN_AGE', 'CANCER.OTH_Diagnosis Method', 'CANCER.TYPE_STD','CANCER.Dead End', 'N_CANCER.DERIV_PRSN_AGE', 'N_CANCER.DERIV_PRSN_AGE3', 'N_CANCER.OTH_Diagnosis Method', 'N_CANCER.TYPE', 'N_CANCER.Dead End', 'PRTRT.DERIV_PRSN_AGE', 'PRTRT.Oth Intent', 'PRTRT.Oth Procedure Validation', 'LEGACY_ID'], axis = 1)

# Section creates new columns as placeholders for family_name
df.columns = ['id','first_name','last_name','family_id','father_id','mother_id','sex','deceased','date_of_birth','date_of_death','contact','spouse_number','spouse_id','multiple_birth_type','multiple_birth_id','cancer_number','cancer_behavior','cancer_date_of_diagnosis','cancer_estimated_age_at_diagnosis','cancer_age_at_diagnosis','cancer_cancer_diagnosis_method','icd_o_3_site','icd_o_3_morphology','cancer_laterality','stage','non_cancer_number','non_cancer_age_at_diagnosis','non_cancer_date_of_diagnosis','non_cancer_diagnosis_method','non_cancer_laterality','icd_10','procedure_number','date_of_procedure','age_at_procedure','estimated_age_at_procedure','icd_9_cm','procedure_laterality','intent','procedure_validation','vital_status']
df['family_name'] = np.nan

# Reorder columns based on index/iloc dues to same named columns that cannot be changed
df_reorder = df.iloc[:,[3,0,4,5,6,7,8,9,10,40,2,1,14,13,11,12,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39]]

# Section sorts the values based on id and cancer number
df_reorder.sort_values(["id", "cancer_number"], ascending = [True, True], inplace = True)

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

dtyping = df_reorder.dtypes

df_reorder.to_csv(output_file, index = False)
print("\nNew Progeny CSV created\n")