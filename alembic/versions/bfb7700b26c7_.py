"""empty message

Revision ID: bfb7700b26c7
Revises: 2cd2de26cc32
Create Date: 2022-04-29 18:49:24.038529

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "bfb7700b26c7"
down_revision = "2cd2de26cc32"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("contacts_position_id_fkey", "contacts", type_="foreignkey")
    op.drop_column("contacts", "position_id")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "contacts",
        sa.Column("position_id", sa.INTEGER(), autoincrement=False, nullable=True),
    )
    op.create_foreign_key(
        "contacts_position_id_fkey", "contacts", "positions", ["position_id"], ["id"]
    )
    # ### end Alembic commands ###
