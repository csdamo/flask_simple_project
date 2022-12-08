import json
import requests


class WhatsAppWrapper:
        
    def __init__(self, **kwargs):
        
        if kwargs:     
            self.api_url = kwargs['api_url']
            self.api_token = kwargs['api_token']
            self.phone_number_from = kwargs['phone_number_from']
            self.version = kwargs['version']
                    
            self.headers = {
                "Authorization": f"Bearer {self.api_token}",
                "Content-Type": "application/json",
            }
            self.url = self.api_url + '/' + self.version + '/' + self.phone_number_from

    def send_template_message(self, template_name, language_code, recipient_phone_number, params):
        payload = json.dumps({
            "messaging_product": "whatsapp",
            "to": recipient_phone_number,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {
                    "code": language_code
                },
                "components": [
                    {
                        "type": "header",
                        "parameters": [
                            {
                                "type": "text",
                                "text": params['IMAGE_HEADER']
                            }
                        ]
                    },  
                    {
                        "type": "body",
                        "parameters": [
                            {
                                "type": "text",
                                "text": params['HEADER_1']
                            },
                            {
                                "type": "text",
                                "text": params['PARAM_1']
                            },
                            {
                                "type": "text",
                                "text": params['PARAM_2']
                            },
                                                  {
                                "type": "text",
                                "text": params['PARAM_3']
                            },
                            {
                                "type": "text",
                                "text": params['PARAM_4']
                            },
                            {
                                "type": "text",
                                "text": params['PARAM_5']
                            }
                        ]
                    }
                ]
            }
        })
        
        response_dict = {}
        id_message = ''
        phone_to = ''  
        
        try:
            response = requests.request("POST", f"{self.url}/messages", headers=self.headers, data=payload)
            if response.status_code == requests.codes.ok:
                return_data_property = response.json()
                
                contacts = return_data_property['contacts']
                phone_to = contacts[0]['wa_id']
                
                messages = return_data_property['messages']
                id_message = messages[0]['id']
                
                # successful response
    
                #  { 
                #     'messaging_product': 'whatsapp', 
                #     'contacts': [ 
                #         { 
                #             'input': '5554991984793', 
                #             'wa_id': '555491984793' 
                #         } 
                #     ], 
                #     'messages': [ 
                #         { 
                #             'id': 'wamid.HBgMNTU1NDkxOTg0NzkzFQIAERgSRkVEMTM4MDQ5QkU4OTBBNjQ2AA==' 
                #         } 
                #     ] 
                # }" 
                
                # examplo error response
                # {
                    # "error":{
                        # "message":"(#132001) Template name does not exist in the translation",
                        # "type":"OAuthException",
                        # "code":132001,
                        # "error_data":{
                            # "messaging_product":"whatsapp",
                            # "details":"template name (aviso_atualizacao_imovel_perfil) does not exist in pt_BR"
                        # },
                        # "error_subcode":2494073,
                        # "fbtrace_id":"AaC4PDmPG9UPOfnROjIJk-W"
                    # }
                # }

        except:
            print("Erro ao enviar mensagem via whatsapp")
    
            
        response_dict['status_code'] = response.status_code
        response_dict['message_id_whatsApp'] = id_message
        response_dict['phone_to'] = phone_to  
  
        return response_dict
    
    def process_webhook_notification(self, data):
        response = []
                   
        for entry in data['entry']:
            for change in entry["changes"]:
                response.append(
                    {   
                        'object': data["object"],  # igual em todos
                        'entryid': entry['id'],  # igual em todos
                        'field': change['field'],    # igual em todos
                        'messaging_product': change['value']['messaging_product'],  # igual em todos
                        'display_phone_number': change['value']['metadata']['display_phone_number'],  # igual em todos
                        'phone_number_id': change['value']['metadata']['phone_number_id'],  # igual em todos
                        'name_contacts': change['value']['contacts'][0]['profile']['name'],  # igual em todos
                        'wa_id': change['value']['contacts'][0]['wa_id'],  # igual em todos
                        'from': change['value']['messages'][0]['from'],  # igual em todos
                        'message_id': change['value']['messages'][0]['id'],  # igual em todos
                        'timestamp': change['value']['messages'][0]['timestamp'],  # igual em todos
                        'type': change['value']['messages'][0]['type'],  # igual em todos
                        'text_body': change['value']['messages'][0]['text']['body'],  # altera para cada tipo de mensagem
                    }
                )
                
        return response
