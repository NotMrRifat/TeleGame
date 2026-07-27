"""Dynamic Game Plugin Manager and Registry."""

import importlib
import os

from app.config.logging import logger
from app.core.engine.base_game import BaseGame


class PluginManager:
    """Discovers and registers game plugins dynamically from the app/games package."""

    def __init__(self) -> None:
        self._games: dict[str, type[BaseGame]] = {}

    def discover_plugins(self) -> dict[str, type[BaseGame]]:
        """Scans app/games for game plugins and registers them dynamically."""
        self._games.clear()
        import app.games as games_pkg

        games_dir = os.path.dirname(games_pkg.__file__)
        if not os.path.exists(games_dir):
            return self._games

        for item in os.listdir(games_dir):
            item_path = os.path.join(games_dir, item)
            if os.path.isdir(item_path):
                game_module_path = os.path.join(item_path, "game.py")
                if os.path.exists(game_module_path):
                    full_module_name = f"app.games.{item}.game"
                    try:
                        module = importlib.import_module(full_module_name)
                        game_cls = getattr(module, "GamePlugin", None) or getattr(
                            module, "Game", None
                        )
                        if game_cls and issubclass(game_cls, BaseGame) and game_cls is not BaseGame:
                            slug = getattr(game_cls, "slug", item)
                            self._games[slug] = game_cls
                            logger.info(
                                f"Successfully loaded Game Plugin: '{slug}' ({game_cls.__name__})"
                            )
                    except Exception as err:
                        logger.error(f"Failed to load Game Plugin '{item}': {err}")

        return self._games

    def get_game_class(self, slug: str) -> type[BaseGame]:
        """Fetch game plugin class by slug."""
        if slug not in self._games:
            raise KeyError(f"Game plugin '{slug}' is not registered.")
        return self._games[slug]

    def list_available_games(self) -> dict[str, type[BaseGame]]:
        """List all loaded game plugins."""
        if not self._games:
            self.discover_plugins()
        return self._games


plugin_manager = PluginManager()
