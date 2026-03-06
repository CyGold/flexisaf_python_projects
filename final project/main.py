"""
 Weather Tracker
API        — Open-Meteo (free, no key needed)
Database   — SQLite with full CRUD operations
"""

import sqlite3
import urllib.request
import json
from datetime import datetime

class WeatherRecord:
    """Represents a single weather data snapshot."""

    def __init__(self, city: str, temperature: float, windspeed: float,
                 condition: str, timestamp: str = None):
        self.city        = city
        self.temperature = temperature
        self.windspeed   = windspeed
        self.condition   = condition
        self.timestamp   = timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __repr__(self):
        return (f"WeatherRecord(city={self.city!r}, "
                f"temp={self.temperature}°C, "
                f"wind={self.windspeed} km/h, "
                f"condition={self.condition!r})")

    def summary(self):
        return (f"  City       : {self.city}\n"
                f"   Temperature: {self.temperature}°C\n"
                f"  Wind Speed : {self.windspeed} km/h\n"
                f"   Condition  : {self.condition}\n"
                f"   Recorded   : {self.timestamp}")


#  API
class WeatherAPI:
    """
    Fetches live weather from Open-Meteo API.
    Docs: https://open-meteo.com/
    """

    # Preset coordinates for demo cities
    CITIES = {
        "Lagos":   (6.5244, 3.3792),
        "London":  (51.5074, -0.1278),
        "Abuja":   (9.0765, 7.3986),
        "New York": (40.7128, -74.0060),
        "Paris":   (48.8566, 2.3522),
    }

    WMO_CODES = {
        0: "Clear Sky", 1: "Mainly Clear", 2: "Partly Cloudy",
        3: "Overcast", 45: "Foggy", 48: "Icy Fog",
        51: "Light Drizzle", 61: "Slight Rain", 63: "Moderate Rain",
        71: "Slight Snow", 80: "Rain Showers", 95: "Thunderstorm",
    }

    def fetch(self, city: str) -> WeatherRecord:
        """Fetch current weather for a city and return a WeatherRecord."""
        if city not in self.CITIES:
            raise ValueError(f"City '{city}' not found. Available: {list(self.CITIES)}")

        lat, lon = self.CITIES[city]
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            f"&current_weather=true"
        )

        print(f"  Fetching weather for {city}...")
        try:
            with urllib.request.urlopen(url, timeout=8) as response:
                data = json.loads(response.read())

            cw = data["current_weather"]
            condition = self.WMO_CODES.get(int(cw["weathercode"]), "Unknown")

            return WeatherRecord(
                city=city,
                temperature=cw["temperature"],
                windspeed=cw["windspeed"],
                condition=condition,
            )
        except Exception as e:
            raise ConnectionError(f"API request failed: {e}")



#  DATABASE

