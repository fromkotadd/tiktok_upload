import glob
import os
import random
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from video_link_path import link_2_dl
from geko_path import path

firefox_options = webdriver.FirefoxOptions()

# firefox_options.headless = True            # фоновый режим (без запуска пользовательского интерфейса драйвера)

firefox_options.add_argument("--mute-audio")


def logo_pass():
	"""
	Загрузка файла с логинами и паролями в список
	Файл должен содержаться в текущем каталоге исполняемого файла.
	"""
	with open('4988610.txt', 'r', encoding='utf8') as file:
		logo_pass_list = file.readlines()
		return logo_pass_list


def registration_on_tik_tok(login, password):
	"""
	переход на окно аутентификация в Тик-токе через твиттер
	"""
	browser.get('https://www.tiktok.com/login?redirect_url=https%3A%2F%2Fwww.tiktok.com%2Ffeedback')
	time.sleep(random.randint(4, 6))
	window_before = browser.window_handles[0]
	browser.find_element_by_xpath('//*[@id="root"]/div/div[1]/div/div[1]/div[2]/div[5]/div[2]').click()
	window_after = browser.window_handles[1]

	time.sleep(random.randint(4, 6))

	browser.switch_to.window(window_after)

	username_input = browser.find_element_by_id('username_or_email')
	username_input.clear()
	username_input.send_keys(login)

	password_input = browser.find_element_by_id('password')
	password_input.clear()
	password_input.send_keys(password)

	password_input.send_keys(Keys.ENTER)

	time.sleep(random.randint(4, 6))
	browser.switch_to.window(window_before)


def age_data_entry():
	"""
	Выбор Параметров возраста не ниже 18 лет,
	запись ника сгенерированного при регистрации в текстовый файл.
	Выкл. при использовании уже ранее регистрированных аккаунтов Тик-тока
	"""
	date_input_list = browser.find_element_by_class_name('date-selector-pc-oyWlO').find_elements_by_class_name(
		'container-1lSJp')
	for i in date_input_list:
		if i != date_input_list[-1]:
			i.click()
			choice_date = i.find_element_by_class_name('list-container-2f5zg').find_elements_by_tag_name('li')
			random.choice(choice_date).click()
			time.sleep(random.randint(4, 6))
		else:
			i.click()
			choice_date = i.find_element_by_class_name('list-container-2f5zg').find_elements_by_tag_name('li')
			random.choice(choice_date[18:]).click()
			time.sleep(random.randint(4, 6))

	browser.find_element_by_class_name('login-button-31D24').click()
	time.sleep(random.randint(4, 6))

	regist_name = browser.find_element_by_class_name('suggest-item-1zUHI').text
	browser.find_element_by_class_name('suggest-item-1zUHI').click()
	print(regist_name)
	with open("reg_name.txt", "a") as file:
		file.write(f"{regist_name}\n")

	time.sleep(random.randint(4, 6))

	browser.find_element_by_class_name('login-button-31D24').click()


def video_list_generation():
	"""
	генерация списка видео-файлов в указанной паке
	(путь к файловой папке указывается через модуль video_link_path.py)
	"""
	os.chdir(rf"{link_2_dl}")
	file_2_dl_list = []
	for file in glob.glob("*.mp4"):
		file_2_dl_list.append(file)
	return file_2_dl_list


def description_text():
	"""
	загрузка файла с описанием видео в список.
	Файл должен содержаться в текущем каталоге исполняемого файла.
	"""
	with open('4988611.txt', 'r', encoding='utf8') as file:
		description_text = file.read().split('\n')
	return description_text


def video_upload(file_2_dl_list):
	"""
	функция загрузки видео-файлов в Тик-ток
	"""
	browser.get("https://www.tiktok.com/upload?lang=ru-RU")
	browser.refresh()
	time.sleep(random.randint(4, 6))
	elem_for_load = browser.find_element_by_name('upload-btn')

	link_on_video = rf"{link_2_dl}\{file_2_dl_list}"  # абсолютный путь к файлу
	elem_for_load.send_keys(link_on_video)


def description_text_input(description_text):
	"""
	функция внесения в поле описания видео - текста. Публикация видео
	"""
	time.sleep(random.randint(1, 2))
	browser.find_element_by_css_selector("div.notranslate.public-DraftEditor-content").send_keys("\b\b\b\b\b\b\b\b\b\b\b\b")
	browser.find_element_by_css_selector("div.notranslate.public-DraftEditor-content").send_keys(f' {description_text}')
	time.sleep(3)
	browser.find_element_by_class_name('tiktok-btn-pc-primary').click()
	time.sleep(random.randint(6, 8))


def multithreaded_load(description_text, video_list_generation):
	"""
	Функция многооконной заливки видео в тик-ток.
	Количество заливаемых видео за раз равно количеству видео-файлов в указанном каталоге
	"""
	counter = 0
	window_list = []
	for i in range(len(video_list_generation)):
		time.sleep(random.randint(4, 6))
		window_list.append(browser.window_handles[i])
		browser.execute_script("window.open();")
		time.sleep(random.randint(4, 6))
		browser.switch_to.window(browser.window_handles[i])
		video_upload(video_list_generation[i])
		time.sleep(random.randint(3, 5))
	for i in range(len(window_list)):
		browser.switch_to.window(browser.window_handles[i])
		if description_text[counter] == description_text[-1]:
			description_text_input(description_text[counter])
			counter = 0
		else:
			description_text_input(description_text[counter])
			counter = counter + 1


if __name__ == "__main__":
	logo_pass_list = logo_pass()
	description_text = description_text()
	video_list_generation = video_list_generation()
	for list in logo_pass_list:
		browser = webdriver.Firefox(executable_path=rf'{path}\geckodriver.exe',
									options=firefox_options)
		login = list.split(':')[0]
		password = list.split(":")[1]
		registration_on_tik_tok(login, password)
		#age_data_entry()  # функция генерации возраста и записи сгенерированного ника. Выкл. при использовании уже
		# ранее регистрированных аккаунтов Тик-тока
		multithreaded_load(description_text, video_list_generation)
		browser.quit()
		time.sleep(5)
		browser = None
