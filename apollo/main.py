import argparse
import datetime
import logging
from pathlib import Path
import shutil
import tomllib

from apollo import nfo, tmdb

import guessit

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


class MaybeInvalidMediaType(Exception):
    pass


def process_file(
    tmdb_client: tmdb.TMDB,
    output: Path,
    file: Path,
    preserve: bool = False,
    dry_run: bool = False,
    forced_type: str | None = None,
    forced_title: str | None = None,
):
    logger.info("Processing %s", file)
    guess = guessit.guessit(file)
    logger.debug("Guess data: %", guess)

    guess_title = forced_title or guess.get("alternative_title") or guess["title"]
    media_type = forced_type or guess["type"]

    result = tmdb_client.search(
        guess_title,
        video_type={"movie": "movie", "episode": "tv"}[media_type],
        year=guess.get("year"),
    )

    # open old nfo file and try to match tmdbid

    overview = result["overview"]
    tmdb_id = str(result["id"])
    if media_type == "movie":
        title = result["title"]
        original_title = result["original_title"]

        year = str(datetime.datetime.strptime(result["release_date"], "%Y-%m-%d").year)
        file_name = f"{title} ({year}) [tmdbid-{tmdb_id}]"

        output_folder = output / "movie" / file_name
        output_file = output_folder / f"{file_name}{file.suffix}"
        output_nfo = output_folder / f"{file_name}.nfo"

    elif media_type == "episode":
        series_name = result["name"]
        year = str(
            datetime.datetime.strptime(result["first_air_date"], "%Y-%m-%d").year
        )
        try:
            season_number = guess["season"]
        except KeyError:
            raise MaybeInvalidMediaType
        episode_number = guess["episode"]

        episode_result = tmdb_client.search_episode(
            tmdb_id, season_number, episode_number
        )
        episode_name = episode_result["name"]
        tmdb_episode_id = episode_result["id"]

        output_series_folder = output / f"{series_name} ({year}) [tmdbid-{tmdb_id}]"
        output_season_folder = output_series_folder / f"Season{season_number:02}"
        file_name = f"{series_name} S{season_number:02}E{episode_number:02} {episode_name} [tmdbid-{tmdb_episode_id}]"
        output_file = output_season_folder / f"{file_name}{file.suffix}"

    else:
        raise NotImplementedError(guess["type"])

    # check if file already exists
    if output_file.exists():
        logger.warning("File %s already exists", output_file)

    # moving file
    logger.info("%s -> %s", file, output_file)
    if input("Press key to proceed or s to skip") == "s":
        return 
    if not dry_run:
        output_file.parent.mkdir(exist_ok=True, parents=True)
        if preserve:
            shutil.copy(file, output_file)
        else:
            file.rename(output_file)
        # creating nfo data
        nfo.create_nfo(title, original_title, overview, tmdb_id, year, output_nfo)


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--settings", type=Path, default=Path("settings.toml"))
    parser.add_argument("--preserve", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("-verbose", "-v", action="store_true")
    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    with open(args.settings, "rb") as settings_file:
        logger.info("Loading settings from %s", args.settings.absolute().as_posix())
        settings = tomllib.load(settings_file)

    tmdb_client = tmdb.TMDB(settings["tmdb"]["account_id"], settings["tmdb"]["token"])

    for file in args.input.rglob("*"):
        if not file.is_file():
            continue
        if file.suffix not in [".mp4", ".mkv", ".avi"]:
            logger.debug("Ignoring %s", file.absolute().as_posix())
            continue
        try:
            process_file(tmdb_client, args.output, file, args.preserve, args.dry_run)
        except (MaybeInvalidMediaType, tmdb.MovieNotFound):
            process_file(
                tmdb_client,
                args.output,
                file,
                args.preserve,
                args.dry_run,
                forced_type=input("Media type (movie or episode): "),
                forced_title=input("Title: "),
            )


if __name__ == "__main__":
    run()
