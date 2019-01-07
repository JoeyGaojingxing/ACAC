# _*_ coding: utf-8 _*_
"""
    :author: Mojerro (高景行)
    :url: http://mojerro.我爱你
    :copyright: © 2018
    :license: MIT, see LICENSE for more details
"""
import click

from acac import app, db


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database"""
    if drop:
        db.drop_all()
        click.echo('Database dropped')
    db.create_all()
    click.echo('Initialized database')
