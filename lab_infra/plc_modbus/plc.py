import asyncio
import requests
import threading
import time
from pymodbus.server import StartAsyncTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext

# Simulated PLC registers
store = ModbusSlaveContext(
    hr=ModbusSequentialDataBlock(0, [50, 10, 85, 0]), # Register 0 is pump speed
    single=True
)
context = ModbusServerContext(slaves=store, single=True)

def sync_with_engine():
    """Background thread to push PLC state to the Digital Twin."""
    while True:
        try:
            # Read Register 0 (Pump Speed) from the store
            speed = store.getValues(3, 0, 1)[0]
            requests.post("http://factory_engine:9000/api/update", json={"pump_speed": speed}, timeout=1)
        except Exception:
            pass
        time.sleep(0.5)

async def run_server():
    # Start sync thread
    threading.Thread(target=sync_with_engine, daemon=True).start()
    print("Modbus PLC Sync started. Running server on 5020...")
    await StartAsyncTcpServer(context=context, address=("0.0.0.0", 5020))

if __name__ == "__main__":
    asyncio.run(run_server())
