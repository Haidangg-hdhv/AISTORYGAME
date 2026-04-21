from __future__ import annotations

# 1. Đã thêm chữ Header vào đây để lấy thẻ căn cước từ web
from fastapi import APIRouter, Depends, HTTPException, Header 

from app.api.dependencies import get_game_service
from app.domain.schemas import (
    ActionRequest,
    GameStateResponse,
    StartGameRequest,
    StartGameResponse,
    TurnResponse,
)
from app.services.game_service import GameService
from app.services.world_definitions import list_worlds

router = APIRouter(prefix="/game", tags=["game"])

@router.post("/start", response_model=StartGameResponse)
def start_game(
    request: StartGameRequest,
    game_service: GameService = Depends(get_game_service),
    # 2. Hứng thẻ UID ở đây
    x_user_id: str = Header(alias="X-User-ID", default="guest") 
) -> StartGameResponse:
    try:
        # Truyền cái UID (x_user_id) xuống dưới để tạo file save cho đúng người
        game_state = game_service.start_new_game(request.model_dump(), user_id=x_user_id)

        return StartGameResponse(
            session_id=game_state.session_id,
            message=(
                f"Đã tạo phiên chơi mới cho nhân vật "
                f"{game_state.character_profile.name} trong thế giới "
                f"{game_state.world_definition.name}."
            ),
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/turn", response_model=TurnResponse)
def process_turn(
    request: ActionRequest,
    game_service: GameService = Depends(get_game_service),
    # Hứng thẻ UID ở đây
    x_user_id: str = Header(alias="X-User-ID", default="guest") 
) -> TurnResponse:
    try:
        if not game_service.session_exists(request.session_id):
            raise HTTPException(
                status_code=404,
                detail=f"Không tìm thấy session: {request.session_id}",
            )

        # Đưa thẻ UID cho game_service để nó biết lưu vào ngăn tủ của ai
        result = game_service.process_turn(
            session_id=request.session_id,
            action_type=request.action_type,
            content=request.content,
            user_id=x_user_id 
        )

        return TurnResponse(
            narrative=result.narrative,
            choices=result.choices,
            state_changes=result.state_changes,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/worlds")
def get_worlds() -> dict:
    try:
        return {"worlds": list_worlds()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{session_id}", response_model=GameStateResponse)
def get_game_state(
    session_id: str,
    game_service: GameService = Depends(get_game_service),
) -> GameStateResponse:
    try:
        if not game_service.session_exists(session_id):
            raise HTTPException(
                status_code=404,
                detail=f"Không tìm thấy session: {session_id}",
            )

        game_state = game_service.get_game_state(session_id)

        return GameStateResponse(
            session_id=game_state.session_id,
            world_name=game_state.world_definition.name,
            player_name=game_state.character_profile.name,
            location=game_state.world.location,
            current_objective=game_state.story_state.current_objective,
            turn_count=game_state.turn_count,
            hp=game_state.character_profile.hp,
            stamina=game_state.character_profile.stamina,
            stress=game_state.character_profile.stress,
        )
    except HTTPException:
        raise
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{session_id}")
def delete_game(
    session_id: str,
    game_service: GameService = Depends(get_game_service),
) -> dict:
    try:
        if not game_service.session_exists(session_id):
            raise HTTPException(
                status_code=404,
                detail=f"Không tìm thấy session: {session_id}",
            )

        game_service.delete_game(session_id)
        return {"message": f"Đã xóa session {session_id}."}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sessions/{user_id}")
def get_user_sessions(
    user_id: str,
    game_service: GameService = Depends(get_game_service),
) -> dict:
    try:
        sessions = game_service.repository.get_sessions_by_user(user_id)
        return {"sessions": sessions}
    except AttributeError:
        raise HTTPException(
            status_code=501, 
            detail="Tính năng lấy danh sách save chưa được cài đặt trong Repository hiện tại."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))