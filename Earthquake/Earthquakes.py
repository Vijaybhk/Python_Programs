# Submitted by Vijaybhaskar Kothapally (RedID: 828583711)

# Commenting installation command required for google colab
# !pip install xmltodict

# Importing libraries
import json, xmltodict, requests, datetime, csv

def get_location(lat, long):
  """
  Function to get location using latitude and longitude from OpenCage
  :param lat: latitude of the location
  :param long: longitude of the location
  :return: county name and state name
  """
  full_url = "https://api.opencagedata.com/geocode/v1/xml?q={}+{}&key=9ab50494c510450f852cedc2bf621e76".format(float(lat), float(long))
  response2 = requests.get(full_url)
  if response2:
    # Status code 200 - connection was good
    location_data = xmltodict.parse(response2.text)
    components_data = location_data["response"]["results"]["result"]["components"]
    try:
      county_name = components_data["county"]
      state_name = components_data["state"]
    except:
      county_name = "N/A"
      state_name = "N/A"
  else:
    # Status code other than 200 - connection error
    print("Connection error")
  return county_name, state_name

def get_time_str(data, time_label):
  """
  Function to get time string from unix epoch time
  :param data: Input json data
  :param time_label: Input time label in the json data
  :return: time string
  """

  # Extract time(Unix epoch time format) from the data using time_label in the parser
  orig_time = data[time_label]

  # Convert milliseconds to seconds
  orig_time_sec = orig_time / 1000

  # Convert Unix epoch time to datetime object
  datetime_timestamp = datetime.datetime.utcfromtimestamp(orig_time_sec)

  # Subtract 7 hours to adjust for time zone difference 
  datetime_adj_timestamp = datetime_timestamp - datetime.timedelta(hours = 7)

  # Convert to human-interpretable string
  # It would say: “September 01, 2022 at 12:00:00 AM”
  time_str = datetime_adj_timestamp.strftime("%B %d, %Y at %I:%M:%S %p")
  
  return time_str

def main():
  """
  Main function to extract earthquakes information and print output and save the data to csv
  """
  response1 = requests.get("https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson")

  earthquake_data = json.loads(response1.text)

  # List to store earthquakes information
  earthquakes_list = []

  if response1:
    # Status code 200 - connection was good

    features_data = earthquake_data["features"]
    for line in features_data:
      properties_data = line["properties"]

      # Earthquake magnitude
      magnitude = properties_data["mag"]

      # Earthquake time str
      time = get_time_str(data=properties_data, time_label="time")

      # Earthquake coordinates
      geometry_data = line["geometry"]
      coordinates_data = geometry_data["coordinates"]
      longitude = coordinates_data[0]
      latitude = coordinates_data[1]

      # Earthquake location
      location = get_location(lat=latitude, long=longitude)
      county = location[0]
      state = location[1]

      # List of each earthquake properties
      earthquake_output = [time, magnitude, latitude, longitude, county, state]

      # Appends above list as list of lists to the earthquake_list
      earthquakes_list.append(earthquake_output)

      # Print output with county and state names
      if county != "N/A" and state != "N/A":
        print("Magnitude {} earthquake on {} and located at ({}, {}) in {}, {}.".format(magnitude, time, latitude, longitude, county, state))

      # Print output if there is no county and state name
      else:
        print("Magnitude {} earthquake on {} and located at ({}, {}) in the Ocean.".format(magnitude, time, latitude,
                                                                                           longitude))

    # csv writer, overwrites everytime the file is run
    with open("earthquakes.csv", "w", newline="") as opener:
      writer = csv.writer(opener)

      # Header row
      writer.writerow(["Time", "Magnitude", "Latitude", "Longitude", "County", "State"])

      # Writes all rows to the csv using the earthquakes_list(list of lists)
      writer.writerows(earthquakes_list)

  else:
    # Status code other than 200 - connection error
    print("Connection error")

  return


if __name__ == "__main__":
  main()