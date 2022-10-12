from faker import Faker
import pandas as pd
import os



from .synthetic_generator.src.synthetic_data import *
# from src.snowflake_query import *
# from src.utilities import *

from .synthetic_generator.src.store_shopify import *
# from src.store_magento import *
# from src.store_bigcommerce import *
# from src.store_woocommerce import *

from .synthetic_generator.config.data_parameters import *
from .synthetic_generator.config.tables_dtypes import *
from .synthetic_generator.config.mapping_shopify import *



class DataGenerator:
    def __init__(self):
        self.fake = Faker()
        
        self.curve_key = ""
        self.unique_key = ""
        self.no_customers = 0 # Number of customers
        self.no_orders = 0 # Number of orders
        self.no_transactions = 0 # Number of transactions
        self.no_fulfillments = 0 # Number of fulfillments

        
        self.STORE_SHOPIFY = False
        self.STORE_MAGENTO = False 
        self.STORE_BIGCOMMERCE = False 
        self.STORE_WOOCOMMERCE = False
        
        
        self.CUSTOMERS_MASTER = False
        # True - Generate customers master data based on the 'customers_param' parameters specified in the data_parameters.py (see data_parameters.py in config folder)
        self.ORDERS_MASTER = False
        # True - Generate orders master data based on the 'orders_param' parameters specified in the data_parameters.py (see data_parameters.py in config folder)
        self.TRANSACTIONS_MASTER = False
        # True - Generate transactions master data based on the 'transactions_param' parameters specified in the data_parameters.py (see data_parameters.py in config folder)
        self.FULFILLMENTS_MASTER = False
        # True - Generate fulfillments master data based on the 'fulfillments_param' parameters specified in the data_parameters.py (see data_parameters.py in config folder)
        self.PRODUCT_MASTER = False
        # True - Generate fulfillments master data based on the 'product_param' parameters specified in the data_parameters.py (see data_parameters.py in config folder)


        # ## necessary for correct states abbrevation
        self.states_df = pd.read_csv('app/synthetic_generator/database/states.tsv', sep='\t')
        self.states_df.index = self.states_df['Postal Code']
        
        
    #  New Data Generation function  
    def generateNewData(self):
        result = None
        try:
            
            if self.CUSTOMERS_MASTER:
                result = self.customerMaster()
            if self.ORDERS_MASTER:
                self.orderMaster()
            if self.TRANSACTIONS_MASTER:
                self.transactionMaster()
            if self.FULFILLMENTS_MASTER:
                self.fulfillmentMaster()
            if self.PRODUCT_MASTER:
                self.productMaster()
            return result
        except Exception as e:
            return e
    
    #  Download Data Extract function  
    def extractData(self):
        pass
    
    def downloadData(self):
        data = []
        if self.CUSTOMERS_MASTER:
            data.append(self.customerMaster_Download())
        return data
    
    
    def customerMaster(self):
        print("====================================================================")
        print(" CUSTOMERS MASTER DATA ")
        print("====================================================================")
        
         #===========================================================================
        #	CUSTOMERS MASTER DATA 
        #===========================================================================
        data_ecommerce = synthetic_data(total_count=self.no_customers)
        
		# Generating new customers master data
        customers = data_ecommerce.customers_master(self.states_df, fake, None, None)
        customers_master_df = pd.DataFrame(customers)
        #customers_master_df.to_excel(os.path.join('synthetic_generator/data','customers_master.xlsx'), index=False) # writes to output file
        customers_master_df.to_csv(os.path.join('app/synthetic_generator/data','customers_master.csv'), index=False)
        #---------------------------------------------------------------------------
		# UPDATE DB - CUSTOMERS SHOPIFY (STORE 1)
		#---------------------------------------------------------------------------
        if(self.STORE_SHOPIFY):
            print('SHOPIFY')
            customers_shopify_df = customers_shopify(customers_master_df)
            #customers_shopify_df.to_excel(os.path.join('synthetic_generator/data','customers_shopify.xlsx'), index=False) # writes to output file
            customers_master_df.to_csv(os.path.join('app/synthetic_generator/data','customers_shopify.csv'), index=False)
        #==========================================================================

		#---------------------------------------------------------------------------
		# UPDATE DB - CUSTOMERS MAGENTO (STORE 2)
		#---------------------------------------------------------------------------
        if(self.STORE_MAGENTO):
	        print('MAGENTO')
			
		#==========================================================================

		#---------------------------------------------------------------------------
		# UPDATE DB - CUSTOMERS BIGCOMMERCE (STORE 3)
		#---------------------------------------------------------------------------
        if(self.STORE_BIGCOMMERCE):
	        print('BIGCOMMERCE')
			
		#==========================================================================

		#---------------------------------------------------------------------------
		# UPDATE DB - CUSTOMERS WOOCOMMERCE (STORE 4)
		#---------------------------------------------------------------------------
        if(self.STORE_WOOCOMMERCE):
            print('WOOCOMMERCE')
			
		#==========================================================================

        del customers_master_df
        return "success"
            
    def customerMaster_Download(self):
        print("====================================================================")
        print(" CUSTOMERS MASTER DATA ")
        print("====================================================================")
        
         #===========================================================================
        #	CUSTOMERS MASTER DATA 
        #===========================================================================
        data_ecommerce = synthetic_data(total_count=self.no_customers)
        customer_data = {}
		
        # Fetch the Customer DF here 
        customers = data_ecommerce.customers_master(self.states_df, fake, None, None)
        customers_master_df = pd.DataFrame(customers)
        customer_data["customer_master"] = customers_master_df
      
        if(self.STORE_SHOPIFY):
            print('SHOPIFY')
            # Fetch the Customer Shopify DF here
            customers_shopify_df = customers_shopify(customers_master_df)
            customer_data["customer_shopify"] = customers_shopify_df
        #==========================================================================

	
        if(self.STORE_MAGENTO):
            print('MAGENTO')
            # Fetch the Customer MAGENTO DF here
            customers_magento_df = customers_shopify(customers_master_df)
            customer_data["customer_magento"] = customers_magento_df
			
		#==========================================================================

		
        if(self.STORE_BIGCOMMERCE):
            print('BIGCOMMERCE')
            # Fetch the Customer BIGCOMMERCE DF here
            customers_bigcommece_df = customers_shopify(customers_master_df)
            customer_data["customer_bigcommece"] = customers_bigcommece_df
            
			
		#==========================================================================

		
        if(self.STORE_WOOCOMMERCE):
            print('WOOCOMMERCE')
            # Fetch the Customer WOOCOMMERCE DF here
            customers_woocommerce_df = customers_shopify(customers_master_df)
            customer_data["customer_woocommerce"] = customers_woocommerce_df
			
		#==========================================================================

        return customer_data

    def orderMaster(self):
       
        print("====================================================================")
        print(" Order MASTER DATA ")
        print("====================================================================")
        
         #===========================================================================
        #	Order MASTER DATA 
        #===========================================================================
        data_ecommerce = synthetic_data(total_count=self.no_customers)
        customer_data = {}
		
        # Fetch the Customer DF here 
        customers = data_ecommerce.customers_master(self.states_df, fake, None, None)
        customers_master_df = pd.DataFrame(customers)
        customer_data["order_master"] = customers_master_df
      
        if(self.STORE_SHOPIFY):
            print('SHOPIFY')
            # Fetch the Customer Shopify DF here
            customers_shopify_df = customers_shopify(customers_master_df)
            customer_data["order_shopify"] = customers_shopify_df
        #==========================================================================

	
        if(self.STORE_MAGENTO):
            print('MAGENTO')
            # Fetch the Customer MAGENTO DF here
            customers_magento_df = customers_shopify(customers_master_df)
            customer_data["order_magento"] = customers_magento_df
			
		#==========================================================================

		
        if(self.STORE_BIGCOMMERCE):
            print('BIGCOMMERCE')
            # Fetch the Customer BIGCOMMERCE DF here
            customers_bigcommece_df = customers_shopify(customers_master_df)
            customer_data["order_bigcommece"] = customers_bigcommece_df
            
			
		#==========================================================================

		
        if(self.STORE_WOOCOMMERCE):
            print('WOOCOMMERCE')
            # Fetch the Customer WOOCOMMERCE DF here
            customers_woocommerce_df = customers_shopify(customers_master_df)
            customer_data["order_woocommerce"] = customers_woocommerce_df
			
		#==========================================================================
        return customer_data
    
    def transactionMaster(self):
        print("====================================================================")
        print(" Order MASTER DATA ")
        print("====================================================================")
        
         #===========================================================================
        #	Transaction MASTER DATA 
        #===========================================================================
        data_ecommerce = synthetic_data(total_count=self.no_customers)
        customer_data = {}
		
        # Fetch the Customer DF here 
        customers = data_ecommerce.customers_master(self.states_df, fake, None, None)
        customers_master_df = pd.DataFrame(customers)
        customer_data["transaction_master"] = customers_master_df
      
        if(self.STORE_SHOPIFY):
            print('SHOPIFY')
            # Fetch the Customer Shopify DF here
            customers_shopify_df = customers_shopify(customers_master_df)
            customer_data["transaction_shopify"] = customers_shopify_df
        #==========================================================================

	
        if(self.STORE_MAGENTO):
            print('MAGENTO')
            # Fetch the Customer MAGENTO DF here
            customers_magento_df = customers_shopify(customers_master_df)
            customer_data["transaction_magento"] = customers_magento_df
			
		#==========================================================================

		
        if(self.STORE_BIGCOMMERCE):
            print('BIGCOMMERCE')
            # Fetch the Customer BIGCOMMERCE DF here
            customers_bigcommece_df = customers_shopify(customers_master_df)
            customer_data["transaction_bigcommece"] = customers_bigcommece_df
            
			
		#==========================================================================

		
        if(self.STORE_WOOCOMMERCE):
            print('WOOCOMMERCE')
            # Fetch the Customer WOOCOMMERCE DF here
            customers_woocommerce_df = customers_shopify(customers_master_df)
            customer_data["transaction_woocommerce"] = customers_woocommerce_df
			
		#==========================================================================
        return customer_data
    
    def fulfillmentMaster(self):
        print("fulfillment Master")
        return None
    
    def productMaster(self):
        print("product Master")
        return None