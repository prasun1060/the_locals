"""empty message

Revision ID: 4b7fec733325
Revises: 
Create Date: 2021-01-17 22:14:12.566101

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4b7fec733325'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('business_owners',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('business_name', sa.Text(), nullable=False),
    sa.Column('business_logo', sa.Text(), nullable=True),
    sa.Column('address1', sa.Text(), nullable=False),
    sa.Column('address2', sa.Text(), nullable=True),
    sa.Column('city', sa.Text(), nullable=False),
    sa.Column('zip', sa.Integer(), nullable=False),
    sa.Column('state', sa.Text(), nullable=False),
    sa.Column('country', sa.Text(), nullable=False),
    sa.Column('phone_number', sa.Integer(), nullable=False),
    sa.Column('business_category', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('phone_number')
    )
    op.create_table('customers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.Text(), nullable=False),
    sa.Column('last_name', sa.Text(), nullable=False),
    sa.Column('profile_pic', sa.Text(), nullable=True),
    sa.Column('address1', sa.Text(), nullable=False),
    sa.Column('address2', sa.Text(), nullable=True),
    sa.Column('city', sa.Text(), nullable=False),
    sa.Column('zip', sa.Integer(), nullable=False),
    sa.Column('state', sa.Text(), nullable=False),
    sa.Column('country', sa.Text(), nullable=False),
    sa.Column('phone_number', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('sex', sa.Text(), nullable=False),
    sa.Column('date_of_birth', sa.Date(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('phone_number')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_role', sa.Text(), nullable=False),
    sa.Column('phone_number', sa.Integer(), nullable=False),
    sa.Column('password', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_index(op.f('ix_users_phone_number'), 'users', ['phone_number'], unique=True)
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_name', sa.Text(), nullable=False),
    sa.Column('product_image', sa.Text(), nullable=False),
    sa.Column('product_description', sa.Text(), nullable=False),
    sa.Column('product_type', sa.Text(), nullable=False),
    sa.Column('product_quantity', sa.Float(), nullable=False),
    sa.Column('product_quantity_units', sa.Text(), nullable=False),
    sa.Column('mrp', sa.Float(precision=10), nullable=False),
    sa.Column('discount', sa.Float(precision=3), nullable=False),
    sa.Column('price', sa.Float(precision=10), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=True),
    sa.Column('business_owner_id', sa.Integer(), nullable=False),
    sa.Column('availibility_in_no', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['business_owner_id'], ['business_owners.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('order_quantity', sa.Integer(), nullable=False),
    sa.Column('bucket_type', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('orders')
    op.drop_table('products')
    op.drop_index(op.f('ix_users_phone_number'), table_name='users')
    op.drop_table('users')
    op.drop_table('customers')
    op.drop_table('business_owners')
    # ### end Alembic commands ###
