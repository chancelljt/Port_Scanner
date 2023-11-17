import requests
import folium

def get_ip_geolocation(ip_address):
    url = f"https://ipinfo.io/{ip_address}/json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Failed to fetch geolocation data for IP: {ip_address}")
        return None

def main():
    ip_address = input("Enter an IP address: ")
    geolocation_data = get_ip_geolocation(ip_address)
    
    if geolocation_data:
        location = geolocation_data.get("loc")
        if location:
            latitude, longitude = location.split(",")
            country = geolocation_data.get("country")
            city = geolocation_data.get("city")
            isp = geolocation_data.get("org", "Unknown ISP")
            
            print(f"IP Address: {ip_address}")
            print(f"Location: {city}, {country}")
            print(f"ISP: {isp}")
            
            # Create a map with the IP address location
            map_osm = folium.Map(location=[float(latitude), float(longitude)], zoom_start=10)
            folium.Marker([float(latitude), float(longitude)], popup=f"{city}, {country}, ISP: {isp}").add_to(map_osm)
            map_osm.save("ip_geolocation_map.html")
            print("Map saved to 'ip_geolocation_map.html'")
        else:
            print(f"Geolocation data not available for IP: {ip_address}")
    else:
        print(f"Failed to fetch geolocation data for IP: {ip_address}")

if __name__ == "__main__":
    main()