class WeatherDB:
    """Handles all SQLite database operations."""

    def __init__(self, db_path: str = "weather.db"):
        self.db_path = db_path
        self._init_db()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        """Create table if it doesn't exist."""
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS weather_records (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    city        TEXT    NOT NULL,
                    temperature REAL    NOT NULL,
                    windspeed   REAL    NOT NULL,
                    condition   TEXT    NOT NULL,
                    timestamp   TEXT    NOT NULL
                )
            """)
        print("   Database ready (weather.db)")

    # CREATE
    def save(self, record: WeatherRecord) -> int:
        """Insert a WeatherRecord and return its new ID."""
        with self._connect() as conn:
            cursor = conn.execute(
                "INSERT INTO weather_records (city, temperature, windspeed, condition, timestamp) "
                "VALUES (?, ?, ?, ?, ?)",
                (record.city, record.temperature, record.windspeed,
                 record.condition, record.timestamp)
            )
            return cursor.lastrowid

    # READ — all records for a city
    def get_by_city(self, city: str) -> list[WeatherRecord]:
        """Fetch all saved records for a given city."""
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT city, temperature, windspeed, condition, timestamp "
                "FROM weather_records WHERE city = ? ORDER BY timestamp DESC",
                (city,)
            ).fetchall()
        return [WeatherRecord(*row) for row in rows]

    # READ — all records
    def get_all(self) -> list[WeatherRecord]:
        """Fetch every saved record."""
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT city, temperature, windspeed, condition, timestamp "
                "FROM weather_records ORDER BY timestamp DESC"
            ).fetchall()
        return [WeatherRecord(*row) for row in rows]

    # READ — city stats
    def get_stats(self, city: str) -> dict:
        """Return min/max/avg temperature for a city."""
        with self._connect() as conn:
            row = conn.execute(
                "SELECT COUNT(*), MIN(temperature), MAX(temperature), AVG(temperature) "
                "FROM weather_records WHERE city = ?",
                (city,)
            ).fetchone()
        if not row or row[0] == 0:
            return None
        return {"count": row[0], "min": row[1], "max": row[2], "avg": round(row[3], 2)}

    # DELETE
    def delete_city(self, city: str) -> int:
        """Delete all records for a city. Returns rows deleted."""
        with self._connect() as conn:
            cursor = conn.execute(
                "DELETE FROM weather_records WHERE city = ?", (city,)
            )
            return cursor.rowcount



# SERVICE — WeatherTracker

class WeatherTracker:
    """
    High-level service combining API + DB.
    Demonstrates composition: uses WeatherAPI and WeatherDB together.
    """

    def __init__(self):
        self.api = WeatherAPI()
        self.db  = WeatherDB()

    def track(self, city: str):
        """Fetch weather from API and persist it to DB."""
        record = self.api.fetch(city)
        record_id = self.db.save(record)
        print(f"  Saved to DB with ID #{record_id}")
        return record

    def history(self, city: str):
        """Print all saved records for a city."""
        records = self.db.get_by_city(city)
        if not records:
            print(f"  ⚠  No records found for '{city}'.")
            return
        print(f"\n   {len(records)} record(s) for {city}:")
        for r in records:
            print(f"    [{r.timestamp}] {r.temperature}°C | {r.windspeed} km/h | {r.condition}")

    def stats(self, city: str):
        """Print temperature statistics for a city."""
        s = self.db.get_stats(city)
        if not s:
            print(f"    No data for '{city}'.")
            return
        print(f"\n   Stats for {city} ({s['count']} records):")
        print(f"    Min: {s['min']}°C  |  Max: {s['max']}°C  |  Avg: {s['avg']}°C")


#  MAIN — Demo Run

def main():
    print("\n" + "="*55)
    print("  🌤️   WEATHER TRACKER  —  OOP + API + SQLite")
    print("="*55)

    tracker = WeatherTracker()

    # ── Track multiple cities ──
    cities_to_track = ["Lagos", "London", "Abuja"]
    print(f"\n{'─'*55}")
    print("   STEP 1: Fetch & Save Weather ")
    print(f"{'─'*55}")

    records = []
    for city in cities_to_track:
        try:
            record = tracker.track(city)
            records.append(record)
            print(record.summary())
            print()
        except Exception as e:
            print(f"   Error for {city}: {e}\n")

    # ── Show history for one city ──
    print(f"\n{'─'*55}")
    print("   STEP 2: Query History from DB")
    print(f"{'─'*55}")
    tracker.history("London")

    # ── Show stats ──
    print(f"\n{'─'*55}")
    print("   STEP 3: Aggregate Stats from DB")
    print(f"{'─'*55}")
    for city in cities_to_track:
        tracker.stats(city)

    # ── Show all records ──
    print(f"\n{'─'*55}")
    print("   STEP 4: All Records in DB")
    print(f"{'─'*55}")
    all_records = tracker.db.get_all()
    print(f"  Total records stored: {len(all_records)}")
    for r in all_records:
        print(f"    • {r.city:<10} {r.temperature}°C  {r.timestamp}")

    print(f"\n{'='*55}")
    print("   Done! Data saved to weather.db")
    print("="*55 + "\n")


if __name__ == "__main__":
    main()