from faker import Faker
import datetime
import random
import string

fake = Faker()
fake.random.seed()

from ..config.data_parameters import *

CID_VAL_MIN = customers_params['id_values_min']
CID_VAL_MAX = customers_params['id_values_max']
CID_VAL_LEN = customers_params['id_values_length']

#===========================================================================
# CUSTOMERS MASTER DATA - PRIMARY
#===========================================================================
def customers_master_primary(states_df):
    """Generate primary attributes for customer master data"""

    # list of customer primary attributes
    list_attributes = ['FIRST_NAME', 'MIDDLE_NAME', 'LAST_NAME',
                        'GENDER', 'PREFIX','SUFFIX','EMAIL',
                        'PHONE', 'ADDRESS1']

    # dictionary based on above list i.e. list_attributes
    attribute_dict = dict.fromkeys(list_attributes)

    method_first_name = 1
    method_cust_prefix = fake.boolean(chance_of_getting_true=70)
    method_cust_suffix = fake.boolean(chance_of_getting_true=30)


    if(method_first_name == 1): # Male - Male
        attribute_dict['FIRST_NAME'] = fake.first_name_male()
        attribute_dict['LAST_NAME'] = fake.last_name_male()
        attribute_dict['GENDER'] = 'Male'
        if(method_cust_prefix):
            attribute_dict['PREFIX'] = fake.prefix_male()
        else:
            attribute_dict['PREFIX'] = ""

        if(method_cust_suffix):
            attribute_dict['SUFFIX'] = fake.suffix_male()
        else:
            attribute_dict['SUFFIX'] = ""


    

    attribute_dict['MIDDLE_NAME'] = fake.first_name_nonbinary()[0:1].upper()+'.'

    attribute_dict['EMAIL'] = attribute_dict['FIRST_NAME'].lower()+'.'+attribute_dict['LAST_NAME'].lower()+'@gmail.com'
    attribute_dict['PHONE'] = fake.phone_number()

    street_address = fake.street_address()
    city = fake.city()
    state_abbr = fake.state_abbr()
    state = states_df.loc[state_abbr]['State']
    zip_code = fake.postalcode_in_state(state_abbr=state_abbr)
    cust_address1 = street_address+', '+city+', '+state_abbr+' '+zip_code

    attribute_dict['STREET'] = street_address
    attribute_dict['CITY'] = city
    attribute_dict['STATE_CODE'] = state_abbr
    attribute_dict['STATE'] = state
    attribute_dict['ZIP_CODE'] = zip_code
    attribute_dict['ADDRESS1'] = cust_address1
    attribute_dict['ADDRESS2'] = " "


    attribute_dict['COUNTRY'] = "United States"
    attribute_dict['COUNTRY_CODE'] = "US"

    return attribute_dict


#===========================================================================
# CUSTOMERS MASTER DATA - SECONDARY
#===========================================================================
def customers_master_secondary(attribute_primary = {}):
    """Generate secondary attributes for customer master data"""

    first_name = attribute_primary['FIRST_NAME']
    last_name = attribute_primary['LAST_NAME']

    # list of secondary customer attributes
    list_attributes = ['CUSTOMER_ID', 'COMPANY', 'USER_LOGIN', 'USER_PASSWORD']
    attribute_dict = dict.fromkeys(list_attributes)

    if('CUSTOMER_ID' in list_attributes):
        customer_id = int(fake.fixed_width(data_columns=[(CID_VAL_LEN, 'pyint', {'min_value': CID_VAL_MIN, 'max_value': CID_VAL_MAX})], align='left', num_rows=1))
        attribute_dict['CUSTOMER_ID'] = customer_id
    if('COMPANY' in list_attributes):
        attribute_dict['COMPANY'] = fake.company()

    if('USER_LOGIN' in list_attributes):
        # random number to pick first name, last name, or first+last name for user login
        method_name = random.randint(0,2)
        # 0 - use first name
        # 1 - use last name
        # 2 - use first and last name
        
        method_no = random.randint(2,5) # number of digits attached in username
        method_underscore = random.randint(0,1) # underscore between name and number
        method_no_min = pow(10,method_no-1)
        method_no_max = pow(10,method_no)-1
        user_number = int(fake.fixed_width(data_columns=[(method_no, 'pyint', {'min_value': method_no_min, 'max_value': method_no_max})], align='left', num_rows=1))

        if(method_name == 0):
            if(method_underscore == 0):
                user_login = first_name.lower()+str(user_number)
            elif(method_underscore == 1):
                user_login = first_name.lower()+'_'+str(user_number)

        elif(method_name == 1):
            if(method_underscore == 0):
                user_login = last_name.lower()+str(user_number)
            elif(method_underscore == 1):
                user_login = last_name.lower()+'_'+str(user_number)

        elif(method_name == 2):
            if(method_underscore == 0):
                user_login = first_name.lower()+last_name.lower()+str(user_number)
            elif(method_underscore == 1):
                user_login = first_name.lower()+last_name.lower()+'_'+str(user_number)

        attribute_dict['USER_LOGIN'] = user_login

    if('USER_PASSWORD' in list_attributes):
        password_len_min = random.randint(8,14) #
        password_len_max = random.randint(password_len_min,20) #
        ch_all = string.ascii_letters + string.digits + string.punctuation
        user_password = "".join(random.sample(ch_all,password_len_max))

        attribute_dict['USER_PASSWORD'] = user_password

    return attribute_dict


