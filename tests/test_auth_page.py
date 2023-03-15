from pages.auth_page import AuthPage
from selenium.webdriver.common.by import By
import pytest
from settings import *

#  тесты настроены на запуск через консоль командой:
#  'python -m pytest -v --driver Chrome --driver-path chromedriver test_auth_page.py'


#  ТЕСТ №1
# ПЕРЕКЛЮЧЕНИЕ ТАБА ПРИ ВВОДЕ ПОЧТЫ ИЛИ ЛОГИНА В ПОЛЕ "НОМЕР"
@pytest.mark.positive
@pytest.mark.parametrize('phone', [russian_chars(), english_chars(), special_chars(), chinese_chars(),
                                   f'{russian_chars()}555555', valid_email],
                         ids=['russian_chars', 'english_chars', 'special_chars', 'chinese_chars',
                             'russian_chars_figure', valid_email])
def test_auth_page_change_tab_phone(selenium, phone):
    page = AuthPage(selenium)
    page.btn_phone.click()
    page.enter_email(phone)
    selenium.implicitly_wait(3)
    page.enter_pass(valid_password)
    selenium.implicitly_wait(3)
    # таб выбора аутентификации меняется на "логин" или "почта"
    assert page.btn_login.get_attribute("class") == 'rt-tab rt-tab--small rt-tab--active' or \
           page.btn_mail.get_attribute("class") == 'rt-tab rt-tab--small rt-tab--active'


#  ТЕСТ №2
# ПЕРЕКЛЮЧЕНИЕ ТАБА ПРИ ВВОДЕ ЛОГИНА ИЛИ НОМЕРА ТЕЛЕФОНА ИЛИ ЛИЦЕВОГО СЧЕТА В ПОЛЕ "ПОЧТА"
@pytest.mark.positive
@pytest.mark.parametrize('mail', [valid_phone, '123456789123', 'dfjdhg555'],
                         ids=[valid_phone, 'personal_account', 'login'])
def test_auth_page_change_tab_email(selenium, mail):
    page = AuthPage(selenium)
    page.btn_mail.click()
    page.enter_email(mail)
    selenium.implicitly_wait(3)
    page.enter_pass(valid_password)
    selenium.implicitly_wait(3)

    # таб выбора аутентификации меняется на "логин" или "номер" или "л/с"
    assert page.btn_login.get_attribute("class") == 'rt-tab rt-tab--small rt-tab--active' or \
           page.btn_phone.get_attribute("class") == 'rt-tab rt-tab--small rt-tab--active' or \
           page.btn_personal_account.get_attribute("class") == 'rt-tab rt-tab--small rt-tab--active'


#  ТЕСТ №3
# ПЕРЕКЛЮЧЕНИЕ ТАБА ПРИ ВВОДЕ ПОЧТЫ ИЛИ НОМЕРА ТЕЛЕФОНА ИЛИ Л/С В ПОЛЕ "ЛОГИН"
@pytest.mark.positive
@pytest.mark.parametrize('login', [valid_phone, '123456789123', valid_email],
                         ids=[valid_phone, 'personal_account', 'valid_emai'])
def test_auth_page_change_tab_login(selenium, login):
    page = AuthPage(selenium)
    page.btn_login.click()
    page.enter_email(login)
    selenium.implicitly_wait(3)
    page.enter_pass(valid_password)
    selenium.implicitly_wait(3)

    # таб выбора аутентификации меняется на "почта" или "номер" или "л/с"
    assert page.btn_mail.get_attribute("class") == 'rt-tab rt-tab--small rt-tab--active' or \
           page.btn_phone.get_attribute("class") == 'rt-tab rt-tab--small rt-tab--active' or \
           page.btn_personal_account.get_attribute("class") == 'rt-tab rt-tab--small rt-tab--active'


# #  ТЕСТ №4
# ПЕРЕКЛЮЧЕНИЕ ТАБА ПРИ ВВОДЕ ПОЧТЫ ИЛИ НОМЕРА ТЕЛЕФОНА ИЛИ ЛОГИНА В ПОЛЕ "Л/C"
@pytest.mark.positive
@pytest.mark.parametrize('personal_account', [valid_phone, 'adsfadfd5689', valid_email],
                         ids=[valid_phone, 'login', 'valid_emai'])
