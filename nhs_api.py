import requests
import xml.etree.ElementTree as ET
import untangle

SUBSCRIPTION_KEY = "03a679cfd7e44542877f1b264d8565ec"
BASE_URL = "https://api.nhs.uk/data/"

# hospitals/postcode/LS74QH/?distance=10&subscription-key=03a679cfd7e44542877f1b264d8565ec"

class Hospital():

    id = None
    title = None
    phone_number = None

    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.id = raw_data.id.cdata.split("/")[-1]
        self.title = raw_data.title.cdata
        self.phone_number = raw_data.content.s_organisationSummary.s_contact.s_telephone.cdata

class Facilities():

    parking_summary = None

    def __init__(self, raw_data):
        self.raw_data = raw_data
        facility_groups = raw_data.s_facilityGroups.s_facilityGroup
        facility_groups = [(group.s_name.cdata, group) for group in facility_groups]

        for (name, group) in facility_groups:
            print(name)
            if name == 'Parking':
                self.parking_summary = group.s_summaryText

class NHSOrganisationApi():
    """
    Usage:
      client = NHSOrganisationApi()
      hospitals = client.get_hospitals()
    """

    def make_request(self, path, **kwargs):
        """
        path - API request path
        **kwargs - query parameters
        """

        full_path = BASE_URL + path
        get_params = {
            **kwargs,
            'subscription-key': SUBSCRIPTION_KEY,
        }
        response = requests.get(full_path, params=get_params)
        return untangle.parse(response.text)

    def get_hospitals(self):
        """Returns a list of all hospitals"""
        # TODO: This API is paginated.
        response = self.make_request("hospitals/all")
        return [Hospital(entry) for entry in response.feed.entry]

    def get_hospitals_by_postcode(self, postcode, distance):
        response = self.make_request("hospitals/postcode/%s" % postcode, distance=distance)
        return [Hospital(entry) for entry in response.feed.entry]

    def get_hospitals_by_name(self, name):
        response = self.make_request("hospitals/name/%s" % name)

        if isinstance(response.feed.entry, list):
            first_result = response.feed.entry[0]
        else:
            first_result = response.feed.entry

        return Hospital(first_result)

    def get_hospital(self, id):
        response = self.make_request("hospitals/%s" % id)
        # Turn the XML tree into something useful
        return response

    def get_hospital_facilities(self, id):
        response = self.make_request("hospitals/%s/facilities" % id)
        return Facilities(response.feed.entry.content.s_facilities)