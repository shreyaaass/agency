import csv
import pandas as pd

# Specify the file paths
input_file_path = 'youthoob.csv'
output_file_path = 'your_output_file.csv'
df = pd.DataFrame(columns=["Title", "Description", "Views", "Transcript"])

with open(input_file_path, 'r') as input_file:
    csv_reader = csv.reader(input_file, delimiter=';')

    for i, row in enumerate(csv_reader):
        title, description, views = row[0], row[1], row[2]
        transcript = "".join(row[3:])
        df.loc[i] = [title, description, views, transcript]

df.to_csv(output_file_path, index=False, sep=';')
print(df.head())