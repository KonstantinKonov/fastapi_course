"""add_users_with_unique_email

Revision ID: 01dd6ff133bd
Revises: b9e582bfdfdf
Create Date: 2024-11-27 22:44:07.783489

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "01dd6ff133bd"
down_revision: Union[str, None] = "b9e582bfdfdf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("users_id_key", "users", type_="unique")
    op.create_unique_constraint(None, "users", ["email"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "users", type_="unique")
    op.create_unique_constraint("users_id_key", "users", ["id"])
    # ### end Alembic commands ###