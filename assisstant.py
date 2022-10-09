import subprocess
import pyttsx3
import cv2
import face_recognition as fr
import numpy as np
import pygetwindow as gw
from io import *
import random
from getpass import getpass
import speech_recognition as sr
import pyautogui as pg
import datetime
import win32clipboard
import wikipedia
import webbrowser
import bs4
import os
import PIL
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import winshell
import pyjokes
import ctypes
import time
import requests
from word2number import w2n

awake = 1
rememberkeyword = None
conversationID = None

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 170)

def speak(audio):
	engine.say(audio)
	print(f"Mark : {audio}")
	engine.runAndWait()

# '''
def takeCommand():
	r = sr.Recognizer()
	with sr.Microphone() as source:
		if awake == 1:
			print("Listening...")
		r.adjust_for_ambient_noise(source, duration = 1)
		r.pause_threshold = 1
		audio = r.listen(source)

	try:
		if awake == 1:
			print("Recognizing...")
		query = r.recognize_google(audio, language ='en-in')
		print(f"User : {query}\n")
		return query

	except Exception as e:
		print(e)
		if awake == 1:
			print("Unable to Recognize your voice.")
			rand = random.randint(0, 1)
			if rand == 0:
				speak("What'd you say again?")
			elif rand == 1:
				speak("I didn't understand. Please repeat once again sir.")
		return "None"

'''
def takeCommand():
	query = input("Enter your query : ")
	return query
'''

def inactivity(time_sec):
	if time_sec == 0:
		global awake
		awake = 0
		return "none"
	else:
		query = takeCommand().lower()
		if query == "none":
			inactivity(time_sec - 1)
		else:
			return query
		return query

def querycheck(query):
	if query != 'none':
		rand = random.randint(0, 2)
		if rand == 0:
			speak("Sorry sir, this service is currently unavailable.")
		elif rand == 1:
			speak("Sorry sir, you didn't install this service in my program yet.")
		elif rand == 2:
			speak("I am still learning sir!")

def weather():
	base_url = "http://api.openweathermap.org/data/2.5/weather?"
	test = requests.get('https://ipinfo.io/')
	d = test.json()
	city_name = d['city']
	complete_url = base_url + "q=" + city_name + '&appid=2f30c408e5a1a5f491d431591811e7a3'
	response = requests.get(complete_url)
	x = response.json()
	if x["cod"] != "404":
		y = x["main"]
		current_temperature = y["temp"]
		z = x["weather"]
		weather_description = z[0]["description"]
		speak(f"The temperature in {city_name} right now is {round(current_temperature - 273.15)} degree celsius with {weather_description}")

def wishMe():
	minute = int(datetime.datetime.now().minute)
	hour = int(datetime.datetime.now().hour)
	
	if hour >= 4 and hour < 7:
		speak("Good Morning Sir !")
		speak(f"It's {hour} {minute} AM. You are up so early. This invokes my curiosity. How about my help sir?")

	elif hour >= 7 and hour < 12:
		speak("Good Morning Sir !")
		speak(f"It's {hour} {minute} AM.")
		weather()
		speak("I am here at you service sir.")

	elif hour > 0 and hour < 4:
		speak(f"Hello Sir! It's around {hour} {minute} AM. What's keeping you up so late sir? Need some help?")

	elif hour == 0:
		speak(f"Hello Sir! It's around 12 {minute} AM. What's keeping you up so late sir? Need some help?")
	
	elif hour == 12:
		speak("Good Afternoon Sir !")
		speak(f"It's 12 {minute} pm.")
		weather()
		speak("I am here at your service sir.")

	elif hour > 12 and hour < 16:
		speak("Good Afternoon Sir !")
		speak(f"It's {hour - 12} {minute} PM.")
		weather()
		speak("I am here at your service sir.")

	elif hour >=16 and hour <=23:
		speak("Good Evening Sir !")
		speak(f"It's {hour - 12} {minute} PM.")
		weather()
		speak("I am here at your service sir.")

