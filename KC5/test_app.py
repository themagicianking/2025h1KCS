from app import get_works, get_image, submit
import requests
import json
form_data = {}


def test_get_works():
    # check that valid tag returns 200 status
    assert get_works("art")["status"] == 200
    # check that valid tag returns dict that has a "works" property
    assert get_works("art")["works"] is not None
    # check that invalid tag returns 404 status
    assert get_works("blah blah blah")["status"] == 404

def test_get_image():
    # check that valid tag returns image object
    assert get_image("art")["url"] is not None