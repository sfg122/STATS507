import pandas as pd
import pickle

cohorts = ['G','H', 'I', 'J']

# Demographics columns
demo_cols = ['SEQN',
             'RIDAGEYR', 
             'RIDRETH3', 
             'DMDEDUC2', 
             'DMDMARTL',
             'RIDSTATR',
             'SDMVPSU',
             'SDMVSTRA',
             'WTMEC2YR', 
             'WTINT2YR']


demo_names = ['unique id',
              'age',
              'ethnicity',
              'education',
              'martial status',
              'interview status',
              'masked variance: psu',
              'masked variance: stratum',
              'exam weight',
              'inverview weight']

ethnicity_dict = {1: 'Mexican American',
                  2: 'Other Hispanic',
                  3: 'Non-Hispanic White',
                  4: 'Non-Hispanic Black',
                  6: 'Non-Hispanic Asian',
                  7: 'Other Race - Including Multi-Racial'}

education_dict = {1: 'Less than 9th grade',
                  2: '9-11th grade (Includes 12th grade with no diploma)',
                  3: 'High school graduate/GED or equivalent',
                  4: 'Some college or AA degree',
                  5: 'College graduate or above',
                  7: 'Refused',
                  9: 'Don\'t Know'}

marital_dict = {1:  'Married',
                2:  'Widowed',
                3:  'Divorced',
                4:  'Separated',
                5:  'Never married',
                6:  'Living with partner',
                77: 'Refused',
                99: 'Don\'t know'}

interview_dict = {1: 'Interviewd only',
                  2: 'Both interviewed and MEC examined'}

demo_cat = zip(demo_names[2:6],
               [ethnicity_dict, education_dict, marital_dict, interview_dict])

demo_fname = 'Demo_'


# Dental columns
ohdn_cols = ['SEQN',
             'OHDDESTS']

ohdn_names = ['unique id',
              'dentition status code']

num_TC = 0
for i in range(1, 33):
    ohdn_cols.append(f'OHX{i:02d}TC')
    ohdn_names.append(f'tooth count: #{i}')
    num_TC += 1 

#keeps all CTCs after TCs in name list, which speeds up pulling out columns
num_CTC = 0
for i in range(1,33):
    if i not in [1, 16, 17, 32]: # excludeds teeth 1, 16, 17, and 32
        ohdn_cols.append(f'OHX{i:02d}CTC')
        ohdn_names.append(f'coronal caries: tooth count #{i}')
        num_CTC += 1

dentition_dict = {1: 'Complete',
                  2: 'Partial',
                  3: 'Not Done'}

TC_dict = {1: 'Primary tooth (deciduous) present',
           2: 'Permanent tooth present',
           3: 'Dental implant',
           4: 'Tooth not present',
           5: 'Permanent dental root fragment present',
           9: 'Could not assess'}

CTC_dict = {'A': 'Primary tooth with a restored surface condition',
            'D': 'Sound primary tooth',
            'E': 'Missing due to dental disease',
            'F': 'Permanent tooth with a restored surface condition',
            'J': 'Permanent root tip is present but no restorative\
                  replacement is present',
            'K': 'Primary tooth with a dental carious surface condition',
            'M': 'Missing due to other causes',
            'P': 'Missing due to dental disease but replaced by a removable\
                  restoration',
            'Q': 'Missing due to other causes but replaced by a removable\
                  restoration',
            'R': 'Missing due to dental disease but replaced by a fixed\
                  restoration',
            'S': 'Sound permanent tooth',
            'T': 'Permanent root tip is present but a restorative replacement\
                  is present',
            'U': 'Unerupted',
            'X': 'Missing due to other causes but replaced by a fixed\
                  restoration',
            'Y': 'Tooth present, condition cannot be assessed',
            'Z': 'Permanent tooth with a dental carious surface condition'}

ohdn_cat = zip(ohdn_names[1:],
               [dentition_dict] + [TC_dict]*num_TC + [CTC_dict]*num_CTC)

ohdn_fname = 'OHXDEN_'

# get data function
def get_data(cols, names, fname, cohorts, categorical_dicts):
    
    df = pd.DataFrame(columns = cols + ['cohort'])
    
    # Create maps for column names
    name_map = dict()
    for col, newname in zip(cols, names):
        name_map[col] = newname

    # Read in data
    for cohort in cohorts:
        temp = pd.read_sas(f'{fname}{cohort}.xpt')
        temp = temp[cols]
        temp['cohort'] = cohort
        df = df.append(temp)
        
    #rename columns    
    df = df.rename(columns = name_map)
    
    #create categorical data
    for col, cat_dict in categorical_dicts:
        df[col] = pd.Categorical(df[col].replace(cat_dict))
    
    return df



demo_data = get_data(demo_cols, demo_names, demo_fname, cohorts, demo_cat)
ohdn_data = get_data(ohdn_cols, ohdn_names, ohdn_fname, cohorts, ohdn_cat)

print(f'There are {demo_data.shape[0]: d} cases in the demographic data')
print(f'There are {ohdn_data.shape[0]: d} cases in the dental data')

pickle.dump(demo_data, open('demo_data.p', 'wb'))
pickle.dump(ohdn_data, open('ohdn_data.p', 'wb'))
