import paramiko
from io import BytesIO
import pandas as pd

# Define the SSH connection parameters
hostname = 'random_path'
port = 22  # Default SSH port
username = 'name'
password = 'pw'  
remote_file_path = 'path'

# Create an SSH client
ssh_client = paramiko.SSHClient()

# Automatically add the server's host key (this is not recommended for production)
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    # Connect to the remote server
    ssh_client.connect(hostname, port, username, password)

    # Open an SFTP session to retrieve the file
    sftp = ssh_client.open_sftp()

    # Read the file from the remote server into a BytesIO buffer
    remote_file = sftp.file(remote_file_path, 'rb')
    buffer = BytesIO(remote_file.read())

    # Close the SFTP session
    sftp.close()

    # Close the SSH connection
    ssh_client.close()

    # Convert the BytesIO buffer to a DataFrame (modify this part according to your file format)
    df = pd.read_csv(buffer, sep=',', on_bad_lines='skip', engine='c', header=0)  # For example, reading a CSV file

    # Return the DataFrame to Power BI
    df
except Exception as e:
    print(f"An error occurred: {str(e)}")
    None