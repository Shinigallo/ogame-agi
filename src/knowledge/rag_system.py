"""
RAG System for OGame Strategic Knowledge
Retrieval-Augmented Generation for strategic decision making
"""

import os
import json
import logging
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
# import numpy as np  # Commented for minimal build
from dataclasses import dataclass

# For future implementation - would need embedding models
# from sentence_transformers import SentenceTransformer


@dataclass
class StrategyDocument:
    """Strategic knowledge document"""
    id: str
    title: str
    content: str
    category: str
    priority: int
    tags: List[str]
    embedding: Optional[List[float]] = None


class OGameRAG:
    """RAG system for OGame strategic knowledge retrieval"""
    
    def __init__(self, knowledge_base_path: str = "/app/docs/strategic_knowledge_base.md"):
        self.logger = logging.getLogger(__name__)
        self.knowledge_base_path = knowledge_base_path
        self.documents: List[StrategyDocument] = []
        self.categories = {
            "fleetsaving": 10,      # Critical - safety first
            "combat": 9,            # High - profit/loss decisions
            "resource_management": 8, # High - efficiency core
            "research": 7,          # Medium-High - long-term growth
            "fleet_composition": 6,  # Medium - tactical decisions
            "expeditions": 5,       # Medium - steady income
            "general_strategy": 4   # Lower - broad guidance
        }
        
        # TODO: Initialize embedding model for semantic search
        # self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        
        self.load_knowledge_base()
        
    def load_knowledge_base(self):
        """Load and parse the strategic knowledge base"""
        try:
            if not os.path.exists(self.knowledge_base_path):
                self.logger.error(f"Knowledge base not found: {self.knowledge_base_path}")
                return
                
            with open(self.knowledge_base_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Parse markdown content into structured documents
            self._parse_markdown_content(content)
            self.logger.info(f"📚 Loaded {len(self.documents)} strategic documents")
            
        except Exception as e:
            self.logger.error(f"Failed to load knowledge base: {e}")
            
    def _parse_markdown_content(self, content: str):
        """Parse markdown content into structured documents"""
        sections = content.split('###')  # Split by h3 headers
        
        for i, section in enumerate(sections[1:], 1):  # Skip first empty section
            lines = section.strip().split('\n')
            if not lines:
                continue
                
            title = lines[0].strip().replace('*', '').strip()
            section_content = '\n'.join(lines[1:]).strip()
            
            # Determine category and priority
            category = self._categorize_content(title, section_content)
            priority = self.categories.get(category, 3)
            
            # Extract tags
            tags = self._extract_tags(title, section_content)
            
            doc = StrategyDocument(
                id=f"doc_{i}",
                title=title,
                content=section_content,
                category=category,
                priority=priority,
                tags=tags
            )
            
            # TODO: Generate embeddings for semantic search
            # doc.embedding = self.embedder.encode(f"{title} {section_content}").tolist()
            
            self.documents.append(doc)
            
    def _categorize_content(self, title: str, content: str) -> str:
        """Categorize content based on title and content analysis"""
        title_lower = title.lower()
        content_lower = content.lower()
        
        if any(keyword in title_lower for keyword in ['fleetsave', 'fleetsaving', 'fleet save']):
            return "fleetsaving"
        elif any(keyword in title_lower for keyword in ['combat', 'battle', 'fleet composition', 'attack']):
            return "combat"  
        elif any(keyword in title_lower for keyword in ['resource', 'mining', 'production', 'miner']):
            return "resource_management"
        elif any(keyword in title_lower for keyword in ['research', 'technology', 'tech']):
            return "research"
        elif any(keyword in title_lower for keyword in ['expedition']):
            return "expeditions"
        elif any(keyword in content_lower for keyword in ['fleet', 'ship', 'destroyer', 'cruiser']):
            return "fleet_composition"
        else:
            return "general_strategy"
            
    def _extract_tags(self, title: str, content: str) -> List[str]:
        """Extract relevant tags from content"""
        tags = []
        text = f"{title} {content}".lower()
        
        # Key strategic terms
        tag_keywords = {
            'safety': ['fleetsave', 'safe', 'protect', 'security'],
            'profit': ['profit', 'resource', 'gain', 'efficiency'],
            'combat': ['attack', 'battle', 'fight', 'raid'],
            'research': ['research', 'technology', 'tech'],
            'fleet': ['fleet', 'ship', 'destroyer', 'cruiser'],
            'defense': ['defense', 'turtle', 'protect'],
            'expedition': ['expedition', 'explore', 'dark matter'],
            'timing': ['time', 'timing', 'duration', 'schedule']
        }
        
        for tag, keywords in tag_keywords.items():
            if any(keyword in text for keyword in keywords):
                tags.append(tag)
                
        return tags
        
    def retrieve_relevant_strategies(self, query: str, context: Dict[str, Any], max_results: int = 5) -> List[StrategyDocument]:
        """Retrieve most relevant strategic knowledge for a query/context"""
        
        # For now, use simple keyword matching
        # TODO: Implement semantic similarity with embeddings
        
        scored_docs = []
        query_lower = query.lower()
        
        for doc in self.documents:
            score = self._calculate_relevance_score(doc, query_lower, context)
            if score > 0:
                scored_docs.append((doc, score))
                
        # Sort by score and priority
        scored_docs.sort(key=lambda x: (x[1], x[0].priority), reverse=True)
        
        return [doc for doc, score in scored_docs[:max_results]]
        
    def _calculate_relevance_score(self, doc: StrategyDocument, query: str, context: Dict[str, Any]) -> float:
        """Calculate relevance score for a document"""
        score = 0.0
        
        # Title matching (high weight)
        if query in doc.title.lower():
            score += 10.0
            
        # Content matching (medium weight)  
        content_lower = doc.content.lower()
        query_words = query.split()
        for word in query_words:
            if word in content_lower:
                score += 2.0
                
        # Tag matching (medium weight)
        for tag in doc.tags:
            if tag in query:
                score += 3.0
                
        # Context-based relevance
        if context:
            # Prioritize safety if fleet is at risk
            if context.get('fleet_at_risk', False) and 'safety' in doc.tags:
                score += 5.0
                
            # Prioritize profit strategies if resources are low
            if context.get('low_resources', False) and 'profit' in doc.tags:
                score += 4.0
                
            # Match game phase
            game_phase = context.get('game_phase', 'early')
            if game_phase == 'early' and any(tag in doc.tags for tag in ['research', 'resource']):
                score += 2.0
            elif game_phase == 'late' and any(tag in doc.tags for tag in ['combat', 'fleet']):
                score += 2.0
                
        return score
        
    def get_strategic_advice(self, situation: str, game_state: Dict[str, Any]) -> str:
        """Get strategic advice for a specific situation"""
        
        relevant_docs = self.retrieve_relevant_strategies(situation, game_state)
        
        if not relevant_docs:
            return "No specific strategic guidance found for this situation."
            
        # Combine the most relevant strategies
        advice_parts = []
        for doc in relevant_docs[:3]:  # Top 3 most relevant
            advice_parts.append(f"**{doc.title}**:\n{doc.content[:200]}...")
            
        return "\n\n".join(advice_parts)
        
    def get_emergency_procedures(self) -> List[StrategyDocument]:
        """Get critical safety procedures (fleetsaving, etc.)"""
        return [doc for doc in self.documents if doc.category == "fleetsaving"]
        
    def get_category_guidance(self, category: str) -> List[StrategyDocument]:
        """Get all documents for a specific category"""
        return [doc for doc in self.documents if doc.category == category]
        
    def search_by_tags(self, tags: List[str]) -> List[StrategyDocument]:
        """Search documents by tags"""
        matching_docs = []
        for doc in self.documents:
            if any(tag in doc.tags for tag in tags):
                matching_docs.append(doc)
        return sorted(matching_docs, key=lambda x: x.priority, reverse=True)
        
    def get_stats(self) -> Dict[str, Any]:
        """Get RAG system statistics"""
        category_counts = {}
        for doc in self.documents:
            category_counts[doc.category] = category_counts.get(doc.category, 0) + 1
            
        return {
            'total_documents': len(self.documents),
            'categories': category_counts,
            'avg_priority': sum(doc.priority for doc in self.documents) / len(self.documents) if self.documents else 0,
            'total_tags': len(set(tag for doc in self.documents for tag in doc.tags))
        }