import os       

# Data Manipulation Packages
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Package To Ignore Warnings
import warnings
warnings.filterwarnings("ignore")

Root = os.path.normpath(os.getcwd() + os.sep + os.pardir)
Name = 'MyAffliates_SalesFile'


Month = (datetime.now() - timedelta(days=1)).strftime('%m') + '_' + (datetime.now() - timedelta(days=1)).strftime('%B') + '/'
Year  = (datetime.now() - timedelta(days=1)).strftime('%Y') + '/'
Day   = (datetime.now() - timedelta(days=1)).strftime('%Y_%m_%d')

export_path = Root + '/Reports/SalesFiles/' + Year + Month
file_name   = Name +'_'+ Day + '.xlsx'
file_path   = export_path + file_name

if not os.path.exists(export_path):
        os.makedirs(export_path)