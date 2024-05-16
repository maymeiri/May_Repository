import pandas as pd
import pycountry

# Specify the file path
file_path_alcohol = '/Users/may/Documents/Python/Alcohol/alcohol_intake.csv'
file_path_liver = '/Users/may/Documents/Python/Alcohol/HFAMDB_159_EN.csv'

# Read the CSV file into a pandas DataFrame
df_alcohol = pd.read_csv(file_path_alcohol)
df_liver = pd.read_csv(file_path_liver)

#Change columns name
df_alcohol = df_alcohol.rename(columns={'Countries, territories and areas': 'COUNTRY_NAME',
                        'Year': 'YAER',
                        'Both sexes':'B',
                        'Male': 'M',
                        'Female': 'F'
                        }, inplace=False)


def get_country_alpha_3(name):
    try:
        return pycountry.countries.get(name=name).alpha_3
    except AttributeError:
        return None

# Apply the function to the 'country' column
df_alcohol['COUNTRY_CODE'] = df_alcohol['COUNTRY_NAME'].apply(get_country_alpha_3)

# Check - ilter rows where 'COUNTRY_CODE' is None
df_null_country_code = df_alcohol[df_alcohol['COUNTRY_CODE'].isnull()]
print(df_null_country_code) 

# Replace None in 'COUNTRY_CODE' for specific 'COUNTRY_NAME'
df_alcohol.loc[df_alcohol['COUNTRY_NAME'] == 'Bolivia (Plurinational State of)', 'COUNTRY_CODE'] = 'BOL'
df_alcohol.loc[df_alcohol['COUNTRY_NAME'] == "Cote d'Ivoire", 'COUNTRY_CODE'] = 'CIV'
df_alcohol.loc[df_alcohol['COUNTRY_NAME'] == "Democratic People's Republic of Korea", 'COUNTRY_CODE'] = 'PRK'
df_alcohol.loc[df_alcohol['COUNTRY_NAME'] == "Democratic Republic of the Congo", 'COUNTRY_CODE'] = 'COD'
df_alcohol.loc[df_alcohol['COUNTRY_NAME'] == "Iran (Islamic Republic of)", 'COUNTRY_CODE'] = 'IRN'
df_alcohol.loc[df_alcohol['COUNTRY_NAME'] == "Micronesia (Federated States of)", 'COUNTRY_CODE'] = 'FSM'
df_alcohol.loc[df_alcohol['COUNTRY_NAME'] == "Netherlands (Kingdom of the)", 'COUNTRY_CODE'] = 'NLD'
df_alcohol.loc[df_alcohol['COUNTRY_NAME'] == "Republic of Korea", 'COUNTRY_CODE'] = 'KOR'
df_alcohol.loc[df_alcohol['COUNTRY_NAME'] == "Republic of Moldova", 'COUNTRY_CODE'] = 'MDA'
df_alcohol.loc[df_alcohol['COUNTRY_NAME'] == "Turkiye", 'COUNTRY_CODE'] = 'TUR'
df_alcohol.loc[df_alcohol['COUNTRY_NAME'] == "United Kingdom of Great Britain and Northern Ireland", 'COUNTRY_CODE'] = 'GBR'
df_alcohol.loc[df_alcohol['COUNTRY_NAME'] == "United Republic of Tanzania", 'COUNTRY_CODE'] = 'TZA'
df_alcohol.loc[df_alcohol['COUNTRY_NAME'] == "United States of America", 'COUNTRY_CODE'] = 'USA'
df_alcohol.loc[df_alcohol['COUNTRY_NAME'] == "Venezuela (Bolivarian Republic of)", 'COUNTRY_CODE'] = 'VEN'

# Check - ilter rows where 'COUNTRY_CODE' is None
df_null_country_code = df_alcohol[df_alcohol['COUNTRY_CODE'].isnull()]
print(df_null_country_code) 


# Split the 'F' column into two new columns
df_alcohol['F_MEAN'] = df_alcohol['F'].str.rsplit(' ',n=1).str[0]
df_alcohol['M_MEAN'] = df_alcohol['M'].str.rsplit(' ',n=1).str[0]
df_alcohol['B_MEAN'] = df_alcohol['B'].str.rsplit(' ',n=1).str[0]

#Save df to csv
df_alcohol.to_csv('/Users/may/Documents/Python/Alcohol/alcohol_intake_cleaned.csv', index=False)