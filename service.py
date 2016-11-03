# -*- coding: utf-8 -*-
import json
import xml.etree.ElementTree as ET
import re

import boto3
import requests

XML_ENDPOINT = "http://emenuapps.ita.doc.gov/ePublic/GetPost?type={}"
OFFICE_TYPES = ["odo", "oio"]
RESOURCES = [XML_ENDPOINT.format(office_type) for office_type in OFFICE_TYPES]
INVALID_CITY = 'European Union'
TAGS = ['ADDRESS', 'POST', 'OFFICENAME', 'COUNTRYID', 'STATE', 'EMAIL', 'FAX', 'MAIL_INSTR', 'PHONE', 'POSTTYPE']

s3 = boto3.resource('s3')
regexp = re.compile(r'[A-Z]{2}\s+[0-9]{5}(-\d{4})*$')


def handler(event, context):
    items = get_items(RESOURCES[0]) + get_items(RESOURCES[1])
    entries = [get_location(item) for item in items]
    if len(entries) > 0:
        s3.Object('ita-office-locations', 'ita_office_locations.json').put(Body=json.dumps(entries), ContentType='application/json')
        return "Uploaded ita_office_locations.json file with %i locations" % len(entries)
    else:
        return "No entries loaded so there is no JSON file to upload"


def get_items(url):
    print "Fetching XML feed of items from {}...".format(url)
    response = requests.get(url)
    root = ET.fromstring(response.text.encode('utf-8'))
    items = root.findall('POSTINFO')
    print "Found {} items in {}".format(len(items), url)
    return items


def get_location(item):
    location = {tag.lower(): get_text(item, tag) for tag in TAGS}
    location["country_name"] = item.find("COUNTRYID").attrib['name']
    location["city"] = assign_city_from_address(location)
    return location


def assign_city_from_address(location):
    city = None
    if location["countryid"] == "840":
        city = parse_city_from_address(location["address"])
    elif location["post"] != INVALID_CITY:
        city = location["post"]
    return city


def parse_city_from_address(address_array):
    try:
        return next(city_state_zip for city_state_zip in address_array if regexp.search(city_state_zip)).split(',')[::-1][1]
    except (StopIteration, IndexError):
        return None


def get_text(item, tag):
    inner_text = get_inner_text(item, tag)
    if inner_text is None:
        return None
    elif type(inner_text) == str:
        return format_text(inner_text)
    else:
        return [format_text(inner) for inner in inner_text]


def format_text(inner_text):
    result_text = '{}'.format(inner_text)
    return result_text


def get_inner_text(item, tag):
    element = item.findall(tag)
    if len(element) == 1:
        return encode_text(element[0])
    elif len(element) == 0:
        return None
    else:
        return [encode_text(e) for e in element]


def encode_text(element):
    try:
        element_text = element.text.encode('utf8')
    except AttributeError:
        element_text = ""
    return element_text
