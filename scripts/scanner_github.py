import pandas as pd
import subprocess
import argparse
import datetime
import os



arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("--csv", type=str)
arg_parser.add_argument("--git_url", type=str)
arg_parser.add_argument("--language", type=str)
args = arg_parser.parse_args()


def shell(command: str):
    subprocess.run(command, shell=True)


def clone_git_repo(git_url: str, src_dir: str):
    src_dir = os.path.abspath(src_dir)
    subprocess.run(
        f"cd {src_dir} && git clone {git_url}",
        capture_output=True,
        shell=True
    )
    print("Git Repo Cloned to Source Directory")


def create_dirs(git_url: str):
    src_base_path = os.getenv("SOURCE_DIR")
    res_base_path = os.getenv("RESULT_DIR")
    name = get_git_repo_name(git_url)
    owner = get_git_repo_owner(git_url)
    src_dir = os.path.join(src_base_path, owner)
    res_dir = os.path.join(res_base_path, owner, name)
    shell(f"mkdir -p {src_dir} {res_dir}")
    return src_dir, res_dir


def get_current_date_version():
    return datetime.date.today().strftime("%Y.%m.%d")


def get_git_repo_name(git_url: str):
    return git_url.rstrip("/").split("/")[-1]


def get_git_repo_owner(git_url: str):
    return git_url.rstrip("/").split("/")[-2]


def get_git_repo_latest_commit(src_dir: str):
    hash = subprocess.run(
        f"cd {src_dir} && git rev-parse HEAD",
        capture_output=True,
        shell=True
    ).stdout.decode("utf-8").strip()
    print("Git Repo Latest Commit Hash:", hash)
    return hash


def scan_codeql(src_dir: str, res_dir: str, language: str):
    docker_image = os.getenv("DOCKER_IMAGE")
    shell(f"docker run --rm -v {src_dir}:/workspace/source -v {res_dir}:/workspace/result -t {docker_image} --language {language} --queries security-and-quality")


def process_single(git_url: str, language: str):
    try:
        print("[logging] Processing:", git_url)

        repo_name = get_git_repo_name(git_url)
        owner_name = get_git_repo_owner(git_url)
        src_dir, res_dir = create_dirs(git_url)

        print("[logging] Cloning:", git_url)
        clone_git_repo(
            git_url=git_url,
            src_dir=src_dir
        )
        src_dir = os.path.join(src_dir, repo_name)
        git_repo_version = get_current_date_version()

        print("[logging] Scanning:", git_url)
        scan_codeql(
            src_dir=src_dir,
            res_dir=res_dir,
            language=language
        )

        print("[logging] Post-processing:", git_url)
        sarif_dir = os.getenv("SARIF_DIR")
        for sarif_file in os.listdir(res_dir):
            if sarif_file.endswith(".sarif"):
                final_file = f"github__{language}__{owner_name}__{repo_name}__{git_repo_version}__{sarif_file}"
                shell(f"cp {res_dir}/{sarif_file} {sarif_dir}/{final_file}")
                print("SARIF files copied to destination")

    except Exception as e:
        print("[logging] Exception:")
        print(e)


def main():

    if args.csv:
        csv_path = os.path.abspath(args.csv)
        df = pd.read_csv(csv_path)

        for _, row in df.iterrows():
            git_url = row["repo_url"]
            language = row["repo_language"]
            process_single(git_url, language)

    elif args.git_url:
        process_single(args.git_url, args.language)

    else:
        arg_parser.print_usage()
        exit(0)


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    main()
