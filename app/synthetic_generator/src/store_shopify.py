import pandas as pd
from ..config.mapping_shopify import *


#===========================================================================
# CUSTOMERS SHOPIFY (MAPPING FROM MASTER DATA TO SHOPIFY)
#===========================================================================
def customers_shopify(customers_master_df):
    """Mapping customers masters data to shopfy format"""

    # INPUT:
    # customers_master_df   -   customers master DataFrame
    # 
    # OUTPUT:
    # customers_shopify_df  -   Mapped DataFrame based on Shopify customer attributes
    
    # list of attributes based on Shopify customer template
    col_list = list(customer_shopify_master.keys())
    customers_shopify_df = pd.DataFrame(columns = col_list)

    for ii in range(len(customers_master_df)):
        for columns in col_list:
            if(len(customer_shopify_master[columns]) > 0):
                # mapping master data to shopify format based on the mapping criteria specified in mapping_shopify.py (see config folder)
                customers_shopify_df.loc[ii,columns] = customers_master_df.loc[ii, customer_shopify_master[columns]] 

    return customers_shopify_df

