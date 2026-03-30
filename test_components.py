"""
Simple test runner for OGame AGI without Docker
Test the core components before containerization
"""

import os
import sys
import asyncio
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

async def test_gemini_connection():
    """Test Gemini API connection"""
    try:
        from agents.enhanced_gemini_brain import EnhancedGeminiBrain
        
        brain = EnhancedGeminiBrain()
        
        # Simple test query
        test_response = await brain.model.generate_content_async("Test: respond with 'OK' if you can hear me")
        print(f"✅ Gemini API: {test_response.text.strip()}")
        
        return True
    except Exception as e:
        print(f"❌ Gemini API Error: {e}")
        return False

async def test_rag_system():
    """Test RAG knowledge retrieval"""
    try:
        from knowledge.rag_system import OGameRAG
        
        rag = OGameRAG()
        
        # Test strategy retrieval
        context = {'game_phase': 'early', 'fleet_at_risk': False}
        strategies = rag.retrieve_relevant_strategies("new account strategy", context)
        
        print(f"✅ RAG System: Retrieved {len(strategies)} strategies")
        if strategies:
            print(f"   Top strategy: {strategies[0].title}")
        
        return True
    except Exception as e:
        print(f"❌ RAG System Error: {e}")
        return False

def test_config():
    """Test configuration loading"""
    try:
        # Load environment variables
        from dotenv import load_dotenv
        load_dotenv()
        
        username = os.getenv('OGAME_USERNAME')
        has_api_key = bool(os.getenv('GEMINI_API_KEY'))
        
        print(f"✅ Config: Username={username}, API Key={'Yes' if has_api_key else 'No'}")
        return bool(username and has_api_key)
    except Exception as e:
        print(f"❌ Config Error: {e}")
        return False

async def main():
    """Run all tests"""
    print("🧪 OGame AGI Component Tests")
    print("=" * 40)
    
    # Test configuration
    config_ok = test_config()
    
    if not config_ok:
        print("⚠️ Configuration incomplete - fix .env file first")
        return
    
    # Test RAG system
    rag_ok = await test_rag_system()
    
    # Test Gemini connection
    gemini_ok = await test_gemini_connection()
    
    print("=" * 40)
    
    if all([config_ok, rag_ok, gemini_ok]):
        print("✅ All tests passed! Ready for OGame connection test")
        
        # Optional: Test basic strategy analysis
        if rag_ok and gemini_ok:
            print("\n🎯 Testing strategic analysis...")
            try:
                from agents.enhanced_gemini_brain import EnhancedGeminiBrain
                
                brain = EnhancedGeminiBrain()
                
                # Simulate new account state
                game_data = {
                    'resources': {'metal': 500, 'crystal': 500, 'deuterium': 0},
                    'buildings': {},
                    'research': {},
                    'fleet': {}
                }
                
                analysis = await brain.analyze_strategic_situation(game_data, "new account just created")
                
                print(f"📋 Strategic Analysis Sample:")
                if 'immediate_priorities' in analysis:
                    for priority in analysis['immediate_priorities'][:2]:
                        print(f"   - {priority.get('action', 'Unknown')}: {priority.get('reasoning', 'No reason')}")
                
            except Exception as e:
                print(f"⚠️ Strategic analysis test failed: {e}")
    else:
        print("❌ Some tests failed - check configuration and dependencies")

if __name__ == "__main__":
    asyncio.run(main())