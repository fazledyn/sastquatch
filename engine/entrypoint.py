import subprocess
import argparse
import sys


arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("--language", type=str)
arg_parser.add_argument("--queries", type=str)
args = arg_parser.parse_args()


def print_help():
    sys.stdout.write("Usage: <script> --language $value --queries $value\n")
    sys.stdout.write("Options:                                          \n")
    sys.stdout.write("--language                                        \n")
    sys.stdout.write("    python                                        \n")
    sys.stdout.write("    javascript                                    \n")
    sys.stdout.write("\n")
    sys.stdout.write("--queries                                         \n")
    sys.stdout.write("    code-scanning            Low                  \n")
    sys.stdout.write("    security-extended        Medium               \n")
    sys.stdout.write("    security-and-quality     High                 \n")
    sys.stdout.write("\n")


if not args.language or not args.queries:
    print_help()
    exit(0)


SOURCE_DIR = "/workspace/source"
RESULT_DIR = "/workspace/result"

language = args.language
queries = args.queries
querypack = f"{language}-{queries}.qls"


# default CodeQL
# ========================================================
sys.stdout.write("Starting Default CodeQL Analysis ...\n")

sys.stdout.write("Step [1/3] Creating CodeQL Database ...\n")
subprocess.run(f"codeql database create --overwrite --language {language} -s {SOURCE_DIR} {RESULT_DIR}/_codeqldb.{queries}", shell=True)

sys.stdout.write("Step [2/3] Analyzing CodeQL Database ...\n")
subprocess.run(f"codeql database analyze --format sarif-latest --output {RESULT_DIR}/codeql-result.temp.sarif {RESULT_DIR}/_codeqldb.{queries} {querypack}", shell=True)

sys.stdout.write("Step [3/3] Formatting Output & Cleaning Up ...\n")
subprocess.run(f"jq . {RESULT_DIR}/codeql-result.temp.sarif --indent 4 > {RESULT_DIR}/codeql-result.{queries}.sarif", shell=True)
subprocess.run(f"rm -rf {RESULT_DIR}/_codeqldb.{queries} {RESULT_DIR}/codeql-result.temp.sarif", shell=True)

sys.stdout.write("Ending Default CodeQL Analysis ...\n")
# ========================================================


# default Semgrep
# ========================================================
sys.stdout.write("Starting Semgrep Analysis ...\n")

sys.stdout.write("Step [1/2] Running Semgrep Queries ...\n")
subprocess.run(f"cd {SOURCE_DIR} && semgrep -f /workspace/tools/semgrep/rules --sarif > {RESULT_DIR}/semgrep-result.temp.sarif", shell=True)

sys.stdout.write("Step [2/2] Formatting Semgrep Output ...\n")
subprocess.run(f"jq . {RESULT_DIR}/semgrep-result.temp.sarif --indent 4 > {RESULT_DIR}/semgrep-result.sarif", shell=True)
subprocess.run(f"rm -rf {RESULT_DIR}/semgrep-result.temp.sarif", shell=True)

sys.stdout.write("Ending Semgrep Analysis ...\n")
# ========================================================

