from faker import Faker
import datetime
import pandas as pd
from pandas import ExcelWriter
import numpy as np
import pathlib
import random
import os

import snowflake.connector 
from snowflake.connector.pandas_tools import write_pandas

from src.synthetic_data import *
# from src.snowflake_query import *
# from src.utilities import *

from src.store_shopify import *
# from src.store_magento import *
# from src.store_bigcommerce import *
# from src.store_woocommerce import *

from config.data_parameters import *
from config.tables_dtypes import *
from config.mapping_shopify import *

if __name__ == '__main__':

	fake = Faker()

	CUSTOMERS_MASTER = True
	# True - Generate customers master data based on the 'customers_param' parameters specified in the data_parameters.py (see data_parameters.py in config folder)
	ORDERS_MASTER = False
	# True - Generate orders master data based on the 'orders_param' parameters specified in the data_parameters.py (see data_parameters.py in config folder)
	TRANSACTIONS_MASTER = False
	# True - Generate transactions master data based on the 'transactions_param' parameters specified in the data_parameters.py (see data_parameters.py in config folder)
	FULFILLMENTS_MASTER = False
	# True - Generate fulfillments master data based on the 'fulfillments_param' parameters specified in the data_parameters.py (see data_parameters.py in config folder)

	no_customers = 100 # Number of customers
	no_orders = 80 # Number of orders
	no_transactions = 50 # Number of transactions
	no_fulfillments = 30 # Number of fulfillments

	STORE_SHOPIFY = True # Store 1: Shopify store plugin
	STORE_MAGENTO = True # Store 2: Magento store plugin
	STORE_BIGCOMMERCE = False # Store 3: BigCommerce store plugin
	STORE_WOOCOMMERCE = False # Store 4: WooCommerece store plugin 


	# ## necessary for correct states abbrevation
	states_df = pd.read_csv('database/states.tsv', sep='\t')
	states_df.index = states_df['Postal Code']
	
	#===========================================================================
	#	CUSTOMERS MASTER DATA 
	#===========================================================================
	data_ecommerce = synthetic_data(total_count=no_customers)
	if(CUSTOMERS_MASTER):
		print("====================================================================")
		print(" CUSTOMERS MASTER DATA ")
		print("====================================================================")
		# Generating new customers master data
		customers = data_ecommerce.customers_master(states_df, fake, None, None)
		customers_master_df = pd.DataFrame(customers)
		customers_master_df.to_excel(os.path.join('data','customers_master.xlsx'), index=False) # writes to output file
		#---------------------------------------------------------------------------
		# UPDATE DB - CUSTOMERS SHOPIFY (STORE 1)
		#---------------------------------------------------------------------------
		if(STORE_SHOPIFY):
			print('SHOPIFY')
			customers_shopify_df = customers_shopify(customers_master_df)
			customers_shopify_df.to_excel(os.path.join('data','customers_shopify.xlsx'), index=False) # writes to output file
		#==========================================================================

		#---------------------------------------------------------------------------
		# UPDATE DB - CUSTOMERS MAGENTO (STORE 2)
		#---------------------------------------------------------------------------
		if(STORE_MAGENTO):
			print('MAGENTO')
			
		#==========================================================================

		#---------------------------------------------------------------------------
		# UPDATE DB - CUSTOMERS BIGCOMMERCE (STORE 3)
		#---------------------------------------------------------------------------
		if(STORE_BIGCOMMERCE):
			print('BIGCOMMERCE')
			
		#==========================================================================

		#---------------------------------------------------------------------------
		# UPDATE DB - CUSTOMERS WOOCOMMERCE (STORE 4)
		#---------------------------------------------------------------------------
		if(STORE_WOOCOMMERCE):
			print('WOOCOMMERCE')
			
		#==========================================================================

		del customers_master_df










	