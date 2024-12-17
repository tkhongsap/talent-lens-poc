from typing import Dict, List, Optional
from datetime import datetime, timedelta
from ..db.mongodb import get_collection, ANALYTICS_COLLECTION
from bson import ObjectId


class AnalyticsService:
    def __init__(self):
        self.collection = get_collection(ANALYTICS_COLLECTION)

    async def track_event(
        self,
        user_id: str,
        event_type: str,
        event_data: Dict
    ) -> Dict:
        """Track a user event in the system."""
        event = {
            "user_id": ObjectId(user_id),
            "event_type": event_type,
            "event_data": event_data,
            "timestamp": datetime.utcnow()
        }
        
        result = await self.collection.insert_one(event)
        event["_id"] = result.inserted_id
        return event

    async def get_user_activity(
        self,
        user_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict]:
        """Get all activity for a specific user within a date range."""
        query = {"user_id": ObjectId(user_id)}
        
        if start_date or end_date:
            query["timestamp"] = {}
            if start_date:
                query["timestamp"]["$gte"] = start_date
            if end_date:
                query["timestamp"]["$lte"] = end_date

        return await self.collection.find(query).sort("timestamp", -1).to_list(None)

    async def get_popular_searches(
        self,
        days: int = 7,
        limit: int = 10
    ) -> List[Dict]:
        """Get most popular search terms in the last N days."""
        start_date = datetime.utcnow() - timedelta(days=days)
        
        pipeline = [
            {
                "$match": {
                    "event_type": "search",
                    "timestamp": {"$gte": start_date}
                }
            },
            {
                "$group": {
                    "_id": "$event_data.query",
                    "count": {"$sum": 1},
                    "last_searched": {"$max": "$timestamp"}
                }
            },
            {"$sort": {"count": -1}},
            {"$limit": limit}
        ]
        
        return await self.collection.aggregate(pipeline).to_list(None)

    async def get_user_engagement_metrics(
        self,
        days: int = 30
    ) -> Dict:
        """Get user engagement metrics for the last N days."""
        start_date = datetime.utcnow() - timedelta(days=days)
        
        pipeline = [
            {
                "$match": {
                    "timestamp": {"$gte": start_date}
                }
            },
            {
                "$group": {
                    "_id": {
                        "user": "$user_id",
                        "date": {"$dateToString": {"format": "%Y-%m-%d", "date": "$timestamp"}}
                    },
                    "events": {"$sum": 1}
                }
            },
            {
                "$group": {
                    "_id": "$_id.date",
                    "active_users": {"$sum": 1},
                    "total_events": {"$sum": "$events"}
                }
            },
            {"$sort": {"_id": 1}}
        ]
        
        daily_metrics = await self.collection.aggregate(pipeline).to_list(None)
        
        return {
            "daily_metrics": daily_metrics,
            "total_days": days,
            "average_daily_active_users": sum(d["active_users"] for d in daily_metrics) / len(daily_metrics) if daily_metrics else 0,
            "total_events": sum(d["total_events"] for d in daily_metrics)
        }

    async def get_skill_trends(
        self,
        days: int = 30,
        limit: int = 10
    ) -> List[Dict]:
        """Get trending skills based on search and profile views."""
        start_date = datetime.utcnow() - timedelta(days=days)
        
        pipeline = [
            {
                "$match": {
                    "timestamp": {"$gte": start_date},
                    "event_type": {"$in": ["search", "profile_view"]},
                    "event_data.skills": {"$exists": True}
                }
            },
            {"$unwind": "$event_data.skills"},
            {
                "$group": {
                    "_id": "$event_data.skills",
                    "count": {"$sum": 1},
                    "last_seen": {"$max": "$timestamp"}
                }
            },
            {"$sort": {"count": -1}},
            {"$limit": limit}
        ]
        
        return await self.collection.aggregate(pipeline).to_list(None)


# Create a singleton instance
analytics_service = AnalyticsService() 