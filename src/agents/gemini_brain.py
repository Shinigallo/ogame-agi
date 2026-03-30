"""
Gemini AI Brain for OGame Strategic Decision Making
"""

import json
import logging
import os
from typing import Dict, List, Any
import google.generativeai as genai


class GeminiBrain:
    """AI Brain using Gemini for strategic decisions"""
    
    def __init__(self, api_key: str, model: str = "gemini-1.5-flash"):
        self.api_key = api_key
        self.model_name = model
        
        # Configure Gemini
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)
        
        self.logger = logging.getLogger('GeminiBrain')
        
        # Load knowledge base
        self.knowledge = self._load_knowledge()
        
    def _load_knowledge(self) -> str:
        """Load OGame knowledge base"""
        try:
            knowledge_files = [
                'knowledge/buildings.md',
                'knowledge/research.md', 
                'knowledge/combat.md',
                'knowledge/fleet.md',
                'knowledge/strategy.md'
            ]
            
            knowledge = []
            for file_path in knowledge_files:
                try:
                    with open(file_path, 'r') as f:
                        knowledge.append(f"## {file_path}\n{f.read()}")
                except FileNotFoundError:
                    continue
                    
            return "\n\n".join(knowledge)
        except Exception as e:
            self.logger.warning(f"Could not load knowledge base: {e}")
            return self._get_basic_knowledge()
            
    def _get_basic_knowledge(self) -> str:
        """Basic OGame knowledge if files not available"""
        return """
# OGame Strategic Knowledge

## Buildings Priority (Early Game)
1. Metal Mine (levels 1-10) - Primary resource
2. Crystal Mine (levels 1-8) - Secondary resource  
3. Deuterium Synthesizer (levels 1-6) - Advanced resource
4. Solar Plant (as needed for energy)
5. Shipyard (level 4+ for combat ships)
6. Research Lab (level 1+ for technologies)

## Research Priority
1. Energy Technology (level 1-3) - Unlocks advanced buildings
2. Combustion Drive (level 1-6) - Ship movement
3. Armor Technology (level 1-5) - Ship defense
4. Weapons Technology (level 1-5) - Ship attack
5. Shields Technology (level 1-5) - Ship shields

## Resource Management
- Keep resources balanced (3:2:1 ratio Metal:Crystal:Deuterium)
- Don't hoard resources (makes you a target)
- Invest excess in fleet or defenses
- Always fleetsave before offline

## Combat Strategy
- Light Fighters for early raids
- Heavy Fighters for stronger targets
- Cruisers for balanced attacks
- Avoid stronger players
- Always scout before attacking

## Fleetsaving
- Send all ships on deployment before going offline
- Use "Deploy" mission to safe coordinates
- Return time should be when you're back online
- Essential for survival
"""

    async def analyze_and_decide(self, context: Dict) -> List[Dict]:
        """Analyze game state and make strategic decisions"""
        try:
            game_state = context['game_state']
            strategy = context['strategy']
            cycle = context['cycle']
            
            # Create prompt for Gemini
            prompt = self._create_decision_prompt(context)
            
            # Generate response
            response = await self._query_gemini(prompt)
            
            # Parse decisions from response
            decisions = self._parse_decisions(response)
            
            self.logger.info(f"AI Brain generated {len(decisions)} decisions")
            return decisions
            
        except Exception as e:
            self.logger.error(f"Decision making failed: {e}")
            return self._get_fallback_decisions(context)
            
    def _create_decision_prompt(self, context: Dict) -> str:
        """Create prompt for Gemini"""
        state = context['game_state']
        
        prompt = f"""
You are an expert OGame strategist controlling an autonomous bot.

KNOWLEDGE BASE:
{self.knowledge}

CURRENT GAME STATE:
- Resources: Metal={state['resources']['metal']}, Crystal={state['resources']['crystal']}, Deuterium={state['resources']['deuterium']}
- Energy: {state['resources']['energy']}
- Strategy: {context['strategy']}
- Risk Tolerance: {context['risk_tolerance']}
- Cycle: {context['cycle']}
- Auto Fleetsave: {context['auto_fleetsave']}

DECISION RULES:
1. Prioritize resource production in early game
2. Balance metal:crystal:deuterium roughly 3:2:1
3. Build fleet when resources are sufficient
4. Research key technologies progressively
5. Always fleetsave if auto_fleetsave=true
6. Avoid risky actions if risk_tolerance=low

OUTPUT FORMAT (JSON):
Return a JSON array of actions to execute:

[
  {{
    "type": "build",
    "target": "metal_mine",
    "priority": 1,
    "reason": "Need more metal production"
  }},
  {{
    "type": "research", 
    "target": "energy_technology",
    "priority": 2,
    "reason": "Unlock advanced buildings"
  }},
  {{
    "type": "fleet_dispatch",
    "mission": "deploy",
    "target": "1:1:1",
    "ships": {{"light_fighter": 10}},
    "priority": 3,
    "reason": "Fleetsave before offline"
  }}
]

Respond ONLY with valid JSON array. No other text.
"""
        return prompt
        
    async def _query_gemini(self, prompt: str) -> str:
        """Query Gemini API"""
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            self.logger.error(f"Gemini query failed: {e}")
            raise
            
    def _parse_decisions(self, response: str) -> List[Dict]:
        """Parse decisions from Gemini response"""
        try:
            # Extract JSON from response
            response = response.strip()
            if response.startswith('```'):
                # Remove code block markers
                lines = response.split('\n')
                response = '\n'.join(lines[1:-1])
                
            decisions = json.loads(response)
            
            # Validate decisions
            valid_decisions = []
            for decision in decisions:
                if self._validate_decision(decision):
                    valid_decisions.append(decision)
                else:
                    self.logger.warning(f"Invalid decision: {decision}")
                    
            return valid_decisions
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse JSON response: {e}")
            return []
        except Exception as e:
            self.logger.error(f"Decision parsing failed: {e}")
            return []
            
    def _validate_decision(self, decision: Dict) -> bool:
        """Validate a decision structure"""
        required_fields = ['type', 'priority']
        
        if not all(field in decision for field in required_fields):
            return False
            
        valid_types = ['build', 'research', 'fleet_dispatch', 'wait']
        if decision['type'] not in valid_types:
            return False
            
        return True
        
    def _get_fallback_decisions(self, context: Dict) -> List[Dict]:
        """Fallback decisions if AI fails"""
        resources = context['game_state']['resources']
        
        decisions = []
        
        # Simple fallback logic
        if resources['metal'] < 1000:
            decisions.append({
                "type": "build",
                "target": "metal_mine", 
                "priority": 1,
                "reason": "Fallback: Need metal"
            })
        elif resources['crystal'] < 500:
            decisions.append({
                "type": "build",
                "target": "crystal_mine",
                "priority": 1, 
                "reason": "Fallback: Need crystal"
            })
        else:
            decisions.append({
                "type": "wait",
                "duration": 300,
                "priority": 1,
                "reason": "Fallback: Wait for resources"
            })
            
        return decisions