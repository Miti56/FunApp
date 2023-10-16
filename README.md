# WeatherApp

**WeatherApp** is a command-line application that allows you to look up current weather and 5-day weather forecasts for a city. It is built using the [Textual](https://pypi.org/project/textual/) module, which enables you to display detailed information in the command line.

## Screenshots

### Home Screen 
![Current Weather](Screenshot 2023-10-16 at 20.20.34.png)

### 5-Day Forecast
![5-Day Forecast](Screenshot 2023-10-16 at 20.20.41.png)

### 5-Day Forecast
![5-Day Forecast](Screenshot 2023-10-16 at 20.21.01.png)

## Features

- Real-time current weather information for a city.
- 5-day weather forecast for a city.

## Installation

To run the WeatherApp, you need to have Python installed. You can install the required dependencies using pip:

```bash
pip install textual httpx
```

## Usage

Run the WeatherApp by executing the following command:
```bash
python your_weather_app.py
```

1) Enter the name of a city in the provided input field and press Enter.

2) The app will display both the current weather information and the 5-day weather forecast for the entered city.

3) To toggle dark mode, press "d" (as specified in the bindings).

## Acknowledgments

The Weather data is fetched from the OpenWeatherMap API.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
 
