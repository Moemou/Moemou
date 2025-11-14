"""
Knowledge base loader for skincare, dermatology, and biomarker information.
"""

import json
import os
from typing import Dict, List, Optional, Any
from pathlib import Path


class KnowledgeBase:
    """Centralized knowledge base for skincare expertise."""

    def __init__(self, knowledge_path: str = "./src/knowledge"):
        self.knowledge_path = Path(knowledge_path)
        self.conditions: Dict[str, Any] = {}
        self.ingredients: Dict[str, Any] = {}
        self.products: Dict[str, Any] = {}
        self.biomarkers: Dict[str, Any] = {}
        self._load_all()

    def _load_json(self, filename: str) -> Dict:
        """Load JSON file from knowledge base."""
        file_path = self.knowledge_path / filename
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _load_all(self):
        """Load all knowledge base files."""
        self.conditions = self._load_json("conditions.json")
        self.ingredients = self._load_json("ingredients.json")
        self.products = self._load_json("products.json")
        self.biomarkers = self._load_json("biomarkers.json")

    def get_condition(self, condition_name: str) -> Optional[Dict]:
        """Get information about a specific skin condition."""
        return self.conditions.get(condition_name.lower())

    def get_ingredient(self, ingredient_name: str) -> Optional[Dict]:
        """Get information about a specific ingredient."""
        return self.ingredients.get(ingredient_name.lower())

    def get_product_category(self, category: str) -> List[Dict]:
        """Get products in a specific category."""
        return [p for p in self.products.get("products", []) if p.get("category") == category]

    def get_biomarker_info(self, biomarker_name: str) -> Optional[Dict]:
        """Get information about a specific biomarker."""
        return self.biomarkers.get(biomarker_name.lower())

    def search_ingredients_by_concern(self, concern: str) -> List[Dict]:
        """Search ingredients that address a specific concern."""
        results = []
        for name, info in self.ingredients.items():
            if concern.lower() in [c.lower() for c in info.get("addresses", [])]:
                results.append({"name": name, **info})
        return results

    def get_acne_treatments(self) -> Dict:
        """Get specialized acne treatment information."""
        acne_info = self.conditions.get("acne", {})
        return {
            "types": acne_info.get("types", {}),
            "treatments": acne_info.get("treatments", []),
            "recommended_ingredients": acne_info.get("recommended_ingredients", []),
            "lifestyle_factors": acne_info.get("lifestyle_factors", [])
        }

    def interpret_biomarker(self, biomarker_name: str, value: str) -> Optional[str]:
        """Interpret a biomarker value."""
        biomarker = self.get_biomarker_info(biomarker_name)
        if biomarker and "interpretations" in biomarker:
            return biomarker["interpretations"].get(value.lower())
        return None

    def get_contraindications(self, ingredient_name: str) -> List[str]:
        """Get contraindications for an ingredient."""
        ingredient = self.get_ingredient(ingredient_name)
        return ingredient.get("contraindications", []) if ingredient else []

    def get_ingredient_combinations(self, ingredient_name: str) -> Dict:
        """Get information about ingredient combinations."""
        ingredient = self.get_ingredient(ingredient_name)
        if ingredient:
            return {
                "synergistic": ingredient.get("synergistic_with", []),
                "avoid_with": ingredient.get("avoid_with", [])
            }
        return {"synergistic": [], "avoid_with": []}
