from typing import Any
from sqlalchemy import Column
from app.db.core import Base


class NotFoundTableRow(Exception):
    def __init__(self, table: Base, column: Column, value: Any):
        self.table: Base = table
        self.column: Column = column
        self.value: Any = value

    def __str__(self):
        return f'There is not any rows with {self.column} = {self.value} in "{self.table.__tablename__}" table.'
