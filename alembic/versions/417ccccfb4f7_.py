"""empty message

Revision ID: 417ccccfb4f7
Revises: 126298949319
Create Date: 2021-11-07 14:06:48.789463

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '417ccccfb4f7'
down_revision = '126298949319'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contacts', sa.Column('command_id', sa.Integer(), nullable=True))
    op.add_column('contacts', sa.Column('email_type_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'contacts', 'commands', ['command_id'], ['id'])
    op.create_foreign_key(None, 'contacts', 'email_types', ['email_type_id'], ['id'])
    op.drop_column('contacts', 'command')
    op.drop_column('contacts', 'email_type')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contacts', sa.Column('email_type', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('contacts', sa.Column('command', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'contacts', type_='foreignkey')
    op.drop_constraint(None, 'contacts', type_='foreignkey')
    op.drop_column('contacts', 'email_type_id')
    op.drop_column('contacts', 'command_id')
    # ### end Alembic commands ###