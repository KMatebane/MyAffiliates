import pysftp

def sftp_connection():
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    server = pysftp.Connection('ftp.myaffiliates.com', username='betika_data', password='P1QY74p7XwUezEcO', cnopts=cnopts)  ############# what's the password
    return server

def test_sftp_connection():
    try:
        server = sftp_connection()
        server.cwd('/myaffiliates/betika/data/queue')  ############## change the directory
        print("SFTP connection test successful")
        server.close()
    except Exception as e:
        print("SFTP connection test failed:", str(e))

test_sftp_connection()