def windowshandler(query):
	a = gw.getAllTitles()

	if 'close' in str(query):
		if 'all' in str(query) or 'everything' in str(query):
			for i in range(len(a)):
				query = gw.getWindowsWithTitle(a[i])[0]
				query.close()

		else:
			query = query.replace('close ', '')
			print(query)
			for i in range(len(a)):
				if str(query) in str(a[i]).lower():
					query = gw.getWindowsWithTitle(a[i])[0]
					query.close()
	
	if 'minimise' in str(query):
		if 'all' in str(query) or 'everything' in str(query):
			for i in range(len(a)):
				query = gw.getWindowsWithTitle(a[i])[0]
				query.minimize()

		else:
			query = query.replace('minimise ', '')
			print(query)
			for i in range(len(a)):
				if str(query) in str(a[i]).lower():
					query = gw.getWindowsWithTitle(a[i])[0]
					if query.isMinimized == False:
						query.minimize()
					else:
						speak('The window is already minimized Sir.')

	elif 'maximise' in str(query):
		if 'all' in str(query) or 'everything' in str(query):
			for i in range(len(a)):
				query = gw.getWindowsWithTitle(a[i])[0]
				query.maximize()

		else:
			query = query.replace('maximise ', '')
			print(query)
			for i in range(len(a)):
				if str(query) in str(a[i]).lower():
					query = gw.getWindowsWithTitle(a[i])[0]
					if query.isMaximized == False:
						query.maximize()
					else:
						speak('The window is already maximized Sir.')

	elif 'restore' in str(query):
		query = query.replace('restore ', '')
		print(query)
		for i in range(len(a)):
			if str(query) in str(a[i]).lower():
				query = gw.getWindowsWithTitle(a[i])[0]
				print(query)
				query.restore()
	
	elif 'switch to' in str(query):
		query = query.replace('switch to ', '')
		print(query)
		for i in range(len(a)):
			if str(query) in str(a[i]).lower():
				query = gw.getWindowsWithTitle(a[i])[0]
				print(query)
				if query.isMinimized == False:
					query.minimize()
					query.restore()

				elif query.isMinimized == True:
					query.restore()

	elif 'change window to' in str(query):
		query = query.replace('change window to ', '')
		print(query)
		for i in range(len(a)):
			if str(query) in str(a[i]).lower():
				query = gw.getWindowsWithTitle(a[i])[0]
				print(query)
				if query.isMinimized == False:
					query.minimize()
					query.restore()

				elif query.isMinimized == True:
					query.restore()
				query.activate()


'''
def s(query):
	
	Sound.mute()
	Sound.mute()
	Sound.volume_set(50)

	if "unmute" in query:
		Sound.track()
		if Sound.ismuted is False:
			speak("Already unmuted sir")
		elif Sound.ismuted is True:
			Sound.ismuted = (not Sound.ismuted)
			Keyboard.key(Keyboard.VK_VOLUME_MUTE)
			speak('Can you hear me now?')

	elif "mute" in query:
		Sound.track()
		if Sound.ismuted is True:
			print("Sound is alread muted")
		elif Sound.ismuted is False:
			speak("Muting")
			Sound.ismuted = (not Sound.ismuted)
			Keyboard.key(Keyboard.VK_VOLUME_MUTE)
			print('Sound Muted')
		
	elif 'set volume to' in query:
		query = query.replace("set volume to", "")
		amount = int(query)
		Sound.volume_set(amount)

	elif 'set system volume to' in query:
		query = query.replace("set system volume to", "")
		amount = int(query)
		Sound.volume_set(amount)
		
	elif 'maximize the volume' or 'maximise the volume' or 'maximise volume' or 'maximize volume' in query or 'increase the volume completely' in query:
		Sound.volume_set(100)

	elif 'minimize the volume' or 'minimise the volume' or 'minimise volume' or 'minimize volume' in query or 'decrease the volume completely' in query:
		Sound.volume_set(0)
'''

d1 = None
music = ' '

