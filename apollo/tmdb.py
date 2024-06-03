import enum
from functools import cache

import requests


class MovieNotFound(Exception):
    pass


class TMDB:
    _url = "https://api.themoviedb.org/3/"

    class VideoType(enum.Enum):
        ANY = 0
        MOVIE = 1
        SHOW = 2

    def __init__(self, account_id: str, token: str) -> None:
        self._account_id = account_id
        self._token = token

    def _get(self, endpoint: str, params: dict[str, str] | None = None):
        _headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self._token}",
        }

        _r = requests.get(url=self._url + endpoint, headers=_headers, params=params)
        return _r.json()
    
    @cache
    def search(
        self,
        query: str,
        video_type: str,
        year: str | None = None,
    ):
        params = {"query": query}
        if year is not None:
            params["year"] = year
        if video_type == "movie":
            results = self._get("search/movie", params=params).get("results")
        elif video_type == "tv":
            results = self._get("search/tv", params=params).get("results")
        else: 
            raise NotImplementedError(video_type)
        if not results:
            raise MovieNotFound(f"Unable to find movie matching: {query}")
        return results[0]
    
    @cache
    def search_episode(self, series_id: int, season_number: int, episode_number: int):
        return self._get(f"tv/{series_id}/season/{season_number}/episode/{episode_number}")
