import datetime
import motor.motor_asyncio
from config import Config

from typing import List, Dict, Any

class Database:
    def __init__(self, uri: str, database_name: str):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self.client[database_name]
        self.col = self.db['users']  # Reference to the specific collection

    # In your database handling class
    async def update_user_subscription(self, user_id: int, plan: str, validity_end: datetime):
        result = await self.col.update_one(
            {"_id": user_id},
            {
                "$set": {
                    "plan": plan,
                    "validity_end": validity_end
                }
            },
            upsert=True  # Create the document if it doesn't exist
        )
        return result

    async def delete_user(self, user_id: int):
        try:
            # Use the correct field for user identification, e.g., "_id" or "user_id"
            result = await self.col.delete_many({"user_id": user_id})  # Adjust this field as necessary
            
            if result:
                print(f"Deleted {result.deleted_count} entries for user {user_id}")
            return result
        except Exception as e:
            print(f"Error deleting user {user_id}: {e}")
            return None


    async def get_user_subscription(self, user_id: int) -> Dict[str, Any]:
        return await self.col.find_one({"_id": user_id})

    async def get_all_users(self) -> List[Dict[str, Any]]:
        collection = self.db['users']
        return await collection.find().to_list(length=None)

    async def get_premium_users(self) -> List[Dict[str, Any]]:
        now = datetime.datetime.now()  # Use full path to datetime
        try:
            # Debugging: Log the current datetime
            print(f"Current datetime for comparison: {now}")

            result = await self.col.find({
                'plan': {'$ne': 'Non-Premium'},
                'validity_end': {'$gte': now}
            }).to_list(length=None)

            # Debugging: Log the result
            print(f"Premium users found: {result}")

            return result

        except Exception as e:
            # Log the error
            print(f"Error fetching premium users: {e}")
            return []
        
    async def remove_user(self, user_id: int):
        result = await self.col.delete_one({"_id": user_id})
        if result.deleted_count == 0:
            raise Exception(f"No user found with ID {user_id}")
    
    async def total_users_count(self) -> int:
        # Get the total count of users
        return await self.col.count_documents({})
    
    async def getid(self) -> List[str]:
        # Fetch all user IDs
        users = await self.col.find({}, {'_id': 1}).to_list(length=None)
        return [str(user['_id']) for user in users]
    
    async def delete(self, user_id: str):
        # Delete a user by ID
        await self.col.delete_one({'_id': user_id})
    
    async def get_user(self, user_id: str) -> Dict[str, Any]:
        # Get a user document by ID
        return await self.col.find_one({'_id': user_id})
    
    async def uploadlimit(self, chat_id, limit):
        await self.col.update_one({"_id": chat_id}, {"$set": {"uploadlimit": limit}})

    async def usertype(self, chat_id, user_type):
        await self.col.update_one({"_id": chat_id}, {"$set": {"usertype": user_type}})

    async def addpre(self, chat_id):
        date = self.add_date()
        await self.col.update_one({"_id": chat_id}, {"$set": {"prexdate": date[0]}})

    async def addpredata(self, chat_id):
        await self.col.update_one({"_id": chat_id}, {"$set": {"prexdate": None}})

    async def find_one(self, chat_id):
        user = await self.col.find_one({"_id": chat_id})
        print(f"Data found for user ID {chat_id}: {user}")
        return user

    async def total_users_count(self):
        return await self.col.count_documents({})

    def add_date(self):
        now = datetime.datetime.now()
        return now, now.date()

    async def getid(self):
        values = []
        async for key in self.col.find():
            id = key["_id"]
            values.append(id)
        return values

    async def delete(self, id):
        await self.col.delete_one({"_id": id})

    async def used_limit(self, chat_id, used):
        await self.col.update_one({"_id": chat_id}, {"$set": {"used_limit": used}})

    def new_user(self, id):
        return dict(
            _id=int(id),
            file_id=None,
            caption=None,
            prefix=None,
            suffix=None,
            metadata=False,
            metadata_code=""" -map 0 -c:s copy -c:a copy -c:v copy -metadata title="Powered By:- @Kdramaland" -metadata author="@Snowball_Official" -metadata:s:s title="Subtitled By :- @Kdramaland" -metadata:s:a title="By :- @Kdramaland" -metadata:s:v title="By:- @Snowball_Official" """
        )

    async def add_user(self, b, m, send_log):
        u = m.from_user
        if not await self.is_user_exist(u.id):
            user = self.new_user(u.id)
            await self.col.insert_one(user)
            await send_log(b, u)

    async def is_user_exist(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return bool(user)

    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def delete_user(self, user_id):
        await self.col.delete_many({'_id': int(user_id)})

    async def set_thumbnail(self, id, file_id):
        await self.col.update_one({'_id': int(id)}, {'$set': {'file_id': file_id}})

    async def get_thumbnail(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('file_id', None)

    async def set_caption(self, id, caption):
        await self.col.update_one({'_id': int(id)}, {'$set': {'caption': caption}})

    async def get_caption(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('caption', None)

    async def set_prefix(self, id, prefix):
        await self.col.update_one({'_id': int(id)}, {'$set': {'prefix': prefix}})

    async def get_prefix(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('prefix', None)

    async def set_suffix(self, id, suffix):
        await self.col.update_one({'_id': int(id)}, {'$set': {'suffix': suffix}})

    async def get_suffix(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('suffix', None)

    async def set_metadata(self, id, bool_meta):
        await self.col.update_one({'_id': int(id)}, {'$set': {'metadata': bool_meta}})

    async def get_metadata(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('metadata', None)

    async def set_metadata_code(self, id, metadata_code):
        await self.col.update_one({'_id': int(id)}, {'$set': {'metadata_code': metadata_code}})

    async def get_metadata_code(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('metadata_code', None)

    # New methods to set and get media type
    async def set_media_type(self, user_id, media_type):
        """Set the media type preference for a user."""
        await self.col.update_one(
            {"_id": user_id},
            {"$set": {"media_type": media_type}},
            upsert=True
        )

    async def get_media_type(self, user_id):
        """Retrieve the media type preference for a user."""
        user_data = await self.col.find_one({"_id": user_id})
        return user_data.get("media_type") if user_data else None

    # Methods to set and get auto rename status
    async def set_auto_rename_status(self, user_id, status):
        """Set the auto rename status for a user."""
        await self.col.update_one({"_id": user_id}, {"$set": {"auto_rename_status": status}}, upsert=True)

    async def get_auto_rename_status(self, user_id):
        """Get the auto rename status for a user."""
        user_data = await self.col.find_one({"_id": user_id})
        return user_data.get("auto_rename_status", "❌") if user_data else "❌"

    # Methods to set and get screenshot response
    async def set_screenshot_response(self, user_id, response):
        """Set the screenshot response for a user."""
        await self.col.update_one({"_id": user_id}, {"$set": {"screenshot_response": response}}, upsert=True)

    async def get_screenshot_response(self, user_id):
        """Get the screenshot response for a user."""
        user_data = await self.col.find_one({"_id": user_id})
        return user_data.get("screenshot_response", "❌") if user_data else "❌"
    
    # Methods to set and get sample video response
    async def set_sample_video_response(self, user_id, response):
        """Set the sample video response for a user."""
        await self.col.update_one({"_id": user_id}, {"$set": {"sample_video_response": response}}, upsert=True)

    async def get_sample_video_response(self, user_id):
        """Get the sample video response for a user."""
        user_data = await self.col.find_one({"_id": user_id})
        return user_data.get("sample_video_response", "❌") if user_data else "❌"

    async def get_preset1(self, user_id: int) -> int:
        """Fetch preset1 value (screenshot count) from the database and ensure it is an integer."""
        user = await self.col.find_one({"user_id": user_id})
        if user is None or "preset1" not in user:
            await self.set_preset1(user_id, 10)  # Set default value of 10
            return 10  # Return the default value
        return int(user.get("preset1", 10))  # Default value of 10 if not set

    async def set_preset1(self, user_id: int, value: int):
        """Set preset1 value (screenshot count) for the user."""
        await self.col.update_one(
            {"user_id": user_id},
            {"$set": {"preset1": value}},
            upsert=True
        )

    async def get_preset2(self, user_id: int) -> int:
        """Fetch preset2 value (sample video duration) from the database and ensure it is an integer."""
        user = await self.col.find_one({"user_id": user_id})
        if user is None or "preset2" not in user:
            await self.set_preset2(user_id, 30)  # Set default value of 30
            return 30  # Return the default value
        return int(user.get("preset2", 30))  # Default value of 30 if not set

    async def set_preset2(self, user_id: int, value: int):
        """Set preset2 value (sample video duration) for the user."""
        await self.col.update_one(
            {"user_id": user_id},
            {"$set": {"preset2": value}},
            upsert=True
        )

    # Methods to set and get auto rename format
    async def set_auto_rename_format(self, user_id, format):
        """Set the auto rename format for a user."""
        await self.col.update_one({"_id": user_id}, {"$set": {"auto_rename_format": format}}, upsert=True)

    async def get_auto_rename_format(self, user_id):
        """Get the auto rename format for a user."""
        user_data = await self.col.find_one({"_id": user_id})
        return user_data.get("auto_rename_format", "Default Format") if user_data else "Default Format"

db = Database(Config.DB_URL, Config.DB_NAME)
