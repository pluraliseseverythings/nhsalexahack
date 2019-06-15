import requests
import xml.etree.ElementTree as ET

SUBSCRIPTION_KEY = "03a679cfd7e44542877f1b264d8565ec"
BASE_URL = "https://api.nhs.uk/data/"

# hospitals/postcode/LS74QH/?distance=10&subscription-key=03a679cfd7e44542877f1b264d8565ec"

class NHSOrganisationApi():
    """
    Usage:
      client = NHSOrganisationApi()
      hospitals = client.get_hospitals()
    """

    def make_request(self, path, **kwargs):
        full_path = BASE_URL + path
        get_params = {
            **kwargs,
            'subscription-key': SUBSCRIPTION_KEY,
        }
        response = requests.get(full_path, params=get_params)
        root = ET.fromstring(response.text)
        return root

    def get_hospitals(self):
        response = self.make_request("hospitals/all", distance="12")
        # Turn the XML tree into something useful
        return response

    def get_hospital(self, id):
        response = self.make_request("hospitals/%s" % id)
        # Turn the XML tree into something useful
        return response
    
    def get_hospital_facilities(self, id):
        response = self.make_request("hospitals/%s/facilities" % id)
        # Turn the XML tree into something useful
        return response 
