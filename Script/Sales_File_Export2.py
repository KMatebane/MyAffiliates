# Package used to connect to MySQL Databases
import mysql.connector
import pymysql
import paramiko

# Package For Directories
import os

# Data Manipulation Packages
import pandas as pd
import numpy as np

# Package To Ignore Warnings
import warnings
warnings.filterwarnings("ignore")

# Goes One folder Back, And Gets Directory
Root = os.path.normpath(os.getcwd() + os.sep + os.pardir)

# Name of the file that will have date suffixed to it
Name = 'MyAffiliates_SalesFile'

# Files That Contains MySQL Credentials
file = open(Root + '/Connect/Connect.txt', 'r')
text = file.readlines()

# Code To Connect MySQL
cobi_betika = mysql.connector.connect(host=text[0].strip()
                                      ,database=text[7].strip()
                                      ,user=text[5].strip()
                                      ,password=text[6].strip()
                                      ,port=text[4].strip())

# Connect to MySQL database
try:
    with cobi_betika.cursor() as cursor:
        df = pd.read_sql("SELECT x.TRANSACTION_DATE\
                                ,x.BTAG\
                                ,x.PLAYER_ID\
                                ,x.PLAYER_CURRENCY\
                                ,x.ROLLBACKS\
                                ,x.DEPOSITS\
                                ,x.SPORTSBOOK_BETS	\
                                ,x.SPORTSBOOK_STAKE	\
                                ,x.SPORTSBOOK_GROSS_REVENUE	\
                                ,x.SPORTSBOOK_BONUS	\
                                ,(x.SPORTSBOOK_GROSS_REVENUE - x.SPORTSBOOK_BONUS) AS SPORTSBOOK_NET_REVENUE	\
                                ,x.CRASH_BETS	\
                                ,x.CRASH_STAKE	\
                                ,x.CRASH_GROSS_REVENUE	\
                                ,x.CRASH_BONUS	\
                                ,(x.CRASH_GROSS_REVENUE - x.CRASH_BONUS) AS CRASH_NET_REVENUE	\
                                ,x.CASINO_BETS	\
                                ,x.CASINO_STAKE	\
                                ,x.CASINO_GROSS_REVENUE	\
                                ,x.CASINO_BONUS	\
                                ,(x.CASINO_GROSS_REVENUE - x.CASINO_BONUS) AS CASINO_NET_REVENUE	\
                                ,x.VIRTUALS_BETS	\
                                ,x.VIRTUALS_STAKES	\
                                ,x.VIRTUALS_GROSS_REVENUE	\
                                ,x.VIRTUALS_BONUS\
                                ,(x.VIRTUALS_GROSS_REVENUE - x.VIRTUALS_BONUS) AS VIRTUALS_NET_REVENUE\
\
                            FROM (SELECT a.summary_date                     AS TRANSACTION_DATE\
                                        ,c.affiliate_tag                    AS BTAG\
                                        ,a.profile_id                       AS PLAYER_ID	\
                                        ,'GHS'                              AS PLAYER_CURRENCY\
                                        ,0 AS ROLLBACKS\
                                        ,CASE WHEN e.first_deposit IS NULL \
                                            THEN 0 ELSE 1 \
                                            END AS DEPOSITS\
                                        ,a.qty_sp_cash                      AS SPORTSBOOK_BETS	\
                                        ,a.to_sp_cash                       AS SPORTSBOOK_STAKE	\
                                        ,(a.GGR_sp - (a.GGR_sp * 0.25))     AS SPORTSBOOK_GROSS_REVENUE	\
                                        ,d.sp_cash_bonus_amt                AS SPORTSBOOK_BONUS	\
                                        ,a.qty_cr                           AS CRASH_BETS	\
                                        ,a.to_cr                            AS CRASH_STAKE	\
                                        ,(a.GGR_cr - (a.GGR_cr * 0.25))     AS CRASH_GROSS_REVENUE	\
                                        ,d.cr_cash_bonus_amt                AS CRASH_BONUS	\
                                        ,a.qty_ca                           AS CASINO_BETS	\
                                        ,a.to_ca                            AS CASINO_STAKE	\
                                        ,(a.GGR_ca - (a.GGR_ca * 0.25))     AS CASINO_GROSS_REVENUE	\
                                        ,d.ca_cash_bonus_amt                AS CASINO_BONUS	\
                                        ,a.qty_v                            AS VIRTUALS_BETS	\
                                        ,a.to_v                             AS VIRTUALS_STAKES	\
                                        ,(a.GGR_v - (a.GGR_v * 0.25))       AS VIRTUALS_GROSS_REVENUE	\
                                        ,d.vi_cash_bonus_amt                AS VIRTUALS_BONUS\
\
                                FROM betika_bi_gh.f_kpi_gh AS a\
\
                                LEFT JOIN betika_bi_gh.profile AS b\
                                ON a.profile_id = b.profile_id\
\
                                LEFT JOIN betika_bi_gh.affiliate_tx AS c\
                                ON a.profile_id = c.profile_id\
\
                                LEFT JOIN betika_bi_gh.f_bonus_credited AS d\
                                ON a.profile_id = d.profile_id\
\
                                LEFT JOIN betika_bi_gh.dim_first_last_gh AS e\
                                ON a.profile_id = e.profile_id\
\
                                WHERE DATE(a.summary_date) >= DATE(CURDATE()- INTERVAL 1 DAY)\
                                AND DATE(d.summary_date) >= DATE(CURDATE()- INTERVAL 1 DAY)\
\
                                GROUP BY 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22\
\
                                ORDER BY a.profile_id\
                                        ,a.summary_date\
                                \
                                ) AS x;"
                         ,cobi_betika)
        
finally:
    cobi_betika.close()

# Gets Date, Month & Year that the data is created from. Date helps name the file, and Year & Month help create the folders that report sits in. 
Month = df['TRANSACTION_DATE'][0].strftime('%m') + '_' + df['TRANSACTION_DATE'][0].strftime('%B') + '/'
Year  = df['TRANSACTION_DATE'][0].strftime('%Y') + '/'
Date  = df['TRANSACTION_DATE'][0].strftime('%Y_%m_%d')

# creates path that file will be placed in
export_path = Root + '/Reports/SalesFiles/' + Year + Month

# creates file name
file_name   = Name +'_'+ Date + '.xlsx'

# creates path with file name. Will be used to create excel document & used to fetch the correct document
file_path   = export_path + file_name

# Checks if folders and subfolders exit. If not, creates new folders and subfolders
if not os.path.exists(export_path):
        os.makedirs(export_path)

# Exports file to excel document
df.to_excel(file_path,index=False,sheet_name='Sales_File_'+Date)


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
print("SSH connection successful")

# Open an SFTP session
sftp = ssh.open_sftp()
print("SFTP connection successful")

#sftp.mkdir(remote_filepath)
#print("Path Has Be Created")

#sftp.put(file_path, remote_filepath)
#print(f"File {file_path} uploaded to {remote_filepath}")

# List directory contents after upload
print("Listing directory contents after upload:")
print(sftp.listdir())


# Close the SFTP session and SSH client
sftp.close()
ssh.close()