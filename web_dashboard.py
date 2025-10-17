from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime
import os
import json
import requests
import producer_manager

app = Flask(__name__)

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client["trafiklab"]
collection = db["departures"]

API_KEY = os.getenv("TRAFIKLAB_KEY")

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/search-stops')
def search_stops():
    query = request.args.get('q', '').strip()
    if not query or len(query) < 2:
        return jsonify({"success": True, "data": []})
    
    try:
        url = f"https://realtime-api.trafiklab.se/v1/stops/name/{query}?key={API_KEY}"
        response = requests.get(url, timeout=10)
        
        if not response.ok:
            return jsonify({"success": False, "error": "Failed to search stops"}), 500
        
        data = response.json()
        stop_groups = data.get('stop_groups', [])
        
        results = []
        for group in stop_groups[:20]:
            area_type = group.get('area_type', '')
            if area_type in ['META_STOP', 'RIKSHALLPLATS']:
                results.append({
                    "id": group['id'],
                    "name": group['name'],
                    "area_type": area_type,
                    "transport_modes": group.get('transport_modes', [])
                })
        
        return jsonify({"success": True, "data": results})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/departures')
def get_departures():
    """API endpoint to fetch latest UNIQUE departures from MongoDB (deduplicating by composite key)."""
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 50))
        skip = (page - 1) * per_page
        stop_id = request.args.get('stop_id', '740098000') 

        pipeline = []
        
        if stop_id:
            pipeline.append({"$match": {"stop_id": stop_id}})
        
        pipeline.extend([
            {
                "$sort": {"_id": -1}  
            },
            {
                "$group": {
                    "_id": {
                        "operator": "$operator",
                        "line": "$line",
                        "destination": "$destination",
                        "scheduled": "$scheduled"
                    },
                    "doc": {"$first": "$$ROOT"} 
                }
            },
            {
                "$replaceRoot": {"newRoot": "$doc"}  
            },
            {
                "$sort": {"scheduled": -1} 
            }
        ])
        
        all_unique = list(collection.aggregate(pipeline))
        total_unique = len(all_unique)
        total_pages = (total_unique + per_page - 1) // per_page  
        
        departures = all_unique[skip:skip + per_page]
        
        for dep in departures:
            dep.pop('_id', None)
        
        total_count = collection.count_documents({"stop_id": stop_id} if stop_id else {})
        
        delay_stats_pipeline = []
        if stop_id:
            delay_stats_pipeline.append({"$match": {"stop_id": stop_id}})
            
        delay_stats_pipeline.extend([
            {"$sort": {"_id": -1}},
            {
                "$group": {
                    "_id": {
                        "operator": "$operator",
                        "line": "$line",
                        "destination": "$destination",
                        "scheduled": "$scheduled"
                    },
                    "doc": {"$first": "$$ROOT"}
                }
            },
            {"$replaceRoot": {"newRoot": "$doc"}},
            {"$match": {"delay_seconds": {"$ne": None}}},
            {
                "$group": {
                    "_id": None,
                    "avg_delay": {"$avg": "$delay_seconds"},
                    "max_delay": {"$max": "$delay_seconds"},
                    "min_delay": {"$min": "$delay_seconds"}
                }
            }
        ])
        delay_stats = list(collection.aggregate(delay_stats_pipeline))
        
        stats = {
            "total_records": total_count,
            "unique_departures": total_unique,
            "avg_delay": round(delay_stats[0]["avg_delay"], 2) if delay_stats else 0,
            "max_delay": delay_stats[0]["max_delay"] if delay_stats else 0,
            "min_delay": delay_stats[0]["min_delay"] if delay_stats else 0,
        }
        
        return jsonify({
            "success": True,
            "data": departures,
            "stats": stats,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total_pages": total_pages,
                "total_items": total_unique
            },
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/start-producer', methods=['POST'])
def start_producer_endpoint():
    data = request.get_json()
    stop_id = data.get('stop_id')
    
    if not stop_id:
        return jsonify({"success": False, "error": "stop_id required"}), 400
    
    success = producer_manager.start_producer(str(stop_id))
    
    return jsonify({
        "success": success,
        "stop_id": stop_id,
        "active_stops": producer_manager.get_active_stops()
    })

@app.route('/api/active-producers')
def get_active_producers():
    return jsonify({
        "success": True,
        "active_stops": producer_manager.get_active_stops()
    })

if __name__ == '__main__':
    print("Starting Trafiklab Dashboard on http://localhost:5432")
    app.run(debug=True, host='0.0.0.0', port=5432)