def pyt(query):
	global music
	global d1
	if music not in query:
		if d1 is not None:
			music = query.replace('play', '')
			d1.get('https://www.youtube.com/results?search_query=' + music)
			wait = WebDriverWait(d1, 20)
			visible = EC.visibility_of_element_located
			wait.until(visible((By.ID, "video-title")))
			d1.find_element(By.ID, 'video-title').click()
			try:
				skip = wait.until(visible((By.CLASS_NAME, 'ytp-ad-preview-container')))
				if skip is not None:
					wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'ytp-ad-skip-button-container')))
					d1.find_element(By.CLASS_NAME, 'ytp-ad-skip-button-container').click()
			except Exception as e:
				return
			
		else:
			options = webdriver.FirefoxOptions()
			options.add_argument('media.allowed-to-play.enabled')
			#query = 'the tale of seventh hokage'
			visible = EC.visibility_of_element_located
			d1 = webdriver.Firefox(executable_path = r"C:\\Users\\sansk\\Desktop\\geckodriver.exe", options = options)
			wait = WebDriverWait(d1, 20)
			if 'play' in query:
				music = query.replace('play', '')
				d1.get('https://www.youtube.com/results?search_query=' + music)
				wait.until(visible((By.ID, "video-title")))
				d1.find_element(By.ID, 'video-title').click()
				try:
					skip = wait.until(visible((By.CLASS_NAME, 'ytp-ad-preview-container')))
					if skip is not None:
						wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'ytp-ad-skip-button-container')))
						d1.find_element(By.CLASS_NAME, 'ytp-ad-skip-button-container').click()
				except Exception as e:
					return

	else:
		if 'play' in query:
			d1.find_element(By.CLASS_NAME, 'ytp-play-button').click()
		elif 'pause' in query or 'stop' in query:
			d1.find_element(By.CLASS_NAME, 'ytp-play-button').click()

def playmusic(query):
	global music
	global d1
	if 'the music' in query or 'the song' in query or 'it' in query or query == 'play' or query == 'pause':
		if music is None:
			pyt(query)
		elif music is not None:
			query = query.replace('the music', '')
			query = query.replace('it', '')
			query = query.replace('the song', '')
			query = query + ' ' + music
			pyt(query)	 
	else:
		pyt(query)

def remember(query):
	global rememberkeyword
	query = query.replace("remember that ", "")
	query = query.replace("remember to ", "")
	query = query.replace("Will you remember ", "")
	rememberkeyword = query
	speak("Okay sir, I'll remember that.")

def getLocation():
	options = webdriver.FirefoxOptions()
	options.preferences["permissions.default.geo"]=1
	options.add_argument('--headless')
	timeout = 20
	driver = webdriver.Firefox(executable_path = r"C:\\Users\\sansk\\Desktop\\geckodriver.exe", options = options)
	url = "https://mycurrentlocation.net"
	#url = "https://where-am-i.org/"
	#//*[@id="address"]
	#url = "https://findmylocation.org/"
	#//*[@id="locationname"]
	driver.get(url)
	wait = WebDriverWait(driver, timeout)
	loc = driver.find_element(By.XPATH, '//*[@id="neighborhood"]')
	loc = loc.get_attribute('innerHTML')
	driver.quit()
	return loc

def facerec():
	images = []
	classNames = []
	path = 'D:\\CodeDump\\assistants\\face_rec\\faces'
	list = os.listdir(path)

	for cl in list:
		curimg = cv2.imread(f'{path}/{cl}')
		images.append(curimg)
		classNames.append(os.path.splitext(cl)[0])

	def findEncodings(images):
		encodeList = []
		for img in images:
			img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
			encode = fr.face_encodings(img)[0]
			encodeList.append(encode)
		return encodeList

	encodeListKnown = findEncodings(images)

	cap = cv2.VideoCapture(0)

	while True:
		success, frame = cap.read()
		frameS = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
		frameS = cv2.cvtColor(frameS, cv2.COLOR_BGR2RGB)
		faceLocs = fr.face_locations(frameS)
		encode = fr.face_encodings(frameS, faceLocs)
		name = "Unknown"

		for encodeface, faceLoc in zip(encode, faceLocs):
			matches = fr.compare_faces(encodeListKnown, encodeface)
			faceDis = fr.face_distance(encodeListKnown, encodeface)
			matchIndex = np.argmin(faceDis)
			if matches[matchIndex]:
				name = classNames[matchIndex]
				#print(name, matches)

			top, right, bottom, left = faceLoc
			top, right, bottom, left = top * 4, right * 4, bottom * 4, left * 4
			cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 255), 2)
			cv2.rectangle(frame, (left, bottom + 20), (right, bottom), (255, 0, 255), cv2.FILLED)
			cv2.putText(frame, name, (left + 10, bottom + 15), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.75, (255, 255, 255), 1)
		
		cv2.imshow('Camera', frame)
		#cv2.waitKey(1)

		'''for name in classNames:
			ra = random.randint(0, 1)
			if ra == 1:
				speak(f'hello {name}')'''

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	cap.release()
	cv2.destroyAllWindows()

