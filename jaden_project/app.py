from wsgiref import headers
from flask import jsonify, render_template, flash,Flask
from flask import redirect, url_for, request
import pandas as pd
import datetime
from datetime import date
# for accessing google sheets services
from apiclient import discovery
SERVICE_ACCOUNT_FILE = 'gs_key.json'
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
from time import strptime
SCOPES = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive.file']
API_SERVICE_NAME = 'sheets'
API_VERSION = 'v4'
creds = None
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE,scopes=SCOPES)
app = Flask(__name__,static_url_path='/static')
#import logging
#logging.getLogger("werkzeug").disabled = True

def python_date_to_jquery_date(strr):
    sp = strr.split("-")
    month_num = strptime(sp[1],'%b').tm_mon
    if month_num <10:
        month_num = "0"+str(month_num)
    #return sp[0]+"/"+str(month_num)+"/20"+sp[2]
    return "20"+sp[2]+"-"+str(month_num)+"-"+sp[0]

def date_format(strr):
    sp = strr.split("-")
    month_num = sp[1]
    datetime_object = datetime.datetime.strptime(month_num, "%m")
    month_name = datetime_object.strftime("%b")
    return (sp[2]+"-"+month_name+"-"+sp[0].replace("20",""))

def create_spreadsheet (sheet_name, ss_id): # for closing calculator
    OUTLET_SPREADSHEET_ID = ss_id #'1vZVur1ov5SRKKY5tSMH0HbabmpLFHKJOzTvtTAUzbgk' #this is the unique id of outlet sheet
    service = build('sheets','v4',credentials=creds)
    spreadsheets = service.spreadsheets()

    header_body = [ 'Day',
                    'Date',
                    'Full',
                    'Outlet',
                    'NO',
                    'By',
                    'T.Cash',
                    'Ewallet',
                    'Petty Cash',
                    'Actual Sales Max (Sales,Zreport)',
                    'Foodpanda',
                    'Grabfood',
                    'Grand Total',
                    'Ice Quantity(pkt)',
                    'Ice Price/pkt (RM)',
                    'Ice (RM)',
                    'Eggs (RM)',	
                    'Sugar (RM)',	
                    'Oils (RM)',	
                    'Full Cream Milk (RM)',	
                    'Fresh Milk (RM)',	
                    'Whipped Cream (RM)',
                    'Others (RM)',	
                    'Ice (pkt)',	
                    'Black Pearl (gram)',	
                    'Waffle Mix (tong)',	
                    'Chocolate Waffle Mix (senduk)',	
                    'Sugar (tong)',
                    'Milk Tea (Big)',
                    'Milk Tea (Small)'
    ]
    request_body = {
            'requests': [{
                'addSheet': {
                    'properties': {
                        'title': sheet_name,
                        'tabColor': {
                            'red': 0.44,
                            'green': 0.99,
                            'blue': 0.50
                        }
                    }
                }
            }]
    }
    creation_response = spreadsheets.batchUpdate(spreadsheetId=OUTLET_SPREADSHEET_ID,body=request_body).execute()
    fileId = creation_response.get('spreadsheetId') # Added
    res = spreadsheets.values().append(spreadsheetId = fileId,range=sheet_name+"!A1:AD1",valueInputOption="USER_ENTERED",insertDataOption="INSERT_ROWS",body={"values":[header_body]}).execute()
    return fileId


def create_spreadsheet_for_opening_calculator (sheet_name): # for opening calculator
    OUTLET_SPREADSHEET_ID = '1YZvru2vsXM2Nlze72a4pMx4pPH6PyLTJ4biinWZ3Fcs' #this is the unique id of outlet sheet
    service = build('sheets','v4',credentials=creds)
    spreadsheets = service.spreadsheets()

    header_body = [ 'Day',
                    'Date',
                    'Full',
                    'Outlet',
                    'NO',
                    'By',
                    'T.Cash In Drawer',
                    # 'T.Bank In (Link from other place)',
                    # 'T.Balance',
                    # 'Foodpanda',
                    # 'Ewallet',
                    # 'Petty Cash',
                    # 'Actual Sales Max (Sales,Zreport)',	
                    'Ice',	
                    'Black Pearl',	
                    'Waffle Mix',	
                    'Chocolate Waffle Mix',	
                    'Sugar',
                    'Milk Tea (Big)',
                    'Milk Tea (Small)'
    ]
    request_body = {
            'requests': [{
                'addSheet': {
                    'properties': {
                        'title': sheet_name,
                        'tabColor': {
                            'red': 0.44,
                            'green': 0.99,
                            'blue': 0.50
                        }
                    }
                }
            }]
    }
    creation_response = spreadsheets.batchUpdate(spreadsheetId=OUTLET_SPREADSHEET_ID,body=request_body).execute()
    fileId = creation_response.get('spreadsheetId') # Added
    res = spreadsheets.values().append(spreadsheetId = fileId,range=sheet_name+"!A1:AC1",valueInputOption="USER_ENTERED",insertDataOption="INSERT_ROWS",body={"values":[header_body]}).execute()
    return fileId
    

def get_current_month(): # this function will return us month name (May, Apr)
    mydate = datetime.datetime.now()
    todays_date = date.today()
    return (mydate.strftime("%b")+"'"+ str(todays_date.year)[2::])


