import getopt
import logging
import os
import pathlib
import subprocess
import sys

from utils.utils import exec_sql_file, resource_path


class Differ:
    """
    differ
    """
    def __init__(self) -> None:
        self._usage_str = "Usage: {} diff [OPTIONS]\n" \
            "\n" \
            "Options: \n" \
            "  -h, --host   [REQUIRED] mysql host\n" \
            "  -P, --port   [OPTIONAL] mysql port\n" \
            "  -u, --user   [REQUIRED] mysql user\n" \
            "  -p, --passwd [REQUIRED] mysql password\n" \
            "    , --src    [REQUIRED] source sql file\n" \
            "    , --dst    [REQUIRED] destination sql file\n" \
            "".format(sys.argv[0])
        self._host = ""
        self._port = 3306
        self._user = ""
        self._passwd = ""
        self._src = ""
        self._dst = ""
        self._src_name = ""
        self._dst_name = ""
        self._src_db = ""
        self._dst_db = ""

    def run(self, args):
        """
        run differ
        """
        if self._init(args=args) is False:
            return False

        logging.info("----------------")
        logging.info("generate src database({}) from file({})".format(self._src_db, self._src))
        ret = exec_sql_file(self._src, self._host, self._port, self._user, self._passwd, self._src_db)
        if ret is not True:
            logging.error("failed generate source database")
            sys.exit(1)

        logging.info("----------------")
        logging.info("generate dst database({}) from file({})".format(self._dst_db, self._dst))
        ret = exec_sql_file(self._dst, self._host, self._port, self._user, self._passwd, self._dst_db)
        if ret is not True:
            logging.error("failed generate dst database")
            sys.exit(1)

        os.makedirs("output", exist_ok=True)

        logging.info("----------------")
        logging.info("generate update sql file")
        mysqldef = resource_path("tools/mysqldef")
        args = [mysqldef,
                "-h", self._host,
                "-P", str(self._port),
                "-u", self._user,
                "-p", self._passwd,
                self._src_db, "--dry-run"]
        update_sql_filepath = os.path.join(
            "output", "update-{}-{}.sql".format(self._src_name, self._dst_name))
        with open(update_sql_filepath, "w", encoding="utf-8") as writer:
            with subprocess.Popen(
                args=args,
                stdin=open(self._dst, "r", encoding="utf-8"),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True) as proc:
                for line in proc.stdout:
                    if line.startswith("--"):
                        continue
                    writer.write(line.rstrip())
                    writer.write("\n")
                proc.communicate()
        logging.info("generate update sql file: {}".format(update_sql_filepath))

        logging.info("----------------")
        logging.info("generate rollback sql file")
        mysqldef = resource_path("tools/mysqldef")
        args = [mysqldef,
                "-h", self._host,
                "-P", str(self._port),
                "-u", self._user,
                "-p", self._passwd,
                self._dst_db, "--dry-run"]
        rollback_sql_filepath = os.path.join(
            "output", "rollback-{}-{}.sql".format(self._src_name, self._dst_name))
        with open(rollback_sql_filepath, "w", encoding="utf-8") as writer:
            with subprocess.Popen(
                args=args,
                stdin=open(self._src, "r", encoding="utf-8"),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True) as proc:
                for line in proc.stdout:
                    if line.startswith("--"):
                        continue
                    writer.write(line.rstrip())
                    writer.write("\n")
                proc.communicate()
        logging.info("generate rollback sql file: {}".format(rollback_sql_filepath))

    def _init(self, args):
        """
        init arguments
        """
        opts, _ = getopt.getopt(
            args, "h:P:u:p:",
            ["help", "host=", "port=", "user=", "passwd=", "src=", "dst="]
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
            elif opt in ("--dst"):
                self._dst = arg
                self._dst_name = pathlib.Path(self._dst).stem
                self._dst_db = self._dst_name.replace(".", "_")

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
        if len(self._dst) == 0:
            logging.error("run without 'dst' field")
            logging.error(self._usage_str)
            return False

        return True