def test_auth_page_change_tab_personal_account(selenium, personal_account):
    page = AuthPage(selenium)
    page.btn_personal_account.click()
    page.enter_email(personal_account)
    selenium.implicitly_wait(3)
    page.enter_pass(valid_password)
    selenium.implicitly_wait(3)

    # таб выбора аутентификации меняется на "почта" или "номер" или "логин"
    assert page.btn_mail.get_attribute("class") == 'rt-tab rt-tab--small rt-tab--active' or \
           page.btn_login.get_attribute("class") == 'rt-tab rt-tab--small rt-tab--active' or \
           page.btn_phone.get_attribute("class") == 'rt-tab rt-tab--small rt-tab--active'


# # ТЕСТ №5
# ПОЗИТИВНЫЙ ТЕСТ , проверка поля ввода НОМЕРА ТЕЛЕФОНА в форме авторизации
# невозможно проверить валидный логин и л/с в связи с отсутствием данных.
@pytest.mark.positive
@pytest.mark.parametrize('number', [valid_email, valid_phone],
                         ids=['valid_email', 'valid_phone'])

def test_auth_page_number_enter_figure(selenium, number):
    page = AuthPage(selenium)

    page.btn_phone.click()
    page.enter_email(number)
    selenium.implicitly_wait(3)
    page.enter_pass(valid_password)
    page.btn_click()
    selenium.implicitly_wait(3)

    assert page.get_relative_link() == '/account_b2c/page', "login error"


# # ТЕСТ №6
# НЕГАТИВНЫЙ ТЕСТ , проверка поля ввода НОМЕРА ТЕЛЕФОНА в форме авторизации
# Авторизации клиента по номеру телефона при вводе цифр,
@pytest.mark.negative
@pytest.mark.parametrize('number', ['', figure(8), valid_phone, figure(10), figure(11)],
                         ids=['empty', 'figure_8', 'valid_phgone', 'figure_10', 'figure_11'])
# Авторизации клиента по номеру телефона при вводе цифр,

def test_auth_page_number_enter_figure(selenium, number):
    page = AuthPage(selenium)
    page.btn_phone.click()
    page.enter_email(number)
    selenium.implicitly_wait(8)
    page.enter_pass(valid_password)
    page.btn_click()
    selenium.implicitly_wait(3)

    if (0 < len(number) < 10 and number.isdigit()) or len(number) == 0:
        wrong_format_number = selenium.find_element(By.CLASS_NAME, 'rt-input-container__meta--error')
        assert (wrong_format_number.text == "Неверный формат телефона") or\
               (wrong_format_number.text == 'Введите номер телефона')
    elif len(number) >= 10 and number.isdigit():
        form_error = selenium.find_element(By.ID, 'form-error-message')
        assert form_error.text == 'Неверный логин или пароль'


# # ТЕСТ №7
# НЕГАТИВНЫЙ ТЕСТ , проверка поля ввода НОМЕРА ТЕЛЕФОНА в форме авторизации
# Авторизации клиента по номеру телефона при вводе  НЕ цифр,
@pytest.mark.negative
@pytest.mark.parametrize('number', [russian_chars(), english_chars(), chinese_chars(), special_chars()
                                    , '@', '@.', '.', f'{russian_chars()}@mail.ru',
                                   f'{chinese_chars()}@mail.ru', f'{special_chars()}@mail.ru'
                                    ],
                         ids=['russian_chars', 'english_chars', 'chinese_chars', 'special_chars'
                              , '@', '@ and point', 'point', 'russian format', 'chinese format', 'special format'
                              ])
def test_auth_page_number_enter_figure(selenium, number):
    page = AuthPage(selenium)
    page.btn_phone.click()
    page.enter_email(number)
    selenium.implicitly_wait(3)
    page.enter_pass(valid_password)
    page.btn_click()
    selenium.implicitly_wait(3)
    form_error = selenium.find_element(By.ID, 'form-error-message')
    if (number is not number.isdigit()) and len(number) != 0:
        assert form_error.text == 'Неверный логин или пароль' or form_error.text == 'Неверно введен текст с картинки'