@app.route('/')
def home():
    OUTLET_SPREADSHEET_ID = '1vZVur1ov5SRKKY5tSMH0HbabmpLFHKJOzTvtTAUzbgk' #this is the unique id of outlet sheet
    service = build('sheets','v4',credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId = OUTLET_SPREADSHEET_ID,range="Setting").execute()
    values = result.get('values',[])

    return render_template('home.html',outlet_count = len(values[2::]))

@app.route('/closing_calculator',methods = ['GET','POST'])
def closing_cal():
    OUTLET_SPREADSHEET_ID = '1vZVur1ov5SRKKY5tSMH0HbabmpLFHKJOzTvtTAUzbgk' #this is the unique id of outlet sheet
    service = build('sheets','v4',credentials=creds)
    # get all the sheets names
    working_sheets = service.spreadsheets().get(spreadsheetId = OUTLET_SPREADSHEET_ID).execute()
    all_sheets_name = [sheet['properties']['title'] for sheet in working_sheets['sheets']]
    all_sheets_id = [sheet['properties']['sheetId'] for sheet in working_sheets['sheets']]
    current_month_sheet_name = get_current_month()
    
    current_month_sheet_flag_exists = 0
    current_month_values = []
    if current_month_sheet_name in all_sheets_name:
        current_month_sheet_flag_exists = 1
        sheet = service.spreadsheets()
        current_month_result = sheet.values().get(spreadsheetId = OUTLET_SPREADSHEET_ID,range=current_month_sheet_name).execute()
        current_month_values = current_month_result.get('values',[])
        #print(current_month_values)
    
    if request.method=="GET":
    ######## Getting the outlet data from google 
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId = OUTLET_SPREADSHEET_ID,range="Setting").execute()
        values = result.get('values',[])
        arr_to_send  = [python_date_to_jquery_date(str(val[1]))+","+str(val[2])+","+str(val[3]).strip() for val in current_month_values[1::]]    
        return render_template('closing_calculator.html',result = values[2::],current_month_sheet_flag_exists=current_month_sheet_flag_exists,arr_to_send=arr_to_send ) # sending outlet data without its headers

    else:
        stuff_name = request.form['stuff_name'].strip()
        date = date_format(request.form['date'])
        day = request.form['day']
        outlet_full = request.form['outlet_name'].strip()
        outlet_name = request.form['outlet_code']
        outlet_code = request.form['outlet_name'].split(".")[0].strip()
        total_bank_in = request.form['total_bank_in']
        e_wallet = request.form['e_wallet']
        petty_cash = request.form['petty_cash']
        # total_sale = request.form['total_sale']
        z_report = request.form['z_report']
        groceries_ice_input = request.form['groceries_ice_input']
        groceries_ice_input_quantity = request.form['groceries_ice_input_quantity']
        groceries_ice_input_per_packet_price = request.form['groceries_ice_input_per_packet_price']
        groceries_eggs_input = request.form['groceries_eggs_input']
        groceries_sugar_input = request.form['groceries_sugar_input']
        groceries_oils_input = request.form['groceries_oils_input']
        groceries_fullcream_milk_input = request.form['groceries_fullcream_milk_input']
        groceries_fresh_milk_input = request.form['groceries_fresh_milk_input']
        whipped_cream_input = request.form['whipped_cream_input']
        groceries_others = request.form['groceries_others']
        ice_input = request.form['ice_input']
        black_pearl_input = request.form['black_pearl_input']
        tepung_waffle_input = request.form['tepung_waffle_input']
        tepung_cw_input = request.form['tepung_cw_input']
        gula_input = request.form['gula_input']
        milk_tea_big_jag_input = request.form['milk_tea_big_jag_input']
        milk_tea_small_jag_input = request.form['milk_tea_small_jag_input']
        
        ## Array for insert into google sheet
        insertRow = [[day[0:3],date,outlet_full,outlet_name,outlet_code,stuff_name,total_bank_in,e_wallet,petty_cash,'','','','',groceries_ice_input_quantity,groceries_ice_input_per_packet_price,groceries_ice_input,groceries_eggs_input,groceries_sugar_input,groceries_oils_input,groceries_fullcream_milk_input,groceries_fresh_milk_input,whipped_cream_input,groceries_others,ice_input,black_pearl_input,tepung_waffle_input,tepung_cw_input,gula_input,milk_tea_big_jag_input,milk_tea_small_jag_input]]
        if current_month_sheet_flag_exists==0: # if the sheet does not found then this will create the sheet and push values into it
            sheet_id = create_spreadsheet(current_month_sheet_name, OUTLET_SPREADSHEET_ID)
            #print(sheet_id)
            sheet = service.spreadsheets()
            res = sheet.values().append(spreadsheetId = sheet_id,range=current_month_sheet_name+"!A1:AB1",valueInputOption="USER_ENTERED",insertDataOption="INSERT_ROWS",body={"values":insertRow}).execute()
            res1 = sheet.values().update(spreadsheetId = sheet_id,range=current_month_sheet_name+"!J1",valueInputOption="USER_ENTERED",body={"values":[['={"Actual Sales";ARRAYFORMULA(IF(D2:D<>"",G2:G+H2:H+I2:I,))}']]}).execute()
            res2 = sheet.values().update(spreadsheetId = sheet_id,range=current_month_sheet_name+"!K1",valueInputOption="USER_ENTERED",body={"values":[['={"Foodpanda";ARRAYFORMULA(IF(D2:D<>"",IFERROR(VLOOKUP(D2:D&B2:B,Foodpanda!B:I,MATCH("Net Sales",Foodpanda!B2:I2,0),0),),))}']]}).execute()
            res3 = sheet.values().update(spreadsheetId = sheet_id,range=current_month_sheet_name+"!L1",valueInputOption="USER_ENTERED",body={"values":[['={"Grabfood";ARRAYFORMULA(IF(D2:D<>"",IFERROR(VLOOKUP(D2:D&B2:B,Grabfood!B:F,MATCH("Net Sales",Grabfood!B2:F2,0),0),),))}']]}).execute()
            res4 = sheet.values().update(spreadsheetId = sheet_id,range=current_month_sheet_name+"!M1",valueInputOption="USER_ENTERED",body={"values":[['={"Grand Total";ARRAYFORMULA(IF(D2:D<>"",J2:J+K2:K+L2:L,))}']]}).execute()
        else:
            res = sheet.values().append(spreadsheetId=OUTLET_SPREADSHEET_ID,range=current_month_sheet_name+"!A1:AD1",valueInputOption="USER_ENTERED",insertDataOption="INSERT_ROWS",body={"values":insertRow}).execute()
            # res2 = sheet.values().update(spreadsheetId = OUTLET_SPREADSHEET_ID,range=current_month_sheet_name+"!H1",valueInputOption="RAW",body={"values":[['={"T.Balance (RM)";ARRAYFORMULA(IF(c$2:c<>"",f$2:f-g$2:g,))}']]}).execute()
            

        return jsonify({'success':1,'msg':'record has been added successfully'})

