"""
OGame AGI Brain Test - Direct implementation without Docker
Test core strategic AI with manual browser interaction
"""

import asyncio
import json
from pathlib import Path


class MockGameState:
    """Mock OGame game state for testing"""
    
    def __init__(self):
        self.resources = {'metal': 500, 'crystal': 500, 'deuterium': 0, 'energy': 0}
        self.buildings = {
            'metal_mine': 1,
            'crystal_mine': 1,
            'deuterium_synthesizer': 1,
            'solar_plant': 1,
            'robot_factory': 0,
            'nanite_factory': 0,
            'shipyard': 0
        }
        self.research = {}
        self.fleet = {}
        
    def can_afford(self, cost):
        """Check if we can afford the given cost"""
        return all(self.resources.get(resource, 0) >= amount for resource, amount in cost.items())
        
    def spend_resources(self, cost):
        """Spend resources"""
        for resource, amount in cost.items():
            self.resources[resource] -= amount
            
    def get_building_cost(self, building_name, level):
        """Calculate building cost (simplified formula)"""
        base_costs = {
            'metal_mine': {'metal': 60, 'crystal': 15},
            'crystal_mine': {'metal': 48, 'crystal': 24},
            'deuterium_synthesizer': {'metal': 225, 'crystal': 75},
            'solar_plant': {'metal': 75, 'crystal': 30},
            'robot_factory': {'metal': 400, 'crystal': 120, 'deuterium': 200},
            'shipyard': {'metal': 400, 'crystal': 200, 'deuterium': 100}
        }
        
        if building_name not in base_costs:
            return {}
            
        base = base_costs[building_name]
        multiplier = 1.5 ** (level - 1)  # Each level costs 1.5x more
        
        return {resource: int(cost * multiplier) for resource, cost in base.items()}


class OGameStrategicAI:
    """Strategic AI for OGame decision making"""
    
    def __init__(self):
        self.knowledge_base = {
            'early_game_priorities': [
                "Metal Mine is the foundation - upgrade to level 5-7 first",
                "Energy balance is critical - upgrade Solar Plant when needed", 
                "Crystal Mine level 3-4 for research prerequisites",
                "Never build fleet until economy is established",
                "Always ensure positive energy production"
            ],
            'building_priorities': {
                'phase_1': ['metal_mine', 'solar_plant'],  # Levels 1-5
                'phase_2': ['crystal_mine', 'deuterium_synthesizer'],  # Levels 2-4
                'phase_3': ['robot_factory', 'shipyard']  # Later game
            }
        }
        
    def analyze_game_state(self, game_state):
        """Analyze current game state and recommend actions"""
        
        recommendations = []
        
        # Check energy balance first
        if game_state.resources['energy'] <= 0:
            cost = game_state.get_building_cost('solar_plant', game_state.buildings['solar_plant'] + 1)
            if game_state.can_afford(cost):
                recommendations.append({
                    'priority': 1,
                    'action': 'upgrade_solar_plant',
                    'reasoning': 'Energy deficit is limiting production - critical bottleneck',
                    'cost': cost,
                    'urgency': 'critical'
                })
        
        # Metal mine priority (foundation of economy)
        if game_state.buildings['metal_mine'] < 6:
            cost = game_state.get_building_cost('metal_mine', game_state.buildings['metal_mine'] + 1)
            if game_state.can_afford(cost):
                recommendations.append({
                    'priority': 2,
                    'action': 'upgrade_metal_mine',
                    'reasoning': 'Metal is foundation of economy - priority until level 6',
                    'cost': cost,
                    'urgency': 'high'
                })
        
        # Crystal mine for research
        if game_state.buildings['crystal_mine'] < 4 and game_state.buildings['metal_mine'] >= 3:
            cost = game_state.get_building_cost('crystal_mine', game_state.buildings['crystal_mine'] + 1)
            if game_state.can_afford(cost):
                recommendations.append({
                    'priority': 3,
                    'action': 'upgrade_crystal_mine',
                    'reasoning': 'Crystal needed for research and advanced buildings',
                    'cost': cost,
                    'urgency': 'medium'
                })
        
        # Deuterium for advanced gameplay
        if game_state.buildings['deuterium_synthesizer'] < 2 and game_state.buildings['metal_mine'] >= 4:
            cost = game_state.get_building_cost('deuterium_synthesizer', game_state.buildings['deuterium_synthesizer'] + 1)
            if game_state.can_afford(cost):
                recommendations.append({
                    'priority': 4,
                    'action': 'upgrade_deuterium_synthesizer', 
                    'reasoning': 'Deuterium needed for fleet and research',
                    'cost': cost,
                    'urgency': 'low'
                })
        
        return sorted(recommendations, key=lambda x: x['priority'])
    
    def get_strategic_advice(self, game_state):
        """Get comprehensive strategic advice"""
        
        recommendations = self.analyze_game_state(game_state)
        
        advice = {
            'immediate_actions': recommendations[:3],
            'strategy_phase': self._determine_game_phase(game_state),
            'economic_analysis': self._analyze_economy(game_state),
            'next_goals': self._get_next_goals(game_state)
        }
        
        return advice
    
    def _determine_game_phase(self, game_state):
        """Determine current game phase"""
        metal_level = game_state.buildings['metal_mine']
        crystal_level = game_state.buildings['crystal_mine']
        
        if metal_level <= 3:
            return "early_foundation"
        elif metal_level <= 6:
            return "economic_expansion"
        elif game_state.buildings.get('shipyard', 0) == 0:
            return "infrastructure_buildup"
        else:
            return "fleet_development"
    
    def _analyze_economy(self, game_state):
        """Analyze economic state"""
        return {
            'production_ratio': f"Metal:{game_state.buildings['metal_mine']} Crystal:{game_state.buildings['crystal_mine']} Deut:{game_state.buildings['deuterium_synthesizer']}",
            'energy_status': 'deficit' if game_state.resources['energy'] <= 0 else 'surplus',
            'resource_storage': sum(game_state.resources.values()),
            'infrastructure_level': sum(game_state.buildings.values())
        }
    
    def _get_next_goals(self, game_state):
        """Get next strategic goals"""
        phase = self._determine_game_phase(game_state)
        
        goals = {
            'early_foundation': ['Metal Mine level 5', 'Energy stability', 'Crystal Mine level 3'],
            'economic_expansion': ['Metal Mine level 8', 'Crystal Mine level 5', 'Deuterium level 3'],
            'infrastructure_buildup': ['Robot Factory', 'Research Lab', 'Shipyard'],
            'fleet_development': ['First fleet units', 'Research priorities', 'Colony planning']
        }
        
        return goals.get(phase, ['Continue balanced development'])


