"""
Strategic Planner - High-level game strategy and decision making
"""

import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum


class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class StrategicGoal:
    name: str
    description: str
    priority: Priority
    estimated_time: int  # in minutes
    resources_required: Dict[str, int]
    prerequisites: List[str]


class StrategicPlanner:
    """High-level strategic planning and goal management"""
    
    def __init__(self, brain):
        self.brain = brain
        self.logger = logging.getLogger(__name__)
        self.current_goals: List[StrategicGoal] = []
        self.completed_goals: List[StrategicGoal] = []
        
    async def analyze_and_plan(self, game_state: Dict[str, Any]) -> List[StrategicGoal]:
        """Analyze game state and create strategic plan"""
        
        # Get AI analysis from Gemini brain
        ai_analysis = await self.brain.analyze_game_state(game_state)
        
        # Generate strategic goals based on analysis
        goals = await self._generate_goals(game_state, ai_analysis)
        
        # Prioritize goals
        self.current_goals = self._prioritize_goals(goals)
        
        self.logger.info(f"📋 Generated {len(self.current_goals)} strategic goals")
        return self.current_goals
        
    async def _generate_goals(self, game_state: Dict[str, Any], ai_analysis: Dict[str, Any]) -> List[StrategicGoal]:
        """Generate strategic goals based on current situation"""
        
        goals = []
        
        # Example goal generation logic (to be expanded)
        if self._needs_resource_boost(game_state):
            goals.append(StrategicGoal(
                name="Increase Resource Production",
                description="Upgrade mines to improve resource generation",
                priority=Priority.HIGH,
                estimated_time=120,  # 2 hours
                resources_required={'metal': 50000, 'crystal': 25000},
                prerequisites=[]
            ))
            
        if self._needs_fleet_expansion(game_state):
            goals.append(StrategicGoal(
                name="Expand Fleet",
                description="Build more combat ships for raids and defense",
                priority=Priority.MEDIUM,
                estimated_time=180,  # 3 hours
                resources_required={'metal': 100000, 'crystal': 50000, 'deuterium': 25000},
                prerequisites=["Increase Resource Production"]
            ))
            
        if self._needs_research(game_state):
            goals.append(StrategicGoal(
                name="Advanced Research",
                description="Research key technologies for progression",
                priority=Priority.MEDIUM,
                estimated_time=240,  # 4 hours
                resources_required={'metal': 75000, 'crystal': 100000},
                prerequisites=[]
            ))
            
        return goals
        
    def _prioritize_goals(self, goals: List[StrategicGoal]) -> List[StrategicGoal]:
        """Sort goals by priority and dependencies"""
        
        # Sort by priority first, then by prerequisites
        sorted_goals = sorted(goals, key=lambda g: (g.priority.value, len(g.prerequisites)), reverse=True)
        
        # TODO: Implement more sophisticated dependency resolution
        return sorted_goals
        
    def get_next_action(self) -> Optional[str]:
        """Get the next immediate action to take"""
        
        if not self.current_goals:
            return None
            
        # Return the highest priority goal's next action
        current_goal = self.current_goals[0]
        
        # TODO: Break down goals into specific actions
        return f"Work on: {current_goal.name}"
        
    def _needs_resource_boost(self, game_state: Dict[str, Any]) -> bool:
        """Determine if resource production needs improvement"""
        # TODO: Analyze resource production rates and storage
        return True  # Placeholder
        
    def _needs_fleet_expansion(self, game_state: Dict[str, Any]) -> bool:
        """Determine if fleet needs expansion"""
        # TODO: Analyze current fleet composition vs targets
        return True  # Placeholder
        
    def _needs_research(self, game_state: Dict[str, Any]) -> bool:
        """Determine if research should be prioritized"""
        # TODO: Analyze research progress vs game progression
        return True  # Placeholder
        
    def mark_goal_completed(self, goal_name: str):
        """Mark a goal as completed"""
        for i, goal in enumerate(self.current_goals):
            if goal.name == goal_name:
                completed_goal = self.current_goals.pop(i)
                self.completed_goals.append(completed_goal)
                self.logger.info(f"✅ Goal completed: {goal_name}")
                break
                
    def get_progress_report(self) -> Dict[str, Any]:
        """Get current progress report"""
        return {
            'active_goals': len(self.current_goals),
            'completed_goals': len(self.completed_goals),
            'current_focus': self.current_goals[0].name if self.current_goals else "No active goals",
            'estimated_completion': sum(g.estimated_time for g in self.current_goals)
        }