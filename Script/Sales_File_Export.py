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
Name = 'Betika_SalesFile'

# Files That Contains MySQL Credentials
file = open('/home/kmatebane/Github/MyAffiliates/Connect/Connect.txt', 'r')
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
                                ,x.FIRST_DEPOSIT_AMOUNT\
                                ,x.TOTAL_DEPOSITS\
                                ,x.SPORTSBOOK_BETS      \
                                ,x.SPORTSBOOK_STAKE     \
                                ,x.SPORTSBOOK_GROSS_REVENUE     \
                                ,COALESCE(y.SPORTSBOOK_BONUS,0)                                 AS SPORTSBOOK_BONUS\
                                ,(x.SPORTSBOOK_GROSS_REVENUE - COALESCE(y.SPORTSBOOK_BONUS,0))  AS SPORTSBOOK_NET_REVENUE    \
                                ,x.CRASH_BETS   \
                                ,x.CRASH_STAKE  \
                                ,x.CRASH_GROSS_REVENUE  \
                                ,COALESCE(y.CRASH_BONUS,0) AS CRASH_BONUS\
                                ,(x.CRASH_GROSS_REVENUE - COALESCE(y.CRASH_BONUS,0))            AS CRASH_NET_REVENUE \
                                ,x.CASINO_BETS  \
                                ,x.CASINO_STAKE \
                                ,x.CASINO_GROSS_REVENUE \
                                ,COALESCE(y.CASINO_BONUS, 0)                                    AS CASINO_BONUS \
                                ,(x.CASINO_GROSS_REVENUE - COALESCE(y.CASINO_BONUS,0))          AS CASINO_NET_REVENUE\
                                ,x.VIRTUALS_BETS        \
                                ,x.VIRTUALS_STAKES      \
                                ,x.VIRTUALS_GROSS_REVENUE       \
                                ,COALESCE(y.VIRTUALS_BONUS,0) AS VIRTUALS_BONUS\
                                ,(x.VIRTUALS_GROSS_REVENUE - COALESCE(y.VIRTUALS_BONUS,0))      AS VIRTUALS_NET_REVENUE\
\
                        FROM (SELECT  z.TRANSACTION_DATE\
                                    ,z.BTAG\
                                    ,z.PLAYER_ID\
                                    ,z.PLAYER_CURRENCY\
                                    ,z.ROLLBACKS\
                                    ,z.FIRST_DEPOSIT_AMOUNT\
                                    ,z.TOTAL_DEPOSITS\
                                    ,z.SPORTSBOOK_BETS  \
                                    ,z.SPORTSBOOK_STAKE \
                                    ,z.SPORTSBOOK_GROSS_REVENUE \
                                    ,z.CRASH_BETS       \
                                    ,z.CRASH_STAKE      \
                                    ,z.CRASH_GROSS_REVENUE      \
                                    ,z.CASINO_BETS      \
                                    ,z.CASINO_STAKE     \
                                    ,z.CASINO_GROSS_REVENUE     \
                                    ,z.VIRTUALS_BETS    \
                                    ,z.VIRTUALS_STAKES  \
                                    ,z.VIRTUALS_GROSS_REVENUE   \
\
                            FROM (SELECT a.summary_date                             AS TRANSACTION_DATE\
                                        ,c.affiliate_tag                                AS BTAG\
                                        ,a.profile_id                                   AS PLAYER_ID    \
                                        ,'GHS'                                          AS PLAYER_CURRENCY\
                                        ,0 AS ROLLBACKS\
                                        ,CASE WHEN e.first_deposit = a.summary_date \
                                            THEN a.dep ELSE 0 \
                                            END AS FIRST_DEPOSIT_AMOUNT\
                                        ,a.dep                                          AS TOTAL_DEPOSITS\
                                        ,a.qty_sp_cash                                  AS SPORTSBOOK_BETS      \
                                        ,a.to_sp_cash                                   AS SPORTSBOOK_STAKE     \
                                        ,(a.GGR_sp - (a.GGR_sp * 0.25))                 AS SPORTSBOOK_GROSS_REVENUE  \
                                        ,a.NGR_sp                                       AS SPORTSBOOK_NET_REVENUE    \
                                        ,a.qty_cr                                       AS CRASH_BETS   \
                                        ,a.to_cr                                        AS CRASH_STAKE  \
                                        ,(a.GGR_cr - (a.GGR_cr * 0.25))                 AS CRASH_GROSS_REVENUE       \
                                        ,a.NGR_cr                                       AS CRASH_NET_REVENUE    \
                                        ,a.qty_ca                                       AS CASINO_BETS  \
                                        ,a.to_ca                                        AS CASINO_STAKE \
                                        ,(a.GGR_ca - (a.GGR_ca * 0.25))                 AS CASINO_GROSS_REVENUE      \
                                        ,a.NGR_ca                                       AS CASINO_NET_REVENUE   \
                                        ,a.qty_v                                        AS VIRTUALS_BETS        \
                                        ,a.to_v                                         AS VIRTUALS_STAKES      \
                                        ,(a.GGR_v - (a.GGR_v * 0.25))                   AS VIRTUALS_GROSS_REVENUE    \
                                        ,a.NGR_v                                        AS VIRTUALS_NET_REVENUE\
                                        ,c.created\
                                        ,RANK() OVER (PARTITION BY c.profile_id ORDER BY c.created DESC) AS Ranking\
\
                                FROM betika_bi_gh.f_kpi_gh AS a\
\
                                LEFT JOIN betika_bi_gh.profile AS b\
                                ON a.profile_id = b.profile_id\
\
                                LEFT JOIN betika_bi_gh.affiliate_tx AS c\
                                ON a.profile_id = c.profile_id\
\
                                LEFT JOIN betika_bi_gh.dim_first_last_gh AS e\
                                ON a.profile_id = e.profile_id\
\
                                WHERE DATE(a.summary_date) >= DATE(CURDATE()- INTERVAL 1 DAY)\
\
                                AND (c.affiliate_tag IS NOT NULL AND c.affiliate_tag NOT IN ('None', 'Null'))\
\
                                GROUP BY 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24\
\
                                ORDER BY a.profile_id\
                                        ,a.summary_date\
                                \
                                ) AS z\
                                WHERE z.Ranking = 1\
                            ) AS x\
