# auth.py
from pydantic import BaseModel
from typing import Dict, Any, List
from datetime import datetime

# 1. Define the core user schema
class UserInDB(BaseModel):
    username: str
    email: str
    full_name: str = None
    hashed_password: str

# 2. Establish in-memory storage for active sessions and history
# In a production environment, this interfaces with AWS DynamoDB
active_sessions: Dict[str, Any] = {}
user_recommendations: Dict[str, List[Any]] = {}

# 3. Define the Dependency Injection function for FastAPI routes
async def get_current_active_user(token: str = None):
    """
    Validates the JWT token and retrieves the current authenticated user.
    Paste your existing JWT decoding and validation logic here.
    """
    # Example placeholder: Replace with your exact token verification logic
    # payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    # return UserInDB(**user_data)
    pass

# 4. Define the history tracking utility
def save_to_history(username: str, recommendation_type: str, input_data: dict, result: dict):
    """
    Persists the AI-generated recommendations to the user's session history.
    """
    if username not in user_recommendations:
        user_recommendations[username] = []
    
    history_entry = {
        "id": str(datetime.utcnow().timestamp()),
        "timestamp": datetime.utcnow().isoformat(),
        "recommendation_type": recommendation_type,
        "input_summary": input_data,
        "full_result": result
    }
    user_recommendations[username].append(history_entry)