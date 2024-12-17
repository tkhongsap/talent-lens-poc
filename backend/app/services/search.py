from typing import List, Dict, Optional
from ..db.mongodb import get_collection, RESUMES_COLLECTION, USERS_COLLECTION
from bson import ObjectId


class SearchService:
    def __init__(self):
        self.resume_collection = get_collection(RESUMES_COLLECTION)
        self.users_collection = get_collection(USERS_COLLECTION)

    async def search_by_skills(
        self,
        skills: List[str],
        location: Optional[str] = None,
        experience_years: Optional[int] = None,
        page: int = 1,
        limit: int = 10
    ) -> Dict:
        """Search resumes by skills and other criteria."""
        skip = (page - 1) * limit
        query = {"skills": {"$in": skills}}

        if location:
            query["location"] = location

        if experience_years:
            query["total_experience"] = {"$gte": experience_years}

        cursor = self.resume_collection.find(query).skip(skip).limit(limit)
        total = await self.resume_collection.count_documents(query)
        results = await cursor.to_list(length=limit)

        return {
            "results": results,
            "total": total,
            "page": page,
            "limit": limit,
            "pages": (total + limit - 1) // limit
        }

    async def search_professionals(
        self,
        query: str,
        filters: Dict = None,
        page: int = 1,
        limit: int = 10
    ) -> Dict:
        """Search for professionals based on various criteria."""
        skip = (page - 1) * limit
        search_query = {
            "$text": {"$search": query}
        }

        if filters:
            search_query.update(filters)

        cursor = self.users_collection.find(search_query).skip(skip).limit(limit)
        total = await self.users_collection.count_documents(search_query)
        results = await cursor.to_list(length=limit)

        return {
            "results": results,
            "total": total,
            "page": page,
            "limit": limit,
            "pages": (total + limit - 1) // limit
        }

    async def get_similar_profiles(
        self,
        profile_id: str,
        limit: int = 5
    ) -> List[Dict]:
        """Find similar profiles based on skills and experience."""
        profile = await self.resume_collection.find_one({"_id": ObjectId(profile_id)})
        if not profile:
            return []

        similar_profiles = await self.resume_collection.find({
            "_id": {"$ne": ObjectId(profile_id)},
            "skills": {"$in": profile.get("skills", [])}
        }).limit(limit).to_list(length=limit)

        return similar_profiles

    async def search_by_text(
        self,
        text: str,
        collection_name: str,
        filters: Dict = None,
        page: int = 1,
        limit: int = 10
    ) -> Dict:
        """Generic text search across specified collection."""
        skip = (page - 1) * limit
        collection = get_collection(collection_name)

        search_query = {
            "$text": {"$search": text}
        }

        if filters:
            search_query.update(filters)

        cursor = collection.find(search_query).skip(skip).limit(limit)
        total = await collection.count_documents(search_query)
        results = await cursor.to_list(length=limit)

        return {
            "results": results,
            "total": total,
            "page": page,
            "limit": limit,
            "pages": (total + limit - 1) // limit
        }


# Create a singleton instance
search_service = SearchService() 