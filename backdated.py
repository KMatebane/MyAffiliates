
import pysftp
import paramiko
import os

host     = 'ftp.myaffiliates.com'
username = 'betika_data'
password = 'P1QY74p7XwUezEcO'
port     =  2222
Root = os.path.normpath(os.getcwd() + os.sep + os.pardir)


remote_source_dir = Root + '/MyAffiliates/Backdated'
remote_destination_dir = '/myaffiliates/betika/data/queue'


ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.load_system_host_keys()


ssh.connect(hostname=host, port=port, username=username, password=password)
print("SSH connection successful")


sftp = ssh.open_sftp()
print("SFTP connection successful")


transport = paramiko.Transport((host, port))
transport.connect(username=username, password=password)

# Start SFTP session
sftp = paramiko.SFTPClient.from_transport(transport)

try:
    # List all files in the remote source directory
    for filename in sftp.listdir(remote_source_dir):
        remote_file_path = f'{remote_source_dir}/{filename}'
        remote_dest_file_path = f'{remote_destination_dir}/{filename}'

        # Check if the current item is a file
        if paramiko.SFTPAttributes.is_file(sftp.stat(remote_file_path)):
            # Option 1: Move files within the SFTP server
            sftp.rename(remote_file_path, remote_dest_file_path)
            print(f'Moved {filename} to {remote_destination_dir}')
            
            # Option 2: Download files to the local machine
            # local_file_path = os.path.join(local_destination_dir, filename)
            # sftp.get(remote_file_path, local_file_path)
            # print(f'Downloaded {filename} to {local_destination_dir}')
finally:
    # Close the SFTP session and SSH transport
    sftp.close()
    transport.close()

print("All files have been moved/downloaded successfully.")


