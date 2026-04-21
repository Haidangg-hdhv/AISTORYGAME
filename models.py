from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


# =========================
# WORLD
# =========================
@dataclass
class WorldDefinition:
    world_id: str
    name: str
    genre: str
    tone: str
    core_theme: str
    world_lore: str
    notable_regions: List[str] = field(default_factory=list)
    factions: List[str] = field(default_factory=list)
    danger_types: List[str] = field(default_factory=list)
    rules: List[str] = field(default_factory=list)


# =========================
# CHARACTER ROLL
# =========================
@dataclass
class CharacterProfile:
    name: str
    background: str
    personality_traits: List[str] = field(default_factory=list)
    virtues: List[str] = field(default_factory=list)
    flaws: List[str] = field(default_factory=list)
    fears: List[str] = field(default_factory=list)
    goals: List[str] = field(default_factory=list)

    # Chỉ số mở rộng
    hp: int = 100
    stamina: int = 100
    hunger: int = 0
    thirst: int = 0
    stress: int = 0
    reputation: int = 0


# =========================
# STORY STATE
# =========================
@dataclass
class StoryState:
    current_situation: str
    current_tension: str
    current_objective: str
    current_location_hint: str = ""
    current_time_context: str = "ban ngày"

    active_threads: List[str] = field(default_factory=list)
    unresolved_questions: List[str] = field(default_factory=list)
    recent_story_beats: List[str] = field(default_factory=list)


# =========================
# DYNAMIC QUEST
# =========================
@dataclass
class DynamicQuest:
    quest_id: str
    title: str
    summary: str
    origin: str
    objective: str
    stakes: str
    status: str = "active"
    related_npcs: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)


# =========================
# ITEM
# =========================
@dataclass
class Item:
    item_id: str
    name: str
    description: str = ""
    quantity: int = 1

    # 👉 thêm
    item_type: str = "misc"   # weapon, armor, consumable
    power: int = 0           # damage / defense / heal

# =========================
# NPC
# =========================
@dataclass
class NPCPersonality:
    traits: List[str] = field(default_factory=list)
    speaking_style: str = "trung tính"
    moral_alignment: str = "không rõ"


@dataclass
class NPCMemory:
    short_term: List[str] = field(default_factory=list)
    long_term_facts: List[str] = field(default_factory=list)


@dataclass
class NPC:
    npc_id: str
    name: str
    role: str
    personality: NPCPersonality = field(default_factory=NPCPersonality)
    memory: NPCMemory = field(default_factory=NPCMemory)


# =========================
# WORLD RUNTIME STATE
# =========================
@dataclass
class Discovery:
    content: str
    type: str = "generic"   # generic, blood, magic, npc, item, danger, clue


@dataclass
class WorldState:
    # Giữ lại để tương thích code cũ
    location: str = ""

    region: str = ""
    landmark: str = ""

    danger_level: int = 1  # 1 -> 5
    threat_state: str = "ổn định"

    discoveries: List[Discovery] = field(default_factory=list)

    flags: Dict[str, bool] = field(default_factory=dict)
    time_of_day: str = "ban ngày"
    in_combat: bool = False
    combat_enemy: str = ""

    @property
    def full_location(self) -> str:
        if self.region and self.landmark:
            return f"{self.region} - {self.landmark}"
        if self.region:
            return self.region
        if self.landmark:
            return self.landmark
        return self.location

    def refresh_location(self) -> None:
        self.location = self.full_location

    def refresh_threat_state(self) -> None:
        if self.danger_level <= 2:
            self.threat_state = "ổn định"
        elif self.danger_level == 3:
            self.threat_state = "bất an"
        elif self.danger_level == 4:
            self.threat_state = "nguy hiểm"
        else:
            self.threat_state = "cực kỳ nguy hiểm"


# =========================
# MEMORY
# =========================
@dataclass
class StoryMemory:
    recent_events: List[str] = field(default_factory=list)
    important_facts: List[str] = field(default_factory=list)

# =========================
# EVENT SYSTEM
# =========================
@dataclass
class WorldEvent:
    event_id: str
    title: str
    description: str

    event_type: str = "generic"   # generic, encounter, combat, clue, quest, ambush, boss
    trigger_source: str = ""      # danger_level, discovery_type, action_type, world_progression
    severity: int = 1             # 1 -> 5

    is_resolved: bool = False
    related_discovery: str = ""
    related_region: str = ""
    related_landmark: str = ""

    tags: List[str] = field(default_factory=list)

# =========================
# GAME STATE
# =========================
@dataclass
class GameState:
    session_id: str
    

    world_definition: WorldDefinition
    character_profile: CharacterProfile
    story_state: StoryState

    dynamic_quests: List[DynamicQuest] = field(default_factory=list)
    active_events: List[WorldEvent] = field(default_factory=list)

    npcs: List[NPC] = field(default_factory=list)
    inventory: List[Item] = field(default_factory=list)

    world: WorldState = field(default_factory=WorldState)
    story_memory: StoryMemory = field(default_factory=StoryMemory)

    turn_count: int = 0
    user_id: str = "anonymous"


# =========================
# TURN I/O
# =========================
@dataclass
class PlayerAction:
    action_type: str
    content: str


@dataclass
class TurnResult:
    narrative: str
    state_changes: List[str] = field(default_factory=list)
    choices: List[str] = field(default_factory=list)


