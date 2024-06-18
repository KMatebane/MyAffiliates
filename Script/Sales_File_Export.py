# Package used to connect to MySQL Databases
import mysql.connector
import pymysql

# XML Creation
import xml.etree.ElementTree as ET
import os

# Data Manipulation Packages
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

# Package To Ignore Warnings
import warnings
warnings.filterwarnings("ignore")

Root = os.path.normpath(os.getcwd() + os.sep + os.pardir)
Name = 'MyAffiliates_SalesFile'

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
                                        ,a.NGR_sp                           AS SPORTSBOOK_NET_REVENUE	\
                                        ,a.qty_cr                           AS CRASH_BETS	\
                                        ,a.to_cr                            AS CRASH_STAKE	\
                                        ,(a.GGR_cr - (a.GGR_cr * 0.25))     AS CRASH_GROSS_REVENUE	\
                                        ,d.cr_cash_bonus_amt                AS CRASH_BONUS	\
                                        ,a.NGR_cr                           AS CRASH_NET_REVENUE	\
                                        ,a.qty_ca                           AS CASINO_BETS	\
                                        ,a.to_ca                            AS CASINO_STAKE	\
                                        ,(a.GGR_ca - (a.GGR_ca * 0.25))     AS CASINO_GROSS_REVENUE	\
                                        ,d.ca_cash_bonus_amt                AS CASINO_BONUS	\
                                        ,a.NGR_ca                           AS CASINO_NET_REVENUE	\
                                        ,a.qty_v                            AS VIRTUALS_BETS	\
                                        ,a.to_v                             AS VIRTUALS_STAKES	\
                                        ,(a.GGR_v - (a.GGR_v * 0.25))       AS VIRTUALS_GROSS_REVENUE	\
                                        ,d.vi_cash_bonus_amt                AS VIRTUALS_BONUS\
                                        ,a.NGR_v                            AS VIRTUALS_NET_REVENUE\
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
                                GROUP BY 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26\
\
                                ORDER BY a.profile_id\
                                        ,a.summary_date\
                                \
                                ) AS x;"
                         ,cobi_betika)
        
finally:
    cobi_betika.close()


Month = df['TRANSACTION_DATE'][0].strftime('%m') + '. ' + df['TRANSACTION_DATE'][0].strftime('%B') + '/'
Year  = df['TRANSACTION_DATE'][0].strftime('%Y') + '/'
Day   = df['TRANSACTION_DATE'][0].strftime('%Y_%m_%d')

export_path = Root + '/Reports/SalesFiles/' + Year + Month
file_name   = Name +'_'+ Day + '.xlsx'
file_path   = export_path + file_name

if not os.path.exists(export_path):
        os.makedirs(export_path)

df.to_excel(file_path,index=False,sheet_name='Sales_File_'+Day)