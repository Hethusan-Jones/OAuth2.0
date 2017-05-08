import os
import logging
import json
import jinja2
import webapp2
import urllib
import hashlib
from google.appengine.api import urlfetch


client_id = "1016136940228-8eqgf7817ailevij436do6k3cd6btj7i.apps.googleusercontent.com"
redirect_uri = "http://localhost:8080/oauth"
client_secret = "N7B8F-X94JDsg8m36axvL79b"


JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)
# [END imports]


class loginHandler(webapp2.RequestHandler):

	def get(self):
		state = hashlib.sha256(os.urandom(1024)).hexdigest()

		# May need to parse this json object a little more
		payload = {
		'response_type': 'code',
		'state' : state,
		'client_id' : client_id,
		'redirect_uri' : redirect_uri,
		'scope' : "email",
		'access_type':'offline',
		'prompt': 'consent select_account'
		}

		#encodedString = urllib.urlencode(data)
		address = 'https://accounts.google.com/o/oauth2/auth' 
		encodedGetData = urllib.urlencode(payload)
		newAddress = address + '?' + encodedGetData
		return self.redirect(newAddress)



		"""auth_uri = flow.step1_get_authorize_url()
		r = requests.get(auth_uri)
		if r['error']:
			r.response.write("You have denied access")
			r.response.status = "401  You denied access"
			return
		auth_code = r.get('code')
		client_secret = r.get('state')
		client_id = r.get('client_id')

		credentials = flow.step2_exchange(auth_code)
		http_auth = credentials.authorize(httplib2.Http())"""

	def post(self):
		pass

class OAuthHandler(webapp2.RequestHandler):

	def get(self):
		r_data = self.request.GET
		if 'error' in r_data:
			self.response.write("You have denied access")
			self.response.status = "401  You denied access"
			return		

		post_data = {
			'code': r_data['code'],
			'client_id' : client_id,
			'client_secret' : client_secret,
			'grant_type' : 'authorization_code',
			'redirect_uri' : redirect_uri
		}

		encodedPostData = urllib.urlencode(post_data)
		url_to_post = 'https://accounts.google.com/o/oauth2/token'
		headers = {'Content-Type': 'application/x-www-form-urlencoded', }
		result = urlfetch.Fetch(url=url_to_post, payload=encodedPostData, method=urlfetch.POST, headers=headers)
		jsonResponse = json.loads(result.content)
		#self.response.write(jsonResponse)
		accessToken = jsonResponse['access_token']
		auth_header = {'Authorization': 'Bearer ' + accessToken }

		req2 = urlfetch.fetch('https://www.googleapis.com/plus/v1/people/me', headers=auth_header)
		req2jsonResponse = json.loads(req2.content)

		#for i in req2jsonResponse:
			#self.response.write(i)
		#self.response.write(req2jsonResponse)
	
		#email = req2jsonResponse.emails['values']
		name = req2jsonResponse['displayName']

		googlePlusUrl = req2jsonResponse['url']

		template_values = {
		'name' : name,
		'plusUrl': googlePlusUrl,
		'state': r_data['state']
		}

		template = JINJA_ENVIRONMENT.get_template('./display.html')
		self.response.write(template.render(template_values))

		#self.response.write(r2)"""


		
class ClientPage(webapp2.RequestHandler):

	def get(self):
		template_values = {
		'url': "/login",
		'url_linktext': 'Click this link',
		}

		template = JINJA_ENVIRONMENT.get_template('./ClientPage.html')
		self.response.write(template.render(template_values))


# [START app]
app = webapp2.WSGIApplication([
	('/', ClientPage),
	('/login', loginHandler),
	('/oauth.*', OAuthHandler)
], debug=True)
# [END app]
