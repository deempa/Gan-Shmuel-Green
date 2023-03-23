import requests


ENDPOINT="http://3.76.109.165:8088"

## HEALTH TEST
def test_health():
    request=requests.get(ENDPOINT + "/health")
    assert request.status_code == 200
  

## POST PROVIDER TEST
def test_post_provider():
    payload={"name":"test"}
    request=requests.post(ENDPOINT + "/provider", json=payload)
    assert request.status_code == 200

## POST PROVIDER BAD REQUEST TEST
def test_post_provider_bad_request():
    exist_payload={"name":"test"}
    request=requests.post(ENDPOINT + "/provider", json=exist_payload)
    assert request.status_code == 400
    no_value_payload={"name":""}
    request=requests.post(ENDPOINT + "/provider", json=no_value_payload)
    assert request.status_code == 400
    not_json_payload="hello there"
    request=requests.post(ENDPOINT + "/provider", data=not_json_payload)
    assert request.status_code == 400
    bad_json_payload={"na":"test"}
    request=requests.post(ENDPOINT + "/provider", json=bad_json_payload)
    assert request.status_code == 400
    bad_method_payload={"name":"test"}
    request=requests.put(ENDPOINT + "/provider", json=bad_method_payload)
    assert request.status_code == 405

## PUT PROVIDER TEST
def test_put_provider():
    payload={"name":"test1"}
    request=requests.put(ENDPOINT + "/provider/10001", json=payload)
    assert request.status_code == 200

## PUT PROVIDER BAD REQUEST TEST
def test_put_provider_bad_request():
    bad_id_payload={"name":"test"}
    request=requests.put(ENDPOINT + "/provider/12000",json=bad_id_payload)
    assert request.status_code == 400
    no_value_payload={"name":""}
    request=requests.put(ENDPOINT + "/provider/10001",json=no_value_payload)
    assert request.status_code == 400
    not_json_payload="hello there"
    request=requests.put(ENDPOINT + "/provider/10001",data=not_json_payload)
    assert request.status_code == 400
    bad_json_payload={"ni":"test"}
    request=requests.put(ENDPOINT + "/provider/10001",json=bad_json_payload)
    assert request.status_code == 400
    bad_method_payload={"name":"test"}
    request=requests.post(ENDPOINT + "/provider/10001", json=bad_method_payload)
    assert request.status_code == 405


## GET TRUCK NO DATA TEST


## POST TRUCK TEST
def test_post_truck():
    payload={"provider":"10001", "id":"90909090"}
    request=requests.post(ENDPOINT + "/truck", json=payload)
    assert request.status_code == 200

## POST TRUCK BAD REQUEST TEST
def test_post_truck_bad_requst():
    exist_payload={"provider":"10001", "id":"90909090"}
    request=requests.post(ENDPOINT + "/truck", json=exist_payload)
    assert request.status_code == 400
    no_value_payload={"provider":"", "id":""}
    request=requests.post(ENDPOINT + "/truck", json=no_value_payload)
    assert request.status_code == 400
    not_json_payload="hello there"
    request=requests.post(ENDPOINT + "/truck", data=not_json_payload)
    assert request.status_code == 400
    bad_json_payload={"provder":"10001", "i":"80808080"}
    request=requests.post(ENDPOINT + "/truck", json=bad_json_payload)
    assert request.status_code == 400
    bad_method_payload={"provider":"10001", "id":"80808080"}
    request=requests.put(ENDPOINT + "/truck", json=bad_method_payload)
    assert request.status_code == 405

## GET TRUCK NO ID TEST

## GET TRUCK NO QUERY TEST

## GET TRUCK SEMI QUERY TEST

## GET TRUCK FULL QUERY TEST

## PUT TRUCK TEST
def test_put_truck():
    payload={"provider":"10001"}
    request=requests.put(ENDPOINT + "/truck/90909090", json=payload)
    assert request.status_code == 200

## PUT TRUCK BAD REQUEST TEST
def test_put_truck_bad_request():
    bad_id_payload={"provider":"10001"}
    request=requests.put(ENDPOINT + "/truck/1321312", json=bad_id_payload)
    assert request.status_code == 400
    no_value_payload={"provider":""}
    request=requests.put(ENDPOINT + "/truck/80909090",json=no_value_payload)
    assert request.status_code == 400
    not_json_payload="hello there"
    request=requests.put(ENDPOINT + "/truck/80909090",data=not_json_payload)
    assert request.status_code == 400
    bad_json_payload={"proder":"10001"}
    request=requests.put(ENDPOINT + "/truck/80909090",json=bad_json_payload)
    assert request.status_code == 400
    bad_method_payload={"provider":"10001"}
    request=requests.post(ENDPOINT + "/truck/80909090", json=bad_method_payload)
    assert request.status_code == 405


## GET RATES NO DATA TEST

## POST RATES TEST

## POST RATES BAD REQUEST

## POST RATES UNSUPPORTED FILE TEST

## GET RATES TEST


## GET BILL TEST
