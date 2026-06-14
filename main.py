import json
import requests
import os
from dotenv import load_dotenv

# ================= CONFIG =================

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5"
HISTORY_FILE = "history.json"

AQI_ADVISORY = {
    1: ("Good", "Air quality is satisfactory."),
    2: ("Fair", "Air quality is acceptable."),
    3: ("Moderate", "Sensitive individuals should reduce outdoor activity."),
    4: ("Poor", "Reduce prolonged outdoor exertion."),
    5: ("Very Poor", "Avoid outdoor activities if possible.")
}


# ================= DISPLAY =================

def header():
    print()
    print("=" * 50)
    print("\t\tWEATHER APP")
    print("=" * 50)


# ================= HISTORY =================

def load_history():
    try:
        with open(HISTORY_FILE, "r") as file:
            return json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_history(api_data):
    history = load_history()

    history.append(api_data)

    # Keep only last 5 searches
    history = history[-5:]

    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)


def history_fn():

    data = load_history()

    if not data:
        print("\nNo history found.\n")
        return

    print("\n" + "=" * 57)
    print(f"{'City':<10}{'Temp(°C)':<10}{'Humidity(%)':<13}{'Wind Speed(km/h)':<20}{'AQI':<7}")
    print("=" * 57)

    for item in data:
        print(
            f"{item['city']:<11}"
            f"{item['temp']:<13}"
            f"{item['humidity']:<14}"
            f"{item['wind_speed']:<16}"
            f"{item['aqi']:<7}"
        )

    print("=" * 57)


def last_search():

    history = load_history()

    if not history:
        return

    last = history[-1]

    print("Last Search:")
    print(
        f"{last['city']} | "
        f"{last['temp']}°C | "
        f"{last['humidity']}% | "
        f"{last['wind_speed']} km/h | "
        f"AQI {last['aqi']} | "
        f"{last['condition']}"
    )


# ================= API =================

def weather_fn(city):

    weather_url = (
        f"{BASE_URL}/weather"
        f"?q={city}&appid={API_KEY}&units=metric"
    )

    try:
        response = requests.get(weather_url, timeout=10)
        response.raise_for_status()
        data_py = response.json()

    except requests.exceptions.RequestException:
        print("Unable to connect to the weather service.")
        return None

    temp = data_py.get("main", {}).get("temp", "N/A")
    feel_like = data_py.get("main", {}).get("feels_like", "N/A")
    humidity = data_py.get("main", {}).get("humidity", "N/A")
    condition = data_py.get("weather", [{}])[0].get("description", "N/A")
    wind_speed = data_py.get("wind", {}).get("speed", "N/A")

    lat = data_py["coord"]["lat"]
    lon = data_py["coord"]["lon"]

    aqi_url = (
        f"{BASE_URL}/air_pollution"
        f"?lat={lat}&lon={lon}&appid={API_KEY}"
    )

    try:
        response2 = requests.get(aqi_url, timeout=10)
        response2.raise_for_status()
        data_aqi = response2.json()

    except requests.exceptions.RequestException:
        print("Unable to fetch AQI data.")
        return None

    aqi = data_aqi["list"][0]["main"]["aqi"]

    status, advisory = AQI_ADVISORY.get(
        aqi,
        ("Unknown", "No advisory available.")
    )

    api_data = {
        "city": data_py["name"],
        "temp": temp,
        "humidity": humidity,
        "wind_speed": wind_speed,
        "condition": condition,
        "aqi": aqi
    }

    save_history(api_data)

    return {
        "temp": temp,
        "feel_like": feel_like,
        "humidity": humidity,
        "condition": condition,
        "wind_speed": wind_speed,
        "aqi": aqi,
        "status": status,
        "advisory": advisory
    }


# ================= OUTPUT =================

def print_weather_fn(city, data):

    print()
    print(f"Weather in {city}")
    print(f"Temp : {data['temp']}°C (Feels like {data['feel_like']}°C)")
    print(f"Humidity : {data['humidity']}%")
    print(f"Condition : {data['condition']}")
    print(f"Wind Speed : {data['wind_speed']} km/h")
    print(f"Air Quality Index: {data['aqi']} — {data['status']}")
    print(f"Advisory: {data['advisory']}")
    print()


# ================= MAIN =================

def main():

    if not API_KEY:
        print("OPENWEATHER_API_KEY not found in .env file.")
        return

    while True:

        header()
        last_search()
        print()

        city = input(
            "Enter city name ('history' to view history, Enter to exit): "
        ).strip()

        if city == "":
            print("Goodbye!")
            break

        if city.lower() == "history":
            history_fn()
            input("\nPress Enter to continue...")
            continue

        result = weather_fn(city)

        if result:
            print_weather_fn(city, result)

            input("Press Enter to continue...")


if __name__ == "__main__":
    main()