from pathlib import Path
import shutil

import textual.app
import textual.containers
import textual.lazy
import textual.screen
import textual.widgets

from apollo import common, tmdb

logger = common.setup_logger(__name__)


class AppProcessMovieScreenContainer(textual.containers.Container):

    def __init__(self, media_infos: dict, movie_not_found: bool = False, *args, **kwargs):
        self._media_infos = media_infos
        self._not_found = movie_not_found
        super().__init__(*args, **kwargs)

    def on_input_submitted(self, submitted: textual.widgets.Input.Submitted):
        if submitted.input.id == "movie-title":
            self.parent.update_media_data(forced_title=submitted.input.value)
            self.parent.refresh(recompose=True)

    def compose(self) -> textual.app.ComposeResult:
        with textual.containers.Horizontal():
            yield textual.widgets.Label("Title :", classes="label")
            yield textual.widgets.Input(self._media_infos["title"], id="movie-title")
        if not self._not_found:
            with textual.containers.Horizontal():
                yield textual.widgets.Label("Overview : ", classes="label")
                yield textual.widgets.Static(self._media_infos["overview"], classes="overview-content")
        else:
            with textual.containers.Center():
                yield textual.widgets.Static("Movie not found", classes="error-message", markup=False)


class AppProcessEpisodeScreenContainer(textual.containers.Container):

    def __init__(self, media_infos: dict, extra_infos: dict, *args, **kwargs):
        self._media_infos = media_infos
        self._extra_infso = extra_infos
        super().__init__(*args, **kwargs)

    def compose(self) -> textual.app.ComposeResult:
        raise NotImplementedError()


class AppProcessMediaScreen(textual.screen.ModalScreen):
    BINDINGS = [
        ("q", "stop", "Stop Processing Media"),
        ("m", "move", "Move"),
        ("c", "copy", "Copy"),
        ("ctrl+d", "delete", "Delete"),
    ]

    def __init__(self, media: Path, origin_widget, *args, **kwargs):
        self._media = media
        self._origin_widget = origin_widget
        self._forced_title = None
        self._forced_type = None
        self.update_media_data()

        super().__init__(*args, **kwargs)

    def _remove_origin_widget(self):
        self._origin_widget.remove()
        self.dismiss()
        self.app.query_one("#content").focus()

    def action_stop(self):
        self.dismiss()

    def action_move(self):
        self._destination.parent.mkdir(exist_ok=True, parents=True)
        self._media.rename(self._destination)
        self._remove_origin_widget()

    def action_copy(self):
        self._destination.parent.mkdir(exist_ok=True, parents=True)
        shutil.copy(self._media, self._destination)
        self._remove_origin_widget()

    def action_delete(self):
        raise NotImplementedError()

    def on_button_pressed(self, event: textual.widgets.Button.Pressed):
        if event.button.id == "move":
            self.action_move()
        elif event.button.id == "copy":
            self.action_copy()
        elif event.button.id == "delete":
            self.action_delete()

    def on_mount(self):
        self.title = self._media.name

    def update_media_data(self, forced_type: str | None = None, forced_title: str | None = None) -> None:
        self._error_state = None
        self._forced_title = forced_title or self._forced_title
        self._forced_type = forced_type or self._forced_type
        try:
            self._media_type, self._media_infos, self._extra_infos = common.get_media_info(
                self.app.tmdb_client,
                self._media,
                forced_type=self._forced_type,
                forced_title=self._forced_title,
                logger=logger,
            )
            self._destination = common.generate_new_path(
                self.app._output_folder,
                self._media,
                self._media_type,
                self._media_infos,
                self._extra_infos,
            )
        except tmdb.MovieNotFound as exc:
            self._error_state = exc

    def compose(self):

        yield textual.widgets.Header()
        with textual.containers.Container():
            with textual.widgets.RadioSet():
                # TODO: handle change of radio button
                yield textual.widgets.RadioButton("movie", value=self._media_type == "movie")
                yield textual.widgets.RadioButton("episode", value=self._media_type == "episode")
        if self._media_type == "movie":
            yield AppProcessMovieScreenContainer(
                self._media_infos, movie_not_found=isinstance(self._error_state, tmdb.MovieNotFound)
            )
        elif self._media_type == "episode":
            yield AppProcessEpisodeScreenContainer(self._media_infos, self._extra_infos)
        if self._error_state is None:
            with textual.containers.Horizontal(classes="destination-container"):
                yield textual.widgets.Label("Destination : ")
                yield textual.widgets.Static(self._destination.as_posix(), markup=False)
                if self._destination.exists():
                    yield textual.widgets.Static("❗")
                # TODO: show new path / add color if file already exists
        with textual.containers.Horizontal(classes="destination-buttons"):
            if self._error_state is None:
                yield textual.widgets.Button("Move", id="move")
                yield textual.widgets.Button("Copy", id="copy")
            yield textual.widgets.Button("Delete", id="delete")
        yield textual.widgets.Footer()


class AppMediaContainer(textual.containers.Container):
    def __init__(self, media: Path, *args, **kwargs):
        self._media = media
        super().__init__(*args, **kwargs)

    def on_button_pressed(self, event: textual.widgets.Button.Pressed):
        if event.button.id == "process":
            self.app.push_screen(AppProcessMediaScreen(self._media, origin_widget=self))

    def compose(self) -> textual.app.ComposeResult:
        yield textual.widgets.Label("File: ")
        yield textual.widgets.Static(self._media.name, classes="media-title")
        yield textual.widgets.Button("Process", id="process", classes="media-button").focus()


class AppContentContainer(textual.containers.ScrollableContainer):
    pass
    # def compose(self) -> textual.app.ComposeResult:
    #     pass
    #     # TODO: find something better, this is too slow when input contains a lot of media
    #     for media in common.iterate_inputs(self.app._input_folder, logger):
    #         yield textual.lazy.Lazy(AppMediaContainer(media))


class App(textual.app.App):
    CSS_PATH = "statics/apollo.tcss"
    BINDINGS = [
        ("n", "next", "Next Media"),
        ("q", "exit", "Exit"),
    ]

    def __init__(self, input_folder: Path, output_folder: Path, tmdb_client: tmdb.TMDB, *args, **kwargs):
        self._input_folder = input_folder
        self._output_folder = output_folder
        self._tmdb_client = tmdb_client
        self._medias = common.iterate_inputs(self.app._input_folder, logger)
        super().__init__(*args, **kwargs)

    @property
    def tmdb_client(self):
        return self._tmdb_client

    def action_exit(self) -> None:
        return self.exit()

    def action_next(self) -> None:
        new_media = AppMediaContainer(next(self._medias))
        self.query_one("#content").mount(new_media)
        new_media.scroll_visible()

    def on_mount(self):
        self.title = "Apollo Media Manager"

    def compose(self) -> textual.app.ComposeResult:
        yield textual.widgets.Header()
        yield AppContentContainer(id="content")
        yield textual.widgets.Footer()


def run():
    args = common.parse_args()
    settings = common.load_settings(args, logger)
    common.set_log_level(args, logger)
    tmdb_client = common.setup_tmdb_client(settings)

    app = App(args.input, args.output, tmdb_client)
    app.run()


if __name__ == "__main__":
    run()
