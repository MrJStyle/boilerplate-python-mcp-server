"""{{ cookiecutter.project_name }}: {{ cookiecutter.project_description }}"""
from .entrypoint import main


__version__ = "{{ cookiecutter.version }}"
__author__ = "{{ cookiecutter.author_name }}"
__email__ = "{{ cookiecutter.author_email }}"

if __name__ == "__main__":
    main()