\
                        LEFT OUTER JOIN (SELECT z.PLAYER_ID\
                                            ,z.SPORTSBOOK_BONUS\
                                            ,z.CRASH_BONUS\
                                            ,z.CASINO_BONUS\
                                            ,z.VIRTUALS_BONUS\
\
                                        FROM (SELECT a.profile_id AS PLAYER_ID\
                                                    ,a.sp_cash_bonus_amt                            AS SPORTSBOOK_BONUS\
                                                    ,a.cr_cash_bonus_amt                            AS CRASH_BONUS\
                                                    ,a.ca_cash_bonus_amt                            AS CASINO_BONUS\
                                                    ,a.vi_cash_bonus_amt                            AS VIRTUALS_BONUS\
                                                    ,b.created\
                                                    ,RANK() OVER (PARTITION BY b.profile_id ORDER BY b.created DESC) AS Ranking \
                                        \
                                            FROM betika_bi_gh.f_bonus_credited AS a\
                                            LEFT JOIN betika_bi_gh.affiliate_tx AS b\
                                            ON a.profile_id = b.profile_id\
                                            \
                                            WHERE DATE(a.summary_date) >= DATE(CURDATE()- INTERVAL 1 DAY)\
                                            AND (b.affiliate_tag IS NOT NULL AND b.affiliate_tag NOT IN ('None', 'Null'))\
                                            GROUP BY 1,2,3,4,5,6\
                                            \
                                            ) AS z \
                                        WHERE z.Ranking = 1\
                                        ) AS y\
                            \
                        ON x.PLAYER_ID = y.PLAYER_ID;"
                         ,cobi_betika)
        
finally:
    cobi_betika.close()

df['SPORTSBOOK_BETS'] = 0
df['SPORTSBOOK_STAKE'] = 0
df['SPORTSBOOK_GROSS_REVENUE'] = 0
df['SPORTSBOOK_BONUS'] = 0
df['SPORTSBOOK_NET_REVENUE'] = 0

# Gets Date, Month & Year that the data is created from. Date helps name the file, and Year & Month help create the folders that report sits in. 
Month = df['TRANSACTION_DATE'][0].strftime('%m') + '_' + df['TRANSACTION_DATE'][0].strftime('%B') + '/'
Year  = df['TRANSACTION_DATE'][0].strftime('%Y') + '/'
Date  = df['TRANSACTION_DATE'][0].strftime('%Y-%m-%d')

# creates path that file will be placed in
export_path = '/home/kmatebane/Github/MyAffiliates/Reports/SalesFiles/' + Year + Month

# creates file name
file_name   = Name +'_'+ Date + '.csv'

# creates path with file name. Will be used to create excel document & used to fetch the correct document
file_path   = export_path + file_name

# Checks if folders and subfolders exit. If not, creates new folders and subfolders
if not os.path.exists(export_path):
        os.makedirs(export_path)

# Exports file to excel document
df.to_csv(file_path,index=False)

# SFTP Credentials
host = 'ftp.myaffiliates.com'
port = 2222
username = 'betika_data'
password = 'P1QY74p7XwUezEcO'
remote_filepath = '/myaffiliates/betika/data/queue/' + file_name

# Create an SSH client
ssh = paramiko.SSHClient()
ssh.load_system_host_keys()

# Create SSH Connection Container
ssh.connect(hostname=host, port=port, username=username, password=password)
print("SSH connection successful")

# Open an SFTP session
sftp = ssh.open_sftp()
print("SFTP connection successful")

# Upload file from VM to SFTP
sftp.put(file_path, remote_filepath)
print(f"File {file_path} uploaded to {remote_filepath}")

# List directory contents after upload
print("Listing directory contents after upload:")
print(sftp.listdir())


# Close the SFTP session and SSH client
sftp.close()