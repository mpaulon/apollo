import argparse
import datetime
import logging
import tomllib
from typing import Any
from pathlib import Path

import guessit

from apollo import tmdb


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--settings", type=Path, default=Path("settings.toml"))
    parser.add_argument("--preserve", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("-verbose", "-v", action="store_true")
    args = parser.parse_args()

    return args


def set_log_level(args: argparse.Namespace, logger: logging.Logger):
    if args.verbose:
        logger.setLevel(logging.DEBUG)


def load_settings(args: argparse.Namespace, logger: logging.Logger):
    with open(args.settings, "rb") as settings_file:
        logger.info("Loading settings from %s", args.settings.absolute().as_posix())
        settings = tomllib.load(settings_file)

    return settings


def setup_logger(name: str):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(name)
    return logger


def setup_tmdb_client(settings: dict[str, Any]):
    tmdb_client = tmdb.TMDB(settings["tmdb"]["account_id"], settings["tmdb"]["token"])
    return tmdb_client


def iterate_inputs(input: Path, logger: logging.Logger):
    for file in input.rglob("*"):
        if not file.is_file():
            continue
        if file.suffix not in [".mp4", ".mkv", ".avi"]:
            logger.debug("Ignoring %s", file.absolute().as_posix())
            continue
        yield file


def get_media_info(
    tmdb_client: tmdb.TMDB,
    file: Path,
    logger: logging.Logger,
    forced_type: str | None = None,
    forced_title: str | None = None,
):

    guess = guessit.guessit(file)
    logger.debug("Guess data: %", guess)
    processed_guess_title = guess["title"]
    if guess.get("part"):
        processed_guess_title += " " + str(guess["part"])
    guess_title = forced_title or guess.get("alternative_title") or processed_guess_title
    media_type = forced_type or guess["type"]

    result = tmdb_client.search(
        guess_title,
        video_type={"movie": "movie", "episode": "tv"}[media_type],
        year=guess.get("year"),
    )

    if media_type == "movie":
        extra_infos = {}
    elif media_type == "episode":
        tmdb_id = result["id"]
        season_number = guess["season"]
        episode_number = guess["episode"]
        extra_infos = tmdb_client.search_episode(tmdb_id, season_number, episode_number)

    return media_type, result, extra_infos


def extract_year(date: str) -> str:
    return str(datetime.datetime.strptime(date, "%Y-%m-%d").year)


def generate_new_path(
    output: Path,
    file: Path,
    media_type: str,
    media_infos: dict,
    extra_infos: dict,
) -> Path:

    if media_type == "movie":
        file_name = f"{media_infos['title']} ({extract_year(media_infos['release_date'])}) [tmdbid-{media_infos['id']}]"
        output_file = output / "movie" / file_name / (file_name + file.suffix)

    elif media_type == "episode":
        folder_name = (
            f"{media_infos['name']} ({extract_year(media_infos['first_air_date'])}) [tmdbid-{media_infos['id']}]"
        )
        file_name = f"{media_infos['name']} S{extra_infos['season_number']:02}E{extra_infos['episode_number']:02} {extra_infos['name']}"

        output_file = (
            output / "show" / folder_name / f"Season{extra_infos['season_number']:02}" / (file_name + file.suffix)
        )

    return output_file
