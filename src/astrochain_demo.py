
import json
import time
from datetime import datetime

# Импортируем наши модули (в Colab напрямую)
exec(open('src/astronomical/data_fetcher.py').read())
exec(open('src/core/blockchain.py').read())
exec(open('src/consensus/proof_of_astronomy.py').read())

class AstroChainDemo:
    """
    Демонстрация полной работы AstroChain системы
    """
    
    def __init__(self):
        print("🚀 Initializing AstroChain Demo...")
        
        # Инициализируем компоненты
        self.data_fetcher = AstronomicalDataFetcher()
        self.blockchain = AstroBlockchain()
        self.consensus = ProofOfAstronomy(block_interval_minutes=1)  # Для демо: 1 минута
        
        print(f"✅ Node ID: {self.consensus.node_id}")
        print(f"✅ Genesis block created: {self.blockchain.get_latest_block().hash[:16]}...")
    
    def demonstrate_transaction_flow(self):
        """Демонстрирует создание и обработку транзакций"""
        print("\n🔄 === TRANSACTION FLOW DEMO ===")
        
        # Создаем тестовые транзакции
        tx1 = Transaction("astro_alice", "astro_bob", 100.0, {"memo": "First AstroChain payment!"})
        tx2 = Transaction("astro_bob", "astro_charlie", 50.0, {"memo": "Cosmic transfer"})
        tx3 = Transaction("astro_charlie", "astro_alice", 25.0)
        
        # Добавляем в blockchain
        self.blockchain.add_transaction(tx1)
        self.blockchain.add_transaction(tx2)
        self.blockchain.add_transaction(tx3)
        
        print(f"✅ Added 3 transactions to pool")
        print(f"📊 Pending transactions: {len(self.blockchain.pending_transactions)}")
        
        return [tx1, tx2, tx3]
    
    def demonstrate_astronomical_consensus(self):
        """Демонстрирует работу астрономического консенсуса"""
        print("\n🌌 === ASTRONOMICAL CONSENSUS DEMO ===")
        
        # Получаем реальные астрономические данные
        print("📡 Fetching real astronomical data...")
        astronomical_snapshot = self.data_fetcher.get_astronomical_snapshot()
        
        if not astronomical_snapshot["sources"]:
            print("❌ No astronomical data available, using mock data")
            astronomical_snapshot = {
                "timestamp": datetime.utcnow().isoformat(),
                "sources": {
                    "iss": {"latitude": 45.123, "longitude": -123.456},
                    "solar": {"flux": 0.2345}
                }
            }
        
        # Вычисляем консенсус
        consensus_hash = self.consensus.calculate_astronomical_consensus(astronomical_snapshot)
        astronomical_snapshot["astronomical_hash"] = consensus_hash
        
        print(f"🔍 Consensus hash: {consensus_hash[:16]}...")
        
        # Проверяем право создать блок
        can_create = self.consensus.can_create_block(consensus_hash, self.consensus.node_id)
        print(f"🎯 Can create block: {can_create}")
        
        if not can_create:
            print("🔨 Searching for valid nonce...")
            nonce = self.consensus.find_valid_nonce(consensus_hash, max_attempts=100000)
            if nonce:
                print(f"✅ Found valid nonce: {nonce}")
                can_create = True
            else:
                print("❌ No valid nonce found")
        
        return astronomical_snapshot, can_create
    
    def demonstrate_block_creation(self, astronomical_data):
        """Демонстрирует создание блока"""
        print("\n⛓️ === BLOCK CREATION DEMO ===")
        
        # Создаем новый блок
        new_block = self.blockchain.create_block(astronomical_data)
        
        print(f"✅ Block #{new_block.index} created!")
        print(f"📦 Block hash: {new_block.hash[:16]}...")
        print(f"🌟 Astronomical hash: {new_block.astronomical_hash[:16]}...")
        print(f"🌳 Merkle root: {new_block.merkle_root[:16]}...")
        print(f"💳 Transactions: {len(new_block.transactions)}")
        
        return new_block
    
    def demonstrate_validation(self, block):
        """Демонстрирует валидацию блока"""
        print("\n✅ === VALIDATION DEMO ===")
        
        # Проверяем блок
        is_valid_astronomical = self.consensus.validate_astronomical_block(block.to_dict())
        is_valid_chain = self.blockchain.is_chain_valid()
        
        print(f"🔍 Astronomical validation: {is_valid_astronomical}")
        print(f"⛓️ Chain validation: {is_valid_chain}")
        
        return is_valid_astronomical and is_valid_chain
    
    def show_final_state(self):
        """Показывает финальное состояние системы"""
        print("\n📊 === FINAL STATE ===")
        
        # Информация о блокчейне
        chain_info = self.blockchain.get_chain_info()
        print(f"🔗 Blockchain length: {chain_info['length']}")
        print(f"💸 Pending transactions: {chain_info['pending_transactions']}")
        
        # Балансы
        addresses = ["astro_alice", "astro_bob", "astro_charlie"]
        print("\n💰 Balances:")
        for addr in addresses:
            balance = self.blockchain.get_balance(addr)
            print(f"   {addr}: {balance} ASTRO")
        
        # Последний блок
        latest = self.blockchain.get_latest_block()
        print(f"\n📦 Latest block:")
        print(f"   Index: {latest.index}")
        print(f"   Hash: {latest.hash[:32]}...")
        print(f"   Astronomical data sources: {list(latest.astronomical_data.get('sources', {}).keys())}")
        
        return chain_info
    
    def run_full_demo(self):
        """Запускает полную демонстрацию"""
        print("=" * 60)
        print("🌌 ASTROCHAIN FULL SYSTEM DEMO 🌌")
        print("=" * 60)
        
        try:
            # 1. Транзакции
            transactions = self.demonstrate_transaction_flow()
            
            # 2. Астрономический консенсус
            astronomical_data, can_create = self.demonstrate_astronomical_consensus()
            
            if can_create:
                # 3. Создание блока
                new_block = self.demonstrate_block_creation(astronomical_data)
                
                # 4. Валидация
                is_valid = self.demonstrate_validation(new_block)
                
                if is_valid:
                    print("\n🎉 === SUCCESS! ALL SYSTEMS WORKING! ===")
                else:
                    print("\n❌ === VALIDATION FAILED ===")
            else:
                print("\n⏸️ === DEMO PAUSED: No consensus for block creation ===")
            
            # 5. Финальное состояние
            final_state = self.show_final_state()
            
            print("\n🚀 === ASTROCHAIN DEMO COMPLETED ===")
            return True
            
        except Exception as e:
            print(f"\n💥 ERROR: {e}")
            import traceback
            traceback.print_exc()
            return False

# Запускаем демо
if __name__ == "__main__":
    demo = AstroChainDemo()
    success = demo.run_full_demo()
    
    if success:
        print("\n✨ AstroChain MVP is working! Ready for production testing! ✨")
    else:
        print("\n🔧 Some issues found. Need debugging.")
