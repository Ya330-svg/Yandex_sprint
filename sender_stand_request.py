import requests
import configuration

def post_new_user(user_body):
    # Формируем URL с помощью конкатенации строк
    url = configuration.BASE_URL + configuration.CREATE_USER_PATH
    response = requests.post(url, json=user_body)
    return response.json()

def post_new_client_kit(kit_body, auth_token):
    # Формируем URL с помощью конкатенации строк
    url = configuration.BASE_URL + configuration.CREATE_KIT_PATH
    headers = {
        "Authorization": auth_token
    }
    response = requests.post(url, json=kit_body, headers=headers)
    return response