import series_lookup.app as app
import series_lookup.config as config


def main():
    a = app.Application(tmdb=config.tmdb, tv=config.tv)
    a()


if __name__ == "__main__":
    main()
