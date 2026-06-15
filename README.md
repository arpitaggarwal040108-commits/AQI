# Weather & AQI App

A simple Python command-line utility that shows weather and air quality information for a city.

## Features

- Fetches current weather from OpenWeatherMap
- Displays temperature, humidity, wind speed, and weather condition
- Fetches Air Quality Index (AQI) data for the city
- Stores last 5 searches in `history.json`
- Supports viewing search history from the command line

## Setup

1. Create a Python virtual environment:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and add your OpenWeather API key:
   ```text
   OPENWEATHER_API_KEY=YOUR_API_KEY_HERE
   ```

## Usage

Run the app:

```powershell
python main.py
```

Enter a city name when prompted. Type `history` to view the latest search history, or press Enter to exit.

## Requirements

- Python 3.10+
- `requests`
- `python-dotenv`

## Notes

- The app saves the last 5 searches to `history.json`.
- Make sure `.env` is not committed to version control.