@app.route('/wkk_closing_calculator',methods = ['GET','POST'])
def wkk_closing_cal():
    OUTLET_SPREADSHEET_ID = '1VAfzKMD1WJm-nM3rhwk31al70SjmB6rVuxYTfDMxaZk' #this is the unique id of outlet sheet
    service = build('sheets','v4',credentials=creds)
    # get all the sheets names
    working_sheets = service.spreadsheets().get(spreadsheetId = OUTLET_SPREADSHEET_ID).execute()
    all_sheets_name = [sheet['properties']['title'] for sheet in working_sheets['sheets']]
    all_sheets_id = [sheet['properties']['sheetId'] for sheet in working_sheets['sheets']]
    current_month_sheet_name = get_current_month()
    
    current_month_sheet_flag_exists = 0
    current_month_values = []
    if current_month_sheet_name in all_sheets_name:
        current_month_sheet_flag_exists = 1
        sheet = service.spreadsheets()
        current_month_result = sheet.values().get(spreadsheetId = OUTLET_SPREADSHEET_ID,range=current_month_sheet_name).execute()
        current_month_values = current_month_result.get('values',[])
        #print(current_month_values)
    
    if request.method=="GET":
    ######## Getting the outlet data from google 
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId = OUTLET_SPREADSHEET_ID,range="Setting").execute()
        values = result.get('values',[])
        arr_to_send  = [python_date_to_jquery_date(str(val[1]))+","+str(val[2])+","+str(val[3]).strip() for val in current_month_values[1::]]    
        return render_template('wkk_closing_calculator.html',result = values[2::],current_month_sheet_flag_exists=current_month_sheet_flag_exists,arr_to_send=arr_to_send ) # sending outlet data without its headers

    else:
        stuff_name = request.form['stuff_name'].strip()
        date = date_format(request.form['date'])
        day = request.form['day']
        outlet_full = request.form['outlet_name'].strip()
        outlet_name = request.form['outlet_code']
        outlet_code = request.form['outlet_name'].split(".")[0].strip()
        total_bank_in = request.form['total_bank_in']
        e_wallet = request.form['e_wallet']
        petty_cash = request.form['petty_cash']
        # total_sale = request.form['total_sale']
        z_report = request.form['z_report']
        groceries_ice_input = request.form['groceries_ice_input']
        groceries_ice_input_quantity = request.form['groceries_ice_input_quantity']
        groceries_ice_input_per_packet_price = request.form['groceries_ice_input_per_packet_price']
        groceries_eggs_input = request.form['groceries_eggs_input']
        groceries_sugar_input = request.form['groceries_sugar_input']
        groceries_oils_input = request.form['groceries_oils_input']
        groceries_fullcream_milk_input = request.form['groceries_fullcream_milk_input']
        groceries_fresh_milk_input = request.form['groceries_fresh_milk_input']
        whipped_cream_input = request.form['whipped_cream_input']
        groceries_others = request.form['groceries_others']
        ice_input = request.form['ice_input']
        black_pearl_input = request.form['black_pearl_input']
        tepung_waffle_input = request.form['tepung_waffle_input']
        tepung_cw_input = request.form['tepung_cw_input']
        gula_input = request.form['gula_input']
        milk_tea_big_jag_input = request.form['milk_tea_big_jag_input']
        milk_tea_small_jag_input = request.form['milk_tea_small_jag_input']
        
        ## Array for insert into google sheet
        insertRow = [[day[0:3],date,outlet_full,outlet_name,outlet_code,stuff_name,total_bank_in,e_wallet,petty_cash,'','','','',groceries_ice_input_quantity,groceries_ice_input_per_packet_price,groceries_ice_input,groceries_eggs_input,groceries_sugar_input,groceries_oils_input,groceries_fullcream_milk_input,groceries_fresh_milk_input,whipped_cream_input,groceries_others,ice_input,black_pearl_input,tepung_waffle_input,tepung_cw_input,gula_input,milk_tea_big_jag_input,milk_tea_small_jag_input]]
        if current_month_sheet_flag_exists==0: # if the sheet does not found then this will create the sheet and push values into it
            sheet_id = create_spreadsheet(current_month_sheet_name, OUTLET_SPREADSHEET_ID)
            #print(sheet_id)
            sheet = service.spreadsheets()
            res = sheet.values().append(spreadsheetId = sheet_id,range=current_month_sheet_name+"!A1:AB1",valueInputOption="USER_ENTERED",insertDataOption="INSERT_ROWS",body={"values":insertRow}).execute()
            res1 = sheet.values().update(spreadsheetId = sheet_id,range=current_month_sheet_name+"!J1",valueInputOption="USER_ENTERED",body={"values":[['={"Actual Sales";ARRAYFORMULA(IF(D2:D<>"",G2:G+H2:H+I2:I,))}']]}).execute()
            res2 = sheet.values().update(spreadsheetId = sheet_id,range=current_month_sheet_name+"!K1",valueInputOption="USER_ENTERED",body={"values":[['={"Foodpanda";ARRAYFORMULA(IF(D2:D<>"",IFERROR(VLOOKUP(D2:D&B2:B,Foodpanda!B:I,MATCH("Net Sales",Foodpanda!B2:I2,0),0),),))}']]}).execute()
            res3 = sheet.values().update(spreadsheetId = sheet_id,range=current_month_sheet_name+"!L1",valueInputOption="USER_ENTERED",body={"values":[['={"Grabfood";ARRAYFORMULA(IF(D2:D<>"",IFERROR(VLOOKUP(D2:D&B2:B,Grabfood!B:F,MATCH("Net Sales",Grabfood!B2:F2,0),0),),))}']]}).execute()
            res4 = sheet.values().update(spreadsheetId = sheet_id,range=current_month_sheet_name+"!M1",valueInputOption="USER_ENTERED",body={"values":[['={"Grand Total";ARRAYFORMULA(IF(D2:D<>"",J2:J+K2:K+L2:L,))}']]}).execute()
        else:
            res = sheet.values().append(spreadsheetId=OUTLET_SPREADSHEET_ID,range=current_month_sheet_name+"!A1:AD1",valueInputOption="USER_ENTERED",insertDataOption="INSERT_ROWS",body={"values":insertRow}).execute()
            # res2 = sheet.values().update(spreadsheetId = OUTLET_SPREADSHEET_ID,range=current_month_sheet_name+"!H1",valueInputOption="RAW",body={"values":[['={"T.Balance (RM)";ARRAYFORMULA(IF(c$2:c<>"",f$2:f-g$2:g,))}']]}).execute()
            

        return jsonify({'success':1,'msg':'record has been added successfully'})

