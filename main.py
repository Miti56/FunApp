from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, Collapsible, Label, Digits, Markdown
from textual.containers import VerticalScroll
from datetime import datetime
from textual import events
import json
import httpx
from textual import work


class WeatherApp(App):
    """A Textual app to manage stopwatches."""

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]
    CSS_PATH = "weather.tcss"

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()
        # Clock
        yield Digits("", id="clock")
        # Input City
        yield Input(placeholder="Search City!")
        with VerticalScroll(id="results-container"):
            yield Markdown(id="results")
            yield Markdown(id="results2")

    def on_ready(self) -> None:
        self.update_clock()
        self.set_interval(1, self.update_clock)

    def update_clock(self) -> None:
        clock = datetime.now().time()
        self.query_one(Digits).update(f"{clock:%T}")

    def on_mount(self) -> None:
        """Called when app starts."""
        # Give the input focus, so we can start typing straight away
        self.query_one(Input).focus()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark



    #WEATHER INSTANT
    async def on_input_changed(self, message: Input.Changed) -> None:
        """A coroutine to handle a text changed message."""
        if message.value:
            self.lookup_word(message.value)
            self.lookup_5_day_forecast(message.value)
        else:
            # Clear the results
            self.query_one("#results", Markdown).update("")


    @work(exclusive=True)
    async def lookup_word(self, city_name: str) -> None:
        """Looks up a City."""
        api_key = '17690709512b5e7158c116dce76e4694'
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            try:
                results = response.json()
            except Exception:
                self.query_one("#results", Markdown).update(response.text)

        if city_name == self.query_one(Input).value:
            markdown = self.make_word_markdown(results)
            self.query_one("#results", Markdown).update(markdown)

    @work(exclusive=True)
    async def lookup_5_day_forecast(self, city_name: str) -> None:
        api_key = '17690709512b5e7158c116dce76e4694'
        url_5_day_forecast = f"http://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={api_key}"

        async with httpx.AsyncClient() as client:
            response_5_day = await client.get(url_5_day_forecast)
            try:
                forecast_data = response_5_day.json()
            except Exception:
                self.query_one("#results", Markdown).update("Error fetching 5-day forecast data.")

        if city_name == self.query_one(Input).value:
            markdown_5_day = self.make_5_day_forecast_markdown(forecast_data)
            self.query_one("#results", Markdown).update(markdown_5_day)



    # SHOW THE RESULTS
    def make_word_markdown(self, weather_data: dict) -> str:
        """Convert the weather data into markdown."""
        lines = []

        if "name" in weather_data:
            city_name = weather_data["name"]
            temperature = weather_data["main"]["temp"]
            description = weather_data["weather"][0]["description"]
            humidity = weather_data["main"]["humidity"]

            lines.append(f"# {city_name}")
            lines.append(f"Temperature: {temperature}°C")
            lines.append(f"Description: {description}")
            lines.append(f"Humidity: {humidity}%")
        else:
            lines.append("City not found. Please check the city name and try again.")

        return "\n".join(lines)

    def make_5_day_forecast_markdown(self, forecast_data: dict) -> str:
        lines = []

        if "city" in forecast_data:
            city_name = forecast_data["city"]["name"]
            lines.append(f"## 5-Day Forecast for {city_name}")

            for forecast in forecast_data["list"]:
                timestamp = forecast["dt"]
                date = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                temperature = forecast["main"]["temp"]
                description = forecast["weather"][0]["description"]
                lines.append(f"### {date}")
                lines.append(f"Temperature: {temperature}°C")
                lines.append(f"Description: {description}")
                lines.append("\n")
        else:
            lines.append("5-Day forecast not available for this city.")

        return "\n".join(lines)


if __name__ == "__main__":
    app = WeatherApp()
    app.run()
