"""Multi-language Internationalization (i18n) Engine."""

import json
import os
from typing import Any

from app.config.logging import logger
from app.config.settings import settings


class I18nEngine:
    """Translation manager supporting dynamic English and Bangla localizations."""

    def __init__(self) -> None:
        self.locales: dict[str, dict[str, str]] = {}
        self.load_locales()

    def load_locales(self) -> None:
        """Loads translation JSON files from app/i18n/locales directory."""
        locales_dir = os.path.join(os.path.dirname(__file__), "locales")
        for lang in settings.SUPPORTED_LANGUAGES:
            file_path = os.path.join(locales_dir, f"{lang}.json")
            if os.path.exists(file_path):
                try:
                    with open(file_path, encoding="utf-8") as f:
                        self.locales[lang] = json.load(f)
                    logger.info(f"Loaded locale: {lang}")
                except Exception as e:
                    logger.error(f"Failed to load locale file '{file_path}': {e}")
                    self.locales[lang] = {}
            else:
                self.locales[lang] = {}

    def get(self, key: str, lang: str = "bn", **kwargs: Any) -> str:
        """Fetch localized string formatting optional kwargs."""
        language = lang if lang in self.locales else settings.DEFAULT_LANGUAGE
        translations = self.locales.get(language, {})
        text = translations.get(key)

        # Fallback to English if translation missing in requested language
        if text is None:
            text = self.locales.get("en", {}).get(key, key)

        if kwargs and isinstance(text, str):
            try:
                return text.format(**kwargs)
            except KeyError:
                return text
        return text


i18n = I18nEngine()
