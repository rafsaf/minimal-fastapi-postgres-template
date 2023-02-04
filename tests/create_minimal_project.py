"""
Creates minimal template project in root folder with default values
"""

from pathlib import Path

from cookiecutter.main import cookiecutter

ROOT_FOLDER = Path(__file__).parent.parent


def main():
    cookiecutter(
        template=str(ROOT_FOLDER),
        no_input=True,
        extra_context={
            "project_name": "minimal_project",
        },
    )


if __name__ == "__main__":
    main()
