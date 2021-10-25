import logging

def config_logger(
    name="",
    level=logging.INFO,
    _format="%(levelname)s - [%(asctime)s] - %(filename)s:%(lineno)d: %(message)s",
    handler=logging.StreamHandler,
    propagate=False,
):
    """ configures a logger """
    _handler = handler()
    _handler.setFormatter(logging.Formatter(_format))
    _logger = logging.getLogger(name)
    _logger.addHandler(_handler)
    _logger.setLevel(level)
    _logger.propagate = propagate
    return _logger
