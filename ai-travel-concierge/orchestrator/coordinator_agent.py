from agents.flight_agent import FlightAgent
from agents.hotel_agent import HotelAgent
from agents.weather_agent import WeatherAgent
from agents.currency_agent import CurrencyAgent
import os
from groq import Groq

class CoordinatorAgent:
    def __init__(self):
        self.flight_agent = FlightAgent()
        self.hotel_agent = HotelAgent()
        self.weather_agent = WeatherAgent()
        self.currency_agent = CurrencyAgent()
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.llm_model = "meta-llama/llama-4-scout-17b-16e-instruct"

    def build_itinerary(self, user_preferences):
        origin = user_preferences.get('origin', 'Unknown')
        destination = user_preferences.get('destination', 'Unknown')
        departure_date = user_preferences.get('departure_date', 'N/A')
        return_date = user_preferences.get('return_date', 'N/A')
        budget = user_preferences.get('budget', 'N/A')
        currency = user_preferences.get('currency', 'USD')
        interests = user_preferences.get('interests', '')

        flight_info = self.flight_agent.get_flight_info(origin, destination, departure_date, return_date)
        hotel_info = self.hotel_agent.get_hotel_info(destination, departure_date, return_date, budget)
        weather_info = self.weather_agent.get_weather_info(destination, departure_date, return_date)
        currency_info = self.currency_agent.get_currency_info('USD', currency, budget)

        # Compose prompt for LLM
        prompt = f"""
You are a world-class travel concierge. Using the following travel details, generate a wonderful, engaging, and highly personalized journey recommendation for the user. Make it inspiring, detailed, and tailored to the user's interests.

Trip: {origin} to {destination}
Dates: {departure_date} to {return_date}
Budget: {budget} {currency}
Interests: {interests}

Flight Details:
{flight_info}

Hotel Suggestions:
{hotel_info}

Weather Forecast:
{weather_info}

Currency Exchange:
{currency_info}
"""
        # Call Groq LLM API
        try:
            client = Groq(api_key=self.groq_api_key)
            response = client.chat.completions.create(
                model=self.llm_model,
                messages=[{"role": "system", "content": "You are a helpful travel assistant."},
                          {"role": "user", "content": prompt}],
                max_tokens=1024,
                temperature=0.8
            )
            recommendation = response.choices[0].message.content.strip()
        except Exception as e:
            recommendation = f"[LLM Error: {str(e)}]"

        return recommendation