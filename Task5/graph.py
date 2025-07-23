from pymongo import MongoClient
import matplotlib.pyplot as plt


class SystemUsageVisualizer:
    def __init__(self, mongo_uri="mongodb://localhost:27017", db_name="power_stats", collection_name="logs"):
        self.mongo_uri = mongo_uri
        self.db_name = db_name
        self.collection_name = collection_name
        self.client = None

    def _connect(self):
        self.client = MongoClient(self.mongo_uri)

    def _disconnect(self):
        if self.client:
            self.client.close()

    def _fetch_logs(self):
        self._connect()
        collection = self.client[self.db_name][self.collection_name]
        logs = list(collection.find().sort("timestamp", 1))
        self._disconnect()
        return logs

    def _prepare_data(self, logs):
        timestamps = [log["timestamp"] for log in logs]
        cpu_values = [log["cpu"] for log in logs]
        ram_used = [log["ram_used"] / (1024 ** 3) for log in logs]
        return timestamps, cpu_values, ram_used

    def _plot(self, timestamps, cpu_values, ram_used):
        plt.figure(figsize=(12, 6))
        plt.plot(timestamps, cpu_values, label="CPU %", color="blue")
        plt.plot(timestamps, ram_used, label="RAM verwendet (GB)", color="green")
        plt.xlabel("Zeit")
        plt.ylabel("Nutzung")
        plt.title("Systemauslastung")
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
        plt.savefig("graph.png")
        print("Grafik wurde als png gespeichert")

    def visualize(self):
        logs = self._fetch_logs()
        if not logs:
            print("Keine daten vorhanden")
            return
        timestamps, cpu_values, ram_used = self._prepare_data(logs)
        self._plot(timestamps, cpu_values, ram_used)


def visualize_data():
    visualizer = SystemUsageVisualizer()
    visualizer.visualize()


if __name__ == "__main__":
    visualize_data()
