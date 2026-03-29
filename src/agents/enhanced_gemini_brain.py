"""
Enhanced Gemini Brain with RAG Integration
Strategic AI with access to OGame knowledge base
"""

import os
import google.generativeai as genai
from typing import Dict, List, Any, Optional
import logging
import json

from knowledge.rag_system import OGameRAG


class EnhancedGeminiBrain:
    """Strategic AI brain with RAG-powered knowledge retrieval"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.setup_gemini()
        self.rag = OGameRAG()
        
        # Strategic context memory
        self.game_phase = "early"  # early, mid, late
        self.strategy_focus = "balanced"  # miner, fleeter, turtle, balanced
        self.risk_tolerance = "medium"  # low, medium, high
        
    def setup_gemini(self):
        """Initialize Gemini AI with strategic system prompt"""
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable required")
            
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Enhanced system prompt for strategic thinking
        self.system_prompt = """
        You are an elite OGame strategist AI with decades of experience. Your role is to:
        
        1. ANALYZE game states with surgical precision
        2. PRIORITIZE actions based on risk/reward optimization  
        3. ADAPT strategies based on current game phase and player situation
        4. ENSURE SAFETY through proper fleetsaving and resource management
        5. MAXIMIZE EFFICIENCY in all resource and time investments
        
        Key Principles:
        - Safety First: Never leave fleet or resources vulnerable
        - ROI Focus: Every action must have positive return on investment
        - Timing Critical: Coordinate multiple operations for maximum efficiency
        - Adapt Continuously: Adjust strategy based on universe dynamics
        
        Always provide specific, actionable recommendations with clear reasoning.
        """
        
        self.logger.info("🧠 Enhanced Gemini brain initialized with strategic context")
        
    async def analyze_strategic_situation(self, game_data: Dict[str, Any], current_situation: str) -> Dict[str, Any]:
        """Deep strategic analysis with RAG-powered knowledge retrieval"""
        
        # Get relevant strategic knowledge
        context = self._build_context_from_game_data(game_data)
        relevant_strategies = self.rag.retrieve_relevant_strategies(current_situation, context)
        
        # Build comprehensive prompt
        prompt = self._build_strategic_prompt(game_data, current_situation, relevant_strategies)
        
        try:
            response = await self.model.generate_content_async(prompt)
            
            # Parse structured response
            analysis = self._parse_strategic_response(response.text)
            
            # Add RAG metadata
            analysis['knowledge_sources'] = [doc.title for doc in relevant_strategies]
            analysis['strategy_confidence'] = self._calculate_confidence(relevant_strategies, game_data)
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Strategic analysis error: {e}")
            return self._get_fallback_analysis(game_data)
            
    def _build_context_from_game_data(self, game_data: Dict[str, Any]) -> Dict[str, Any]:
        """Build context for RAG retrieval from game data"""
        
        context = {}
        
        # Determine game phase
        if game_data.get('research_level', 0) < 5:
            context['game_phase'] = 'early'
        elif game_data.get('research_level', 0) < 15:
            context['game_phase'] = 'mid'  
        else:
            context['game_phase'] = 'late'
            
        # Risk assessment
        fleet_visible = game_data.get('fleet_visible', False)
        resources_exposed = game_data.get('resources', {}).get('total', 0) > 100000
        context['fleet_at_risk'] = fleet_visible
        context['resources_at_risk'] = resources_exposed
        
        # Resource situation
        resource_production = game_data.get('production_rate', 0)
        context['low_resources'] = resource_production < 1000  # Arbitrary threshold
        
        return context
        
    def _build_strategic_prompt(self, game_data: Dict[str, Any], situation: str, strategies: List) -> str:
        """Build comprehensive strategic analysis prompt"""
        
        strategy_knowledge = ""
        if strategies:
            strategy_knowledge = "\n\nRELEVANT STRATEGIC KNOWLEDGE:\n"
            for i, strategy in enumerate(strategies[:3], 1):
                strategy_knowledge += f"\n{i}. {strategy.title}:\n{strategy.content[:300]}...\n"
                
        prompt = f"""
        {self.system_prompt}
        
        CURRENT SITUATION: {situation}
        
        GAME DATA:
        {json.dumps(game_data, indent=2)}
        
        {strategy_knowledge}
        
        Provide a comprehensive strategic analysis in JSON format:
        {{
            "immediate_priorities": [
                {{"action": "specific action", "reasoning": "why this first", "urgency": "critical|high|medium|low"}}
            ],
            "strategic_plan": {{
                "next_hour": ["action1", "action2"],
                "next_day": ["action1", "action2"], 
                "next_week": ["goal1", "goal2"]
            }},
            "risk_assessment": {{
                "current_threats": ["threat1", "threat2"],
                "mitigation_actions": ["action1", "action2"],
                "risk_level": "low|medium|high|critical"
            }},
            "resource_allocation": {{
                "metal_priority": "mines|fleet|research|defense",
                "crystal_priority": "mines|fleet|research|defense", 
                "deuterium_priority": "mines|fleet|research|defense",
                "reasoning": "explanation of allocation strategy"
            }},
            "tactical_recommendations": [
                {{"type": "fleetsave|attack|research|build", "details": "specific instructions"}}
            ],
            "success_metrics": {{
                "short_term": "what to measure in next 24h",
                "long_term": "what to achieve in next week"
            }}
        }}
        """
        
        return prompt
        
    def _parse_strategic_response(self, response_text: str) -> Dict[str, Any]:
        """Parse and validate strategic response"""
        try:
            # Try to extract JSON from response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = response_text[start_idx:end_idx]
                return json.loads(json_str)
            else:
                # Fallback: create structured response from text
                return {"analysis": response_text, "error": "Could not parse JSON"}
                
        except json.JSONDecodeError:
            return {"analysis": response_text, "error": "JSON parsing failed"}
            
    def _calculate_confidence(self, strategies: List, game_data: Dict[str, Any]) -> float:
        """Calculate confidence level for strategic recommendations"""
        
        confidence = 0.5  # Base confidence
        
        # More relevant strategies = higher confidence
        if len(strategies) >= 3:
            confidence += 0.2
        elif len(strategies) >= 2:
            confidence += 0.1
            
        # Complete game data = higher confidence  
        if all(key in game_data for key in ['resources', 'fleet', 'research']):
            confidence += 0.2
            
        # High priority strategies available = higher confidence
        if strategies and max(s.priority for s in strategies) >= 8:
            confidence += 0.1
            
        return min(confidence, 1.0)
        
    def _get_fallback_analysis(self, game_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback analysis when AI fails"""
        
        # Get emergency procedures from RAG
        safety_docs = self.rag.get_emergency_procedures()
        
        return {
            "immediate_priorities": [
                {"action": "fleetsave_check", "reasoning": "Safety first", "urgency": "critical"}
            ],
            "tactical_recommendations": [
                {"type": "fleetsave", "details": "Ensure all ships and resources are protected"}
            ],
            "knowledge_sources": [doc.title for doc in safety_docs],
            "strategy_confidence": 0.3,
            "error": "AI analysis failed, using safety fallback"
        }
        
    async def get_emergency_response(self, threat: str) -> Dict[str, Any]:
        """Immediate response for critical situations"""
        
        emergency_strategies = self.rag.get_emergency_procedures()
        
        prompt = f"""
        EMERGENCY SITUATION: {threat}
        
        Provide immediate response plan focusing on:
        1. Asset protection (fleet & resources)
        2. Threat mitigation  
        3. Recovery planning
        
        Emergency Knowledge:
        {chr(10).join([f"- {doc.title}: {doc.content[:100]}..." for doc in emergency_strategies[:2]])}
        
        Response in JSON:
        {{
            "immediate_actions": ["action1", "action2"],
            "time_critical": true/false,
            "priority_order": ["step1", "step2", "step3"],
            "safety_level": "secure|caution|danger|critical"
        }}
        """
        
        try:
            response = await self.model.generate_content_async(prompt)
            return self._parse_strategic_response(response.text)
        except Exception as e:
            self.logger.error(f"Emergency response error: {e}")
            return {
                "immediate_actions": ["fleetsave_all_ships", "spend_all_resources"],
                "time_critical": True,
                "priority_order": ["fleetsave", "resource_protection", "assess_damage"],
                "safety_level": "critical"
            }
            
    def update_strategic_context(self, game_phase: str = None, strategy_focus: str = None, risk_tolerance: str = None):
        """Update strategic context for decision making"""
        if game_phase:
            self.game_phase = game_phase
        if strategy_focus:
            self.strategy_focus = strategy_focus  
        if risk_tolerance:
            self.risk_tolerance = risk_tolerance
            
        self.logger.info(f"🎯 Strategic context updated: {self.game_phase}/{self.strategy_focus}/{self.risk_tolerance}")
        
    def get_rag_stats(self) -> Dict[str, Any]:
        """Get RAG system statistics"""
        return self.rag.get_stats()