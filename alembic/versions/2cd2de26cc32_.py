"""empty message

Revision ID: 2cd2de26cc32
Revises: af35fdd943bd
Create Date: 2022-04-29 18:36:13.917761

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "2cd2de26cc32"
down_revision = "af35fdd943bd"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "email_addresses",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("address", sa.String(), nullable=False),
        sa.Column("contact_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["contact_id"],
            ["contacts.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("address"),
    )
    op.create_index(
        op.f("ix_email_addresses_id"), "email_addresses", ["id"], unique=False
    )
    op.drop_column("contacts", "instagram")
    op.drop_column("contacts", "location")
    op.drop_column("contacts", "email")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "contacts", sa.Column("email", sa.VARCHAR(), autoincrement=False, nullable=True)
    )
    op.add_column(
        "contacts",
        sa.Column("location", sa.VARCHAR(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "contacts",
        sa.Column("instagram", sa.VARCHAR(), autoincrement=False, nullable=True),
    )
    op.drop_index(op.f("ix_email_addresses_id"), table_name="email_addresses")
    op.drop_table("email_addresses")
    # ### end Alembic commands ###
