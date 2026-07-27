# 🧩 TeleGame Plugin Creation Guide

Creating a new game for TeleGame is simple! You only need to create a single directory inside `app/games/`.

## Step 1: Create Game Folder
Create a folder inside `app/games/my_custom_game/` and create `game.py`.

## Step 2: Implement `BaseGame`
In `app/games/my_custom_game/game.py`:

```python
from typing import Any, Dict, List, Optional
from app.core.engine.base_game import BaseGame, GameMoveResult, GamePlayer


class GamePlugin(BaseGame):
    slug = "my_custom_game"
    title = "My Custom Game"
    description = "Cool new game"
    min_players = 2
    max_players = 4

    def initialize(self, players: List[GamePlayer]) -> Dict[str, Any]:
        return self.serialize()

    def join(self, player: GamePlayer) -> bool:
        return True

    def leave(self, telegram_id: int) -> bool:
        return True

    def start(self) -> Dict[str, Any]:
        return self.serialize()

    def handle_move(self, telegram_id: int, move_data: Dict[str, Any]) -> GameMoveResult:
        return GameMoveResult(success=True, message="Move executed.")

    def next_turn(self) -> Optional[int]:
        return None

    def pause(self) -> bool:
        return True

    def resume(self) -> bool:
        return True

    def end(self, reason: str = "COMPLETED") -> Dict[str, Any]:
        return self.serialize()

    def serialize(self) -> Dict[str, Any]:
        return {}

    def deserialize(self, state_data: Dict[str, Any]) -> None:
        pass

    def validate(self, telegram_id: int, move_data: Dict[str, Any]) -> bool:
        return True

    def timeout(self) -> GameMoveResult:
        return GameMoveResult(success=True, message="Timed out.", is_game_over=True)

    def render(self, language_code: str = "en") -> str:
        return "🎮 My Custom Game Board"
```

The platform will automatically discover and load your plugin on boot!
