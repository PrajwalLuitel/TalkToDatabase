from pydantic import BaseModel, Field


class TableColumn(BaseModel):
    """Table column."""

    name: str
    dtype: str | None


class ForeignKey(BaseModel):
    """Foreign key."""

    # Referenced column
    column: TableColumn
    # References table name
    references_name: str
    # References column
    references_column: TableColumn


class Table(BaseModel):
    """Table."""

    name: str
    columns: list[TableColumn] | None
    pks: list[TableColumn] | None
    # FK from this table to another column in another table
    fks: list[ForeignKey] | None


class DatabaseConnection(BaseModel):

    username: str = Field(..., example="postgres")
    password: str = Field(..., example="")
    host_name: str = Field(..., example="localhost")
    database_name: str = Field(..., example="companydb")
    port: int = Field(..., example=5432)
    database_type: str = Field(..., example="PostgreSQL")
