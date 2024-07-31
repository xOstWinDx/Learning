import logging


def configure_logger(level: int | str = logging.INFO):
    logging.basicConfig(
        level=level,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="[%(asctime)s.%(msecs)03d] %(module)12s:%(lineno)3d %(levelname)-7s - %(name)s - %(message)s",
        handlers=[logging.StreamHandler()]
    )
