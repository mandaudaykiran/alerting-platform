from typing import Set

class Team:
    def __init__(self, team_id: str, name: str):
        self.team_id = team_id
        self.name = name
        self.member_ids: Set[str] = set()
    
    def add_member(self, user_id: str):
        self.member_ids.add(user_id)
    
    def remove_member(self, user_id: str):
        self.member_ids.discard(user_id)
    
    def get_member_count(self) -> int:
        return len(self.member_ids)
    
    def __repr__(self):
        return f"Team(id={self.team_id}, name={self.name}, members={len(self.member_ids)})"
    
    def __str__(self):
        return f"{self.name} ({len(self.member_ids)} members)"