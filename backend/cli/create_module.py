"""
CLI script to create a new FastAPI module following the project structure.
"""

import typer
from pathlib import Path
import re
from typing import Optional
from jinja2 import Environment, FileSystemLoader

app = typer.Typer(
    name="create-module",
    help="Create a new FastAPI module skeleton following Clean Architecture patterns",
    add_completion=False,
)


def get_template_env() -> Environment:
    """Get Jinja2 template environment"""
    template_dir = Path(__file__).parent / "templates"
    return Environment(
        loader=FileSystemLoader(template_dir), trim_blocks=True, lstrip_blocks=True
    )


def get_template_context(feature_name: str) -> dict:
    """Get template context variables"""
    pascal_case = "".join(word.capitalize() for word in feature_name.split("_"))
    return {"feature_name": feature_name, "pascal_case": pascal_case}


def validate_feature_name(feature_name: str) -> bool:
    """Validate feature name format (lowercase, alphanumeric, underscores)"""
    return bool(re.match(r"^[a-z][a-z0-9_]*$", feature_name))


def create_directory_structure(base_path: Path, feature_name: str) -> Path:
    """Create the module directory structure"""
    module_path = base_path / "apiapp" / "modules" / feature_name
    module_path.mkdir(parents=True, exist_ok=True)
    return module_path


def render_template_to_file(template_name: str, output_path: Path, context: dict):
    """Render a Jinja2 template to a file"""
    env = get_template_env()
    template = env.get_template(template_name)
    content = template.render(**context)
    output_path.write_text(content)


def create_module_files(module_path: Path, feature_name: str):
    """Create all module files using templates"""
    context = get_template_context(feature_name)

    # Create __init__.py
    render_template_to_file("__init__.py.j2", module_path / "__init__.py", context)

    # Create schemas.py
    render_template_to_file("schemas.py.j2", module_path / "schemas.py", context)

    # Create repository.py
    render_template_to_file("repository.py.j2", module_path / "repository.py", context)

    # Create use_case.py
    render_template_to_file("use_case.py.j2", module_path / "use_case.py", context)

    # Create router.py
    render_template_to_file("router.py.j2", module_path / "router.py", context)


def create_model_file(base_path: Path, feature_name: str) -> Path:
    """Create model file using template"""
    context = get_template_context(feature_name)
    models_path = base_path / "apiapp" / "models"
    model_file = models_path / f"{feature_name}_model.py"

    render_template_to_file("model.py.j2", model_file, context)
    return model_file


def print_success_message(feature_name: str, module_path: Path, model_file: Path):
    """Print success message with next steps"""
    pascal_case = "".join(word.capitalize() for word in feature_name.split("_"))

    typer.echo("", color=True)
    typer.secho(
        f"✅ Successfully created '{feature_name}' module skeleton!",
        fg=typer.colors.GREEN,
        bold=True,
    )
    typer.secho(f"📁 Module path: {module_path}", fg=typer.colors.BLUE)
    typer.secho(f"📄 Model file: {model_file}", fg=typer.colors.BLUE)
    typer.echo("")
    typer.secho("🔧 Next steps:", fg=typer.colors.YELLOW, bold=True)
    typer.echo(
        f"1. Update apiapp/infrastructure/database.py to include {pascal_case} model"
    )
    typer.echo(
        "2. Customize the generated skeleton files according to your requirements:"
    )
    typer.echo(f"   - Add model fields in {feature_name}_model.py")
    typer.echo("   - Add request/response schemas in schemas.py")
    typer.echo("   - Add repository methods in repository.py")
    typer.echo("   - Add business logic in use_case.py")
    typer.echo("   - Add API endpoints in router.py")
    typer.echo("3. The router will be auto-discovered when you add endpoints")
    typer.echo("")
    typer.secho("📝 Generated skeleton files:", fg=typer.colors.CYAN, bold=True)
    typer.echo(f"   - {module_path}/__init__.py")
    typer.echo(f"   - {module_path}/schemas.py (basic structure)")
    typer.echo(f"   - {module_path}/repository.py (basic structure)")
    typer.echo(f"   - {module_path}/use_case.py (basic structure)")
    typer.echo(f"   - {module_path}/router.py (basic structure)")
    typer.echo(f"   - {model_file} (basic structure)")
    typer.echo("")
    typer.secho(
        "💡 All files contain TODO comments to guide your implementation",
        fg=typer.colors.MAGENTA,
    )


