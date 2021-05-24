from pathlib import Path
import os
import git
from typing import List

MAIN = """
経路計画に主に

"""


def get_git_root(path) -> str:
    git_repo = git.Repo(path, search_parent_directories=True)
    git_root = git_repo.git.rev_parse("--show-toplevel")
    return git_root


def get_papers(base) -> List[str]:
    papers = []
    lookingfor = "summary.md"
    for path in Path(base).rglob(lookingfor):
        paper = os.path.basename(path.parent)

        link = f"{path.parent.relative_to(base)}/{lookingfor}"
        # link = link.replace(" ", "%20")
        line = f"* [{paper}]({link})\n"
        papers.append(line)
    return papers


if __name__ == "__main__":
    git_top = get_git_root(".")
    papers = get_papers(git_top)
    print(papers)

    with open("index.md", "w") as f:
        f.write(MAIN)

        # for paper in papers:
        f.writelines(papers)

    f.close()
