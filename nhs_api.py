import requests
import xml.etree.ElementTree as ET
import untangle

SUBSCRIPTION_KEY = "03a679cfd7e44542877f1b264d8565ec"
BASE_URL = "https://api.nhs.uk/data/"

# hospitals/postcode/LS74QH/?distance=10&subscription-key=03a679cfd7e44542877f1b264d8565ec"

class BadResponseException(Exception):
    pass

class Hospital():

    id = None
    title = None
    phone_number = None
    star_rating = None
    number_of_ratings = None

    def __init__(self, raw_data, data_type="entry"):
        self.raw_data = raw_data

        if data_type == "entry":
            self.parse_entry()
        else:
            self.parse_organisation()

    def parse_entry(self):
        self.id = self.raw_data.id.cdata.split("/")[-1]
        self.title = self.raw_data.title.cdata
        summary = self.raw_data.content.s_organisationSummary
        if 's_contact' in summary:
            if 's_telephone' in summary.s_contact:
                self.phone_number = self.raw_data.content.s_organisationSummary.s_contact.s_telephone.cdata

    def parse_organisation(self):
        self.id = self.raw_data.OrganisationId.cdata
        self.title = self.raw_data.Name.cdata
        self.phone_number = self.raw_data.Telephone.cdata
        self.star_rating = float(self.raw_data.FiveStarRecommendationRating.Value.cdata)
        self.number_of_ratings = int(self.raw_data.FiveStarRecommendationRating.NumberOfRatings.cdata)

class Facilities():

    parking_summary = None
    parking = None
    disabled_parking = None
    cycle_parking = None

    has_cafe = None
    has_shop = None
    has_pharmacy = None

    def __init__(self, raw_data):
        self.raw_data = raw_data

        try:
            facility_groups = raw_data.s_facilityGroups.s_facilityGroup
            facility_groups = [(group.s_name.cdata, group) for group in facility_groups]
        except AttributeError:
            return

        for (name, group) in facility_groups:
            if name == 'Parking':
                self.extract_parking(group)
            elif name == 'Food and amenities on-site':
                self.extract_food(group)

    def extract_value(self, facility):
        if facility.s_facilityExists.cdata == 'Yes':
            return True
        elif facility.s_facilityExists.cdata == 'No':
            return False
        else:
            return None

    def extract_parking(self, facility_group):
        if hasattr(facility_group, 's_summaryText'):
            self.parking_summary = facility_group.s_summaryText.cdata
        facilities = facility_group.s_facilityList.s_facility
        for facility in facilities:
            name = facility.s_name.cdata
            if name == 'Car Parking':
                self.parking = self.extract_value(facility)
            elif name == 'Disabled parking':
                self.disabled_parking = self.extract_value(facility)
            elif name == 'Cycle parking':
                self.cycle_parking = self.extract_value(facility)

    def extract_food(self, facility_group):
        facilities = facility_group.s_facilityList.s_facility
        for facility in facilities:
            name = facility.s_name.cdata
            if name == 'Cafe':
                self.has_cafe = self.extract_value(facility)
            elif name == 'Shop':
                self.has_shop = self.extract_value(facility)
            elif name == 'Pharmacy':
                self.has_pharmacy = self.extract_value(facility)


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
        if response.status_code != 200:
            raise BadResponseException("Received a non-200 response code: %s" % response.status_code)
        return untangle.parse(response.text)

    def get_hospitals(self):
        """Returns a list of all hospitals"""
        # TODO: This API is paginated.
        response = self.make_request("hospitals/all")
        return [Hospital(entry) for entry in response.feed.entry]

    def get_hospitals_by_postcode(self, postcode, distance):
        response = self.make_request("hospitals/postcode/%s" % postcode, distance=distance)
        return [Hospital(entry) for entry in response.feed.entry]

    def get_hospital_by_name(self, name):
        try:
            response = self.make_request("hospitals/name/%s" % name)
        except BadResponseException:
            return None

        if isinstance(response.feed.entry, list):
            first_result = response.feed.entry[0]
        else:
            first_result = response.feed.entry

        return Hospital(first_result)

    def get_nearest_hospital(self, location):
        try:
            response = self.make_request("hospitals/location", latitude=51.525536, longitude=-0.088230, distance=20)
        except BadResponseException:
            return None

        if isinstance(response.feed.entry, list):
            first_result = response.feed.entry[0]
        else:
            first_result = response.feed.entry

        return Hospital(first_result)

    def get_hospital_by_id(self, id):
        response = self.make_request("hospitals/%s" % id)
        return Hospital(response.Organisation, data_type="organisation")

    def get_hospital_by_ods_code(self, ods_code):
        response = self.make_request("hospitals/odscode/%s" % ods_code)
        return Hospital(response.Organisation, data_type="organisation")

    def get_hospital_facilities(self, id):
        response = self.make_request("hospitals/%s/facilities" % id)
        return Facilities(response.feed.entry.content.s_facilities)