@app.command()
def create(
    feature_name: Optional[str] = typer.Argument(
        None, help="Feature name (e.g., 'products', 'orders', 'user_profiles')"
    ),
    force: bool = typer.Option(
        False, "--force", "-f", help="Force creation even if module already exists"
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Show what would be created without actually creating files",
    ),
):
    """
    Create a new FastAPI module skeleton following Clean Architecture patterns.

    Generates basic structure without CRUD implementation - ready for customization.
    """

    # Get current directory
    current_dir = Path.cwd()

    # Check if we're in the right directory
    if not (current_dir / "apiapp").exists():
        typer.secho(
            "❌ Error: This script must be run from the project root directory",
            fg=typer.colors.RED,
            err=True,
        )
        typer.secho(
            "   Make sure you're in the directory containing 'apiapp' folder",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(1)

    # Get feature name from user if not provided
    if not feature_name:
        feature_name = (
            typer.prompt(
                "📝 Enter feature name (e.g., 'products', 'orders', 'user_profiles')"
            )
            .strip()
            .lower()
        )

    if not feature_name:
        typer.secho("❌ Feature name cannot be empty", fg=typer.colors.RED, err=True)
        raise typer.Exit(1)

    if not validate_feature_name(feature_name):
        typer.secho(
            "❌ Invalid feature name. Use lowercase letters, numbers, and underscores only.",
            fg=typer.colors.RED,
            err=True,
        )
        typer.secho(
            "   Examples: 'products', 'user_profiles', 'order_items'",
            fg=typer.colors.YELLOW,
            err=True,
        )
        raise typer.Exit(1)

    # Check if module already exists
    module_path = current_dir / "apiapp" / "modules" / feature_name
    if module_path.exists() and not force:
        typer.secho(
            f"❌ Module '{feature_name}' already exists at {module_path}",
            fg=typer.colors.RED,
            err=True,
        )
        typer.secho(
            "   Use --force to overwrite or choose a different name",
            fg=typer.colors.YELLOW,
            err=True,
        )
        raise typer.Exit(1)

    # Show what will be created
    typer.secho(
        f"📋 Creating module skeleton: {feature_name}", fg=typer.colors.CYAN, bold=True
    )
    typer.secho(f"📁 Location: apiapp/modules/{feature_name}", fg=typer.colors.BLUE)

    if dry_run:
        typer.secho(
            "\n🔍 DRY RUN - Files that would be created:",
            fg=typer.colors.YELLOW,
            bold=True,
        )
        typer.echo(f"   - {module_path}/__init__.py")
        typer.echo(f"   - {module_path}/schemas.py")
        typer.echo(f"   - {module_path}/repository.py")
        typer.echo(f"   - {module_path}/use_case.py")
        typer.echo(f"   - {module_path}/router.py")
        typer.echo(f"   - apiapp/models/{feature_name}_model.py")
        return

    # Confirm creation if not in force mode
    if not force:
        confirm = typer.confirm(f"❓ Create '{feature_name}' module skeleton?")
        if not confirm:
            typer.secho("❌ Module creation cancelled", fg=typer.colors.RED)
            raise typer.Exit(0)

    try:
        # Create module structure
        typer.secho("\n🔨 Creating module skeleton structure...", fg=typer.colors.CYAN)
        module_path = create_directory_structure(current_dir, feature_name)

        # Create files using templates
        typer.echo("📝 Creating module files from templates...")
        create_module_files(module_path, feature_name)

        typer.echo("📝 Creating model file...")
        model_file = create_model_file(current_dir, feature_name)

        # Success message
        print_success_message(feature_name, module_path, model_file)

    except Exception as e:
        typer.secho(f"❌ Error creating module: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(1)


@app.command()
def list():
    """List all existing modules in the project."""
    current_dir = Path.cwd()
    modules_path = current_dir / "apiapp" / "modules"

    if not modules_path.exists():
        typer.secho("❌ No modules directory found", fg=typer.colors.RED, err=True)
        raise typer.Exit(1)

    modules = [
        d.name
        for d in modules_path.iterdir()
        if d.is_dir() and not d.name.startswith(".") and d.name != "__pycache__"
    ]

    if not modules:
        typer.secho("📭 No modules found", fg=typer.colors.YELLOW)
        return

    typer.secho("📚 Existing modules:", fg=typer.colors.CYAN, bold=True)
    for module in sorted(modules):
        typer.secho(f"   - {module}", fg=typer.colors.GREEN)


if __name__ == "__main__":
    app()
