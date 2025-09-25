"""Initial migration

Revision ID: 001
Revises: 
Create Date: 2024-01-01 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create users table
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('telegram_id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('role', sa.Enum('ADMIN', 'USER', 'VIEWER', name='userrole'), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_telegram_id'), 'users', ['telegram_id'], unique=True)

    # Create projects table
    op.create_table('projects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('color', sa.String(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_projects_id'), 'projects', ['id'], unique=False)
    op.create_index(op.f('ix_projects_name'), 'projects', ['name'], unique=False)

    # Create user_projects table
    op.create_table('user_projects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('role', sa.Enum('OWNER', 'MEMBER', 'VIEWER', name='projectrole'), nullable=False),
    sa.Column('joined_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_projects_id'), 'user_projects', ['id'], unique=False)

    # Create tasks table
    op.create_table('tasks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('status', sa.Enum('TODO', 'IN_PROGRESS', 'IN_REVIEW', 'DONE', name='taskstatus'), nullable=False),
    sa.Column('priority', sa.Enum('LOW', 'MEDIUM', 'HIGH', 'URGENT', name='taskpriority'), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('created_by', sa.Integer(), nullable=False),
    sa.Column('assigned_to', sa.Integer(), nullable=True),
    sa.Column('deadline', sa.DateTime(timezone=True), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['assigned_to'], ['users.id'], ),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tasks_id'), 'tasks', ['id'], unique=False)
    op.create_index(op.f('ix_tasks_title'), 'tasks', ['title'], unique=False)

    # Create task_comments table
    op.create_table('task_comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('task_id', sa.Integer(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_task_comments_id'), 'task_comments', ['id'], unique=False)

    # Create task_attachments table
    op.create_table('task_attachments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('filename', sa.String(), nullable=False),
    sa.Column('file_path', sa.String(), nullable=False),
    sa.Column('file_size', sa.Integer(), nullable=False),
    sa.Column('mime_type', sa.String(), nullable=False),
    sa.Column('task_id', sa.Integer(), nullable=False),
    sa.Column('uploaded_by', sa.Integer(), nullable=False),
    sa.Column('uploaded_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], ),
    sa.ForeignKeyConstraint(['uploaded_by'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_task_attachments_id'), 'task_attachments', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_task_attachments_id'), table_name='task_attachments')
    op.drop_table('task_attachments')
    op.drop_index(op.f('ix_task_comments_id'), table_name='task_comments')
    op.drop_table('task_comments')
    op.drop_index(op.f('ix_tasks_title'), table_name='tasks')
    op.drop_index(op.f('ix_tasks_id'), table_name='tasks')
    op.drop_table('tasks')
    op.drop_index(op.f('ix_user_projects_id'), table_name='user_projects')
    op.drop_table('user_projects')
    op.drop_index(op.f('ix_projects_name'), table_name='projects')
    op.drop_index(op.f('ix_projects_id'), table_name='projects')
    op.drop_table('projects')
    op.drop_index(op.f('ix_users_telegram_id'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    
    # Drop enums
    op.execute('DROP TYPE IF EXISTS taskpriority')
    op.execute('DROP TYPE IF EXISTS taskstatus')
    op.execute('DROP TYPE IF EXISTS projectrole')
    op.execute('DROP TYPE IF EXISTS userrole')
