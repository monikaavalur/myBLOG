import MySQLdb as mdb
import click
import os
from django.core.wsgi import get_wsgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "untitled2.settings")

application = get_wsgi_application()

from untitled2 import settings
from blog.models import *

@click.group()
def blog():
    """Create, drop, clear and populate database"""
    pass


@blog.command()
@click.argument('username')
@click.argument('password')
@click.argument('dbname')
def createdb(username, password, dbname):
    con = mdb.connect(port=3309,host='127.0.0.1', user=username,passwd= password)
    with con:
        cur = con.cursor()
        cur.execute("drop database if EXISTS {0}".format(dbname))
        cur.execute("create database {0}".format(dbname))
        pass
    pass

@blog.command()
@click.argument('username')
@click.argument('password')
@click.argument('dbname')
def dropdb(username, password, dbname):
    con = mdb.connect(port=3309,host='127.0.0.1',user= username,passwd= password)
    with con:
        cur = con.cursor()
        cur.execute("drop database if EXISTS {0}".format(dbname))
        pass
    pass
@blog.command()
@click.argument('username')
@click.argument('password')
@click.argument('dbname')
def cleardata(username, password, dbname):
    """Clears the data in tables"""
    con = mdb.connect(port=3309,host='127.0.0.1',user= username,passwd= password,db= dbname)
    with con:
        cur = con.cursor()
        cur.execute("delete from blog_chat")
        cur.execute("delete from blog_User")

if __name__ == '__main__':
    blog()
