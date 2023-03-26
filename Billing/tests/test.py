import requests

#ENDPOINT="http://3.76.109.165:8088"
ENDPOINT="http://localhost:8082"

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
    long_payload={"name":"Lorem ipsum dolor sit amet, nonummy ligula volutpat hac integer nonummy. Suspendisse ultricies, congue etiam tellus, erat libero, nulla eleifend, mauris pellentesque. Suspendisse integer praesent vel, integer gravida mauris, fringilla vehicula lacinia non dfsdf sdfsdf sdf dsf sdf ds"}
    request=requests.post(ENDPOINT + "/provider", json=long_payload)
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
    assert request.status_code == 404
    long_payload={"name":"Lorem ipsum dolor sit amet, nonummy ligula volutpat hac integer nonummy. Suspendisse ultricies, congue etiam tellus, erat libero, nulla eleifend, mauris pellentesque. Suspendisse integer praesent vel, integer gravida mauris, fringilla vehicula lacinia non dfsdf sdfsdf sdf dsf sdf ds"}
    request=requests.post(ENDPOINT + "/provider", json=long_payload)
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
    long_payload={"provider":"10001","id":"123456789012" }
    request=requests.post(ENDPOINT + "/truck", json=long_payload)
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


## GET TRUCK ID NOT EXIST:
def test_truck_id():
    request=requests.get(ENDPOINT + "/truck/456.565")
    assert request.status_code == 404
    assert request.text == 'The truck id is not exist'


## GET TRUCK NO ID TEST
def test_get_truck_no_id():
    request=requests.get(ENDPOINT + "/truck")
    assert request.status_code == 405

## GET TRUCK BAD FORMS
def test_get_truck_bad_forms():
    request=requests.get(ENDPOINT + "/truck/90909090?from=202003&to=202303")
    assert request.status_code == 400
    request=requests.get(ENDPOINT + "/truck/90909090?from=2020033000&to=2019032600")
    assert request.status_code == 400
    request=requests.get(ENDPOINT + "/truck/90909090?from=3902uy3dd&to=2019yoni")
    assert request.status_code == 400
    request=requests.get(ENDPOINT + "/truck/90909090?from=202045450000&to=202103030000")
    assert request.status_code == 400


## PUT TRUCK TEST
def test_put_truck():
    payload={"provider":"10001"}
    request=requests.put(ENDPOINT + "/truck/90909090", json=payload)
    assert request.status_code == 200

## PUT TRUCK BAD REQUEST TEST
def test_put_truck_bad_request():
    bad_id_payload={"provider":"10001"}
    request=requests.put(ENDPOINT + "/truck/1321312", json=bad_id_payload)
    assert request.status_code == 404
    no_value_payload={"provider":""}
    request=requests.put(ENDPOINT + "/truck/90909090",json=no_value_payload)
    assert request.status_code == 400
    not_json_payload="hello there"
    request=requests.put(ENDPOINT + "/truck/90909090",data=not_json_payload)
    assert request.status_code == 400
    bad_json_payload={"proder":"10001"}
    request=requests.put(ENDPOINT + "/truck/90909090",json=bad_json_payload)
    assert request.status_code == 400
    bad_method_payload={"provider":"10001"}
    request=requests.post(ENDPOINT + "/truck/90909090", json=bad_method_payload)
    assert request.status_code == 405


## POST RATES TEST
# def test_post_rates():
#     payload={"file": "rates.xlsx"}
#     request=requests.post(ENDPOINT + "/rates",json=payload)
#     assert request.status_code==200

## POST RATES BAD REQUEST

## GET RATES
def test_get_rates():
    request=requests.get(ENDPOINT + "/rates")
    assert request.status_code==200


## GET BILL TEST
def test_get_bill():
    request=requests.get(ENDPOINT + "/bill/10001")
    assert request.status_code==200

