import getopt
import logging
import os
import pathlib
import subprocess
import sys

from utils.utils import exec_sql_file, resource_path

class Normalizer:
    """
    normailzer
    """
    def __init__(self) -> None:
        self._usage_str = "Usage: {} normal [OPTIONS]\n" \
            "\n" \
            "Options: \n" \
            "  -h, --host    [REQUIRED] mysql host\n" \
            "  -P, --port    [OPTIONAL] mysql port\n" \
            "  -u, --user    [REQUIRED] mysql user\n" \
            "  -p, --passwd  [REQUIRED] mysql password\n" \
            "    , --src     [REQUIRED] source sql file\n" \
            "    , --charset [OPTIONAL] create database with character set, by default, value is utf8mb4\n" \
            "    , --collate [OPTIONAL] create database with collate, by default, value is utf8mb4_bin\n" \
            "".format(sys.argv[0])
        self._host = ""
        self._port = 3306
        self._user = ""
        self._passwd = ""
        self._charset = "utf8mb4"
        self._collate = "utf8mb4_bin"
        self._src = ""

    def run(self, args):
        """
        run normalize
        """
        if self._init(args=args) is False:
            return False

        # write sql into db
        logging.info("----------------")
        logging.info("generate src database({}) from file({})".format(self._src_db, self._src))
        ret = exec_sql_file(
            self._src, self._host, self._port, self._user, self._passwd, self._src_db, self._charset, self._collate)
        if ret is not True:
            logging.error("failed generate source database")
            sys.exit(1)

        os.makedirs("output", exist_ok=True)
        mysqldef = resource_path("tools/mysqldef")

        # generate normal sql file
        logging.info("----------------")
        logging.info("generate normal sql file")
        args = [mysqldef,
                "-h", self._host,
                "-P", str(self._port),
                "-u", self._user,
                "-p", self._passwd,
                self._src_db, "--export"]
        normal_src = os.path.join("output", "{}.sql".format(self._src_name))
        with open(normal_src, "w", encoding="utf-8") as writer:
            with subprocess.Popen(
                args=args,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True) as proc:
                for line in proc.stdout:
                    writer.write(line.rstrip())
                    writer.write("\n")
                proc.communicate()
        logging.info("generate normal src sql file: {}".format(normal_src))

    def _init(self, args):
        """
        init arguments
        """
        opts, _ = getopt.getopt(
            args, "h:P:u:p:",
            ["help", "host=", "port=", "user=", "passwd=", "src=", "dst=", "charset=", "collate=", "normal="]
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
            elif opt in ("--src"):
                self._src = arg
                self._src_name = pathlib.Path(self._src).stem
                self._src_db = self._src_name.replace(".", "_")
            elif opt in ("--charset"):
                self._charset = arg
            elif opt in ("--collate"):
                self._collate = arg

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
        if len(self._src) == 0:
            logging.error("run without 'src' field")
            logging.error(self._usage_str)
            return False

        return True
