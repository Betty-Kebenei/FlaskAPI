"""empty message

Revision ID: f8d81472b136
Revises: 2da4d244ffaf
Create Date: 2017-10-18 17:40:10.760000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f8d81472b136'
down_revision = '2da4d244ffaf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(u'users_shopping_list_id_fkey', 'users', type_='foreignkey')
    op.drop_column('users', 'shopping_list_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('shopping_list_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key(u'users_shopping_list_id_fkey', 'users', 'shoppinglists', ['shopping_list_id'], ['list_id'])
    # ### end Alembic commands ###