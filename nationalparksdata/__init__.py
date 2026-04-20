from .scraper import run_scraper
from .loader import build_dataset


def refresh_dataset(save=True):
    """
    Run scraper, then rebuild final dataset.
    """
    run_scraper()
    return build_dataset(save=save)


__all__ = [
    "run_scraper",
    "build_dataset",
    "refresh_dataset"
]