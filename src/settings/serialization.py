# -*- coding: UTF-8 -*-
from pathlib import Path

import tomlkit

from settings.models import AppSettings, Mode


def update_settings(app_settings: AppSettings):
    settings_file = Path().home() / ".jekyll-cli" / "settings.toml"
    app_settings = app_settings.model_dump(exclude_none=True)
    with settings_file.open("w", encoding="utf-8") as f:
        tomlkit.dump(app_settings, f)


def get_settings() -> AppSettings:
    settings_file = Path().home() / ".jekyll-cli" / "settings.toml"
    if not settings_file.exists():
        app_settings = AppSettings(mode=Mode.File)
        with settings_file.open("w", encoding="utf-8") as f:
            tomlkit.dump(app_settings.model_dump(exclude_none=True), f)
        return app_settings
    else:
        with settings_file.open("r", encoding="utf-8") as f:
            app_settings = tomlkit.load(f).unwrap()
            app_settings = AppSettings.model_validate(app_settings)
            return app_settings
