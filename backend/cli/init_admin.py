"""
CLI command to initialize admin user
"""

import typer
import asyncio
from pathlib import Path
import sys

# Add the parent directory to sys.path to import apiapp
sys.path.insert(0, str(Path(__file__).parent.parent))

app = typer.Typer(
    name="init-admin",
    help="Initialize admin user in the database",
    add_completion=False,
)


async def create_admin_user(
    database_uri: str, email: str, username: str, password: str
):
    """Create admin user in the database"""
    from apiapp import models

    class Setting:
        def __init__(self, db_uri: str):
            self.DATABASE_URI = db_uri

    settings = Setting(database_uri)
    await models.init_beanie(settings)

    typer.echo("🔍 Checking for existing admin user...")
    user = await models.User.find_one(models.User.username == username)

    if user:
        typer.secho(f"✅ Admin user '{username}' already exists", fg=typer.colors.GREEN)
        typer.echo(f"   Email: {user.email}")
        typer.echo(f"   Roles: {user.roles}")
        return user

    typer.echo("👤 Creating new admin user...")
    user = models.User(
        email=email,
        username=username,
        password="",
        first_name="Admin",
        last_name="User",
        roles=["user", "admin"],
        status="active",
    )
    await user.set_password(password)
    await user.save()

    typer.secho(
        f"✅ Admin user '{username}' created successfully!",
        fg=typer.colors.GREEN,
        bold=True,
    )
    typer.echo(f"   Email: {email}")
    typer.echo(f"   Username: {username}")
    typer.echo(f"   Roles: {user.roles}")

    return user


@app.command()
def create(
    database_uri: str = typer.Option(
        "mongodb://localhost/appdb",
        "--database-uri",
        "-d",
        help="MongoDB connection URI",
    ),
    email: str = typer.Option(
        "admin@example.com", "--email", "-e", help="Admin user email"
    ),
    username: str = typer.Option("admin", "--username", "-u", help="Admin username"),
    password: str = typer.Option(
        "p@ssw0rd",
        "--password",
        "-p",
        help="Admin password",
        prompt=True,
        hide_input=True,
        confirmation_prompt=True,
    ),
    docker: bool = typer.Option(
        False, "--docker", help="Use docker MongoDB URI (mongodb://mongodb/appdb)"
    ),
):
    """Create an admin user in the database"""

    if docker:
        database_uri = "mongodb://mongodb/appdb"

    typer.secho("🔧 Initializing admin user...", fg=typer.colors.CYAN, bold=True)
    typer.echo(f"📍 Database URI: {database_uri}")
    typer.echo(f"📧 Email: {email}")
    typer.echo(f"👤 Username: {username}")

    if not typer.confirm("❓ Proceed with admin user creation?"):
        typer.secho("❌ Operation cancelled", fg=typer.colors.RED)
        raise typer.Exit(0)

    try:
        asyncio.run(create_admin_user(database_uri, email, username, password))
    except Exception as e:
        typer.secho(f"❌ Error creating admin user: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