async def main():
    """Test OGame Strategic AI"""
    
    print("🚀 OGame Strategic AI Test - Scorpius Universe")
    print("=" * 55)
    
    # Initialize game state (TestAgent2026 starting conditions)
    game_state = MockGameState()
    ai = OGameStrategicAI()
    
    print(f"📊 Starting Game State:")
    print(f"   Resources: {game_state.resources}")
    print(f"   Buildings: {game_state.buildings}")
    
    # Get strategic analysis
    advice = ai.get_strategic_advice(game_state)
    
    print(f"\n🧠 Strategic Analysis:")
    print(f"   Game Phase: {advice['strategy_phase']}")
    print(f"   Economy: {advice['economic_analysis']}")
    
    print(f"\n🎯 Immediate Actions:")
    for i, action in enumerate(advice['immediate_actions'], 1):
        print(f"   {i}. {action['action']}")
        print(f"      Reasoning: {action['reasoning']}")
        print(f"      Cost: {action['cost']}")
        print(f"      Urgency: {action['urgency']}")
        print()
    
    print(f"📋 Next Goals: {', '.join(advice['next_goals'])}")
    
    # Simulate executing first action
    if advice['immediate_actions']:
        first_action = advice['immediate_actions'][0]
        print(f"\n🎮 Simulating: {first_action['action']}")
        
        if game_state.can_afford(first_action['cost']):
            game_state.spend_resources(first_action['cost'])
            
            if 'metal_mine' in first_action['action']:
                game_state.buildings['metal_mine'] += 1
            elif 'crystal_mine' in first_action['action']:
                game_state.buildings['crystal_mine'] += 1
            elif 'solar_plant' in first_action['action']:
                game_state.buildings['solar_plant'] += 1
                game_state.resources['energy'] += 20  # Simplified energy gain
            
            print(f"   ✅ Action completed!")
            print(f"   💰 Resources after: {game_state.resources}")
            print(f"   🏗️ Buildings after: {game_state.buildings}")
        else:
            print(f"   ❌ Cannot afford: {first_action['cost']}")
    
    print(f"\n🎉 Strategic AI Test Complete!")
    print(f"📌 Ready for integration with Scorpius TestAgent2026 account")


if __name__ == "__main__":
    asyncio.run(main())