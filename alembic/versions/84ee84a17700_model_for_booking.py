"""Model for Booking

Revision ID: 84ee84a17700
Revises: 0cebb3013276
Create Date: 2025-08-01 11:12:33.285291

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '84ee84a17700'
down_revision = '0cebb3013276'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bookings',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('train_id', sa.UUID(), nullable=False),
    sa.Column('seat_number', sa.Integer(), nullable=True),
    sa.Column('booking_time', sa.DateTime(), nullable=True),
    sa.Column('status', sa.Enum('CONFIRMED', 'WAITING', 'TATKAL', 'CANCELLED', name='bookingstatus', native_enum=False), nullable=False),
    sa.ForeignKeyConstraint(['train_id'], ['trains.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bookings')
    # ### end Alembic commands ###