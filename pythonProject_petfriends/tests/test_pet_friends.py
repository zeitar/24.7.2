from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os


pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data(name='<Бобик>', animal_type='собакен',
                                    age='3', pet_photo='images/dawg.jpg'):
   pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

   _, auth_key = pf.get_api_key(valid_email, valid_password)

   status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

   assert status == 200
   assert result['name'] == name

def test_successful_delete_self_pet():

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Перс", "мегаперс", "1", "images/cat.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

        # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

        # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

        # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()

def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

# Доп. тесты
def test_get_api_key_for_invalid_user(email=invalid_email, password=invalid_password):
    # Проверяем что статус ответа = 403 при вводе неверных данных
    status, result = pf.get_api_key(email, password)
    assert status == 403

def test_get_api_key_for_invalid_password(email=valid_email, password=invalid_password):
    # Проверяем что статус ответа = 403 при вводе неверного пароля
    status, result = pf.get_api_key(email, password)
    assert status == 403

def test_get_api_key_for_invalid_email(email=invalid_email, password=valid_password):
    # Проверяем что статус ответа = 403 при вводе неверного пароля
    status, result = pf.get_api_key(email, password)
    assert status == 403

def test_get_my_pets(filter='my_pets'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_invalid_age(name='<Бобик>', animal_type='собакен',
                                    age='invalid', pet_photo='images/dawg.jpg'):
    # Проверяем что статус ответа = 403 при вводе неверного возраста
   pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

   _, auth_key = pf.get_api_key(valid_email, valid_password)

   status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
   # Если тест провален - баг апи
   assert status == 400

def test_add_new_pet_with_invalid_image(name='<Бобик>', animal_type='собакен',
                                    age='3', pet_photo='images/gif.txt'):
    # Проверяем что статус ответа = 403 при загрузке изображения неверного формата
   pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

   _, auth_key = pf.get_api_key(valid_email, valid_password)

   status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
   # Если тест провален - баг апи
   assert status == 400

def test_add_new_pet_with_invalid_name(name='', animal_type='собакен',
                                    age='3', pet_photo='images/dawg.jpg'):
    # Проверяем что статус ответа = 403 при отсутствующем имени
   pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

   _, auth_key = pf.get_api_key(valid_email, valid_password)

   status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
   # Если тест провален - баг апи
   assert status == 400

def test_add_new_pet_with_invalid_type(name='<Бобик>', animal_type='',
                                    age='3', pet_photo='images/dawg.jpg'):
    # Проверяем что статус ответа = 403 при загрузке изображения неверного формата
   pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

   _, auth_key = pf.get_api_key(valid_email, valid_password)

   status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
   # Если тест провален - баг апи
   assert status == 400

def test_add_new_pet_with_invalid_data(name='', animal_type='',
                                    age='', pet_photo='images/gif.txt'):
    # Проверяем что статус ответа = 403 при загрузке изображения неверного формата
   pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

   _, auth_key = pf.get_api_key(valid_email, valid_password)

   status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
   # Если тест провален - баг апи
   assert status == 400

def test_delete_others_pet():

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, pets = pf.get_list_of_pets(auth_key, "")

        # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

        # Ещё раз запрашиваем список питомцев
    _, pets = pf.get_list_of_pets(auth_key, "")

        # Проверяем что статус ответа не равен 200, иначе мы удалили чужого питомца, что является багом
    assert status != 200
    assert pet_id in pets.values()




