from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Set

@dataclass
class Regista:
    id:str
    name:str
    height: int
    date_of_birth: datetime
    known_for_movies:str

    film: list = field(default_factory=list)

    #def add_actor(self, actor_id: str):
      #  self.actors.add(actor_id)

    #@property
    #def actors_count(self) -> int:
       # return len(self.actors)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, Regista):
            return self.id == other.id
        return False

    def __repr__(self):
        return f"{self.title} ({self.year if self.year is not None else 'N/D'})"