@app.route('/jm_closing_calculator',methods = ['GET','POST'])
def jm_closing_cal():
    OUTLET_SPREADSHEET_ID = '16MeiJiEMUGZXPCXQywcspowa7dC9ufWb_ubczx8UTT4' #this is the unique id of outlet sheet
    service = build('sheets','v4',credentials=creds)
    # get all the sheets names
    working_sheets = service.spreadsheets().get(spreadsheetId = OUTLET_SPREADSHEET_ID).execute()
    all_sheets_name = [sheet['properties']['title'] for sheet in working_sheets['sheets']]
    all_sheets_id = [sheet['properties']['sheetId'] for sheet in working_sheets['sheets']]
    current_month_sheet_name = get_current_month()
    
    current_month_sheet_flag_exists = 0
    current_month_values = []
    if current_month_sheet_name in all_sheets_name:
        current_month_sheet_flag_exists = 1
        sheet = service.spreadsheets()
        current_month_result = sheet.values().get(spreadsheetId = OUTLET_SPREADSHEET_ID,range=current_month_sheet_name).execute()
        current_month_values = current_month_result.get('values',[])
        #print(current_month_values)
    
    if request.method=="GET":
    ######## Getting the outlet data from google 
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId = OUTLET_SPREADSHEET_ID,range="Setting").execute()
        values = result.get('values',[])
        arr_to_send  = [python_date_to_jquery_date(str(val[1]))+","+str(val[2])+","+str(val[3]).strip() for val in current_month_values[1::]]    
        return render_template('jm_closing_calculator.html',result = values[2::],current_month_sheet_flag_exists=current_month_sheet_flag_exists,arr_to_send=arr_to_send ) # sending outlet data without its headers

    else:
        stuff_name = request.form['stuff_name'].strip()
        date = date_format(request.form['date'])
        day = request.form['day']
        outlet_full = request.form['outlet_name'].strip()
        outlet_name = request.form['outlet_code']
        outlet_code = request.form['outlet_name'].split(".")[0].strip()
        total_bank_in = request.form['total_bank_in']
        e_wallet = request.form['e_wallet']
        petty_cash = request.form['petty_cash']
        # total_sale = request.form['total_sale']
        z_report = request.form['z_report']
        groceries_ice_input = request.form['groceries_ice_input']
        groceries_ice_input_quantity = request.form['groceries_ice_input_quantity']
        groceries_ice_input_per_packet_price = request.form['groceries_ice_input_per_packet_price']
        groceries_eggs_input = request.form['groceries_eggs_input']
        groceries_sugar_input = request.form['groceries_sugar_input']
        groceries_oils_input = request.form['groceries_oils_input']
        groceries_fullcream_milk_input = request.form['groceries_fullcream_milk_input']
        groceries_fresh_milk_input = request.form['groceries_fresh_milk_input']
        whipped_cream_input = request.form['whipped_cream_input']
        groceries_others = request.form['groceries_others']
        ice_input = request.form['ice_input']
        black_pearl_input = request.form['black_pearl_input']
        tepung_waffle_input = request.form['tepung_waffle_input']
        tepung_cw_input = request.form['tepung_cw_input']
        gula_input = request.form['gula_input']
        milk_tea_big_jag_input = request.form['milk_tea_big_jag_input']
        milk_tea_small_jag_input = request.form['milk_tea_small_jag_input']
        
        ## Array for insert into google sheet
        insertRow = [[day[0:3],date,outlet_full,outlet_name,outlet_code,stuff_name,total_bank_in,e_wallet,petty_cash,'','','','',groceries_ice_input_quantity,groceries_ice_input_per_packet_price,groceries_ice_input,groceries_eggs_input,groceries_sugar_input,groceries_oils_input,groceries_fullcream_milk_input,groceries_fresh_milk_input,whipped_cream_input,groceries_others,ice_input,black_pearl_input,tepung_waffle_input,tepung_cw_input,gula_input,milk_tea_big_jag_input,milk_tea_small_jag_input]]
        if current_month_sheet_flag_exists==0: # if the sheet does not found then this will create the sheet and push values into it
            sheet_id = create_spreadsheet(current_month_sheet_name, OUTLET_SPREADSHEET_ID)
            #print(sheet_id)
            sheet = service.spreadsheets()
            res = sheet.values().append(spreadsheetId = sheet_id,range=current_month_sheet_name+"!A1:AB1",valueInputOption="USER_ENTERED",insertDataOption="INSERT_ROWS",body={"values":insertRow}).execute()
            res1 = sheet.values().update(spreadsheetId = sheet_id,range=current_month_sheet_name+"!J1",valueInputOption="USER_ENTERED",body={"values":[['={"Actual Sales";ARRAYFORMULA(IF(D2:D<>"",G2:G+H2:H+I2:I,))}']]}).execute()
            res2 = sheet.values().update(spreadsheetId = sheet_id,range=current_month_sheet_name+"!K1",valueInputOption="USER_ENTERED",body={"values":[['={"Foodpanda";ARRAYFORMULA(IF(D2:D<>"",IFERROR(VLOOKUP(D2:D&B2:B,Foodpanda!B:I,MATCH("Net Sales",Foodpanda!B2:I2,0),0),),))}']]}).execute()
            res3 = sheet.values().update(spreadsheetId = sheet_id,range=current_month_sheet_name+"!L1",valueInputOption="USER_ENTERED",body={"values":[['={"Grabfood";ARRAYFORMULA(IF(D2:D<>"",IFERROR(VLOOKUP(D2:D&B2:B,Grabfood!B:F,MATCH("Net Sales",Grabfood!B2:F2,0),0),),))}']]}).execute()
            res4 = sheet.values().update(spreadsheetId = sheet_id,range=current_month_sheet_name+"!M1",valueInputOption="USER_ENTERED",body={"values":[['={"Grand Total";ARRAYFORMULA(IF(D2:D<>"",J2:J+K2:K+L2:L,))}']]}).execute()
        else:
            res = sheet.values().append(spreadsheetId=OUTLET_SPREADSHEET_ID,range=current_month_sheet_name+"!A1:AD1",valueInputOption="USER_ENTERED",insertDataOption="INSERT_ROWS",body={"values":insertRow}).execute()
            # res2 = sheet.values().update(spreadsheetId = OUTLET_SPREADSHEET_ID,range=current_month_sheet_name+"!H1",valueInputOption="RAW",body={"values":[['={"T.Balance (RM)";ARRAYFORMULA(IF(c$2:c<>"",f$2:f-g$2:g,))}']]}).execute()
            

        return jsonify({'success':1,'msg':'record has been added successfully'})

