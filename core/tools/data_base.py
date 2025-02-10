from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId
from dotenv import load_dotenv
import os

# Connect to MongoDB
load_dotenv()
# Load environment variables from .env file
mongo_uri = os.getenv("MONGO_URI")
database_name = os.getenv("DATABASE_NAME")
users_collection_name = os.getenv("USERS_COLLECTION")
bots_collection_name = os.getenv("BOTS_COLLECTION")

client = MongoClient(mongo_uri)
db = client[database_name]
users_collection = db[users_collection_name]
bots_collection = db[bots_collection_name]


# Helper: Create or retrieve an ObjectId
def get_object_id(id_str=None):
    return ObjectId(id_str) if id_str else ObjectId()

# Function to create a new bot with detailed attributes
def create_bot(style, gender, ethnicity, age, eye_color, hair_style, hair_color, body_type, breast_size,
               butt_size, personality, occupation, hobbies, clothing, relationship):
    bot_data = {
        "style": style,
        "gender": gender,
        "ethnicity": ethnicity,
        "age": age,
        "eye_color": eye_color,
        "hair_style": hair_style,
        "hair_color": hair_color,
        "body_type": body_type,
        "breast_size": breast_size,
        "butt_size": butt_size,
        "personality": personality,
        "occupation": occupation,
        "hobbies": hobbies,
        "clothing": clothing,
        "relationship": relationship,
    }
    result = bots_collection.insert_one(bot_data)
    print(f"Bot created with ID: {result.inserted_id}")
    return result.inserted_id

# Function to update bot details
def update_bot(bot_id, updates):
    result = bots_collection.update_one({"_id": get_object_id(bot_id)}, {"$set": updates})
    print(f"Bot {'updated' if result.modified_count > 0 else 'not found or not updated'} with ID: {bot_id}")

# Function to create a user with default modes array and additional attributes
def create_user(chat_id, bot_id, language=None, level=-1, weaknesses=None, strengths=None):
    user_data = {
        "chat_id": chat_id,
        "modes": {},  # empty modes dictionary to start with
        "current_mode": None,
        "bot_id": get_object_id(bot_id) or "" or None,
        "languages": [],
        "last_active": datetime.now(),
        "sentiments": {},  # initial empty sentiments hashmap
        "level": level,
        "weaknesses": weaknesses or [],
        "strengths": strengths or [],
    }
    result = users_collection.insert_one(user_data)
    print(f"User created with ID: {result.inserted_id}")

# Function to create a new mode for a user
def add_mode_to_user(chat_id, mode_name, language, prompt, initial_messages=None):
    initial_messages = initial_messages or []
    mode_data = {
        "messages": initial_messages,
        "language": language,
        "prompt": prompt  # can be mutable if it needs to change dynamically
    }
    # Use the `$set` operator to add or update the mode in the `modes` dictionary
    result = users_collection.update_one(
        {"chat_id": chat_id},
        {"$set": {f"modes.{mode_name}": mode_data}, "$set": {"current_mode": mode_name}}
    )
    if result.modified_count > 0:
        print(f"Mode '{mode_name}' added or updated for user '{chat_id}'.")
    else:
        print(f"User '{chat_id}' not found or mode could not be added.")

# Function to add messages to the current mode of a user
def add_messages_to_current_mode(chat_id, messages):
    user = users_collection.find_one({"chat_id": chat_id}, {"current_mode": 1, "modes": 1})
    if user and user["current_mode"]:
        current_mode = user["current_mode"]
        result = users_collection.update_one(
            {"chat_id": chat_id},
            {"$push": {f"modes.{current_mode}.messages": {"$each": messages}}}
        )
        print(f"Messages added to mode '{current_mode}' for user '{chat_id}'.")
    else:
        print(f"User '{chat_id}' does not have a current mode set.")

# Function to retrieve all information for a specific mode
def get_mode_info(chat_id, mode_name):
    user = users_collection.find_one({"chat_id": chat_id}, {"modes": 1})
    if user and "modes" in user and mode_name in user["modes"]:
        mode_info = user["modes"][mode_name]
        print(f"Information for mode '{mode_name}' of user '{chat_id}':", mode_info)
        return mode_info
    else:
        print(f"Mode '{mode_name}' not found for user '{chat_id}'.")
        return None

# Function to update all user data
def update_user(chat_id, bot_id=None, language=None, level=None, weaknesses=None, strengths=None, modes=None, current_mode=None, sentiments=None):
    # Prepare the fields to update
    update_data = {
        "bot_id": get_object_id(bot_id) if bot_id is not None else None,
        "languages": language if language is not None else [],
        "last_active": datetime.now(),  # update last active time
        "level": level,
        "weaknesses": weaknesses or [],
        "strengths": strengths or [],
        "modes": modes if modes is not None else {},
        "current_mode": current_mode,
        "sentiments": sentiments if sentiments is not None else {},
    }

    # Remove any fields with None values so we don’t update them in the database
    update_data = {k: v for k, v in update_data.items() if v is not None}

    # Perform the update
    result = users_collection.update_one({"chat_id": chat_id}, {"$set": update_data})

    if result.matched_count:
        print(f"User with chat_id {chat_id} updated.")
    else:
        print(f"No user found with chat_id {chat_id}. Consider creating a user first.")

# Helper function to get bot_id as object id
def get_object_id(bot_id):
    # Logic to convert bot_id to object id, if necessary
    return bot_id
"""

# Example usage:
# Step 1: Create a bot
bot_id = create_bot(
    style="Casual", gender="Female", ethnicity="Caucasian", age=25, eye_color="Blue", hair_style="Curly",
    hair_color="Blonde", body_type="Slim", breast_size="Medium", butt_size="Medium", personality="Friendly",
    occupation="Engineer", hobbies=["Reading", "Traveling"], clothing=["Jeans and T-Shirt"], relationship="Single"
)

# Step 2: Create a user linked to the bot
create_user("johndoe", "johndoe@example.com", bot_id, language="English", level=1, weaknesses=["Impatient"], strengths=["Logical"])

# Step 3: Add a mode to the user with initial messages
add_mode_to_user("johndoe", "work", "en", "f", ["Initial work message 1", "Initial work message 2"])

# Step 4: Add additional messages to the current mode
add_messages_to_current_mode("johndoe", ["New work message 1", "New work message 2"])

# Step 5: Update bot details (e.g., changing occupation and personality)
update_bot(bot_id, {"occupation": "Software Developer", "personality": "Analytical"})

# Step 6: Update user attributes, e.g., language or current mode
update_user("johndoe", {"language": "Spanish", "level": 2})

add_mode_to_user("johndoe", "idk", "en", "f", ["Initial work message 1", "Initial work message 2"])

get_mode_info("johndoe", "work")
"""