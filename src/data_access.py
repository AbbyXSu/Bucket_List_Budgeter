from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine.base import Connection
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, engine


app = Flask(__name__)
app.config['SECRET_KEY'] = '88dd6a6854b7f1901b7f01d353186c6a'
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc://BLBAPP:abby@DESKTOP-4K1BGVB/BLB_DB?driver=SQL+Server"
db = SQLAlchemy(app)

Base = automap_base()
Base.prepare(db.engine, reflect=True)

Users = Base.classes.Users
TodoItem = Base.classes.TodoItem
Ledger = Base.classes.Ledger
TodoList = Base.classes.TodoList
BudgetSummary = Base.classes.BudgetSummary


if __name__ == '__main__':
    app.run(port=5000, debug=True, host='0.0.0.0')
