import subprocess
import sys
import os
from pathlib import Path

active_producers = {}

def start_producer(stop_id: str) -> bool:
    for existing_stop_id in list(active_producers.keys()):
        if existing_stop_id != stop_id:
            stop_producer(existing_stop_id)
    
    if stop_id in active_producers:
        if active_producers[stop_id].poll() is None:
            return True
        else:
            del active_producers[stop_id]
    
    try:
        python_exe = sys.executable
        producer_path = Path(__file__).parent / "producer.py"
        
        process = subprocess.Popen(
            [python_exe, str(producer_path), stop_id],
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
        )
        
        active_producers[stop_id] = process
        return True
    
    except Exception as e:
        return False

def stop_producer(stop_id: str) -> bool:
    if stop_id not in active_producers:
        return False
    
    try:
        process = active_producers[stop_id]
        process.terminate()
        process.wait(timeout=5)
        del active_producers[stop_id]
        return True
    
    except Exception as e:
        try:
            process.kill()
            del active_producers[stop_id]
        except:
            pass
        return False

def get_active_stops():
    dead_stops = []
    for stop_id, process in active_producers.items():
        if process.poll() is not None:
            dead_stops.append(stop_id)
    
    for stop_id in dead_stops:
        del active_producers[stop_id]
    
    return list(active_producers.keys())

def stop_all_producers():
    for stop_id in list(active_producers.keys()):
        stop_producer(stop_id)
