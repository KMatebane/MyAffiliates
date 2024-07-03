import paramiko

def test_sftp_connection():
    try:
        # Define connection parameters
        host = 'ftp.myaffiliates.com'
        port = 2222
        username = 'betika_data'
        password = 'P1QY74p7XwUezEcO'
        remote_filepath = '/myaffiliates/betika/data/queue'

        # Create an SSH client
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()

        #ssh.load_host_keys('/home/ekutniakova/.ssh/known_hosts')
        #ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(hostname=host, port=port, username=username, password=password)
        print("SSH connection test successful")

        # Open an SFTP session
        sftp = ssh.open_sftp()
        print("SFTP connection test successful")

        # List directory contents
        print("Listing directory contents:")
        print(sftp.listdir(remote_filepath))

        # Close the SFTP session and SSH client
        sftp.close()
        ssh.close()
    except Exception as e:
        print("SFTP connection test failed:", str(e))


test_sftp_connection()
