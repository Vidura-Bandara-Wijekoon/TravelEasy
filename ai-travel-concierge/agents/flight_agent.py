import os
import requests

class FlightAgent:
    def get_flight_info(self, origin, destination, departure_date, return_date=None):
        api_key = os.getenv("AVIATIONSTACK_API_KEY")
        if not api_key:
            return "AviationStack API key is missing."
        try:
            url = f"http://api.aviationstack.com/v1/flights?access_key={api_key}&dep_iata={origin}&arr_iata={destination}&flight_date={departure_date}"
            response = requests.get(url)
            data = response.json()
            if "data" not in data or not data["data"]:
                return "No flight data found for the given parameters."
            flights = data["data"][:3]  # Show up to 3 flights
            result = []
            for flight in flights:
                airline = flight.get("airline", {}).get("name", "N/A")
                flight_number = flight.get("flight", {}).get("iata", "N/A")
                dep_time = flight.get("departure", {}).get("scheduled", "N/A")
                arr_time = flight.get("arrival", {}).get("scheduled", "N/A")
                result.append(f"{airline} {flight_number}: Departs {dep_time}, Arrives {arr_time}")
            return "\n".join(result)
        except Exception as e:
            return f"Error retrieving flight data: {str(e)}"