@app.route('/cp_closing_calculator',methods = ['GET','POST'])
def cp_closing_cal():
    OUTLET_SPREADSHEET_ID = '11AiPrbrlJ4sqLHaiNdRuOGPPPMB28WDHWeHnrUHTcqk' #this is the unique id of outlet sheet
    service = build('sheets','v4',credentials=creds)
    # get all the sheets names
    working_sheets = service.spreadsheets().get(spreadsheetId = OUTLET_SPREADSHEET_ID).execute()
    all_sheets_name = [sheet['properties']['title'] for sheet in working_sheets['sheets']]
    all_sheets_id = [sheet['properties']['sheetId'] for sheet in working_sheets['sheets']]
    current_month_sheet_name = get_current_month()
    
    current_month_sheet_flag_exists = 0
    current_month_values = []
    if current_month_sheet_name in all_sheets_name:
        current_month_sheet_flag_exists = 1
        sheet = service.spreadsheets()
        current_month_result = sheet.values().get(spreadsheetId = OUTLET_SPREADSHEET_ID,range=current_month_sheet_name).execute()
        current_month_values = current_month_result.get('values',[])
        #print(current_month_values)
    
    if request.method=="GET":
    ######## Getting the outlet data from google 
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId = OUTLET_SPREADSHEET_ID,range="Setting").execute()
        values = result.get('values',[])
        arr_to_send  = [python_date_to_jquery_date(str(val[1]))+","+str(val[2])+","+str(val[3]).strip() for val in current_month_values[1::]]    
        return render_template('cp_closing_calculator.html',result = values[2::],current_month_sheet_flag_exists=current_month_sheet_flag_exists,arr_to_send=arr_to_send ) # sending outlet data without its headers

    else:
        stuff_name = request.form['stuff_name'].strip()
        date = date_format(request.form['date'])
        day = request.form['day']
        outlet_full = request.form['outlet_name'].strip()
        outlet_name = request.form['outlet_code']
        outlet_code = request.form['outlet_name'].split(".")[0].strip()
        total_bank_in = request.form['total_bank_in']
        e_wallet = request.form['e_wallet']
        petty_cash = request.form['petty_cash']
        # total_sale = request.form['total_sale']
        z_report = request.form['z_report']
        groceries_ice_input = request.form['groceries_ice_input']
        groceries_ice_input_quantity = request.form['groceries_ice_input_quantity']
        groceries_ice_input_per_packet_price = request.form['groceries_ice_input_per_packet_price']
        groceries_eggs_input = request.form['groceries_eggs_input']
        groceries_sugar_input = request.form['groceries_sugar_input']
        groceries_oils_input = request.form['groceries_oils_input']
        groceries_fullcream_milk_input = request.form['groceries_fullcream_milk_input']
        groceries_fresh_milk_input = request.form['groceries_fresh_milk_input']
        whipped_cream_input = request.form['whipped_cream_input']
        groceries_others = request.form['groceries_others']
        ice_input = request.form['ice_input']
        black_pearl_input = request.form['black_pearl_input']
        tepung_waffle_input = request.form['tepung_waffle_input']
        tepung_cw_input = request.form['tepung_cw_input']
        gula_input = request.form['gula_input']
        milk_tea_big_jag_input = request.form['milk_tea_big_jag_input']
        milk_tea_small_jag_input = request.form['milk_tea_small_jag_input']
        
        ## Array for insert into google sheet
        insertRow = [[day[0:3],date,outlet_full,outlet_name,outlet_code,stuff_name,total_bank_in,e_wallet,petty_cash,'','','','',groceries_ice_input_quantity,groceries_ice_input_per_packet_price,groceries_ice_input,groceries_eggs_input,groceries_sugar_input,groceries_oils_input,groceries_fullcream_milk_input,groceries_fresh_milk_input,whipped_cream_input,groceries_others,ice_input,black_pearl_input,tepung_waffle_input,tepung_cw_input,gula_input,milk_tea_big_jag_input,milk_tea_small_jag_input]]
        if current_month_sheet_flag_exists==0: # if the sheet does not found then this will create the sheet and push values into it
            sheet_id = create_spreadsheet(current_month_sheet_name, OUTLET_SPREADSHEET_ID)
            #print(sheet_id)
            sheet = service.spreadsheets()
            res = sheet.values().append(spreadsheetId = sheet_id,range=current_month_sheet_name+"!A1:AB1",valueInputOption="USER_ENTERED",insertDataOption="INSERT_ROWS",body={"values":insertRow}).execute()
            res1 = sheet.values().update(spreadsheetId = sheet_id,range=current_month_sheet_name+"!J1",valueInputOption="USER_ENTERED",body={"values":[['={"Actual Sales";ARRAYFORMULA(IF(D2:D<>"",G2:G+H2:H+I2:I,))}']]}).execute()
            res2 = sheet.values().update(spreadsheetId = sheet_id,range=current_month_sheet_name+"!K1",valueInputOption="USER_ENTERED",body={"values":[['={"Foodpanda";ARRAYFORMULA(IF(D2:D<>"",IFERROR(VLOOKUP(D2:D&B2:B,Foodpanda!B:I,MATCH("Net Sales",Foodpanda!B2:I2,0),0),),))}']]}).execute()
            res3 = sheet.values().update(spreadsheetId = sheet_id,range=current_month_sheet_name+"!L1",valueInputOption="USER_ENTERED",body={"values":[['={"Grabfood";ARRAYFORMULA(IF(D2:D<>"",IFERROR(VLOOKUP(D2:D&B2:B,Grabfood!B:F,MATCH("Net Sales",Grabfood!B2:F2,0),0),),))}']]}).execute()
            res4 = sheet.values().update(spreadsheetId = sheet_id,range=current_month_sheet_name+"!M1",valueInputOption="USER_ENTERED",body={"values":[['={"Grand Total";ARRAYFORMULA(IF(D2:D<>"",J2:J+K2:K+L2:L,))}']]}).execute()
        else:
            res = sheet.values().append(spreadsheetId=OUTLET_SPREADSHEET_ID,range=current_month_sheet_name+"!A1:AD1",valueInputOption="USER_ENTERED",insertDataOption="INSERT_ROWS",body={"values":insertRow}).execute()
            # res2 = sheet.values().update(spreadsheetId = OUTLET_SPREADSHEET_ID,range=current_month_sheet_name+"!H1",valueInputOption="RAW",body={"values":[['={"T.Balance (RM)";ARRAYFORMULA(IF(c$2:c<>"",f$2:f-g$2:g,))}']]}).execute()
            

        return jsonify({'success':1,'msg':'record has been added successfully'})

