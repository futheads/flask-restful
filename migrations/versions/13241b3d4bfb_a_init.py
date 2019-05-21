"""【A】init

Revision ID: 13241b3d4bfb
Revises: 
Create Date: 2019-05-21 17:52:43.088951

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '13241b3d4bfb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('phone_number', sa.String(length=11), nullable=True),
    sa.Column('password', sa.String(length=30), nullable=True),
    sa.Column('nickname', sa.String(length=30), nullable=True),
    sa.Column('register_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_nickname'), ['nickname'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_phone_number'), ['phone_number'], unique=False)

    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=80), nullable=True),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('pub_date', sa.DateTime(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_phone_number'))
        batch_op.drop_index(batch_op.f('ix_user_nickname'))

    op.drop_table('user')
    op.drop_table('category')
    # ### end Alembic commands ###