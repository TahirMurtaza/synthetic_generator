# rendering contact.html template and making JSON response
from logging import exception
import time
import zipfile
from flask import Flask, render_template, jsonify,make_response,request,Response,g
from flask_login import current_user, LoginManager, login_user, logout_user, login_required
from flask.helpers import flash, url_for
import pandas as pd
from werkzeug.utils import redirect, send_file
from werkzeug.wrappers import response
from app.data_generator import DataGenerator
from flask import Blueprint
import simplejson
from app.models import Rights, User

home = Blueprint('main', __name__)
from main import db,create_app

#create database
db.create_all(app=create_app())

@home.route("/")
@login_required
def index():
    return render_template("home.html")

@home.route("/userrights")
def get_rights():
    id = current_user.get_id()
    user = User.query.filter_by(id=id).first()
    rights = Rights.query.filter_by(name=user.rights).first()
    resp = {'rights': rights.rights}
    return make_response(jsonify(resp), 200)

@home.route('/generatemaster', methods=['POST'])
def generatmaster():
    if request.method == 'POST':
        try:
            # Get checked Synthetic Data Generator Radio
            data_generator = request.form['synthetic_generator']
            
            # Get Field Parameters from Form
            curve_key = request.form['curve_key']
            unique_key = request.form['unique_key']
            if request.form['customer'] != "" : customer = int(request.form['customer']) 
            else: customer = 0
            if request.form['order'] != "": order = int(request.form['order'])
            else: order = 0
            if request.form['transaction'] != "": transaction = int(request.form['transaction'])
            else: transaction = 0
            if request.form['fulfillment'] != "": fulfillment = int(request.form['fulfillment'])
            else: fulfillment = 0
            # Get checked Store Parameters comma seprated from Form
            stores = request.form['stores']
            
            # Output Parameters comma seprated
            output_params = request.form['output_params']
            
            # Initialize DataGenerator class
            datagen = DataGenerator()
            
            # Set Field variables in Data Generator class
            datagen.curve_key = curve_key
            datagen.unique_key = unique_key
            datagen.no_customers = customer
            datagen.no_orders = order
            datagen.no_transactions = transaction
            datagen.no_fulfillments = fulfillment
            
            # Set Shop variables in Data Generator class
            if stores:
                if "Shopify" in stores:
                    datagen.STORE_SHOPIFY = True # Store 1: Shopify store plugin
                if "Magento" in stores:
                    datagen.STORE_MAGENTO = True # Store 2: Magento store plugin
                if "WooCommerce" in stores:
                    datagen.STORE_WOOCOMMERCE = True # Store 3: WooCommerece store plugin
                if "BigCommerce" in stores:
                    datagen.STORE_BIGCOMMERCE = True # Store 4: BigCommerce store plugin 

            
            # Set Output variables in Data Generator class
        
            if output_params:
                if 'customer' in output_params:
                    datagen.CUSTOMERS_MASTER = True
                    
                if 'order' in output_params:
                    datagen.ORDERS_MASTER = True
                    
                if 'transaction' in output_params:
                    datagen.TRANSACTIONS_MASTER = True
                    
                if 'fulfillment' in output_params:
                    datagen.FULFILLMENTS_MASTER = True
                
                if 'product' in output_params:
                    datagen.PRODUCT_MASTER = True
            
            # resp variable to show response to user
            resp = ''
            if data_generator == "New Data Generation":
                # New data Generator function
                res = datagen.generateNewData()
               
                if res:
                    # return response from generateNewData() and display to user
                    resp = {'feedback': res}
                else:
                    resp = {'feedback': "New Data Generated Successfully"}
            else:
                # Download Data Extract function
                datagen.extractData()
                resp = {'feedback': "Data Extracted Successfully"}
                
        except Exception as e:
                resp = {'feedback': str(e)}
                
    return make_response(jsonify(resp), 200)


@home.route("/downloadcsv", methods=['POST'])
def download_file():
   
    # Get checked Synthetic Data Generator Radio
    data_generator = request.form['synthetic_generator']
    
    # Get Field Parameters from Form
    
    curve_key = request.form['curve_key']
    unique_key = request.form['unique_key']
    if request.form['customer'] != "" : customer = int(request.form['customer']) 
    else: customer = 0
    if request.form['order'] != "": order = int(request.form['order'])
    else: order = 0
    if request.form['transaction'] != "": transaction = int(request.form['transaction'])
    else: transaction = 0
    if request.form['fulfillment'] != "": fulfillment = int(request.form['fulfillment'])
    else: fulfillment = 0
    # Get checked Store Parameters comma seprated from Form
    stores = request.form['stores']
    
    # Output Parameters comma seprated
    output_params = request.form['output_params']
    
    # Initialize DataGenerator class
    datagen = DataGenerator()
    
    # Set Field variables in Data Generator class
    datagen.curve_key = curve_key
    datagen.unique_key = unique_key
    datagen.no_customers = customer
    datagen.no_orders = order
    datagen.no_transactions = transaction
    datagen.no_fulfillments = fulfillment
    
    
    

    # Set Shop variables in Data Generator class
    if stores:
        if "Shopify" in stores:
            datagen.STORE_SHOPIFY = True # Store 1: Shopify store plugin
        if "Magento" in stores:
            datagen.STORE_MAGENTO = True # Store 2: Magento store plugin
        if "WooCommerce" in stores:
            datagen.STORE_WOOCOMMERCE = True # Store 3: WooCommerece store plugin
        if "BigCommerce" in stores:
            datagen.STORE_BIGCOMMERCE = True # Store 4: BigCommerce store plugin 

    
    # Set Output variables in Data Generator class
    if output_params:
        if 'customer' in output_params:
            datagen.CUSTOMERS_MASTER = True
            
        if 'order' in output_params:
            datagen.ORDERS_MASTER = True
            
        if 'transaction' in output_params:
            datagen.TRANSACTIONS_MASTER = True
            
        if 'fulfillment' in output_params:
            datagen.FULFILLMENTS_MASTER = True
        
        if 'product' in output_params:
                    datagen.PRODUCT_MASTER = True
                    
   
    if data_generator == "New Data Generation":
        # Fetched data from snowflake according to the selected checked boxes
        my_data = datagen.downloadData()
        
        return make_response(jsonify(my_data),200)
        # with zipfile.ZipFile('app/synthetic_generator/data/csvfiles.zip', 'w') as csv_zip:
        #     for dt in my_data:
        #         # Iterating through keys of DataFrame 
        #         for key, df in dt.items():
        #                 if isinstance(df, pd.DataFrame):
        #                     file_name= f"{key}.csv" 
        #                     csv_zip.writestr(file_name,df.to_csv())
        
    else:
        # Download Data Extract function
        
        datagen.no_customers= 200
        my_data = datagen.downloadData()
        for dt in my_data:
            # Iterating through keys of DataFrame 
            for key, df in dt.items():
                if isinstance(df, pd.DataFrame):
                    # converting df to json
                    dt[key] = simplejson.loads(simplejson.dumps(list(df.T.to_dict().values()),ignore_nan=True))
        
        # Added timer to check the progress loading
        time.sleep(5)
        return make_response(jsonify(my_data),200)
        
   


@home.route("/download")   
def download():
    path = "app/synthetic_generator/data/"
    return send_file(path+'csvfiles.zip',mimetype = 'zip',
                as_attachment=True, environ=request.environ,
                )



def customer_master(customer_count):
    """Synthetic Customer Generator"""
    try:
        return str("OK")
    except ValueError:
        return "invalid input"
    
 

