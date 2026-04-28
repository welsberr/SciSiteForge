from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import shutil


REPO_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class ThemeSpec:
    name: str
    display_name: str
    template_path: Path
    stylesheet_path: Path
    extra_assets: tuple[Path, ...] = field(default_factory=tuple)
    body_class: str = ""
    shell_class: str = ""
    page_class: str = ""
    description: str = ""


def _theme_path(*parts: str) -> Path:
    return REPO_ROOT.joinpath(*parts)


_THEMES: dict[str, ThemeSpec] = {
    "evo-edu": ThemeSpec(
        name="evo-edu",
        display_name="Evo-Edu",
        template_path=_theme_path("theme", "themes", "evo-edu", "base.html"),
        stylesheet_path=_theme_path("theme", "themes", "evo-edu", "style.css"),
        body_class="theme-evo-edu",
        shell_class="site-shell",
        page_class="evo-edu-page",
        description="Warm learning-focused theme derived from the evo-edu.org home page.",
    ),
    "talkorigins-modern": ThemeSpec(
        name="talkorigins-modern",
        display_name="TalkOrigins Modern",
        template_path=_theme_path("theme", "themes", "talkorigins-modern", "base.html"),
        stylesheet_path=_theme_path("theme", "themes", "talkorigins-modern", "style.css"),
        extra_assets=(
            _theme_path("theme", "themes", "talkorigins-modern", "assets", "toa.ico"),
            _theme_path("theme", "themes", "talkorigins-modern", "assets", "toa_logo_001_edit_001.png"),
        ),
        body_class="theme-talkorigins-modern",
        shell_class="site-shell",
        page_class="talkorigins-preview",
        description="Archive-forward theme derived from the www2.talkorigins.org modernization proof-of-concept.",
    ),
    "pandasthumb": ThemeSpec(
        name="pandasthumb",
        display_name="Panda's Thumb",
        template_path=_theme_path("theme", "themes", "pandasthumb", "base.html"),
        stylesheet_path=_theme_path("theme", "themes", "pandasthumb", "style.css"),
        body_class="theme-pandasthumb",
        shell_class="site-shell",
        page_class="pandasthumb-page",
        description="Legacy-archive theme derived from pandasthumb.net.",
    ),
}


def available_themes() -> list[ThemeSpec]:
    return [_THEMES[name] for name in sorted(_THEMES)]


def get_theme(name: str | None) -> ThemeSpec:
    theme_name = name or "evo-edu"
    try:
        return _THEMES[theme_name]
    except KeyError as exc:
        raise KeyError(f"Unknown SciSiteForge theme: {theme_name}") from exc


def materialize_theme(theme: ThemeSpec, output_dir: str | Path) -> dict[str, str]:
    out = Path(output_dir)
    theme_root = out / "theme"
    assets_root = theme_root / "assets"
    assets_root.mkdir(parents=True, exist_ok=True)

    style_target = theme_root / "style.css"
    shutil.copyfile(theme.stylesheet_path, style_target)

    copied_assets: list[str] = []
    for asset in theme.extra_assets:
        target = assets_root / asset.name
        shutil.copyfile(asset, target)
        copied_assets.append(target.relative_to(out).as_posix())

    shared_js = _theme_path("theme", "main.js")
    if shared_js.exists():
        shutil.copyfile(shared_js, theme_root / "main.js")

    return {
        "theme_name": theme.name,
        "theme_display_name": theme.display_name,
        "theme_description": theme.description,
        "theme_stylesheet_href": "/theme/style.css",
        "theme_script_href": "/theme/main.js",
        "theme_asset_prefix": "/theme/assets",
        "theme_assets": copied_assets,
    }