def security():
	def sendmsg():
		cv2.imwrite('intruder.jpg', frame1)
		webbrowser.open("https://web.whatsapp.com/send?phone=+919818001599&text=Intruder%20Detected!")
		image = PIL.Image.open("D:\\CodeDump\\New Assistant\\intruder.jpg")
		output = BytesIO()
		image.convert('RGB').save(output, "BMP")
		data = output.getvalue()[14:]
		output.close()
		win32clipboard.OpenClipboard()
		win32clipboard.EmptyClipboard()
		win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
		win32clipboard.CloseClipboard()
		time.sleep(2)
		pg.hotkey('ctrl', 'v')
		pg.press('enter')

	cam = cv2.VideoCapture(0)
	while cam.isOpened():
		ret, frame1 = cam.read()
		ret, frame2 = cam.read()
		diff = cv2.absdiff(frame1, frame2)
		gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
		blur = cv2.GaussianBlur(gray, (5, 5), 0)
		_, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
		dilated = cv2.dilate(thresh, None, iterations=3)
		contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		# cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)
		for c in contours:
			if cv2.contourArea(c) > 2500:
				# continue
				x, y, w, h = cv2.boundingRect(c)
				cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
				sendmsg()

		if cv2.waitKey(10) == ord('q'):
			break
		cv2.imshow('Granny Cam', frame1)

def hello():
	t = random.randint(0, 1)
	if t == 1:
		speak("Hello Sir!")
	elif t == 0:
		speak("Hey there! Nice to meet you!")
	

