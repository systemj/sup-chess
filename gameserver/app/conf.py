""" load configuration from yaml file """
from yaml import load
# import CLoader (fast) if available
try:
    from yaml import CSafeLoader as Loader
except ImportError:
    from yaml import SafeLoader as Loader


# app default configuration settings
defaults = {
    "DEBUG": False,
    "chess_engine_url_scheme": "http",
    "chess_engine_url_host": "chess-engine",
    "chess_engine_url_port": "8000",
    "redis_host": "redis",
    "redis_port": "6379",
}


def init(app):
    """ load settings from external configuration file """
    # load defaults
    for setting in defaults:
        app.config[setting] = defaults[setting]
    try:
        with open(app.config["config_file"], "r") as config_yaml:
            config_data = load(config_yaml, Loader=Loader)
            # apply the settings from the file
            for key in config_data:
                app.config[key] = config_data[key]
    except FileNotFoundError:
        # If config.yaml doesn't exist the defaults will be used
        pass
