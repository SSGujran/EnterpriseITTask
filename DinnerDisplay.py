from flask import Flask, render_template
import pycurl
from io import BytesIO
import json

app = Flask(__name__)

def fetch_data_from_api():
    # The URL to send the request to
    url = "https://uk.api.just-eat.io/discovery/uk/restaurants/enriched/bypostcode/LS27HY"

    # Create a BytesIO object to capture the output
    buffer = BytesIO()

    # Initialize a pycurl object
    c = pycurl.Curl()

    # Set the URL
    c.setopt(c.URL, url)

    # Write the output to the BytesIO buffer
    c.setopt(c.WRITEDATA, buffer)

    # Perform the request
    c.perform()

    # Get the HTTP response code
    http_code = c.getinfo(c.RESPONSE_CODE)

    # Close the pycurl object
    c.close()

    # Get the content from the BytesIO buffer
    body = buffer.getvalue().decode('utf-8')

    # Check if it was successful
    if http_code == 200:
        data = body
        return data
    else:
        print("Error")
        print(http_code)
        return None
        

def extract_restaurant_details(restaurants):
    # Extract details of the first 10 restaurants
    restaurant_details = []
    for index, restaurant in enumerate(restaurants[:10], start=1):
        restaurant_info = {
            "name": restaurant['name'],
            "cuisine": restaurant['cuisines'][0]['name'],
            "rating": restaurant['rating'],
            "address": restaurant['address']
        }
        restaurant_details.append(restaurant_info)
    return restaurant_details

@app.route('/')
def index():
    # Fetch data from the API
    restaurant_data = fetch_data_from_api()
    
    if restaurant_data:
        # Convert the JSON string to a Python dictionary
        restaurant_data_dict = json.loads(restaurant_data)
        
        # Extract restaurant details from the response
        restaurants = restaurant_data_dict.get('restaurants', [])
        
        if restaurants:
            # Extract details of the first 10 restaurants
            restaurant_details = extract_restaurant_details(restaurants)
            return render_template('index.html', restaurant_details=restaurant_details)
    
    return "No restaurant data available"

if __name__ == "__main__":
    app.run(debug=True)
