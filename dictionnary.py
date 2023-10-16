from __future__ import annotations
import httpx
import json


from textual import work
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Input, Markdown


class DictionaryApp(App):
    """Searches ab dictionary API as-you-type."""

    CSS_PATH = "dictionnary.tcss"

    def compose(self) -> ComposeResult:
        yield Input(placeholder="Search for a word")
        with VerticalScroll(id="results-container"):
            yield Markdown(id="results")

    def on_mount(self) -> None:
        """Called when app starts."""
        # Give the input focus, so we can start typing straight away
        self.query_one(Input).focus()

    async def on_input_changed(self, message: Input.Changed) -> None:
        """A coroutine to handle a text changed message."""
        if message.value:
            self.lookup_word(message.value)
        else:
            # Clear the results
            self.query_one("#results", Markdown).update("")

    @work(exclusive=True)
    async def lookup_word(self, word: str) -> None:
        """Looks up a word."""
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            try:
                results = response.json()
            except Exception:
                self.query_one("#results", Markdown).update(response.text)

        if word == self.query_one(Input).value:
            markdown = self.make_word_markdown(results)
            self.query_one("#results", Markdown).update(markdown)

    def make_word_markdown(self, results: object) -> str:
        """Convert the weather data into markdown."""
        lines = []

        if isinstance(results, dict):
            city_name = results.get("name", "City not found")
            temperature = results.get("main", {}).get("temp", "N/A")
            description = results.get("weather", [{}])[0].get("description", "N/A")
            humidity = results.get("main", {}).get("humidity", "N/A")

            lines.append(f"# Weather for {city_name}")
            lines.append(f"Temperature: {temperature}°C")
            lines.append(f"Description: {description}")
            lines.append(f"Humidity: {humidity}%")
        else:
            lines.append("City not found. Please check the city name and try again.")

        return "\n".join(lines)


if __name__ == "__main__":
    app = DictionaryApp()
    app.run()