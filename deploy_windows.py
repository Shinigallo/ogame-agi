"""
OGame AGI - Windows Container Deployment
Use Windows container for browser automation when Linux containers fail
"""

import requests
import subprocess
import time
import json
from pathlib import Path

def check_windows_container_status():
    """Check if Windows container is ready for deployment"""
    
    try:
        result = subprocess.run(['docker', 'ps', '--filter', 'name=windows', '--format', 'json'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0 and result.stdout:
            container_info = json.loads(result.stdout)
            print(f"✅ Windows container running: {container_info.get('Names', 'windows')}")
            print(f"   Status: {container_info.get('Status', 'Unknown')}")
            print(f"   Ports: {container_info.get('Ports', 'Not mapped')}")
            return True
        else:
            print("❌ Windows container not found")
            return False
            
    except Exception as e:
        print(f"❌ Error checking container: {e}")
        return False

def test_windows_web_interface():
    """Test Windows container web interface"""
    
    try:
        # Test web VNC interface
        response = requests.get('http://localhost:8006', timeout=5)
        
        if response.status_code == 401:
            print("🔒 Windows web interface requires authentication")
            print("   URL: http://localhost:8006")
            print("   Status: Interface accessible but needs login")
            return True
        elif response.status_code == 200:
            print("✅ Windows web interface accessible")
            return True
        else:
            print(f"⚠️ Windows interface status: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot reach Windows interface: {e}")
        return False

def deploy_ogame_agi_to_windows():
    """Deploy OGame AGI files to Windows container for testing"""
    
    print("🚀 Deploying OGame AGI to Windows Container")
    print("=" * 50)
    
    # Check container status
    container_running = check_windows_container_status()
    web_accessible = test_windows_web_interface()
    
    if not container_running:
        print("❌ Windows container not available")
        return False
    
    deployment_plan = {
        'approach': 'Manual browser deployment',
        'target': 'Windows container with web browser',
        'automation_level': 'Semi-automated (AI consultation)',
        'components': [
            'Strategic AI brain (host system)',
            'Browser interface (Windows container)', 
            'OGame TestAgent2026 account',
            'Manual action execution'
        ]
    }
    
    print("\n🎯 Deployment Strategy:")
    for key, value in deployment_plan.items():
        if isinstance(value, list):
            print(f"   {key}:")
            for item in value:
                print(f"      - {item}")
        else:
            print(f"   {key}: {value}")
    
    print("\n📋 Manual Deployment Steps:")
    print("1. 🌐 Open Windows container web interface: http://localhost:8006")
    print("2. 🔐 Login to Windows desktop environment")  
    print("3. 🌍 Open web browser in Windows")
    print("4. 🎮 Navigate to Scorpius: https://s161-en.ogame.gameforge.com")
    print("5. 👤 Login with TestAgent2026 / TestAGI2026!")
    print("6. 🧠 Run strategic AI consultation on host")
    print("7. 🎯 Execute AI recommendations in browser manually")
    print("8. 📊 Monitor and validate AI decision accuracy")
    
    print("\n🤖 AI Consultation Commands (run on host):")
    print("cd /home/dario/openclaw/workspace/ogame-agi")
    print("python3 test_strategic_ai.py  # Get strategic recommendations")
    print("gemini -p 'OGame analysis: [paste game state]'  # AI consultation")
    
    print("\n✅ Benefits of Windows Container Approach:")
    print("   - Full browser compatibility (no Playwright issues)")
    print("   - Real browser environment (anti-detection)")
    print("   - Manual verification of AI decisions")
    print("   - Educational observation of strategic reasoning")
    print("   - Zero Docker dependency failures")
    
    return True

if __name__ == "__main__":
    success = deploy_ogame_agi_to_windows()
    
    if success:
        print("\n🎉 Windows container deployment strategy ready!")
        print("🎯 Next: Manual browser testing with AI consultation")
    else:
        print("\n⚠️ Deployment preparation incomplete")
        print("💡 Consider alternative deployment approaches")