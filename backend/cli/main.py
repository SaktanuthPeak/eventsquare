"""
Main CLI application for FastAPI Beanie Starter
"""

import typer
import subprocess
import os
from .create_module import app as create_module_app
from .init_admin import app as init_admin_app

app = typer.Typer(
    name="velo", help="FastAPI Beanie Starter CLI Tools", add_completion=False
)

# Create app subcommand group
app_commands = typer.Typer(
    name="app", help="Application server commands", add_completion=False
)

# Add subcommands
app.add_typer(app_commands, name="app")
app.add_typer(create_module_app, name="module")
app.add_typer(init_admin_app, name="admin")


@app_commands.command()
def run(
    mode: str = typer.Argument(..., help="Server mode: dev or prod"),
    host: str = typer.Option("0.0.0.0", "--host", "-h", help="Host to bind to"),
    port: int = typer.Option(9000, "--port", "-p", help="Port to bind to"),
    log_level: str = typer.Option(
        None, "--log-level", "-l", help="Logging level (DEBUG, INFO, WARNING, ERROR)"
    ),
):
    """Run the FastAPI application server in development or production mode"""

    # Validate mode
    if mode not in ["dev", "prod", "development", "production"]:
        typer.secho(
            f"❌ Invalid mode '{mode}'. Use 'dev' or 'prod'",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(1)

    # Normalize mode
    is_dev = mode in ["dev", "development"]
    mode_name = "development" if is_dev else "production"

    # Set default log level based on mode
    if log_level is None:
        log_level = "DEBUG" if is_dev else "INFO"

    # Display startup message
    color = typer.colors.CYAN if is_dev else typer.colors.GREEN
    emoji = "🔧" if is_dev else "🚀"
    typer.secho(f"{emoji} Starting {mode_name} server...", fg=color, bold=True)
    typer.echo(f"📍 Host: {host}")
    typer.echo(f"🔌 Port: {port}")
    typer.echo(f"📊 Log Level: {log_level}")

    # Set environment variables
    env = os.environ.copy()
    env["APP_ENV"] = "dev" if is_dev else "prod"

    # Map log level to numeric value
    log_level_map = {"DEBUG": "10", "INFO": "20", "WARNING": "30", "ERROR": "40"}
    env["LOGGING_LEVEL"] = log_level_map.get(log_level.upper(), "20")

    # Build command based on mode
    if is_dev:
        cmd = [
            "poetry",
            "run",
            "fastapi",
            "dev",
            "apiapp/main.py",
            "--host",
            host,
            "--port",
            str(port),
        ]
    else:
        cmd = ["poetry", "run", "fastapi", "run", "apiapp/main.py", "--port", str(port)]

    try:
        subprocess.run(cmd, env=env, check=True)
    except KeyboardInterrupt:
        typer.secho(
            f"\n🛑 {mode_name.capitalize()} server stopped", fg=typer.colors.YELLOW
        )
    except subprocess.CalledProcessError as e:
        typer.secho(
            f"❌ Failed to start {mode_name} server: {e}", fg=typer.colors.RED, err=True
        )
        raise typer.Exit(1)


def main():
    """Main entry point for the CLI"""
    app()


if __name__ == "__main__":
    main()
