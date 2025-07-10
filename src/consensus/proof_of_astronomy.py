
import time
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List

class ProofOfAstronomy:
    """
    Консенсус-алгоритм на основе астрономических данных
    """
    
    def __init__(self, block_interval_minutes: int = 10):
        self.block_interval = timedelta(minutes=block_interval_minutes)
        self.last_block_time = None
        self.difficulty_target = "0000"  # Начальная сложность
        self.node_id = hashlib.sha256(str(time.time()).encode()).hexdigest()[:16]
    
    def is_time_for_new_block(self, last_block_timestamp: str) -> bool:
        """Проверяет, пора ли создавать новый блок"""
        if not last_block_timestamp:
            return True
        
        try:
            last_time = datetime.fromisoformat(last_block_timestamp.replace('Z', '+00:00').replace('+00:00', ''))
            current_time = datetime.utcnow()
            return (current_time - last_time) >= self.block_interval
        except:
            return True
    
    def calculate_astronomical_consensus(self, astronomical_data: Dict[str, Any]) -> str:
        """
        Вычисляет консенсус-хеш на основе астрономических данных
        Этот хеш определяет, кто может создать блок
        """
        consensus_components = []
        
        # Добавляем данные МКС
        if "iss" in astronomical_data.get("sources", {}):
            iss = astronomical_data["sources"]["iss"]
            # Округляем координаты для стабильности
            lat_rounded = round(float(iss["latitude"]), 2)
            lon_rounded = round(float(iss["longitude"]), 2)
            consensus_components.append(f"iss_{lat_rounded}_{lon_rounded}")
        
        # Добавляем солнечную активность
        if "solar" in astronomical_data.get("sources", {}):
            solar = astronomical_data["sources"]["solar"]
            flux_rounded = round(float(solar["flux"]), 4)
            consensus_components.append(f"solar_{flux_rounded}")
        
        # Добавляем временную метку (округленную до минут)
        timestamp = astronomical_data.get("timestamp", "")
        if timestamp:
            try:
                dt = datetime.fromisoformat(timestamp.replace('Z', ''))
                # Округляем до 10-минутных интервалов
                minutes_rounded = (dt.minute // 10) * 10
                time_rounded = dt.replace(minute=minutes_rounded, second=0, microsecond=0)
                consensus_components.append(f"time_{time_rounded.isoformat()}")
            except:
                consensus_components.append(f"time_{timestamp}")
        
        # Создаем консенсус-строку
        consensus_string = "_".join(consensus_components)
        
        # Хешируем
        consensus_hash = hashlib.sha256(consensus_string.encode()).hexdigest()
        
        return consensus_hash
    
    def can_create_block(self, consensus_hash: str, node_id: str) -> bool:
        """
        Определяет, может ли данный узел создать блок
        на основе астрономического консенсуса
        """
        # Комбинируем консенсус-хеш с ID узла
        node_hash = hashlib.sha256(f"{consensus_hash}_{node_id}".encode()).hexdigest()
        
        # Проверяем, начинается ли хеш с определенного количества нулей
        return node_hash.startswith(self.difficulty_target)
    
    def find_valid_nonce(self, consensus_hash: str, max_attempts: int = 100000) -> Optional[int]:
        """
        Ищет nonce, который позволит создать блок
        (упрощенная версия майнинга)
        """
        for nonce in range(max_attempts):
            candidate_hash = hashlib.sha256(f"{consensus_hash}_{self.node_id}_{nonce}".encode()).hexdigest()
            
            if candidate_hash.startswith(self.difficulty_target):
                return nonce
        
        return None
    
    def validate_astronomical_block(self, block_data: Dict[str, Any]) -> bool:
        """
        Проверяет валидность блока с астрономическими данными
        """
        try:
            # Проверяем наличие астрономических данных
            if "astronomical_data" not in block_data:
                return False
            
            astronomical_data = block_data["astronomical_data"]
            
            # Пересчитываем консенсус-хеш
            recalculated_consensus = self.calculate_astronomical_consensus(astronomical_data)
            
            # Проверяем, совпадает ли с заявленным
            claimed_hash = astronomical_data.get("astronomical_hash", "")
            if recalculated_consensus != claimed_hash:
                return False
            
            return True
            
        except Exception as e:
            print(f"Error validating astronomical block: {e}")
            return False
    
    def get_consensus_info(self) -> Dict[str, Any]:
        """Возвращает информацию о консенсусе"""
        return {
            "algorithm": "Proof of Astronomy (PoA)",
            "block_interval_minutes": self.block_interval.total_seconds() / 60,
            "difficulty_target": self.difficulty_target,
            "node_id": self.node_id
        }


# Тестирование консенсус-движка
if __name__ == "__main__":
    print("=== TESTING ASTRONOMICAL CONSENSUS ===")
    
    # Симулируем астрономические данные
    test_astronomical_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "sources": {
            "iss": {"latitude": 36.39, "longitude": 173.77},
            "solar": {"flux": 0.1826}
        }
    }
    
    # Тестируем консенсус
    consensus = ProofOfAstronomy()
    consensus_hash = consensus.calculate_astronomical_consensus(test_astronomical_data)
    
    print(f"Astronomical data: {test_astronomical_data}")
    print(f"Consensus hash: {consensus_hash}")
    print(f"Node ID: {consensus.node_id}")
    print(f"Can create block: {consensus.can_create_block(consensus_hash, consensus.node_id)}")
    
    # Пробуем найти валидный nonce
    print("Searching for valid nonce...")
    nonce = consensus.find_valid_nonce(consensus_hash, max_attempts=50000)
    if nonce is not None:
        print(f"✅ Found valid nonce: {nonce}")
    else:
        print("❌ No valid nonce found in 50k attempts")
    
    print(f"\nConsensus info: {consensus.get_consensus_info()}")
