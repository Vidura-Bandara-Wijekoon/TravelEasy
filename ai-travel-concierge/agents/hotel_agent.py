import os
import requests

class HotelAgent:
    def get_hotel_info(self, destination, check_in, check_out, budget):
        api_key = os.getenv("HOTELAPI_API_KEY")
        if not api_key:
            return "HotelAPI.co API key is missing."
        try:
            url = "https://api.makcorps.com/free"
            headers = {"Authorization": api_key}
            params = {"destination": destination, "check_in": check_in, "check_out": check_out}
            response = requests.get(url, headers=headers, params=params)
            data = response.json()
            if data.get("status") != "success" or not data.get("data"):
                return f"No hotel data found for {destination} on the given dates."
            hotels = data["data"][:3]  # Show up to 3 hotels
            result = []
            for hotel in hotels:
                name = hotel.get("hotel_name", "N/A")
                price = hotel.get("price", "N/A")
                currency = hotel.get("currency", "N/A")
                result.append(f"{name}: {price} {currency}")
            return "\n".join(result)
        except Exception as e:
            return f"Error retrieving hotel data: {str(e)}"