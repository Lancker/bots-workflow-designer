from config import Configuration
from utils.SeleniumHelper import SeleniumHelper

URL_INIT = 'https://www.linkedin.com/'
FIELD_LOGIN_USER = '#login-email'
FIELD_LOGIN_PASS = '#login-password'
ELEMENT_TOP_BAR = '.header-section'

def get_conn_id(html):
	connId = ''
	arr1 = html.split('connId=')
	if len(arr1) > 1:
		arr2 = arr1[1].split('&')
		connId = arr2[0]
	return connId

def get_driver(params=None):
	if params:
		if 'driver' in params:
			return params['driver']
	return SeleniumHelper(Configuration.selenium_driver_type)

def login(driver, params, skipLoad=False):
	cookies = None
	if not skipLoad:
		driver.loadPage(URL_INIT)
	logged = driver.getElement(ELEMENT_TOP_BAR)
	if not logged:
		if params['cookies']:
			driver.applyCookies(URL_INIT, params['cookies'])
			logged = driver.getElement(ELEMENT_TOP_BAR)
		if not logged:
			if params['cookies']:
				driver.cleanCookies()
			driver.selectAndWrite(FIELD_LOGIN_USER, params['email'])
			driver.selectAndWrite(FIELD_LOGIN_PASS, params['password'])
			driver.submitFormSelector(FIELD_LOGIN_PASS)
			cookies = driver.getCookies()
			driver.waitShowElement(ELEMENT_TOP_BAR)
	return cookies

def get_logged_in_driver(params=None):
	if params:
		if 'driver' in params:
			return params['driver']
	driver = SeleniumHelper(Configuration.selenium_driver_type)
	login(driver, params)
	return driver

def clone_driver(driver):
	return driver.cloneDriverSite(URL_INIT)

def clone_driver_wait(driver):
	return driver.waitCloneDriverSite(URL_INIT, ELEMENT_TOP_BAR)