"""
University Info Service
Handles all CRUD operations for university information
"""
from database import get_supabase_client
from typing import List, Dict, Optional

class UniversityInfoService:
    def __init__(self):
        self.supabase = get_supabase_client()
        self.table_name = "university_info"

    def create_info(self, category: str, info: str) -> Dict:
        """
        Create new university information entry
        """
        try:
            data = {
                "category": category.strip().lower(),
                "info": info.strip()
            }
            
            result = self.supabase.table(self.table_name).insert(data).execute()
            
            if result.data:
                return {
                    "success": True,
                    "message": "University info created successfully",
                    "data": result.data[0]
                }
            else:
                return {
                    "success": False,
                    "message": "Failed to create university info",
                    "data": None
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Error creating university info: {str(e)}",
                "data": None
            }

    def get_all_info(self) -> Dict:
        """
        Get all university information
        """
        try:
            result = self.supabase.table(self.table_name).select("*").order("category", desc=False).execute()
            
            return {
                "success": True,
                "message": "University info retrieved successfully",
                "data": result.data
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error retrieving university info: {str(e)}",
                "data": []
            }

    def get_info_by_id(self, info_id: int) -> Dict:
        """
        Get university information by ID
        """
        try:
            result = self.supabase.table(self.table_name).select("*").eq("id", info_id).execute()
            
            if result.data:
                return {
                    "success": True,
                    "message": "University info retrieved successfully",
                    "data": result.data[0]
                }
            else:
                return {
                    "success": False,
                    "message": "University info not found",
                    "data": None
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Error retrieving university info: {str(e)}",
                "data": None
            }

    def get_info_by_category(self, category: str) -> Dict:
        """
        Get university information by category
        """
        try:
            result = self.supabase.table(self.table_name).select("*").eq("category", category.strip().lower()).execute()
            
            return {
                "success": True,
                "message": "University info retrieved successfully",
                "data": result.data
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error retrieving university info: {str(e)}",
                "data": []
            }

    def update_info(self, info_id: int, category: str = None, info: str = None) -> Dict:
        """
        Update university information
        """
        try:
            # Check if record exists
            existing = self.supabase.table(self.table_name).select("*").eq("id", info_id).execute()
            
            if not existing.data:
                return {
                    "success": False,
                    "message": "University info not found",
                    "data": None
                }

            # Prepare update data
            update_data = {}
            if category is not None:
                update_data["category"] = category.strip().lower()
            if info is not None:
                update_data["info"] = info.strip()

            if not update_data:
                return {
                    "success": False,
                    "message": "No data provided for update",
                    "data": None
                }

            result = self.supabase.table(self.table_name).update(update_data).eq("id", info_id).execute()
            
            if result.data:
                return {
                    "success": True,
                    "message": "University info updated successfully",
                    "data": result.data[0]
                }
            else:
                return {
                    "success": False,
                    "message": "Failed to update university info",
                    "data": None
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Error updating university info: {str(e)}",
                "data": None
            }

    def delete_info(self, info_id: int) -> Dict:
        """
        Delete university information by ID
        """
        try:
            # Check if record exists
            existing = self.supabase.table(self.table_name).select("*").eq("id", info_id).execute()
            
            if not existing.data:
                return {
                    "success": False,
                    "message": "University info not found",
                    "data": None
                }

            result = self.supabase.table(self.table_name).delete().eq("id", info_id).execute()
            
            return {
                "success": True,
                "message": "University info deleted successfully",
                "data": existing.data[0]
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error deleting university info: {str(e)}",
                "data": None
            }

    def search_info(self, query: str) -> Dict:
        """
        Search university information by keyword in category or info content
        """
        try:
            # Search in both category and info fields
            result = self.supabase.table(self.table_name).select("*").or_(
                f"category.ilike.%{query.strip()}%,info.ilike.%{query.strip()}%"
            ).execute()
            
            return {
                "success": True,
                "message": "Search completed successfully",
                "data": result.data
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error searching university info: {str(e)}",
                "data": []
            }

    def get_categories(self) -> Dict:
        """
        Get all unique categories
        """
        try:
            result = self.supabase.table(self.table_name).select("category").execute()
            
            categories = list(set([item["category"] for item in result.data]))
            categories.sort()
            
            return {
                "success": True,
                "message": "Categories retrieved successfully",
                "data": categories
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error retrieving categories: {str(e)}",
                "data": []
            }
