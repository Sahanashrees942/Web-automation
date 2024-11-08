import requests


def test_get_request_status_code():
    url = "https://reqres.in/api/users/2"

    # Step 2: Make the GET request
    response = requests.get(url)

    # Step 3: Validate whether the response code is 200
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"


    print("\n \n Response JSON:\n", response.json())