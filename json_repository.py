from __future__ import annotations

import json
import os

from app.domain.models import (
    CharacterProfile,
    DynamicQuest,
    GameState,
    Item,
    NPC,
    NPCMemory,
    NPCPersonality,
    PlayerAction,
    StoryMemory,
    StoryState,
    TurnResult,
    WorldDefinition,
    WorldEvent,
    WorldState,
)
from app.storage.save_repository import BaseSaveRepository

from app.domain.models import Discovery
class JsonSaveRepository(BaseSaveRepository):
    def __init__(self, save_dir: str = "saves"):
        self.save_dir = save_dir
        os.makedirs(save_dir, exist_ok=True)

    def _get_path(self, session_id: str) -> str:
        return os.path.join(self.save_dir, f"{session_id}.json")

    def save(self, game_state: GameState) -> None:
        path = self._get_path(game_state.session_id)
        data = self._serialize_game_state(game_state)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load(self, session_id: str) -> GameState:
        path = self._get_path(session_id)

        if not os.path.exists(path):
            raise FileNotFoundError(f"Không tìm thấy save cho session_id={session_id}")

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return self._deserialize_game_state(data)

    def exists(self, session_id: str) -> bool:
        return os.path.exists(self._get_path(session_id))

    def delete(self, session_id: str) -> None:
        path = self._get_path(session_id)
        if os.path.exists(path):
            os.remove(path)

    def _serialize_game_state(self, game_state: GameState) -> dict:
        return {
            "session_id": game_state.session_id,
            "user_id": game_state.user_id,  # <--- BỔ SUNG DÒNG NÀY
            "world_definition": {
                "world_id": game_state.world_definition.world_id,
                "name": game_state.world_definition.name,
                "genre": game_state.world_definition.genre,
                "tone": game_state.world_definition.tone,
                "core_theme": game_state.world_definition.core_theme,
                "world_lore": game_state.world_definition.world_lore,
                "notable_regions": game_state.world_definition.notable_regions,
                "factions": game_state.world_definition.factions,
                "danger_types": game_state.world_definition.danger_types,
                "rules": game_state.world_definition.rules,
            },
            "character_profile": {
                "name": game_state.character_profile.name,
                "background": game_state.character_profile.background,
                "personality_traits": game_state.character_profile.personality_traits,
                "virtues": game_state.character_profile.virtues,
                "flaws": game_state.character_profile.flaws,
                "fears": game_state.character_profile.fears,
                "goals": game_state.character_profile.goals,
                "hp": game_state.character_profile.hp,
                "stamina": game_state.character_profile.stamina,
                "hunger": game_state.character_profile.hunger,
                "thirst": game_state.character_profile.thirst,
                "stress": game_state.character_profile.stress,
                "reputation": game_state.character_profile.reputation,
            },
            "story_state": {
                "current_situation": game_state.story_state.current_situation,
                "current_tension": game_state.story_state.current_tension,
                "current_objective": game_state.story_state.current_objective,
                "current_location_hint": game_state.story_state.current_location_hint,
                "current_time_context": game_state.story_state.current_time_context,
                "active_threads": game_state.story_state.active_threads,
                "unresolved_questions": game_state.story_state.unresolved_questions,
                "recent_story_beats": game_state.story_state.recent_story_beats,
            },
            "dynamic_quests": [
                {
                    "quest_id": q.quest_id,
                    "title": q.title,
                    "summary": q.summary,
                    "origin": q.origin,
                    "objective": q.objective,
                    "stakes": q.stakes,
                    "status": q.status,
                    "related_npcs": q.related_npcs,
                    "tags": q.tags,
                }
                for q in game_state.dynamic_quests
            ],
            "active_events": [
                {
                    "event_id": e.event_id,
                    "title": e.title,
                    "description": e.description,
                    "event_type": e.event_type,
                    "trigger_source": e.trigger_source,
                    "severity": e.severity,
                    "is_resolved": e.is_resolved,
                    "related_discovery": e.related_discovery,
                    "related_region": e.related_region,
                    "related_landmark": e.related_landmark,
                    "tags": e.tags,
                }
                for e in game_state.active_events
            ],
            "npcs": [
                {
                    "npc_id": npc.npc_id,
                    "name": npc.name,
                    "role": npc.role,
                    "personality": {
                        "traits": npc.personality.traits,
                        "speaking_style": npc.personality.speaking_style,
                        "moral_alignment": npc.personality.moral_alignment,
                    },
                    "memory": {
                        "short_term": npc.memory.short_term,
                        "long_term_facts": npc.memory.long_term_facts,
                    },
                }
                for npc in game_state.npcs
            ],
            "inventory": [
                {
                    "item_id": item.item_id,
                    "name": item.name,
                    "description": item.description,
                    "quantity": item.quantity,
                    "item_type": item.item_type,
                    "power": item.power,
                }
                for item in game_state.inventory
            ],
            "world": {
            "location": game_state.world.location,
            "region": game_state.world.region,
            "landmark": game_state.world.landmark,
            "danger_level": game_state.world.danger_level,
            "threat_state": game_state.world.threat_state,
            "in_combat": game_state.world.in_combat,
            "combat_enemy": game_state.world.combat_enemy,

            "discoveries": [
                {
                    "content": d.content,
                    "type": d.type
                }
                for d in game_state.world.discoveries
            ],

            "flags": game_state.world.flags,
            "time_of_day": game_state.world.time_of_day,
        },
            "story_memory": {
                "recent_events": game_state.story_memory.recent_events,
                "important_facts": game_state.story_memory.important_facts,
            },
            "turn_count": game_state.turn_count,
        }

    def _deserialize_game_state(self, data: dict) -> GameState:
        world_definition_data = data["world_definition"]
        character_profile_data = data["character_profile"]
        story_state_data = data["story_state"]
        world_data = data["world"]
        story_memory_data = data["story_memory"]

        world_definition = WorldDefinition(
            world_id=world_definition_data["world_id"],
            name=world_definition_data["name"],
            genre=world_definition_data["genre"],
            tone=world_definition_data["tone"],
            core_theme=world_definition_data["core_theme"],
            world_lore=world_definition_data["world_lore"],
            notable_regions=world_definition_data.get("notable_regions", []),
            factions=world_definition_data.get("factions", []),
            danger_types=world_definition_data.get("danger_types", []),
            rules=world_definition_data.get("rules", []),
        )

        character_profile = CharacterProfile(
            name=character_profile_data["name"],
            background=character_profile_data["background"],
            personality_traits=character_profile_data.get("personality_traits", []),
            virtues=character_profile_data.get("virtues", []),
            flaws=character_profile_data.get("flaws", []),
            fears=character_profile_data.get("fears", []),
            goals=character_profile_data.get("goals", []),
            hp=character_profile_data.get("hp", 100),
            stamina=character_profile_data.get("stamina", 100),
            hunger=character_profile_data.get("hunger", 0),
            thirst=character_profile_data.get("thirst", 0),
            stress=character_profile_data.get("stress", 0),
            reputation=character_profile_data.get("reputation", 0),
        )

        story_state = StoryState(
            current_situation=story_state_data["current_situation"],
            current_tension=story_state_data["current_tension"],
            current_objective=story_state_data["current_objective"],
            current_location_hint=story_state_data.get("current_location_hint", ""),
            current_time_context=story_state_data.get("current_time_context", "ban ngày"),
            active_threads=story_state_data.get("active_threads", []),
            unresolved_questions=story_state_data.get("unresolved_questions", []),
            recent_story_beats=story_state_data.get("recent_story_beats", []),
        )

        dynamic_quests = [
            DynamicQuest(
                quest_id=q["quest_id"],
                title=q["title"],
                summary=q["summary"],
                origin=q["origin"],
                objective=q["objective"],
                stakes=q["stakes"],
                status=q.get("status", "active"),
                related_npcs=q.get("related_npcs", []),
                tags=q.get("tags", []),
            )
            for q in data.get("dynamic_quests", [])
        ]

        active_events = [
            WorldEvent(
                event_id=e["event_id"],
                title=e["title"],
                description=e["description"],
                event_type=e.get("event_type", "generic"),
                trigger_source=e.get("trigger_source", ""),
                severity=e.get("severity", 1),
                is_resolved=e.get("is_resolved", False),
                related_discovery=e.get("related_discovery", ""),
                related_region=e.get("related_region", ""),
                related_landmark=e.get("related_landmark", ""),
                tags=e.get("tags", []),
            )
            for e in data.get("active_events", [])
        ]

        npcs = [
            NPC(
                npc_id=n["npc_id"],
                name=n["name"],
                role=n["role"],
                personality=NPCPersonality(
                    traits=n.get("personality", {}).get("traits", []),
                    speaking_style=n.get("personality", {}).get("speaking_style", "trung tính"),
                    moral_alignment=n.get("personality", {}).get("moral_alignment", "không rõ"),
                ),
                memory=NPCMemory(
                    short_term=n.get("memory", {}).get("short_term", []),
                    long_term_facts=n.get("memory", {}).get("long_term_facts", []),
                ),
            )
            for n in data.get("npcs", [])
        ]

        inventory = [
            Item(
                item_id=i["item_id"],
                name=i["name"],
                description=i.get("description", ""),
                quantity=i.get("quantity", 1),
                item_type=i.get("item_type", "misc"),
                power=i.get("power", 0),
            )
            for i in data.get("inventory", [])
        ]

        world = WorldState(
            location=world_data.get("location", ""),

            region=world_data.get("region", ""),
            landmark=world_data.get("landmark", ""),

            danger_level=world_data.get("danger_level", 1),
            threat_state=world_data.get("threat_state", "ổn định"),
            in_combat=world_data.get("in_combat", False),
            combat_enemy=world_data.get("combat_enemy", ""),

            discoveries=[
                Discovery(**d) for d in world_data.get("discoveries", [])
            ],

            flags=world_data.get("flags", {}),
            time_of_day=world_data.get("time_of_day", "ban ngày"),
        )

        story_memory = StoryMemory(
            recent_events=story_memory_data.get("recent_events", []),
            important_facts=story_memory_data.get("important_facts", []),
        )

        return GameState(
            session_id=data["session_id"],
            user_id=data.get("user_id", "anonymous"),  # <--- BỔ SUNG DÒNG NÀY
            world_definition=world_definition,
            character_profile=character_profile,
            story_state=story_state,
            dynamic_quests=dynamic_quests,
            active_events=active_events,
            npcs=npcs,
            inventory=inventory,
            world=world,
            story_memory=story_memory,
            turn_count=data.get("turn_count", 0),
        )
    
    def get_sessions_by_user(self, user_id: str) -> list[dict]:
        sessions = []
        for filename in os.listdir(self.save_dir):
            if filename.endswith(".json"):
                path = os.path.join(self.save_dir, filename)
                with open(path, "r", encoding="utf-8") as f:
                    try:
                        data = json.load(f)
                        # So khớp user_id
                        if data.get("user_id") == user_id or getattr(data, 'user_id', 'anonymous') == user_id:
                            sessions.append({
                                "session_id": data.get("session_id"),
                                "character_name": data.get("character_profile", {}).get("name", "Unknown"),
                                "world_name": data.get("world_definition", {}).get("name", "Unknown"),
                                "turn_count": data.get("turn_count", 0)
                            })
                    except Exception:
                        pass
        return sessions
    