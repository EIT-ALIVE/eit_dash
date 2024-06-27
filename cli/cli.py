import click

from eit_dash.app import app


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """Default prompt. It shows the help command."""
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@cli.command(name="run", help="Start the dashboard.")
def run():
    """Start the dashboard."""
    app.run_server(debug=False)


if __name__ == "__main__":
    cli()