# # ТЕСТ №8
# ПОЗИТИВНЫЙ ТЕСТ , проверка поля ввода ПОЧТА в форме авторизации
@pytest.mark.positive
@pytest.mark.parametrize('email', [valid_email, valid_phone],
                         ids=['valid_email', 'valid_phone'])
def test_auth_page_email_enter_positive(selenium, email):
    page = AuthPage(selenium)
    page.btn_mail_click()
    selenium.implicitly_wait(5)
    page.enter_email(email)
    selenium.implicitly_wait(5)
    page.enter_pass(valid_password)
    page.btn_click()
    if len(email) != 0:
        assert page.get_relative_link() == '/account_b2c/page', "login error"


# # ТЕСТ №9
# НЕГАТИВНЫЙ ТЕСТ , проверка поля ввода ПОЧТА в форме авторизации
@pytest.mark.negative
@pytest.mark.parametrize('email', ['', '@', '@.', '.', f'{russian_chars()}@mail.ru',
                                   f'{chinese_chars()}@mail.ru', f'{special_chars()}@mail.ru', 11111],
                         ids=['empty', '@', '@ and point', 'point', 'russian format',
                              'chinese format', 'special format', 'number'])
def test_auth_page_email_enter_negative(selenium, email):
    page = AuthPage(selenium)
    page.btn_mail_click()
    selenium.implicitly_wait(5)
    page.enter_email(email)
    selenium.implicitly_wait(5)
    page.enter_pass(valid_password)
    page.btn_click()

    if len(email) == 0:
        mistake_empty = selenium.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form/div[1]/div[2]/span')
        assert mistake_empty.text == "Введите адрес, указанный при регистрации"
    else:
        mistake = selenium.find_element(By.ID, 'form-error-message')
        assert mistake.text == "Неверный логин или пароль" or mistake.text == 'Неверно введен текст с картинки'


# ТЕСТ №10
# ПРОВЕРКА РАБОТЫ КНОПКИ "ЗАБЫЛ ПАРОЛЬ"
@pytest.mark.positive
def test_auth_page_forgot_password(selenium):
   page = AuthPage(selenium)
   selenium.implicitly_wait(5)
   page.btn_forgot_password.click()
   assert page.get_relative_link() == '/auth/realms/b2c/login-actions/reset-credentials', "login error"


# ТЕСТ №11
# НЕГАТИВНЫЙ ТЕСТ , проверка поля ввода ПАРОЛЬ в форме авторизации
# Валидный пароль тестируем для того, чтобы не появилась "капча"
@pytest.mark.negative
@pytest.mark.parametrize('password', ['', generate_string_rus(8), generate_string_en(256), valid_password,
                                       figure(8), figure(100)],
                         ids=['empty', '8 chars rus', '256 chars en', 'valid', '8 figure', '100 figure'])
def test_auth_page_password_enter_negative(selenium, password):
    page = AuthPage(selenium)
    page.btn_mail_click()
    selenium.implicitly_wait(5)
    page.enter_email(valid_email)
    selenium.implicitly_wait(5)
    page.enter_pass(password)
    page.btn_click()

    if len(password) == 0:
        assert page.get_relative_link() != '/account_b2c/page', "login error"
    else:
        mistake_form = selenium.find_element(By.ID, 'form-error-message')
        mistake = selenium.find_element(By.XPATH, '// *[ @ id = "page-right"] / div / div / h1')
        assert mistake_form.text == "Неверный логин или пароль" or mistake_form.text == \
               'Неверно введен текст с картинки' or mistake.text == "Ошибка"
        selenium.save_screenshot('result.png')


# # ТЕСТ №12
# ПОЗИТИВНЫЙ ТЕСТ , проверка поля ввода ЛОГИН в форме авторизации
@pytest.mark.positive
@pytest.mark.parametrize('login', [valid_email, valid_phone],
                         ids=['valid_email', 'valid_phone'])
