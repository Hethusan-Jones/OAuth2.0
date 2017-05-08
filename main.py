import os
import urllib
from google.appengine.ext import ndb
import logging
import json
import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# [END imports]


client_id = 1016136940228-8eqgf7817ailevij436do6k3cd6btj7i.apps.googleusercontent.com
client_secret = N7B8F-X94JDsg8m36axvL79b

class OAuthHandler(webapp2.RequestHandler):

	def get(self):
		logging.debug("GET contents: " + repr(self.request.GET))

	
	def post(self):
		if not self.request.body:
			self.response.write("Must provide a body in POST")
			self.response.status = "400 Must provide body in POST"
			return

		post_data = json.loads(self.request.body)		
		pass


class ClientPage(webapp2.RequestHandler):

	def get(self):
		self.response.write("This is the client page")
		template_values = {
		'url': "inputUrl",
		'url_linktext': 'Click this link',
		}
		template = JINJA_ENVIRONMENT.get_template('./ClientPage.html')
		self.response.write(template.render(template_values))


# [START app]
app = webapp2.WSGIApplication([
    ('/', ClientPage),
    ('/oauth.*', OAuthHandler)
], debug=True)
# [END app]
