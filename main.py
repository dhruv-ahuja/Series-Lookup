import series_lookup.config as config
import series_lookup.database as db
from series_lookup.controller import controller


def main():
    """
    The entrypoint to the application.
    """

    conn = db.connect_to_db(config.db_path)

    while True:
        controller(conn, config.tmdb, config.tv)


if __name__ == "__main__":
    main()
