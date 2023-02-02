import pandas as pd

# Read in the original CSV file
df_original = pd.read_csv('original_data.csv')

# Read in the cleaned CSV file
df_cleaned = pd.read_csv('result_API_cleaned_file.csv')

# Combine the two dataframes into a single dataframe, with the original CSV file as the first column and the cleaned CSV file as the second column
df = pd.concat([df_original, df_cleaned], axis=1)
df.to_csv('Result_Dataframe_2.csv')