@app.route('/bwm_closing_calculator',methods = ['GET','POST'])
def bwm_closing_cal():
    OUTLET_SPREADSHEET_ID = '1lgHlXn7KDNjilbJ4G7HBXSjxoXTaxY8qBHekt6uY5Uw' #this is the unique id of outlet sheet
    service = build('sheets','v4',credentials=creds)
    # get all the sheets names
    working_sheets = service.spreadsheets().get(spreadsheetId = OUTLET_SPREADSHEET_ID).execute()
    all_sheets_name = [sheet['properties']['title'] for sheet in working_sheets['sheets']]
    all_sheets_id = [sheet['properties']['sheetId'] for sheet in working_sheets['sheets']]
    current_month_sheet_name = get_current_month()
    
    current_month_sheet_flag_exists = 0
    current_month_values = []
    if current_month_sheet_name in all_sheets_name:
        current_month_sheet_flag_exists = 1
        sheet = service.spreadsheets()
        current_month_result = sheet.values().get(spreadsheetId = OUTLET_SPREADSHEET_ID,range=current_month_sheet_name).execute()
        current_month_values = current_month_result.get('values',[])
        #print(current_month_values)
    
    if request.method=="GET":
    ######## Getting the outlet data from google 
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId = OUTLET_SPREADSHEET_ID,range="Setting").execute()
        values = result.get('values',[])
        arr_to_send  = [python_date_to_jquery_date(str(val[1]))+","+str(val[2])+","+str(val[3]).strip() for val in current_month_values[1::]]    
        return render_template('bwm_closing_calculator.html',result = values[2::],current_month_sheet_flag_exists=current_month_sheet_flag_exists,arr_to_send=arr_to_send ) # sending outlet data without its headers

    else:
        stuff_name = request.form['stuff_name'].strip()
        date = date_format(request.form['date'])
        day = request.form['day']
        outlet_full = request.form['outlet_name'].strip()
        outlet_name = request.form['outlet_code']
        outlet_code = request.form['outlet_name'].split(".")[0].strip()
        total_bank_in = request.form['total_bank_in']
        e_wallet = request.form['e_wallet']
        petty_cash = request.form['petty_cash']
        # total_sale = request.form['total_sale']
        z_report = request.form['z_report']
        groceries_ice_input = request.form['groceries_ice_input']
        groceries_ice_input_quantity = request.form['groceries_ice_input_quantity']
        groceries_ice_input_per_packet_price = request.form['groceries_ice_input_per_packet_price']
        groceries_eggs_input = request.form['groceries_eggs_input']
        groceries_sugar_input = request.form['groceries_sugar_input']
        groceries_oils_input = request.form['groceries_oils_input']
        groceries_fullcream_milk_input = request.form['groceries_fullcream_milk_input']
        groceries_fresh_milk_input = request.form['groceries_fresh_milk_input']
        whipped_cream_input = request.form['whipped_cream_input']
        groceries_others = request.form['groceries_others']
        ice_input = request.form['ice_input']
        black_pearl_input = request.form['black_pearl_input']
        tepung_waffle_input = request.form['tepung_waffle_input']
        tepung_cw_input = request.form['tepung_cw_input']
        gula_input = request.form['gula_input']
        milk_tea_big_jag_input = request.form['milk_tea_big_jag_input']
        milk_tea_small_jag_input = request.form['milk_tea_small_jag_input']
        
        ## Array for insert into google sheet
        insertRow = [[day[0:3],date,outlet_full,outlet_name,outlet_code,stuff_name,total_bank_in,e_wallet,petty_cash,'','','','',groceries_ice_input_quantity,groceries_ice_input_per_packet_price,groceries_ice_input,groceries_eggs_input,groceries_sugar_input,groceries_oils_input,groceries_fullcream_milk_input,groceries_fresh_milk_input,whipped_cream_input,groceries_others,ice_input,black_pearl_input,tepung_waffle_input,tepung_cw_input,gula_input,milk_tea_big_jag_input,milk_tea_small_jag_input]]
        if current_month_sheet_flag_exists==0: # if the sheet does not found then this will create the sheet and push values into it
            sheet_id = create_spreadsheet(current_month_sheet_name, OUTLET_SPREADSHEET_ID)
            #print(sheet_id)
            sheet = service.spreadsheets()
            res = sheet.values().append(spreadsheetId = sheet_id,range=current_month_sheet_name+"!A1:AB1",valueInputOption="USER_ENTERED",insertDataOption="INSERT_ROWS",body={"values":insertRow}).execute()
            res1 = sheet.values().update(spreadsheetId = sheet_id,range=current_month_sheet_name+"!J1",valueInputOption="USER_ENTERED",body={"values":[['={"Actual Sales";ARRAYFORMULA(IF(D2:D<>"",G2:G+H2:H+I2:I,))}']]}).execute()
            res2 = sheet.values().update(spreadsheetId = sheet_id,range=current_month_sheet_name+"!K1",valueInputOption="USER_ENTERED",body={"values":[['={"Foodpanda";ARRAYFORMULA(IF(D2:D<>"",IFERROR(VLOOKUP(D2:D&B2:B,Foodpanda!B:I,MATCH("Net Sales",Foodpanda!B2:I2,0),0),),))}']]}).execute()
            res3 = sheet.values().update(spreadsheetId = sheet_id,range=current_month_sheet_name+"!L1",valueInputOption="USER_ENTERED",body={"values":[['={"Grabfood";ARRAYFORMULA(IF(D2:D<>"",IFERROR(VLOOKUP(D2:D&B2:B,Grabfood!B:F,MATCH("Net Sales",Grabfood!B2:F2,0),0),),))}']]}).execute()
            res4 = sheet.values().update(spreadsheetId = sheet_id,range=current_month_sheet_name+"!M1",valueInputOption="USER_ENTERED",body={"values":[['={"Grand Total";ARRAYFORMULA(IF(D2:D<>"",J2:J+K2:K+L2:L,))}']]}).execute()
        else:
            res = sheet.values().append(spreadsheetId=OUTLET_SPREADSHEET_ID,range=current_month_sheet_name+"!A1:AD1",valueInputOption="USER_ENTERED",insertDataOption="INSERT_ROWS",body={"values":insertRow}).execute()
            # res2 = sheet.values().update(spreadsheetId = OUTLET_SPREADSHEET_ID,range=current_month_sheet_name+"!H1",valueInputOption="RAW",body={"values":[['={"T.Balance (RM)";ARRAYFORMULA(IF(c$2:c<>"",f$2:f-g$2:g,))}']]}).execute()
            

        return jsonify({'success':1,'msg':'record has been added successfully'})
        
