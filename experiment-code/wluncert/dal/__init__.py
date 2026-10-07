try:
    from .regressor import DaLRegressor
except ModuleNotFoundError as error:
    # The DaL helper modules in dal/utils/ are third-party code (DaL-ext) that
    # we do not redistribute; they are downloaded by experiment-code/fetch_dal.py.
    if ".utils" not in (error.name or ""):
        raise
    raise ModuleNotFoundError(
        "DaL helper modules not found ({}). Run `python3 fetch_dal.py` "
        "in experiment-code/ to download them.".format(error.name),
        name=error.name,
    ) from error
