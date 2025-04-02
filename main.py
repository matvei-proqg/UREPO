from fastapi import FastAPI
from auth.jwt_manager import JWTManager
from build.build_system import BuildSystem
from monitoring.metrics import Monitoring
    import click
from rich.console import Console
from rich.table import Table
from core.external_repo import ExternalRepoManager

app = FastAPI()
jwt = JWTManager("secret-key")
monitoring = Monitoring()
build_system = BuildSystem()

@app.on_event("startup")
async def startup():
    monitoring.start_metrics_server()

@app.get("/packages")
async def list_packages():
    monitoring.requests_counter.inc()
    return {"packages": ["nginx", "postgresql"]}

@app.post("/build")
async def build_package():
    if build_system.build_in_container({"name": "test"}):
        return {"status": "success"}
    return {"status": "failed"}



console = Console()
repo_manager = ExternalRepoManager()

@click.group()
def cli():
    """Package manager with multi-repo support"""
    pass

@cli.command()
@click.argument('repository')
def add_repo(repository: str):
    """Add external repository"""
    if repo_manager.enable_repo(repository):
        console.print(f"[green]Repository {repository} added successfully![/green]")
    else:
        console.print(f"[red]Failed to add repository {repository}[/red]")

@cli.command()
@click.argument('query')
def search(query: str):
    """Search packages in all repositories"""
    results = repo_manager.search_in_external(query)

    table = Table(title="Search Results")
    table.add_column("Name")
    table.add_column("Version")
    table.add_column("Description")
    table.add_column("Repository")
    table.add_column("Type")

    for pkg in results:
        table.add_row(
            pkg.name,
            pkg.version,
            pkg.description,
            pkg.repo,
            pkg.package_type
        )

    console.print(table)

@cli.command()
@click.argument('package')
@click.option('--repo', help='Specific repository to install from')
def install(package: str, repo: str = None):
    """Install package from repository"""
    if repo:
        # Установка из конкретного репозитория
        pass
    else:
        # Поиск по всем репозиториям
        results = repo_manager.search_in_external(package)
        if not results:
            console.print("[red]Package not found[/red]")
            return

        # Установка первого найденного варианта
        if repo_manager.install_from_external(results[0]):
            console.print(f"[green]Package {package} installed successfully![/green]")
        else:
            console.print(f"[red]Failed to install {package}[/red]")

if __name__ == '__main__':
    cli()
