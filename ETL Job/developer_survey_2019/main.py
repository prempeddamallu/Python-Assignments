import os
import pandas as pd
import pycountry_convert as pc

# Get the directory where the script is located
# print(os.path.realpath(__file__)) # C:\Users\premk\Documents\PythonAssignments\ETL Job\developer_survey_2019\main.py
script_dir = os.path.dirname(os.path.realpath(__file__)) 
# print(script_dir) # C:\Users\premk\Documents\PythonAssignments\ETL Job\developer_survey_2019


# Construct the file paths
survey_path = os.path.join(script_dir, 'survey_results_public.csv')
# print(survey_path) # C:\Users\premk\Documents\PythonAssignments\ETL Job\developer_survey_2019\survey_results_public.csv
schema_path = os.path.join(script_dir, 'survey_results_schema.csv')
# print(schema_path) # C:\Users\premk\Documents\PythonAssignments\ETL Job\developer_survey_2019\survey_results_schema.csv

# Step 0: Load the Data
try:
    survey_data = pd.read_csv(survey_path)
    # print(survey_data) # [88883 rows x 85 columns]
    schema_data = pd.read_csv(schema_path)
    # print(schema_data) # [85 rows x 2 columns]
except Exception as e:
    print(f"Error loading data: {e}")
    raise




# Step 1: Average Age When Developers First Coded

# print(survey_data['Age1stCode'].dtype) # object
# survey_data['Age1stCode'] = pd.to_numeric(survey_data['Age1stCode'], errors='coerce')
# average_age_first_code = survey_data['Age1stCode'].mean()
# print(f"Average age when developers wrote their first line of code: {average_age_first_code:.2f}")



# Step 2: Percentage of Developers Who Knew Python by Country
# python_devs = survey_data[survey_data['LanguageWorkedWith'].str.contains('Python', na=False)]
# # print(python_devs)
# country_counts = survey_data['Country'].value_counts()
# # print(country_counts)
# python_country_counts = python_devs['Country'].value_counts()
# # print(python_country_counts)
# python_percentage_by_country = (python_country_counts / country_counts) * 100
# print("\nPercentage of developers who knew Python by country:")
# print(python_percentage_by_country)



# Step 3: Average Salary by Continent
def get_continent(country_name):
    try:
        country_alpha2 = pc.country_name_to_country_alpha2(country_name)
        continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
        return continent_code
    except:
        return None

survey_data['Continent'] = survey_data['Country'].apply(get_continent)
average_salary_by_continent = survey_data.groupby('Continent')['ConvertedComp'].mean()
print("\nAverage salary by continent:")
print(average_salary_by_continent)



# Step 4: Most Desired Programming Language for 2020
desired_languages = survey_data['LanguageDesireNextYear'].str.split(';').explode().value_counts()
most_desired_language = desired_languages.idxmax()
print(f"\nMost desired programming language for 2020: {most_desired_language}")




# Step 5: Report for Hobby Coding by Gender and Continent
def categorize_gender(gender):
    if pd.isna(gender):
        return 'OTHERS'
    genders = str(gender).lower()
    # genders = gender.lower()
    if 'man' == genders:
        return 'MAN'
    elif 'woman' == genders:
        return 'WOMAN'
    else:
        return 'OTHERS'

survey_data['GenderCategory'] = survey_data['Gender'].apply(categorize_gender)
hobby_report = survey_data.groupby(['Continent', 'GenderCategory'])['Hobbyist'].value_counts(normalize=True).unstack().fillna(0) # no % yes % 
# hobby_report = survey_data.groupby(['Continent', 'GenderCategory'])['Hobbyist'].value_counts().unstack().fillna(0) # numerical nos no yes
print("\nReport for coding as a hobby by gender and continent:")
print(hobby_report)



# Step 6: Report for Job and Career Satisfaction by Gender and Continent
# Define a mapping for satisfaction levels
satisfaction_mapping = {
    'Very Dissatisfied': 1,
    'Dissatisfied': 2,
    'Slightly dissatisfied': 3,
    'NA': 4,
    'Neither satisfied nor dissatisfied '
    'Slightly satisfied': 5,
    'Satisfied': 6,
    'Very satisfied': 7
}

# Convert satisfaction columns to numeric
survey_data['JobSatNumeric'] = survey_data['JobSat'].map(satisfaction_mapping)
survey_data['CareerSatNumeric'] = survey_data['CareerSat'].map(satisfaction_mapping)

# Group by 'Continent' and 'GenderCategory', then calculate averages
satisfaction_report = survey_data.groupby(['Continent', 'GenderCategory'])[['JobSatNumeric', 'CareerSatNumeric']].mean()

print("\nReport for job and career satisfaction by gender and continent:")
print(satisfaction_report)
