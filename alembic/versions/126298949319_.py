"""empty message

Revision ID: 126298949319
Revises: d44751cbc976
Create Date: 2021-11-07 11:13:55.449389

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "126298949319"
down_revision = "d44751cbc976"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("contacts", sa.Column("command", sa.String(), nullable=True))
    op.add_column("contacts", sa.Column("email_type", sa.String(), nullable=True))
    op.drop_column("contacts", "roster")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "contacts",
        sa.Column("roster", sa.VARCHAR(), autoincrement=False, nullable=True),
    )
    op.drop_column("contacts", "email_type")
    op.drop_column("contacts", "command")
    # ### end Alembic commands ###
