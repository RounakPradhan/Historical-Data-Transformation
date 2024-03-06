import pandas as pd

# Read input CSV file
input_file = 'input.csv'
df = pd.read_csv(input_file)

# Sort DataFrame by employee ID and effective date
df['Date of Joining'] = pd.to_datetime(df['Date of Joining'])
df.sort_values(by=['Employee Code', 'Date of Joining'], inplace=True)

# Initialize list to store transformed records
historical_records = []

# Iterate through each row of the DataFrame
for i in range(len(df)):
    row = df.iloc[i]
    next_row = df.iloc[i + 1] if i < len(df) - 1 else None

    # Derive 'End Date' for each historical record
    end_date = next_row['Date of Joining'] - pd.DateOffset(days=1) if next_row is not None else pd.Timestamp('2100-01-01')

    # Transform columnar data into historical versioning system
    historical_record = {
        'Employee Code': row['Employee Code'],
        'Manager Employee Code': row['Manager Employee Code'],
        'Last Compensation': row['Compensation'],
        'Compensation': row['Compensation 1'],
        'Last Pay Raise Date': row['Compensation 1 date'],
        'Variable Pay': '',
        'Tenure in Org': '',
        'Performance Rating': '',
        'Engagement Score': '',
        'Effective Date': row['Date of Joining'],
        'End Date': end_date
    }

    # Append transformed record to list
    historical_records.append(historical_record)

    # If there is a second compensation entry, add a second historical record
    if not pd.isnull(row['Compensation 2']):
        historical_record = {
            'Employee Code': row['Employee Code'],
            'Manager Employee Code': row['Manager Employee Code'],
            'Last Compensation': row['Compensation 1'],
            'Compensation': row['Compensation 2'],
            'Last Pay Raise Date': row['Compensation 2 date'],
            'Variable Pay': '',
            'Tenure in Org': '',
            'Performance Rating': '',
            'Engagement Score': '',
            'Effective Date': row['Compensation 2 date'],
            'End Date': end_date
        }

        # Append the second transformed record to the list
        historical_records.append(historical_record)

# Convert list of dictionaries to DataFrame
transformed_df = pd.DataFrame(historical_records)

# Write transformed data to CSV
output_file = 'historical_employee_data_output.csv'
transformed_df.to_csv(output_file, index=False)