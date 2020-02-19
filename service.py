# -*- coding: utf-8 -*-
import json
import logging
import re
import xml.etree.ElementTree as ET

import boto3
import requests
from botocore.exceptions import ClientError

UNITED_STATES = "840"
JSON = "application/json"
KEY = "ita_office_locations.json"
BUCKET = "ita-office-locations"
XML_ENDPOINT = "http://emenuapps.ita.doc.gov/ePublic/GetPost?type={}"
OFFICE_TYPES = ["odo", "oio"]
RESOURCES = [XML_ENDPOINT.format(office_type) for office_type in OFFICE_TYPES]
INVALID_CITY = "European Union"
TAGS = [
    "ADDRESS",
    "POST",
    "OFFICENAME",
    "COUNTRYID",
    "STATE",
    "EMAIL",
    "FAX",
    "MAIL_INSTR",
    "PHONE",
    "POSTTYPE",
]
S3_CLIENT = boto3.client("s3")
LOCATION_REGEXP = re.compile(r"[A-Z]{2}\s+[0-9]{5}(-\d{4})*$")


def handler(event, context):
    entries = get_entries()
    response = True
    try:
        S3_CLIENT.put_object(
            Bucket=BUCKET, Key=KEY, Body=json.dumps(entries), ContentType=JSON
        )
        print(f"✅ Uploaded {KEY} file with {len(entries)} locations")
    except ClientError as e:
        logging.error(e)
        response = False
    return response


def get_entries():
    lists = [get_items(resource) for resource in RESOURCES]
    entries = [get_location(item) for sublist in lists for item in sublist]
    return entries


def get_items(url):
    print(f"Fetching XML feed of items from {url}...")
    response = requests.get(url)
    root = ET.fromstring(response.text)
    items = root.findall("POSTINFO")
    print(f"Found {len(items)} items in {url}")
    return items


def get_location(item):
    location = {tag.lower(): get_inner_text(item, tag) for tag in TAGS}
    location["country_name"] = item.find("COUNTRYID").attrib["name"]
    location["city"] = assign_city_from_address(location)
    return location


def assign_city_from_address(location):
    city = None
    if location["countryid"] == UNITED_STATES:
        city = parse_city_from_address(location["address"])
    elif location["post"] != INVALID_CITY:
        city = location["post"]
    return city


def parse_city_from_address(address_array):
    response = None
    try:
        response = next(
            city_state_zip
            for city_state_zip in address_array
            if LOCATION_REGEXP.search(city_state_zip)
        ).split(",")[::-1][1]
    except (StopIteration, IndexError, TypeError):
        pass
    return response


def get_inner_text(item, tag):
    element = item.findall(tag)
    response = None
    num_elements = len(element)
    if num_elements == 1:
        response = element[0].text
    elif num_elements > 1:
        response = [e.text for e in element]
    return response
