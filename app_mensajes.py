from flask import Flask, request, jsonify
import PureCloudPlatformClientV2
from PureCloudPlatformClientV2.rest import ApiException
from PureCloudPlatformClientV2 import ApiClient, Configuration
import requests
from datetime import datetime
import unicodedata
import string

app = Flask(__name__)

def get_organizacion_1_token():
    url = 'url_token_region_genesys'
    response = requests.post(url)
    response_data = response.json()
    return response_data['token']

def get_organizacion_2_token():
    url = 'url_token_region_genesys'
    response = requests.post(url)
    response_data = response.json()
    return response_data['token']

def normalize_text(text):
    text = text.lower()
    text = unicodedata.normalize('NFKD', text)
    text = ''.join(c for c in text if not unicodedata.combining(c))
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text.strip()

def get_conversation_details(api_client, conversation_id, after_time):
    conversations_api = PureCloudPlatformClientV2.ConversationsApi(api_client)
    
    try:
        api_response = conversations_api.get_conversations_message(conversation_id)
        conversation_data = api_response.to_dict()

        customer_messages = []
        for participant in conversation_data.get('participants', []):
            if participant.get('purpose') == 'customer' and 'messages' in participant:
                for message in participant['messages']:
                    message_id = message.get('message_id')
                    message_time = message.get('message_time')
                    if message_id and message_time:
                        customer_messages.append((message_id, message_time))
        
        customer_messages.sort(key=lambda x: x[1])

        for message_id, message_time in customer_messages:
            if message_time > after_time:
                last_message_body, original_message = get_message_body(api_client, conversation_id, message_id)
                readable_time = message_time.strftime("%d de %B de %Y, %I:%M %p")
                return {
                    "message": "El usuario está interactuando",
                    "last_message_body": last_message_body,
                    "original_message": original_message
                }

        return None

    except ApiException as e:
        print(f"Exception when calling ConversationsApi->get_conversations_message: {e}\n")
        return None

def get_message_body(api_client, conversation_id, message_id):
    conversations_api = PureCloudPlatformClientV2.ConversationsApi(api_client)

    try:
        api_response = conversations_api.get_conversations_message_message(conversation_id, message_id)
        message_data = api_response.to_dict()
        text_body = message_data.get('text_body') or message_data.get('normalized_message', {}).get('text')

        option_1_variations = [
            "Valor1", 
            "Valor2" 
        ]

        option_2_variations = [
            "Valor1", 
            "valor2"
        ]

        option_3_variations = [
            "Valor1", 
            "Valor2"
        ]

        text_body_normalized = normalize_text(text_body) if text_body else ''

        if any(normalize_text(variation) == text_body_normalized for variation in option_1_variations):
            return "El usuario va al valor 1", text_body
        if any(normalize_text(variation) == text_body_normalized for variation in option_2_variations):
            return "El usuario va al valor 2", text_body
        if any(normalize_text(variation) == text_body_normalized for variation in option_3_variations):
            return "El usuario va al valor 3", text_body
        
        return "El usuario no seleccionó un valor", text_body
    except ApiException as e:
        print(f"Exception when calling ConversationsApi->get_conversations_message_message: {e}\n")
        return None, None

@app.route('/get_message_after', methods=['POST'])
def get_message_after():
    data = request.json
    conversation_id = data.get('conversation_id')
    after_time_str = data.get('after_time')
    organization = data.get('organization')

    if not conversation_id or not after_time_str or not organization:
        return jsonify({"error": "Missing conversation_id, after_time, or organization"}), 400

    if organization not in ['organizacion 1', 'organizacion 2']:
        return jsonify({"error": "Invalid organization. Use 'organizacion 1' or 'organizacion 2'"}), 400

    try:
        after_time = datetime.fromisoformat(after_time_str.replace('Z', '+00:00'))
    except ValueError:
        return jsonify({"error": "Invalid date format. Use ISO 8601 format 'YYYY-MM-DDTHH:MM:SS.sssZ'"}), 400

    if organization == 'organizacion 1':
        access_token = get_organizacion_1_token()
        host = 'host_organizacion_genesys'
    elif organization == 'organizacion 2':
        access_token = get_organizacion_2_token()
        host = 'host_organizacion_genesys'

    config = Configuration()
    config.host = host
    config.access_token = access_token

    api_client = ApiClient()
    api_client.configuration = config

    message_details = get_conversation_details(api_client, conversation_id, after_time)

    if message_details:
        return jsonify(message_details)
    else:
        return jsonify({"message": "No hubo interacción por parte del usuario."})

if __name__ == '__main__':
    app.run(debug=True)
