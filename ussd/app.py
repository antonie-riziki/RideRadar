from flask import Flask, request
import os
import sys


from dotenv import load_dotenv

sys.path.insert(1, '/')

from send_sms import chunk_message
from ai_response import traffic_alerts
from payment import initiate_payment


app = Flask(__name__)

@app.route("/ussd", methods=['POST'])
def ussd():
    session_id   = request.values.get("sessionId", None)
    serviceCode  = request.values.get("serviceCode", None)
    phone_number = request.values.get("phoneNumber", None)
    text         = request.values.get("text", "default")

    user_response = text.split("*")

    if text == "":
        response = "CON Welcome to Ride Radar. \n"
        response += "1. Find Matatu\n"
        response += "2. Rides and Traffic\n"
        response += "3. Nearby stages\n"
        response += "4. My Favourite Routes\n"
        response += "5. Fare Estimates\n"
        response += "6. Alerts & News\n"
        response += "7. Help & Customer Support\n"



    # ----------------------------- #
    # SECTION 1: Find Matatu #
    # ----------------------------- #
    elif text == "1":
        # if text == "1":
        response = "CON Find Matatu \n"
        response += "1. By Route\n"
        response += "2. By Destination\n"
        response += "3. By Sacco\n"
        response += "4. Nearest Available Matatu\n"

    elif text == "1*1":
        response = "CON Search Matatu by Route \n"
        response += "Enter Route Number: \n"

        # response = f"END Wait for Mpesa STK Push {initiate_payment(phone_number)}"

    elif text == "1*2":
        response = "CON Search Matatu by Destination \n"
        response += "Enter Destination: e.g Town, Rongai, Thika\n"


    elif text == "1*3":
        response = "CON Search Matatu by Sacco \n"
        response += "Enter Sacco Name: e.g Stagecoach, Easy Coach\n"

    



    # ----------------------------- #
    # SECTION 2: Routes and Traffic      #
    # ----------------------------- #

    elif text == "2":
        response = "CON Routes and Traffic \n"
        response += "1. Heavy Traffic\n"  
        response += "2. Smoooth Routes\n"  
        response += "3. Road Accidents\n"  
        response += "4. Suggested Routes\n" 
        response += "5. Road Closures\n" 



            
    # ----------------------------- #
    # SECTION 3: Nearby Stages    #
    # ----------------------------- #

    elif text == "3":
        response = "CON Nearby Stages\n"
        response += "1. Nearest Stage\n"
        response += "2. Search Stage: \n"
        response += "3. Stages on my Route\n"
    
    
    
    # ----------------------------- #
    # SECTION 4: My Favourites   #
    # ----------------------------- #

    elif text == "4":
        response = "CON My Favourites\n"
        response += "1. Saved Route\n"
        response += "2. Saved Stages\n"
        response += "3. Preffered Sacco\n"
        response += "4. Clear Favourites\n"



    # ----------------------------- #
    # SECTION 5: Fare Estimates  #
    # ----------------------------- #

    elif text == "5":
        response = "CON Fare Estimates\n"
        response += "1. By Route\n"
        response += "2. By Stages\n"
        response += "3. Peak vs off-peak\n"


    # ----------------------------- #
    # SECTION 6: News & Alerts #
    # ----------------------------- #

    elif text == "6":
        response = "CON News & Alerts\n"
        response += "1. Traffic Updates & Alerts\n"
        response += "2. Matatu Disruption\n"
        response += "3. Road Closures\n"
        response += "4. Govt Notices\n"
        response += "5. Enable Alerts\n"




    # ----------------------------- #
    # SECTION 7: Help & Support  #
    # ----------------------------- #

    elif text == "7":
        response = "CON Help & Support\n"
        response += "1. How Ride Radar works\n"
        response += "2. Contact Support\n"
        response += "3. FAQ\n"
        response += "4. Language (en/sw)\n"
        response += "5. Terms & Privacy\n"



    return response



if __name__ == '__main__':
    app.run(debug=True, port="8000")