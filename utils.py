import requests
from config import Config
from datetime import datetime

def get_weather(location):
    """
    Fetch real-time weather data for a given location using OpenWeatherMap API.
    """
    api_key = Config.WEATHER_API_KEY
    city = f"{location},IN"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Raise exception for 4XX/5XX
        data = response.json()
        
        weather = {
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "icon": data["weather"][0]["icon"],
            "date": datetime.utcfromtimestamp(data["dt"]).strftime('%Y-%m-%d %H:%M:%S')
        }
        return weather

    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error: {err}")
        print("Check your API key or location name.")
        return None
    except requests.exceptions.RequestException as err:
        print(f"Request Error: {err}")
        print("Check your internet connection or URL.")
        return None


def recommend_crops(season, soil_type, weather_conditions=None):
    """
    Recommend crops based on season.
    """
    recommendations = {
        "summer": ["Rice", "Maize", "Cotton"],
        "winter": ["Wheat", "Barley", "Mustard"],
        "monsoon": ["Paddy", "Sugarcane", "Soybean"]
    }
    return recommendations.get(season.lower(), ["Millets", "Pulses"])


def fertilizer_guidance(crop):
    """
    Provide fertilizer guidance for a given crop.
    """
    guidance = {
        "Rice": "Use Nitrogen rich fertilizers like Urea and apply in three splits.",
        "Wheat": "Apply Phosphorus and Potassium rich fertilizers before sowing.",
        "Maize": "Balanced NPK fertilizers recommended; soil test advised.",
        "Cotton": "Apply nitrogen and micronutrients as per growth stage.",
        "Barley": "Use organic manure and balanced NPK fertilizers.",
        "Mustard": "Apply nitrogen at sowing and top dressing during growth.",
        "Paddy": "Apply nitrogen, phosphorus and potassium in recommended doses.",
        "Sugarcane": "Use nitrogenous fertilizers and micronutrients carefully.",
        "Soybean": "Inoculate seeds with Rhizobium and apply phosphorus fertilizers.",
        "Millets": "Apply nitrogen and phosphorus depending on soil test.",
        "Pulses": "Minimal nitrogen fertilizer; phosphorus and potassium applied."
    }
    return guidance.get(crop, "Follow local agricultural guidelines for fertilizer use.")


def pest_control_guidance(crop):
    """
    Provide pest control guidance for a given crop.
    """
    guidance = {
        "Rice": "Use Tricyclazole fungicide; monitor for stem borer and leaf folder.",
        "Wheat": "Use fungicides for rust; monitor aphids and armyworm.",
        "Maize": "Monitor for stem borer; use pheromone traps and biopesticides.",
        "Cotton": "Control bollworm with Bt cotton or insecticides; monitor aphids.",
        "Barley": "Use fungicides for powdery mildew; monitor aphids.",
        "Mustard": "Control aphids and white rust with insecticides and fungicides.",
        "Paddy": "Regular scouting; use biocontrol agents for pests.",
        "Sugarcane": "Control white grub and borers with crop rotation and insecticides.",
        "Soybean": "Monitor for aphids and pod borers; use neem-based products.",
        "Millets": "Control shoot fly and stem borer with seed treatment and insecticides.",
        "Pulses": "Use resistant varieties and appropriate insecticides for pod borers."
    }
    return guidance.get(crop, "Consult local agricultural extension services for pest control.")


def get_season():
    """
    Determine current season in India based on month.
    """
    month = datetime.now().month
    if month in [3, 4, 5, 6]:
        return "summer"
    elif month in [10, 11, 12, 1, 2]:
        return "winter"
    else:
        return "monsoon"


def translate_text(text_key, lang_code, lang_data):
    """
    Translate text using loaded JSON language data.
    """
    return lang_data.get(text_key, text_key)
