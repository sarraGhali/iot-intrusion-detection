import pandas as pd
import os

# List of dataset file names
dataset_files_list = ['DDoS_TCP_SYN_Flood_attack.csv', 'Distance.csv', 'IR_Receiver.csv', 'Temperature_and_Humidity.csv', 'Water_Level.csv']

# Path to the directory containing dataset files
data_path = '/content/drive/MyDrive/Senior/Dataset/'

# Initialize an empty DataFrame to store the sampled rows
sampled_df = pd.DataFrame()
# Columns to include in the sampled DataFrame
columns_to_include = ['frame.time', 'ip.src_host', 'ip.dst_host', 'tcp.ack', 'tcp.ack_raw', 'tcp.connection.rst','tcp.connection.syn','tcp.flags.ack',
                      'tcp.dstport','tcp.seq', 'tcp.srcport', 'Attack_label']

# Loop through the dataset files
for filename in dataset_files_list:
    # Read the file
    df = pd.read_csv(os.path.join(data_path, filename), usecols=columns_to_include)

    # Determine the number of rows to sample
    num_rows_to_sample = int(len(df) * 0.05)

    # Sample 5% of the rows
    sampled_rows = df.sample(n=num_rows_to_sample, random_state=42)

    # Concatenate the sampled rows to the sampled_df
    sampled_df = pd.concat([sampled_df, sampled_rows])

# Convert the 'frame.time' column to datetime
sampled_df['frame.time'] = pd.to_datetime(sampled_df['frame.time'])

# Sort the sampled dataframe based on the 'frame.time' column
sampled_df = sampled_df.sort_values(by='frame.time')

# Display the sampled dataframe
print(sampled_df)
# Drop rows where 'ip.src_host' or 'ip.dst_host' has a value of '0'
sampled_df = sampled_df[(sampled_df['ip.src_host'] != '0') & (sampled_df['ip.dst_host'] != '0')]

# Convert the 'frame.time' column to epoch time
sampled_df['frame.time'] = pd.to_datetime(sampled_df['frame.time']).astype(int) // 10**9

# Remove dots from IP addresses
ip_columns = ['ip.src_host', 'ip.dst_host']
for column in ip_columns:
    sampled_df[column] = sampled_df[column].str.replace('.', '').astype(int)

# Assuming sampled_df is your DataFrame
df = sampled_df

# Columns to check for zeros
columns_to_check = ['tcp.seq', 'tcp.srcport', 'tcp.ack', 'tcp.ack_raw', 'tcp.dstport']

# Values to check for zeros
zero_values = ['0', '0.0', '0.000000e+00']

# Create a boolean mask to identify rows with zeros in specified columns
mask = df[columns_to_check].astype(str).isin(zero_values).any(axis=1)

# Drop rows with zeros in specified columns
df = df[~mask]

# Print the updated DataFrame
print("DataFrame after dropping rows with zeros in specified columns:")
print(df)
df = df.dropna()
df = df.drop_duplicates()