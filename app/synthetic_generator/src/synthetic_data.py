from faker import Faker
import datetime
import pandas as pd
import json

from numpy import random

from ..config.data_parameters import *
from .customers_master import *



fake1 = Faker()


class synthetic_data:

    def __init__(self, total_count):
        # class constructor
        # Input: total_count (int) - data points to generate

        self.timezone = datetime.timezone(datetime.timedelta(days=0)) # UTC timezone
        self.total_count = total_count

    # --------------------------------------------------------------------------------------------------
    # SYNTHETIC DATA GENERATOR - CUSTOMERS MASTER
    # --------------------------------------------------------------------------------------------------
    def customers_master(self, states_df, fake, cust_df=None, orders_df=None):
        """Synthetic customer data"""

        customers_data = []
        for i in range(0, self.total_count):
            # customer primary attributes e.g. 'FIRST_NAME'
            customer_pri = customers_master_primary(states_df)
            # custoomer seconday attributes e.g. 'USER_LOGIN'
            customer_sec = customers_master_secondary(customer_pri)
            
            customer_val = {**customer_pri,**customer_sec}

            customers_data.append(customer_val)

        return customers_data

   