def test_auth_page_email_enter_positive(selenium, login):
    page = AuthPage(selenium)
    page.btn_login_click()
    selenium.implicitly_wait(5)
    page.enter_email(login)
    selenium.implicitly_wait(5)
    page.enter_pass(valid_password)
    page.btn_click()

    if len(login) != 0:
        assert page.get_relative_link() == '/account_b2c/page', "login error"


# # ТЕСТ №13
# # НЕГАТИВНЫЙ ТЕСТ , проверка поля ввода ЛОГИН в форме авторизации
@pytest.mark.negative
@pytest.mark.parametrize('login', [russian_chars(), english_chars(), special_chars(), chinese_chars(), figure(20)],
                         ids=['russian_chars', 'english_chars', 'special_chars', 'chinese_chars', '20 figure'])
def test_auth_page_login_enter_negative(selenium, login):
    page = AuthPage(selenium)
    page.btn_login_click()
    page.enter_email(login)
    selenium.implicitly_wait(5)
    page.enter_pass(valid_password)
    selenium.implicitly_wait(5)
    page.btn_click()
    mistake = selenium.find_element(By.ID, 'form-error-message')
    assert mistake.text == "Неверный логин или пароль" or mistake.text == 'Неверно введен текст с картинки'


# # ТЕСТ №14
# # НЕГАТИВНЫЙ ТЕСТ , проверка в поле ввода ЛОГИН в форме авторизации граничных значений
@pytest.mark.negative
@pytest.mark.parametrize('login', ['', figure(100), generate_string_en(1000), generate_string_en(256)],
                         ids=['empty', '100 figure', 'generate_string_en_1000', 'generate_string_en_256'])
def test_auth_page_login_enter_negative(selenium, login):
    page = AuthPage(selenium)
    page.btn_login_click()
    page.enter_email(login)
    selenium.implicitly_wait(5)
    page.enter_pass(valid_password)
    selenium.implicitly_wait(5)
    page.btn_click()
    if len(login) == 0:
        mistake_empty = selenium.find_element(By.CSS_SELECTOR, "span.rt-input-container__meta.rt-input-container__meta--error")
        assert mistake_empty.text == "Введите логин, указанный при регистрации"
    else:
        mistake = selenium.find_element(By.ID, 'form-error-message')
        assert mistake.text == "Неверный логин или пароль" or mistake.text == 'Неверно введен текст с картинки'


# # ТЕСТ №15
# # ПОЗИТИВНЫЙ, Авторизации клиента по номеру л/с
# # невозможно проверить валидный логин и л/с в связи с отсутствием данных.
@pytest.mark.positive
def test_auth_page_personal_account_pozitiv(selenium):
   page = AuthPage(selenium)
   page.btn_personal_account_click()
   page.enter_email(valid_email)
   selenium.implicitly_wait(5)
   page.enter_pass(valid_password)
   selenium.implicitly_wait(5)
   page.btn_click()

   assert page.get_relative_link() == '/account_b2c/page', "login error"


# # ТЕСТ №16
# # НЕГАТИВНЫЙ, Авторизации клиента по номеру л/с
# # невозможно проверить валидный логин и л/с в связи с отсутствием данных.
@pytest.mark.negative
@pytest.mark.parametrize('personal_account', ['', figure(8), figure(12), valid_phone],
                         ids=['empty', 'figure_8', 'figure_12', 'valid_number'])
def test_auth_page_personal_account_negativ(selenium, personal_account):
   page = AuthPage(selenium)
   page.btn_personal_account_click()
   page.enter_email(personal_account)
   selenium.implicitly_wait(5)
   page.enter_pass(valid_password)
   selenium.implicitly_wait(5)
   page.btn_click()
   mistake = selenium.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form/div[1]/div[2]/span')
   form_error = selenium.find_element(By.ID, 'form-error-message')
   assert mistake.text == "Проверьте, пожалуйста, номер лицевого счета" or form_error.text == 'Неверный логин или пароль'
   assert page.get_relative_link() != '/account_b2c/page', "login error"
