@app.route('/opening_calculator',methods = ['GET','POST'])
def opening_cal():
    OUTLET_SPREADSHEET_ID = '1YZvru2vsXM2Nlze72a4pMx4pPH6PyLTJ4biinWZ3Fcs' #this is the unique id of outlet sheet
    service = build('sheets','v4',credentials=creds)
    # get all the sheets names
    working_sheets = service.spreadsheets().get(spreadsheetId = OUTLET_SPREADSHEET_ID).execute()
    all_sheets_name = [sheet['properties']['title'] for sheet in working_sheets['sheets']]
    all_sheets_id = [sheet['properties']['sheetId'] for sheet in working_sheets['sheets']]
    current_month_sheet_name = get_current_month()
    current_month_sheet_flag_exists = 0
    current_month_values = []
    if current_month_sheet_name in all_sheets_name:
        current_month_sheet_flag_exists = 1
        sheet = service.spreadsheets()
        current_month_result = sheet.values().get(spreadsheetId = OUTLET_SPREADSHEET_ID,range=current_month_sheet_name).execute()
        current_month_values = current_month_result.get('values',[])
    if request.method=="GET":
    ######## Getting the outlet data from google 
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId = OUTLET_SPREADSHEET_ID,range="Setting").execute()
        values = result.get('values',[])
        arr_to_send  = [python_date_to_jquery_date(str(val[1]))+","+str(val[2])+","+str(val[3]).strip() for val in current_month_values[1::]]    
        print("arr:",arr_to_send)
        return render_template('opening_calculator.html',result = values[1::],current_month_sheet_flag_exists=current_month_sheet_flag_exists,arr_to_send=arr_to_send ) 
    else:
        stuff_name = request.form['stuff_name'].strip()
        date = date_format(request.form['date'])
        day = request.form['day']
        outlet_full = request.form['outlet_name'].strip()
        outlet_name = request.form['outlet_code']
        outlet_code = request.form['outlet_name'].split(".")[0].strip()
        total_cash_in_drawer = request.form['total_cash_in_drawer']
        # total_bank_in = request.form['total_bank_in']
        # e_wallet = request.form['e_wallet']
        # petty_cash = request.form['petty_cash']
        # total_sale = request.form['total_sale']
        # z_report = request.form['z_report']

        ice_input = request.form['ice_input']
        black_pearl_input = request.form['black_pearl_input']
        tepung_waffle_input = request.form['tepung_waffle_input']
        tepung_cw_input = request.form['tepung_cw_input']
        gula_input = request.form['gula_input']
        milk_tea_big_jag_input = request.form['milk_tea_big_jag_input']
        milk_tea_small_jag_input = request.form['milk_tea_small_jag_input']
        ## Array for insert into google sheet
        insertRow = [[day[0:3],date,outlet_full,outlet_name,outlet_code,stuff_name,total_cash_in_drawer,ice_input,black_pearl_input,tepung_waffle_input,tepung_cw_input,gula_input,milk_tea_big_jag_input,milk_tea_small_jag_input]]
        if current_month_sheet_flag_exists==0: # if the sheet does not found then this will create the sheet and push values into it
            sheet_id = create_spreadsheet_for_opening_calculator(current_month_sheet_name)
            #print(sheet_id)
            sheet = service.spreadsheets()
            res = sheet.values().append(spreadsheetId = sheet_id,range=current_month_sheet_name+"!A1:S1",valueInputOption="USER_ENTERED",insertDataOption="INSERT_ROWS",body={"values":insertRow}).execute()
        else:
            res = sheet.values().append(spreadsheetId=OUTLET_SPREADSHEET_ID,range=current_month_sheet_name+"!A1:S1",valueInputOption="USER_ENTERED",insertDataOption="INSERT_ROWS",body={"values":insertRow}).execute()
        return jsonify({'success':1,'msg':'record has been added successfully'})
        
if __name__ == '__main__':
    #app.run() # run the flask app on debug mode
    app.run(host='0.0.0.0',port=80)