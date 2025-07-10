
import requests
import hashlib
import json
import time
from datetime import datetime
from typing import Dict, Any, Optional

class AstronomicalDataFetcher:
    """
    Класс для получения астрономических данных из различных источников
    """
    
    def __init__(self):
        self.sources = {
            "iss": "http://api.open-notify.org/iss-now.json",
            "solar": "https://services.swpc.noaa.gov/json/goes/primary/integral-protons-1-day.json"
        }
        self.timeout = 10
        self.last_fetch_time = None
        self.cached_data = {}
    
    def fetch_iss_position(self) -> Optional[Dict[str, Any]]:
        """Получает текущую позицию МКС"""
        try:
            response = requests.get(self.sources["iss"], timeout=self.timeout)
            if response.status_code == 200:
                data = response.json()
                return {
                    "latitude": float(data["iss_position"]["latitude"]),
                    "longitude": float(data["iss_position"]["longitude"]),
                    "timestamp": data["timestamp"]
                }
        except Exception as e:
            print(f"Error fetching ISS position: {e}")
        return None
    
    def fetch_solar_activity(self) -> Optional[Dict[str, Any]]:
        """Получает данные солнечной активности"""
        try:
            response = requests.get(self.sources["solar"], timeout=self.timeout)
            if response.status_code == 200:
                data = response.json()
                # Берем последнее измерение
                if data and len(data) > 0:
                    latest = data[-1]
                    return {
                        "flux": latest.get("flux", 0),
                        "energy": latest.get("energy", "unknown"),
                        "time_tag": latest.get("time_tag", ""),
                        "satellite": latest.get("satellite", 0)
                    }
        except Exception as e:
            print(f"Error fetching solar activity: {e}")
        return None
    
    def get_astronomical_snapshot(self) -> Dict[str, Any]:
        """Получает снимок всех астрономических данных"""
        current_time = datetime.utcnow()
        
        snapshot = {
            "timestamp": current_time.isoformat(),
            "sources": {}
        }
        
        # Получаем данные МКС
        iss_data = self.fetch_iss_position()
        if iss_data:
            snapshot["sources"]["iss"] = iss_data
        
        # Получаем солнечную активность
        solar_data = self.fetch_solar_activity()
        if solar_data:
            snapshot["sources"]["solar"] = solar_data
        
        # Сохраняем кеш
        self.cached_data = snapshot
        self.last_fetch_time = current_time
        
        return snapshot
    
    def generate_astronomical_hash(self, snapshot: Dict[str, Any]) -> str:
        """Генерирует хеш от астрономических данных"""
        # Создаем строку для хеширования
        hash_data = []
        
        if "iss" in snapshot["sources"]:
            iss = snapshot["sources"]["iss"]
            hash_data.append(f"iss_{iss['latitude']}_{iss['longitude']}")
        
        if "solar" in snapshot["sources"]:
            solar = snapshot["sources"]["solar"]
            hash_data.append(f"solar_{solar['flux']}_{solar['satellite']}")
        
        hash_data.append(snapshot["timestamp"])
        
        # Объединяем и хешируем
        hash_string = "_".join(map(str, hash_data))
        return hashlib.sha256(hash_string.encode()).hexdigest()

# Тестируем класс
if __name__ == "__main__":
    fetcher = AstronomicalDataFetcher()
    snapshot = fetcher.get_astronomical_snapshot()
    astronomical_hash = fetcher.generate_astronomical_hash(snapshot)
    
    print("=== ASTRONOMICAL SNAPSHOT ===")
    print(json.dumps(snapshot, indent=2))
    print(f"\n=== ASTRONOMICAL HASH ===")
    print(f"Hash: {astronomical_hash}")
