from flask import Flask, request, render_template, jsonify
import logging
import logging.handlers
import json
from whatsapp.whatsapp import WhatsAppWrapper

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

def get_params():
    try:
        f = open('whatsapp/params.json',)
        params = json.load(f)
    except:
        params = None
        exit()
    finally:
        f.close()
    
    return params

def get_config_whatsapp():
    """_summary_: Get whatsapp settings"""
    config = {
        "WHATSAPP_API_TOKEN":"EAAL4ohZAnVEcBALNjKtrRb1PSC9NmcH1Iyu5SrWkuTGJaHUumSiWKD7lHJZAZBKlrypwWRXTwxZAZBTmqBwBiixoj76eOGCcb0BYvjxD907pYWscRKRLJZBRHt7CCyve9RQFUDGGghI6WeWYPN0qIKU6XZC4KwXtXMOqgHre1uNmepBmyFZBk9NBGv71G5CzGsWnpQSbWK9EAgZDZD",
        "PHONE_NUMBER_ID":"104006922529786",
        "API_URL": "https://graph.facebook.com",
        "VERSION": "v15.0",
        "VERIFY_TOKEN": "cNKWykYjL71kOnZfWPAJNTFPB3HhruZQ",
        "TEMPLATE": "saudacao",
        "TEMPLATE_LANGUAGE": "pt_BR",
        "PHONE_NUMBER_TO": "5554991984793"
    }
    # try:
    #     f = open('whatsapp/config_whatsapp.json',)
    #     config = json.load(f)
    # except:
    #     config = None
    #     exit()
    # finally:
    #     f.close()
    
    return config

@app.route("/get_send_message",  methods=['GET'])
def get_send_message():
    
    config_whatsapp = get_config_whatsapp()
    params_message = get_params()
    
    data_whats = {
        'api_url': config_whatsapp['API_URL'],
        'version': config_whatsapp['VERSION'],
        'api_token': config_whatsapp['WHATSAPP_API_TOKEN'],
        'phone_number_from': config_whatsapp['PHONE_NUMBER_ID'],
        'template_name': config_whatsapp['TEMPLATE'],
    }
    
    client = WhatsAppWrapper(**data_whats)
                    
    response = client.send_template_message(
        template_name = config_whatsapp['TEMPLATE'],
        language_code = config_whatsapp['TEMPLATE_LANGUAGE'],
        recipient_phone_number = config_whatsapp['PHONE_NUMBER_TO'],
        params = params_message
    )
    

    return jsonify({'response' : response})


@app.route('/webhook', methods=['GET', 'POST'])
def handle_webhook():
    """__summary__: Get message from the webhook"""
    
    if request.method == "GET":
        try:
            whatsapp_config = get_config_whatsapp()
            token = whatsapp_config['VERIFY_TOKEN']
            
        except:
            message = "Erro ao carregar configuração WhatsApp"
            return jsonify({'erro' : message})
        
        verify_token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if verify_token is not None and challenge is not None:
            if verify_token == token:
                return challenge
     
        message = "Falha de verificacao token webhook"
        logging.info(message)
        return jsonify({'erro' : message})
    
    elif request.method == "POST":
        
        client = WhatsAppWrapper()
        response = client.process_webhook_notification(request.get_json())
        
        json_object = json.dumps(response[0], indent = 4) 
        
        with open("mensagens.txt", "a") as outfile: 
            outfile.write(json_object + ',\n') 
            
        return jsonify({'response' : response})
 

LOGFILE = 'app.log'   #Log-File-Name
LOGFILESIZE = 5000000    #Log-File-Size (bytes)
LOGFILECOUNT = 4 #Rotate-Count-File

#Config Log-File
logger = logging.getLogger()
logger.setLevel(logging.INFO)
h = logging.handlers.RotatingFileHandler(LOGFILE, maxBytes=LOGFILESIZE, backupCount=LOGFILECOUNT)
f = logging.Formatter('[%(asctime)s] %(levelname)s:%(message)s', datefmt='%d/%m/%Y %H:%M:%S')
h.setFormatter(f)
logger.addHandler(h)
logging.info('app started')


if __name__ == "__main__":
    app.run(port=3000, debug=True)
    