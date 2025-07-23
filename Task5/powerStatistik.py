import psutil
import datetime
import time
from pymongo import MongoClient


class Power:
    def __init__(self, cpu=None, ram_total=None, ram_used=None, timestamp=None):
        if None in (cpu, ram_total, ram_used, timestamp):
            self.cpu = psutil.cpu_percent(interval=1)
            mem = psutil.virtual_memory()
            self.ram_total = mem.total
            self.ram_used = mem.used
            self.timestamp = datetime.datetime.now()
        else:
            self.cpu = cpu
            self.ram_total = ram_total
            self.ram_used = ram_used
            self.timestamp = timestamp

    def to_dict(self):
        return {
            "cpu": self.cpu,
            "ram_total": self.ram_total,
            "ram_used": self.ram_used,
            "timestamp": self.timestamp
        }


class PowerLogger:
    def __init__(self, uri="mongodb://localhost:27017", db_name="power_stats", collection_name="logs"):
        self.client = MongoClient(uri)
        self.collection = self.client[db_name][collection_name]

    def insert(self, power: Power):
        self.collection.insert_one(power.to_dict())

    def cleanup(self, max_entries=10000):
        total_logs = self.collection.count_documents({})
        if total_logs > max_entries:
            excess = total_logs - max_entries
            old_logs = self.collection.find().sort("timestamp", 1).limit(excess)
            for log in old_logs:
                self.collection.delete_one({"_id": log["_id"]})

    def close(self):
        self.client.close()


def log_power_stats():
    logger = PowerLogger()
    try:
        power = Power()
        logger.insert(power)
        logger.cleanup()
    finally:
        logger.close()


def main():
    while True:
        log_power_stats()
        time.sleep(1)


if __name__ == "__main__":
    main()
