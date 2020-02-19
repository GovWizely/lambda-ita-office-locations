import vcr

from service import get_entries


@vcr.use_cassette()
def test_get_entries():
    """Reads from the `test_get_entries` cassette and processes the entries. Tests that multiple
    entries get read correctly.

    """
    entries = get_entries()
    assert len(entries) == 236
    expected_entry = {
        "address": [
            "Northern Nevada Export Assistance Center",
            "704 W. Nye Lane, Suite 201",
            "Reno, NV 89703",
            "http://www.export.gov/nevada/reno",
        ],
        "post": "Reno",
        "officename": "Reno U.S. Export Assistance Center",
        "countryid": "840",
        "state": "NV",
        "email": "janis.kalnins@trade.gov",
        "fax": None,
        "mail_instr": None,
        "phone": "775-301-0037",
        "posttype": "D",
        "country_name": "United States",
        "city": "Reno",
    }
    assert entries[0] == expected_entry
