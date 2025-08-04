# MCP Server Python Project Template

A [Cookiecutter](https://github.com/cookiecutter/cookiecutter) template for creating Model Context Protocol (MCP) servers in Python.

## Features

- 🚀 **Rapid Setup**: Quickly scaffold a complete Python MCP Server with sensible defaults.
- 📦 **Modern Package Management**: Uses [uv](https://docs.astral.sh/uv/) for blazing-fast dependency management.
- 🏢 **Nexus Publishing Ready**: Streamlined support for packaging and publishing to company private Nexus repository.
- 🐳 **Container-Friendly**: Includes a `Dockerfile` for easy building and deployment of Docker images.

## Prerequisites

- Python >=3.11
- [Cookiecutter](https://cookiecutter.readthedocs.io/en/latest/installation.html)
- [uv](https://docs.astral.sh/uv/) (recommended)

## Quick start

### 1. Install Prerequisites

**Cookiecutter**

```bash
# Using pipx (recommended)
pipx install cookiecutter

# Or using pip
pip install cookiecutter
```

**uv**

```bash
# Using the installer script for macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Generate Your Project

You can generate a new MCP server project from this template in a few ways.

#### Option 1: From GitHub (Recommended)

```bash
cookiecutter git@github.com:AfterShip/boilerplate-python-mcp-server \
  project_name="Your project name" \
  author_name="Your name" \
  author_email="Your email" \
  --no-input \
  --output-dir "Your output directory"
```

#### Option 2: From a Local Clone

```bash
# Clone this template repository
git clone git@github.com:AfterShip/boilerplate-python-mcp-server.git

cd boilerplate-python-mcp-server

cookiecutter . \
  project_name="your_project_name" \
  author_name="your_name" \
  author_email="your_email" \
  --no-input \
  --output-dir "your_output_directory"
```

And that's it! You're now ready to start developing your custom MCP Server.

## Configuration Options

You will be prompted for the following information when generating a project (unless you use `--no-input`):

| Parameter             | Description                                           | Default Value                                          |
| --------------------- | ----------------------------------------------------- | ------------------------------------------------------ |
| `project_name`        | The name of the project (e.g., "Tracking MCP Server") | `my-mcp-server`                                        |
| `project_slug`        | The project identifier (auto-generated)               | `my_mcp_server`                                        |
| `package_name`        | The Python package name (auto-generated)              | `my_mcp_server`                                        |
| `project_description` | A short description of the project.                   | `A modern Python MCP server.`                          |
| `author_name`         | Your name.                                            | `your name`                                            |
| `author_email`        | Your email.                                           | `you@example.com`                                      |
| `version`             | The initial version number.                           | `0.1.0`                                                |
| `python_version`      | The Python version to use.                            | `3.11`                                                 |
| `license`             | The license for the project.                          | `MIT`                                                  |
| `include_tests`       | Include tests? (y/n)                                  | `y`                                                    |
| `include_docker`      | Include Docker configuration? (y/n)                   | `y`                                                    |


## What Happens Next?

After you run `cookiecutter`, a `post_gen_project.py` hook script automatically performs these steps for you inside the newly created project directory:

1. **Initializes a Git repository**: `git init`
2. **Installs dependencies**: `uv sync --dev`
3. **Creates an initial commit**: `git add . && git commit -m "Initial commit"`

## Developing Your MCP Server

Your generated project includes its own `README.md` with detailed instructions for development, testing, and running the server.

Here are some quick commands to get you started (run from your new project's directory):

```bash
# Run the server (defaults to stdio transport)
uv run your_package_name

# Run tests
uv run pytest
```

Refer to the [README.md]({{cookiecutter.project_slug}}/README.md) inside your new project for more details.

## Customizing This Template

You can fork this repository and customize it to your needs:

1. **Modify default values**: Edit the `cookiecutter.json` file.
2. **Add or remove files**: Add/remove files in the `{{cookiecutter.project_slug}}/` directory.
3. **Change file content**: Edit the template files. They use [Jinja2](https://jinja.palletsprojects.com/) syntax for templating.

Example of Jinja2 syntax:

```jinja2
{% if cookiecutter.include_docker == 'y' -%}
# This content will only be included if the user chooses to include Docker support.
{% endif -%}

Project Name: {{ cookiecutter.project_name }}
```

## Contributing

Contributions to improve this template are welcome! Please feel free to submit issues and pull requests.
