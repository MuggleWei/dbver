import getopt
import logging
import os
import sys

import sqlglot


class Fcc:
    """
    field consistency check
    """
    def __init__(self) -> None:
        self._usage_str = "Usage: {} fcc [OPTIONS]\n" \
            "\n" \
            "Options: \n" \
            "  -f, --file  [OPTIONAL] sql file\n" \
            "  -d, --dir   [OPTIONAL] directory that include sql files\n" \
            "".format(sys.argv[0])
        self._files = []
        self._dirs = []

    def run(self, args):
        """
        run fcc
        """
        if self._init(args=args) is False:
            return False

        # parse files into field type dict
        field_type_dict = {}
        files = self._get_sql_files()
        try:
            for file in files:
                with open(file, "r", encoding="utf-8") as f:
                    sql_script = f.read()
                expressions = sqlglot.parse(sql_script, dialect="mysql")
                if expressions:
                    for _, stmt in enumerate(expressions):
                        if isinstance(stmt, sqlglot.exp.Create) and \
                                stmt.args.get("kind") == "TABLE":
                            table_col_dict = self._extract_create_stmt_info(stmt)
                            for col_name, col_type in table_col_dict.items():
                                if col_name not in field_type_dict:
                                    field_type_dict[col_name] = set()
                                field_type_dict[col_name].add(col_type)
        except IOError as e:
            logging.error("IO error: {}".format(e))
            return False
        except Exception as e:
            logging.error("{}".format(e))
            return False

        for field_name, field_type_set in field_type_dict.items():
            if len(field_type_set) > 1:
                logging.error("field '{}' has multiple type: {}".format(field_name, list(field_type_set)))

        return True

    def _extract_create_stmt_info(self, stmt: sqlglot.exp.Create):
        """
        extract field's name, type and attr
        """
        field_type_dict = {}
        schema = stmt.args.get("schema") or stmt.this
        if schema and hasattr(schema, "expressions"):
            for col_def in schema.expressions:
                if not isinstance(col_def, sqlglot.exp.ColumnDef):
                    continue
                col_name = col_def.name

                if col_def.args.get("kind"):
                    type_node = col_def.args["kind"]
                    data_type = type_node.sql()
                    field_type_dict[col_name] = data_type

        return field_type_dict

    def _get_sql_files(self):
        """
        get sql files
        """
        files = []
        for file in self._files:
            if not file.endswith(".sql"):
                logging.error("invalid file '{}', cause it's not endswith sql")
                sys.exit(1)
            if not os.path.exists(file):
                logging.error("file not exists, file: {}".format(file))
                sys.exit(1)
            files.append(file)

        for d in self._dirs:
            for dirpath, _, filenames in os.walk(d):
                for filename in filenames:
                    if not filename.endswith(".sql"):
                        continue
                    filepath = os.path.join(dirpath, filename)
                    files.append(filepath)

        if len(files) == 0:
            logging.error("run without input files")
            logging.error(self._usage_str)
            sys.exit(1)

        return files

    def _init(self, args):
        """
        init arguments
        """
        opts, _ = getopt.getopt(args, "f:d:", ["help", "file", "dir"])
        for opt, arg in opts:
            if opt in ("--help"):
                logging.info(self._usage_str)
                sys.exit(0)
            elif opt in ("-f", "--file"):
                self._files.append(arg)
            elif opt in ("-d", "--dir"):
                self._dirs.append(arg)

        return True
