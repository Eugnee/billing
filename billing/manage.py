import click

manager = click.Group()


@manager.command()
def run_server():
    from billing.commands.run_server import run_server

    run_server()


if __name__ == "__main__":
    manager()
