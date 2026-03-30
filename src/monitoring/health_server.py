"""
Optional Health Check Endpoint for Bot Monitoring
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json
import os
from datetime import datetime
import uvicorn


app = FastAPI(title="OGame Bot Monitor", version="1.0.0")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check if bot is running by looking at recent state
        current_state_path = "data/current_state.json"
        
        if not os.path.exists(current_state_path):
            return JSONResponse(
                status_code=503,
                content={"status": "unhealthy", "reason": "No state file found"}
            )
            
        # Check state file age
        stat = os.stat(current_state_path)
        age_minutes = (datetime.now().timestamp() - stat.st_mtime) / 60
        
        if age_minutes > 10:  # State older than 10 minutes
            return JSONResponse(
                status_code=503,
                content={
                    "status": "unhealthy", 
                    "reason": f"State file is {age_minutes:.1f} minutes old"
                }
            )
            
        return JSONResponse(
            status_code=200,
            content={
                "status": "healthy",
                "last_update": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "age_minutes": round(age_minutes, 1)
            }
        )
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "reason": str(e)}
        )


@app.get("/status")
async def bot_status():
    """Detailed bot status"""
    try:
        status = {
            "timestamp": datetime.now().isoformat(),
            "current_state": None,
            "logs": []
        }
        
        # Read current state
        if os.path.exists("data/current_state.json"):
            with open("data/current_state.json", 'r') as f:
                status["current_state"] = json.load(f)
                
        # Read recent logs
        log_file = "logs/ogame_bot.log"
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                lines = f.readlines()
                status["logs"] = lines[-20:]  # Last 20 lines
                
        return status
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


@app.get("/metrics")
async def bot_metrics():
    """Bot performance metrics"""
    try:
        metrics = {
            "cycles_completed": 0,
            "actions_executed": 0,
            "resources_gained": {},
            "uptime": None
        }
        
        # Parse metrics from state history
        history_file = "data/state_history.jsonl"
        if os.path.exists(history_file):
            with open(history_file, 'r') as f:
                lines = f.readlines()
                metrics["cycles_completed"] = len(lines)
                
                if lines:
                    # Calculate resource gains
                    first_state = json.loads(lines[0])
                    last_state = json.loads(lines[-1])
                    
                    for resource in ['metal', 'crystal', 'deuterium']:
                        first_val = first_state['resources'].get(resource, 0)
                        last_val = last_state['resources'].get(resource, 0)
                        metrics["resources_gained"][resource] = last_val - first_val
                        
        return metrics
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)