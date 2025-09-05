import getopt
import logging
import subprocess
import sys

from utils.utils import resource_path


class Checker:
    """
    checker
    """
    def __init__(self) -> None:
        self._usage_str = "Usage: {} check [OPTIONS\n]" \
            "\n" \
            "Options: \n" \
            "  -h, --host     [REQUIRED] mysql host\n" \
            "  -P, --port     [OPTIONAL] mysql port\n" \
            "  -u, --user     [REQUIRED] mysql user\n" \
            "  -p, --passwd   [REQUIRED] mysql password\n" \
            "    , --database [REQUIRED] database name\n" \
            "    , --dst      [REQUIRED] destination sql file\n" \
            "".format(sys.argv[0])
        self._host = ""
        self._port = 3306
        self._user = ""
        self._passwd = ""
        self._database = ""
        self._dst = ""

    def run(self, args):
        """
        run checker
        """
        if self._init(args=args) is False:
            return False

        logging.info("----------------")
        logging.info("compare database({}:{}/{}) and dst sql file({})".format(
            self._host, self._port, self._database, self._dst))
        mysqldef = resource_path("tools/mysqldef")
        args = [mysqldef,
                "-h", self._host,
                "-P", str(self._port),
                "-u", self._user,
                "-p", self._passwd,
                self._database, "--dry-run"]
        cnt = 0
        with subprocess.Popen(
            args=args,
            stdin=open(self._dst, "r", encoding="utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True) as proc:
            for line in proc.stdout:
                if line.startswith("--"):
                    continue
                logging.warning(line.rstrip())
                cnt += 1
            proc.communicate()
        logging.info("total diff: {}".format(cnt))

    def _init(self, args):
        """
        init arguments
        """
        opts, _ = getopt.getopt(
            args, "h:P:u:p:",
            ["help", "host=", "port=", "user=", "passwd=", "database=", "dst="]
        )
        for opt, arg in opts:
            if opt in ("--help"):
                logging.info(self._usage_str)
                sys.exit(0)
            elif opt in ("-h", "--host"):
                self._host = arg
            elif opt in ("-P", "--port"):
                self._port = int(arg)
            elif opt in ("-u", "--user"):
                self._user = arg
            elif opt in ("-p", "--passwd"):
                self._passwd = arg
            elif opt in ("--database"):
                self._database = arg
            elif opt in ("--dst"):
                self._dst = arg

        if len(self._host) == 0:
            logging.error("run without 'host' field")
            logging.error(self._usage_str)
            return False
        if self._port == 0:
            logging.error("run without 'port' field")
            logging.error(self._usage_str)
            return False
        if len(self._user) == 0:
            logging.error("run without 'user' field")
            logging.error(self._usage_str)
            return False
        if len(self._passwd) == 0:
            logging.error("run without 'passwd' field")
            logging.error(self._usage_str)
            return False
        if len(self._database) == 0:
            logging.error("run without 'database' field")
            logging.error(self._usage_str)
            return False
        if len(self._dst) == 0:
            logging.error("run without 'dst' field")
            logging.error(self._usage_str)
            return False

        return True
