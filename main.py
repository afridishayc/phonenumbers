
import webapp2
import json
import phonenumbers
from phonenumbers import carrier

class MainHandler(webapp2.RequestHandler):
	def get(self):
		res = dict()
		phoneNumber = self.request.get("number")
		country = str(self.request.get("country"))
		if phoneNumber != '' and country !='':
			try:
				info = phonenumbers.parse(phoneNumber, country.upper())
				res['country_code'] = '+' + str(info.country_code)
				res['carrier'] = carrier.name_for_number(info, "en")
				res['is_valid'] = phonenumbers.is_valid_number(info)
				res['is_possible'] = phonenumbers.is_possible_number(info)
				formats = dict()
				formats['national'] = phonenumbers.format_number(info, phonenumbers.PhoneNumberFormat.NATIONAL)
				formats['international'] = phonenumbers.format_number(info, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
				formats['e164'] = phonenumbers.format_number(info, phonenumbers.PhoneNumberFormat.E164)
				res['formats'] = formats
			except:
				res['message'] = 'error'
			self.response.headers.add_header("Access-Control-Allow-Origin", "*")
			self.response.headers['Content-Type'] = 'application/json'
			self.response.write(json.dumps(res))
		else:
			self.set_status(404)

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
