from datetime import datetime
from typing import Set
from enum import Enum

class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"

class User:
    def __init__(self, user_id: str, name: str, email: str, role: UserRole = UserRole.USER):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.role = role
        self.teams: Set[str] = set()
        self.created_at = datetime.now()
    
    def add_to_team(self, team_id: str):
        self.teams.add(team_id)
    
    def is_in_team(self, team_id: str) -> bool:
        return team_id in self.teams
    
    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN
    
    def __repr__(self):
        return f"User(id={self.user_id}, name={self.name}, role={self.role.value})"
    
    def __str__(self):
        return f"{self.name} ({self.role.value})"