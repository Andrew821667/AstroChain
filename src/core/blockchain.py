
import hashlib
import json
import time
from datetime import datetime
from typing import List, Dict, Any, Optional

class Transaction:
    """Базовая транзакция"""
    
    def __init__(self, from_address: str, to_address: str, amount: float, data: Dict = None):
        self.from_address = from_address
        self.to_address = to_address
        self.amount = amount
        self.timestamp = datetime.utcnow().isoformat()
        self.data = data or {}
        self.tx_hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """Вычисляет хеш транзакции"""
        tx_string = f"{self.from_address}{self.to_address}{self.amount}{self.timestamp}{json.dumps(self.data, sort_keys=True)}"
        return hashlib.sha256(tx_string.encode()).hexdigest()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "from": self.from_address,
            "to": self.to_address,
            "amount": self.amount,
            "timestamp": self.timestamp,
            "data": self.data,
            "hash": self.tx_hash
        }

class Block:
    """Блок в астрономическом блокчейне"""
    
    def __init__(self, index: int, transactions: List[Transaction], previous_hash: str, astronomical_data: Dict[str, Any]):
        self.index = index
        self.timestamp = datetime.utcnow().isoformat()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.astronomical_data = astronomical_data
        self.astronomical_hash = astronomical_data.get("astronomical_hash", "")
        self.merkle_root = self.calculate_merkle_root()
        self.nonce = 0
        self.hash = self.calculate_hash()
    
    def calculate_merkle_root(self) -> str:
        """Вычисляет Merkle root для транзакций"""
        if not self.transactions:
            return hashlib.sha256("".encode()).hexdigest()
        
        tx_hashes = [tx.tx_hash for tx in self.transactions]
        
        while len(tx_hashes) > 1:
            if len(tx_hashes) % 2 == 1:
                tx_hashes.append(tx_hashes[-1])  # Дублируем последний хеш
            
            new_hashes = []
            for i in range(0, len(tx_hashes), 2):
                combined = tx_hashes[i] + tx_hashes[i + 1]
                new_hashes.append(hashlib.sha256(combined.encode()).hexdigest())
            
            tx_hashes = new_hashes
        
        return tx_hashes[0]
    
    def calculate_hash(self) -> str:
        """Вычисляет хеш блока"""
        block_string = f"{self.index}{self.timestamp}{self.previous_hash}{self.merkle_root}{self.astronomical_hash}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
            "transactions": [tx.to_dict() for tx in self.transactions],
            "astronomical_data": self.astronomical_data,
            "astronomical_hash": self.astronomical_hash,
            "merkle_root": self.merkle_root,
            "nonce": self.nonce,
            "hash": self.hash
        }

class AstroBlockchain:
    """Астрономический блокчейн"""
    
    def __init__(self):
        self.chain: List[Block] = []
        self.pending_transactions: List[Transaction] = []
        self.create_genesis_block()
    
    def create_genesis_block(self):
        """Создает генезис блок"""
        genesis_astronomical_data = {
            "type": "genesis",
            "astronomical_hash": "0000000000000000000000000000000000000000000000000000000000000000"
        }
        genesis_block = Block(0, [], "0", genesis_astronomical_data)
        self.chain.append(genesis_block)
    
    def get_latest_block(self) -> Block:
        """Возвращает последний блок"""
        return self.chain[-1]
    
    def add_transaction(self, transaction: Transaction):
        """Добавляет транзакцию в пул ожидания"""
        self.pending_transactions.append(transaction)
    
    def create_block(self, astronomical_data: Dict[str, Any]) -> Block:
        """Создает новый блок с астрономическими данными"""
        index = len(self.chain)
        previous_hash = self.get_latest_block().hash
        
        # Берем транзакции из пула
        transactions = self.pending_transactions.copy()
        self.pending_transactions = []  # Очищаем пул
        
        # Создаем блок
        new_block = Block(index, transactions, previous_hash, astronomical_data)
        
        # Добавляем в цепочку
        self.chain.append(new_block)
        
        return new_block
    
    def is_chain_valid(self) -> bool:
        """Проверяет валидность всей цепочки"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Проверяем хеш текущего блока
            if current_block.hash != current_block.calculate_hash():
                return False
            
            # Проверяем связь с предыдущим блоком
            if current_block.previous_hash != previous_block.hash:
                return False
        
        return True
    
    def get_balance(self, address: str) -> float:
        """Вычисляет баланс адреса"""
        balance = 0
        
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.from_address == address:
                    balance -= transaction.amount
                if transaction.to_address == address:
                    balance += transaction.amount
        
        return balance
    
    def get_chain_info(self) -> Dict[str, Any]:
        """Возвращает информацию о блокчейне"""
        return {
            "length": len(self.chain),
            "latest_block": self.get_latest_block().to_dict(),
            "pending_transactions": len(self.pending_transactions),
            "is_valid": self.is_chain_valid()
        }

# Тестируем блокчейн
if __name__ == "__main__":
    # Создаем блокчейн
    blockchain = AstroBlockchain()
    
    # Добавляем транзакции
    tx1 = Transaction("alice", "bob", 50.0, {"memo": "test payment"})
    tx2 = Transaction("bob", "charlie", 25.0)
    
    blockchain.add_transaction(tx1)
    blockchain.add_transaction(tx2)
    
    # Симулируем астрономические данные
    test_astronomical_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "sources": {
            "iss": {"latitude": 36.39, "longitude": 173.77},
            "solar": {"flux": 0.18}
        },
        "astronomical_hash": "159fc15a65352da3d352b47ca6032bd34aebdd71c19187dee7c702ae1775cb12"
    }
    
    # Создаем блок
    new_block = blockchain.create_block(test_astronomical_data)
    
    print("=== BLOCKCHAIN INFO ===")
    print(json.dumps(blockchain.get_chain_info(), indent=2))
    
    print(f"\n=== BALANCES ===")
    print(f"Alice: {blockchain.get_balance('alice')}")
    print(f"Bob: {blockchain.get_balance('bob')}")
    print(f"Charlie: {blockchain.get_balance('charlie')}")
