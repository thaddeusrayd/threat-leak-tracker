import requests

def demo_requests():
    url = "https://httpbin.org/get"
    response = requests.get(url)

    print("Status Code:", response.status_code)
    print("Response Headers:", response.headers)
    print("Response Body:", response.text)

if __name__ == "__main__":
    demo_requests()