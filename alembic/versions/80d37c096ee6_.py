"""empty message

Revision ID: 80d37c096ee6
Revises: bfb7700b26c7
Create Date: 2022-04-29 18:51:34.901457

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "80d37c096ee6"
down_revision = "bfb7700b26c7"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("ix_positions_id", table_name="positions")
    op.drop_table("positions")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "positions",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("name", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint("id", name="positions_pkey"),
        sa.UniqueConstraint("name", name="positions_name_key"),
    )
    op.create_index("ix_positions_id", "positions", ["id"], unique=False)
    # ### end Alembic commands ###
