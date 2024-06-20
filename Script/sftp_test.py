import pysftp

def sftp_connection():
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = 'AAAAB3NzaC1yc2EAAAADAQABAAABAQDER1AM/lVwpZIDmjtIXWMMY8mN++RKjBEZNR+jroGwZP6GMIOf1mRgvJ8sszMsLCgPQ7jNzqcPfhaoifBe/Tw3m5zg5UueCluQR3Ttj3n8BIyojvRtyYncE80TOEzku+6TGZFQAl8m53psMJhnlFDN7dtegoFn2LTPfFCEC9xBlnlR6l3OPdE85ni4PfTbt5aeivX2dz32BVGP7QWSujDYDmB4fIzE86mWz8nv6ZZKxYKqjNQarOyBK9DPNLl8MvhsumkF7Mcps62jJXhLPVZ1/5uwHSxRcIVSankbelrrz4iKrf7Ff0HJdnvmxlM2nVHRtgU/tr3xX1Ut6Q/OkQ43'
    server = pysftp.Connection(host='ftp.myaffiliates.com', username='betika_data', password='P1QY74p7XwUezEcO', cnopts=cnopts)  ############# what's the password
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