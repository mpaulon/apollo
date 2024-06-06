import datetime
import logging
from pathlib import Path
import shutil

from apollo import common, nfo, tmdb

import guessit

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


class MaybeInvalidMediaType(Exception):
    pass




def rename_file(output: Path, suffix: str, media_type: str, media_info: dict):
    overview = media_info["overview"]
    tmdb_id = str(media_info["id"])
    if media_type == "movie":
        title = media_info["title"]
        original_title = media_info["original_title"]

        year = str(
            datetime.datetime.strptime(media_info["release_date"], "%Y-%m-%d").year
        )
        file_name = f"{title} ({year}) [tmdbid-{tmdb_id}]"

        output_folder = output / "movie" / file_name
        output_file = output_folder / f"{file_name}{suffix}"
        output_nfo = output_folder / f"{file_name}.nfo"

    elif media_type == "episode":
        series_name = media_info["name"]
        year = str(
            datetime.datetime.strptime(media_info["first_air_date"], "%Y-%m-%d").year
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
        output_file = output_season_folder / f"{file_name}{suffix}"

    else:
        raise NotImplementedError(guess["type"])

    return output_file, output_nfo


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
    media_type, result = get_media_info(tmdb_client, file, forced_type, forced_title)

    # TODO: open old nfo file and try to match tmdbid

    output_file, output_nfo = rename_file(output, file.suffix, media_type, result)

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
    args = common.parse_args()
    settings = common.load_settings(args, logger)
    common.set_log_level(args, logger)
    tmdb_client = common.setup_tmdb_client(settings)

    for file in common.iterate_inputs(args.input):
        # TODO: try automatic process
        # TODO: add option to force no input
        # TODO: ask user validation / skip / manual
        # TODO: if error or manual -> user interaction to edit incorrect data

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
