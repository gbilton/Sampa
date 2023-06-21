"""empty message

Revision ID: 0263699f6966
Revises: 80d37c096ee6
Create Date: 2022-05-01 19:18:09.157553

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "0263699f6966"
down_revision = "80d37c096ee6"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("sent", sa.Column("Email Address ID", sa.Integer(), nullable=False))
    op.drop_constraint("sent_Contact ID_fkey", "sent", type_="foreignkey")
    op.create_foreign_key(None, "sent", "email_addresses", ["Email Address ID"], ["id"])
    op.drop_column("sent", "Contact ID")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "sent",
        sa.Column("Contact ID", sa.INTEGER(), autoincrement=False, nullable=False),
    )
    op.drop_constraint(None, "sent", type_="foreignkey")
    op.create_foreign_key(
        "sent_Contact ID_fkey", "sent", "contacts", ["Contact ID"], ["id"]
    )
    op.drop_column("sent", "Email Address ID")
    # ### end Alembic commands ###