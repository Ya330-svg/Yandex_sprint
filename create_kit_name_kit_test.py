import pytest
import sender_stand_request
import data

def get_auth_token():
    # Запрос для получения токена
    response = sender_stand_request.post_new_user(data.USER_BODY)
    return response['authToken']

def positive_assert(kit_body, auth_token):
    response = sender_stand_request.post_new_client_kit(kit_body, auth_token)
    assert response.status_code == 201
    assert response.json()["name"] == kit_body["name"]

def negative_assert_code_400(kit_body, auth_token):
    response = sender_stand_request.post_new_client_kit(kit_body, auth_token)
    assert response.status_code == 400

# 1. Допустимое количество символов (1)
def test_create_kit_with_1_char():
    auth_token = get_auth_token()
    kit_body = data.get_kit_body("a")
    positive_assert(kit_body, auth_token)

# 2. Допустимое количество символов (511)
def test_create_kit_with_511_chars():
    auth_token = get_auth_token()
    kit_body = data.get_kit_body("a" * 511)
    positive_assert(kit_body, auth_token)

# 3. Количество символов меньше допустимого (0)
def test_create_kit_with_0_chars():
    auth_token = get_auth_token()
    kit_body = data.get_kit_body("")
    negative_assert_code_400(kit_body, auth_token)

# 4. Количество символов больше допустимого (512)
def test_create_kit_with_512_chars():
    auth_token = get_auth_token()
    kit_body = data.get_kit_body("a" * 512)
    negative_assert_code_400(kit_body, auth_token)

# 5. Разрешены английские буквы
def test_create_kit_with_english_letters():
    auth_token = get_auth_token()
    kit_body = data.get_kit_body("QWErty")
    positive_assert(kit_body, auth_token)

# 6. Разрешены русские буквы
def test_create_kit_with_russian_letters():
    auth_token = get_auth_token()
    kit_body = data.get_kit_body("Мария")
    positive_assert(kit_body, auth_token)

# 7. Разрешены спецсимволы
def test_create_kit_with_special_characters():
    auth_token = get_auth_token()
    kit_body = data.get_kit_body("\"№%@\",")
    positive_assert(kit_body, auth_token)

# 8. Разрешены пробелы
def test_create_kit_with_spaces():
    auth_token = get_auth_token()
    kit_body = data.get_kit_body(" Человек и КО ")
    positive_assert(kit_body, auth_token)

# 9. Разрешены цифры
def test_create_kit_with_numbers():
    auth_token = get_auth_token()
    kit_body = data.get_kit_body("123")
    positive_assert(kit_body, auth_token)

# 10. Параметр не передан в запросе
def test_create_kit_without_name():
    auth_token = get_auth_token()
    kit_body = {}
    negative_assert_code_400(kit_body, auth_token)

# 11. Передан другой тип параметра (число)
def test_create_kit_with_number_as_name():
    auth_token = get_auth_token()
    kit_body = data.get_kit_body(123)
    negative_assert_code_400(kit_body, auth_token)