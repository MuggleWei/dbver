import logging
import subprocess
import sys

from __version__ import __version__
from command.checker import Checker
from command.differ import Differ
from command.normalizer import Normalizer
from utils.utils import resource_path


def run_diff():
    """
    run diff
    """
    differ = Differ()
    if differ.run(sys.argv[2:]) is False:
        sys.exit(1)


def run_check():
    """
    run check
    """
    checker = Checker()
    if checker.run(sys.argv[2:]) is False:
        sys.exit(1)

def run_normalize():
    """
    run normalize
    """
    normalizer = Normalizer()
    if normalizer.run(sys.argv[2:]) is False:
        sys.exit(1)


def run_inner():
    """
    run inner
    """
    mysqldef = resource_path("tools/mysqldef")
    args = [mysqldef]
    if len(sys.argv) > 2:
        args.extend(sys.argv[2:])
    with subprocess.Popen(
        args=args,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True)  as proc:
        for line in proc.stdout:
            print(line.rstrip())
        proc.communicate()


class LogCustomFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    fmt = "%(levelname)s - %(message)s"

    FORMATS = {
        logging.DEBUG: grey + fmt + reset,
        logging.INFO: grey + fmt + reset,
        logging.WARNING: yellow + fmt + reset,
        logging.ERROR: red + fmt + reset,
        logging.CRITICAL: bold_red + fmt + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)



if __name__ == "__main__":
    # init log
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(LogCustomFormatter())

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    # parse sys.args
    usage_str = "Usage: {} COMMAND [OPTIONS]\n" \
        "\n" \
        "Commands:\n" \
        "  normal  nromalize sql file\n" \
        "  diff    generate update and rollback sql\n" \
        "  check   check is db match\n" \
        "".format(sys.argv[0])

    if len(sys.argv) < 2:
        logging.error(usage_str)
        sys.exit(1)

    if sys.argv[1] in ("-h", "--help"):
        logging.info(usage_str)
        sys.exit(0)

    if sys.argv[1] in ("-v", "--version"):
        print("dbver {}".format(__version__))
        sys.exit(0)

    # run command
    command_dict = {
        "diff": run_diff,
        "check": run_check,
        "normal": run_normalize,
        "inner": run_inner,
    }

    command = sys.argv[1]
    func = command_dict.get(command, None)
    try:
        if func is not None:
            func()
        else:
            logging.error(usage_str)
            sys.exit(1)
    except Exception as e:
        logging.exception("{}".format(e))
        sys.exit(1)