if __name__ == '__main__':
	clear = lambda: os.system('cls')
	clear()
	wishMe()

	while True:

		if awake == 1:
			query = inactivity(2)

		elif awake == 0:
			query = takeCommand()

		if "my facebook" in query or "my fb" in query or "my Facebook" in query or "Facebook" in query or "facebook" in query:
			if awake == 1:
				driver = webdriver.Firefox(executable_path = r"C:\\Users\\sansk\\Desktop\\geckodriver.exe")
				speak("sure sir!")
				driver.get('https://www.facebook.com')
				time.sleep(5)
				username_box = driver.find_element_by_name("email")
				username_box.click()
				username_box.send_keys('sanskar2405@gmail.com')
				print ("Email Id entered")
				time.sleep(2)
				
				password_box = driver.find_element_by_name("pass")
				password_box.send_keys('sanskar$jain')
				print ("Password entered")
				
				login_box = driver.find_element_by_name("login")
				driver.implicitly_wait(3)
				login_box.click()
				speak("Sir, I have logged into your facebook account in a new window.")
				'''if driver.find_element(By.CLASS_NAME, 'pq6dq46d e9vueds3 ekzkrbhg omvj5yrc jiuqdcnw d82f96u3 gky8063y sibfvsnu px9q9ucb j2ut9x2k p4hiznlx').is_displayed():
					noti = driver.find_element(By.CLASS_NAME, 'bp9cbjyn bwm1u5wc pq6dq46d datstx6m taijpn5t jb3vyjys jxrgncrl qt6c0cv9 qnrpqo6b k4urcfbm')
				if driver.find_element(By.CLASS_NAME, 's45kfl79 emlxlaya bkmhp75w spb7xbtv pq6dq46d e9vueds3 ekzkrbhg omvj5yrc jiuqdcnw d82f96u3 gky8063y').is_displayed():
					mes = driver.find_element(By.CLASS_NAME, 's45kfl79 emlxlaya bkmhp75w spb7xbtv pq6dq46d e9vueds3 ekzkrbhg omvj5yrc jiuqdcnw d82f96u3 gky8063y').get_attribute('innerHTML')
				if mes is None and noti is None:
					speak("It looks like you're all caught up sir!")
				elif mes is not None:
					speak(f"There are {mes.get_attribute('innerHTML')} users waiting for your response sir.")
				elif noti is not None:
					speak(f"You have {noti.get_attribute('innerHTML')} notifications.")
				elif mes is not None and noti is not None:
					speak(f"you have {noti.get_attribute('innerHTML')} notifications and {mes.get_attribute('innerHTML')} messages.")
				text = takeCommand()'''

		elif "weather updates" in query or"weather" in query or "forecast" in query or "temperature" in query or "will it rain today" in query or "rain" in query:
			if awake == 1:
				
				base_url = "http://api.openweathermap.org/data/2.5/weather?"
				test = requests.get('https://ipinfo.io/')
				d = test.json()
				city_name = d['city']
				complete_url = base_url + "q=" + city_name + '&appid=2f30c408e5a1a5f491d431591811e7a3'
				response = requests.get(complete_url)
				x = response.json()
				
				if x["cod"] != "404":
					y = x["main"]
					current_temperature = y["temp"]
					current_pressure = y["pressure"]
					current_humidiy = y["humidity"]
					z = x["weather"]
					weather_description = z[0]["description"]
					print(" Temperature (in kelvin unit) = " +str(round(current_temperature - 273.15, 2)) +"\n atmospheric pressure (in hPa unit) ="+str(current_pressure) +"\n humidity (in percentage) = " +str(current_humidiy) +"\n description = " +str(weather_description))
					if current_temperature >= 30:
						speak(f"The temperature outside is {round(current_temperature - 273.15, 2)} degrees celcius.")
					elif current_temperature > 25 and current_temperature < 30:
						speak(f"The temperature outside is {round(current_temperature - 273.15, 2)} degrees celcius.")
				
				else:
					speak("No data present at the moment.")

		elif 'news' in query or "updates" in query:
			if awake == 1:
				try:
					jsonObj= requests.get("https://newsapi.org/v1/articles?source=the-times-of-india&sortBy=top&apiKey=e5191a2d43e4444c9191b807cdbbe3e8")
					data = jsonObj.json()
					i = 1
					
					speak('here are some top news from the times of india')
					print('''=============== TIMES OF INDIA ============'''+ '\n')
					
					for item in data['articles']:
						
						speak(str(i) + '. ' + item['title'] + '\n')
						print(item['description'] + '\n')
						
						i += 1
				except Exception as e:
					
					print(str(e))

		elif 'free facebook tab' in query or 'new facebook tab' in query:
			if awake == 1:
				driver = webdriver.Firefox(executable_path = r"C:\\Users\\sansk\\Desktop\\geckodriver.exe")
				driver.get('https://www.facebook.com/')
				print("Opened facebook")
				time.sleep(1)
				usr = input("Enter username: ")
				passw = getpass("Enter password: ")
				username_box = driver.find_element_by_id('email')
				username_box.send_keys(usr)
				print ("Email Id entered")
				time.sleep(1)

				password_box = driver.find_element_by_id('pass')
				password_box.send_keys(passw)
				print ("Password entered")

				login_box = driver.find_element_by_name('login')
				driver.implicitly_wait(5)
				login_box.click()

		elif 'college portal' in query or 'amizone' in query or 'Amizone' in query:
			if awake == 1:
				driver = webdriver.Firefox(executable_path = r"C:\\Users\\sansk\\Desktop\\geckodriver.exe")
				speak("Here you go sir!")
				driver.get('https://s.amizone.net')
				time.sleep(5)
				username_box = driver.find_element_by_name('_UserName')
				username_box.send_keys('8764545')
				print ("Email Id entered")
				time.sleep(2)
				
				password_box = driver.find_element_by_name('_Password')
				password_box.send_keys('fba838')
				print ("Password entered")
				
				login_box = driver.find_element_by_class_name('login100-form-btn')
				driver.implicitly_wait(3)
				login_box.click()
				speak("Sir, I have logged into your amizone account in a new window.")

		elif 'play' in query or 'pause' in query or 'resume' in query or 'continue' in query:
			if awake == 1:
				playmusic(query)

		elif 'power point presentation' in query:
			if awake == 1:
				speak("Opening Power Point presentation")
				power = r"C:\\Users\\sansk\\Downloads"
				os.startfile(power)

		elif 'open' in query or 'launch' in query:
			if awake == 1:
				speak("Just a second sir.")
				time.sleep(1)
				speak("Here you go.")
				if 'youtube' in query:
					webbrowser.open("https://www.youtube.com")
				
				elif 'google' in query:
					webbrowser.open("https://www.google.com")

				elif 'stackoverflow' in query:
					webbrowser.open("https://www.stackoverflow.com")

				elif 'calculator' in query or 'calculate' in query:
					os.startfile('C:/Windows/System32/calc.exe')

				elif 'wordpad' in query or 'word pad' in query:
					os.startfile('C:\\Program Files\\Windows NT\\Accessories\\wordpad.exe')

				elif 'word' in query:
					os.startfile('winword')

				elif 'notepad' in query:
					os.startfile("C:\\Windows\\system32\\notepad.exe")

				elif 'excel' in query:
					os.startfile('excel')

				elif 'powerpoint' in query:
					os.startfile('powerpnt')
			
				elif 'that presentation' in query or 'the presentation' in query or 'our presentation' in query:
					os.startfile('C:\\Users\\sansk\\Desktop\\NTCC PPT.pptx')

				else:
					query = query.replace("launch", "")
					query = query.replace("open", "")
					webbrowser.open(query)			

		elif 'the time' in query or 'time is it' in query:
			if awake == 1:
				rand = random.randint(0, 1)
				minute = int(datetime.datetime.now().minute)
				hour = int(datetime.datetime.now().hour)
				if rand == 0:
					if hour < 12:
						speak(f"It's {hour} {minute} AM.")
					elif hour > 12 and hour <= 23:
						speak(f"It's {hour - 12} {minute} PM.")
					elif hour == 12:
						speak("It's 12 PM.")

				elif rand == 1:
					if hour < 12:
						speak(f"{hour} {minute} AM Sir")
					elif hour > 12 and hour <= 23:
						speak(f"{hour - 12} {minute} PM Sir")
					elif hour == 12:
						speak("12 PM Sir")

		elif "what is date" in query or "date" in query or "what's the date" in query or "what date is it today" in query or "what is day" in query or "day" in query or "what's the day" in query or "what day is it today" in query:
			date = datetime.date.today()
			day = datetime.datetime.now().strftime("%A")
			speak(f"It's {day}. {date}.")

		elif 'how are you' in query:
			if awake == 1:
				speak("I am fine, Thank you!")
				speak("How are you Sir?")

		elif 'hello' in query or 'hi' in query:
			if awake == 1:
				hello()
			elif awake == 0:
				awake = not awake
				hello()

		elif 'exit' in query or 'goodbye' in query:
			if awake == 1:
				speak("Thanks for giving me your time")
				exit()

		elif "good morning" in query or 'good afternoon' in query or 'good evening' in query:
			if awake == 1:
				t = random.randint(0, 1)
				if t == 1:
					wishMe()
				elif t == 0:
					hello()
			if  awake == 0:
				t = random.randint(0, 1)
				if t == 1:
					wishMe()
					awake = not awake
				elif t == 0:
					hello()
					awake = not awake

		elif 'fine' in query or 'good' in query or 'great' in query:
			if awake == 1:
				speak("It's good to know that your doing good.")

		elif "what's your name" in query or "what is your name" in query or 'who are you' in query:
			if awake == 1:
				speak("My name is Mark. I am a virtual assistant created by Mr. Sanskar")

		elif "who made you" in query or "who created you" in query:
			if awake == 1:
				speak("I have been created by Sanskar.")

		elif 'joke' in query:
			if awake == 1:
				speak(pyjokes.get_joke())

		elif "who am i" in query:
			if awake == 1:
				speak("If you talk then definitely you're human.")

		elif "why you came to world" in query:
			if awake == 1:
				speak("I was created by Mr. Sanskar as a minor project for college.")

		elif 'reason for you' in query:
			if awake == 1:
				speak("I was created as a minor project by Mister Sanskar ")

		elif 'lock windows' in query or 'lock the device' in query or 'lock the system' in query:
			if awake == 1:
				speak("locking the device")
				ctypes.windll.user32.LockWorkStation()

		elif 'shutdown system' in query:
			if awake == 1:
				speak("Hold On a Sec ! Your system is on its way toshut  down")
				subprocess.call('shutdown /sg')

		elif 'empty recycle bin' in query:
			if awake == 1:
				winshell.recycle_bin().empty(confirm = False, show_progress = False, sound = True)
				speak("Recycle Bin Recycled")

		elif "don't listen" in query or "stop listening" in query:
			if awake == 1:
				speak("For how much time you want to stop Mark from listening commands")
				timer = takeCommand()
				if "minutes" in timer:
					timer = timer.replace("minutes", "")
					a = int(w2n.word_to_num(timer)) * 60
				
				elif "seconds" in timer:
					a = int(w2n.word_to_num(timer.replace("seconds", "")))
				
				time.sleep(a)
				speak("Hello Sir, I am up.")

		elif "where is" in query or "show me the location" in query:
			if awake == 1:
				query = query.replace("where is ", "")
				query = query.replace("show me the location of ", "")
				location = query
				speak("User asked to locate")
				speak(location)
				webbrowser.open("https://www.google.com/maps/place/" + location)

		elif "restart" in query:
			if awake == 1:
				subprocess.call(["shutdown", "/g"])

		elif "hibernate" in query or "sleep" in query:
			if awake == 1:
				speak("Hibernating")
				subprocess.call("shutdown / h")

		elif "log off" in query or "sign out" in query:
			if awake == 1:
				speak("Make sure all the application are closed before sign-out")
				time.sleep(5)
				subprocess.call(["shutdown", "/l"])

		elif "write a note" in query or 'create a note' in query:
			if awake == 1:
				speak("What should i write, sir")
				note = takeCommand()
				file = open('Mark.txt', 'w')
				speak("Sir, Should i include date and time")
				snfm = takeCommand()
				if 'yes' in snfm or 'yep' in snfm  or 'yap' in snfm or 'sure' in snfm or 'why not' in snfm or 'of course' in snfm or 'obviously' in snfm or 'obvious' in snfm or 'make me happy':
					time = datetime.datetime.strptime('20 July 2022', '%d %B %Y')
					strTime = datetime.datetime.strftime(time ,"%d %B %Y, %I:%M %p")
					file.write(strTime)
					file.write(" :- ")
					file.write(note)
				else:
					file.write(note)

		elif "show note" in query or 'show the note' in query:
			if awake == 1:
				speak("Showing Notes")
				file = open("Mark.txt", "r")
				speak(file.read())	

		elif "assistant" in query or "mark" in query or "Mark" in query or 'are you there' in query or 'get up' in query or 'wake up' in query:
			if awake == 1:
				rand = random.randint(0, 1)
				if rand == 0:
					speak("Always here at your service sir.")
				elif rand == 1:
					speak("Your command is my wish sir.")
			
			elif awake == 0:
				awake = not awake
				speak('Yes sir.')

		elif 'some rest' in query or 'take rest' in query:
			if awake == 1:
				speak('Alright Sir, take care!')
				awake = not awake

		elif 'close it' in query or 'minimize it' in query or 'minimise it' in query or 'maximise it' in query or 'maximize it' in query or 'close this' in query or 'minimize this' in query or 'minimise this' in query or 'maximise this' in query or 'maximize this' in query or 'close this window' in query or 'minimize this window' in query or 'minimise this window' in query or 'maximise this window' in query or 'maximize this window' in query:
			if awake == 1:
				a = gw.getActiveWindowTitle()

				if 'close' in str(query):
					query = query.replace('close ', '')
					query = gw.getWindowsWithTitle(a)[0]
					print(query)
					query.close()
				
				if 'minimise' in str(query) or 'minimize' in str(query):
					query = query.replace('minimise ', '')
					query = query.replace('minimize ', '')
					query = gw.getWindowsWithTitle(a)[0]
					print(query)
					if query.isMinimized == False:
						query.minimize()

				if 'maximise' in str(query) or 'maximize' in str(query):
					query = query.replace('maximise ', '')
					query = query.replace('maximize ', '')
					query = gw.getWindowsWithTitle(a)[0]
					print(query)
					if query.isMaximized == False:
						query.maximize()

		elif 'close' in query or 'restore' in query or 'minimise' in query or 'change window to' in query or 'maximise' in query or 'switch to' in query or 'minimize' in query or 'maximize' in query:
			if awake == 1:
				windowshandler(query)

		elif "how are you" in query:
			if awake == 1:
				speak("I'm fine, glad you asked me that")

		elif "screenshot" in query:
			image = pg.screenshot()
			image1 = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
			cv2.imwrite("C:\\Users\\sansk\\Pictures\\Screenshots\\Screenshot.png", image1)
			speak("Screenshot taken successfully")
			image.show()

		elif 'thanks' in query or 'thank you' in query:
			if awake == 1:
				speak("That's my duty sir.")

		elif "I wasn't appreciating" in query or 'not appreciating' in query:
			if awake == 1:
				rand = random.randint(0, 1)
				if rand == 0:
					speak("What else do you want me to do sir?")
				elif rand == 1:
					speak('Sorry for the inconvenience sir. What shall I do then?')

		elif "remember that" in query or "remember to" in query or "remember this" in query or "will you remember" in query:
			if awake == 1:
				remember(query)

		elif "what did i ask you to remember" in query or "do you remember anything" in query or "did i ask you to remember anything" in query or "what do you remember" in query:
			if awake == 1:
				if rememberkeyword is None:
					speak("You didn't ask me to remember anything sir.")
				else:
					speak(f"You asked me to remember that {rememberkeyword}.")

		elif "forget what i said" in query or "forget what i asked you to remember" in query or "forget whatever you remember" in query or "forget that" in query:
			if awake == 1:
				rememberkeyword = None
				speak("Okay sir. Done.")

		elif "face recognition" in query:
			if awake == 1:
				speak('Enabling, FACE RECOGNITION PROTOCOL')
				time.sleep(5)
				speak('All settings toggled. Enabling, video input.')
				facerec()

		elif 'house security protocol' in query:
			if awake == 1:
				security()

		elif 'my location' in query or 'where am ' in query:
			if awake == 1:
				speak('Let\'s see')
				speak(f'Your location is {getLocation()}')

		elif "what is" in query or "who is" in query or "search" in query or "google search" in query or "can you tell me somehting about" in query or "tell me something about" in query or "do you know" in query or "do you know anything related to" in query or "can you tell me" in query or "how much is" in query or "add" in query or "multiply" in query or "divide" in query or "subtract" in query or "who are" in query or "what are" in query or "how many" in query or "how about" in query or "what about" in query:
			if awake == 1:
				temp = None
				if conversationID is None:
					url = "http://api.wolframalpha.com/v2/conversation.jsp?appid=R92R57-P2HGULUP83&input=" + query
				else:
					url = "http://api.wolframalpha.com/v2/conversation.jsp?appid=R92R57-P2HGULUP83&conversationID=" + conversationID + "&input=" + query
				response = requests.get(url)
				response = response.json()
				try:
					temp = response['result']
					conversationID = response['conversationID']
				except KeyError:
					try:
						e = response['error']
					except KeyError:
						temp = None
						continue
	
				if temp is None:
					temp = wikipedia.summary(query, 3)
					if temp is None:
						query = str(query)
						query = query.replace("search", "")
						query = query.replace("google ", "")
						query = query.replace("can you tell me about ", "")
						query = query.replace("tell me something about ", "")
						query = query.replace("do you know anything about", "")
						query = query.replace("do you know anything related to", "")
						query = query.replace("do you know ", "")
						query = query.replace("who is ", "")
						query = query.replace("what is ", "")
						url = 'https://google.com/search?q=' + query
						headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:101.0) Gecko/20100101 Firefox/101.0'}
						request_result = requests.get(url, headers = headers)
						soup = bs4.BeautifulSoup(request_result.content, "html.parser")
						temp = soup.find("span", class_= "Y2IQFc")
						if str(temp) == "None":
							temp = soup.find("span", class_ = "ILfuVd")
							if str(temp) != "None":
								temp = temp.find("span")
							elif str(temp) == "None":
								temp = soup.find("div" , class_ = 'kno-rdesc')
								if str(temp) != "None":
									temp = temp.find("span")
				speak(temp)

		elif "photo" in query or "photograph" in query or "click" in query:
			speak("Okay, ready?")
			time.sleep(1)
			speak("On my count")
			time.sleep(1)
			speak("3...")
			time.sleep(1)
			speak("2...")
			time.sleep(1)
			speak("1...")
			time.sleep(1)
			speak("Say Cheeeeeeese!")
			cam = cv2.VideoCapture(0)
			s, img = cam.read()
			if s:
				cv2.namedWindow("Camera", cv2.WINDOW_AUTOSIZE)
				cv2.imshow("Camera", img)
				cv2.waitKey(1)
				cv2.destroyWindow("Camera")
				cv2.imwrite("Capture.jpg", img)
				cv2.imshow("Capture", img)
				speak("This image will disappear in 5 seconds")
				cv2.waitKey(5000)
				cv2.destroyAllWindows()

		else:
			if awake == 1:
				querycheck(query)

		#elif "unmute" or "mute" or 'set volume to' or 'set system volume to' or 'maximize the volume' or 'maximise the volume' or 'maximise volume' or 'maximize volume' or 'increase the volume completely' or 'minimize the volume' or 'minimise the volume' or 'minimise volume' or 'minimize volume' or 'decrease the volume completely' in query:
			#s(query)