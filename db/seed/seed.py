import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from uuid import uuid4
from datetime import datetime, timezone

# Database connection string
DATABASE_URL = os.getenv("DATABASE_URL")

print(f"DATABASE_URL: {DATABASE_URL}")

# Create the database engine and session
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Dynamic ID generation for workspace and user
workspace_id = str(uuid4())
user_id = str(uuid4())

def validate_environment():
    """Ensure the DATABASE_URL is set and the database is reachable."""
    if not DATABASE_URL:
        print("Error: DATABASE_URL is not set.")
        sys.exit(1)
    try:
        # Test the database connection
        engine.connect()
        print("Database connection successful.")
    except Exception as e:
        print(f"Error: Unable to connect to the database. {e}")
        sys.exit(1)

def seed_workspaces(workspace_id):
    """Seed the workspaces table."""
    try:
        # Commit any pending transactions to ensure the database state is up-to-date
        session.commit()

        # Check if a workspace with the same slug already exists
        existing_workspace = session.execute(text("""
            SELECT id FROM workspaces WHERE slug = :slug
        """), {"slug": "workspace-1"}).fetchone()

        print(f"Existing workspace check result: {existing_workspace}")

        if existing_workspace:
            existing_workspace_id = existing_workspace[0]
            print(f"Workspace with slug 'workspace-1' already exists. Reusing ID: {existing_workspace_id}")
            return existing_workspace_id

        # Insert the new workspace
        query = """
            INSERT INTO workspaces (id, name, slug, data_retention_days, created_at)
            VALUES (:id, :name, :slug, :data_retention_days, :created_at)
        """
        params = {
            "id": workspace_id,
            "name": "Workspace 1",
            "slug": "workspace-1",
            "data_retention_days": 365,
            "created_at": datetime.now(timezone.utc)
        }
        print(f"Executing query: {query}")
        print(f"With parameters: {params}")
        session.execute(text(query), params)
        session.commit()  # Ensure the transaction is committed
        print(f"Seeded workspaces with ID: {workspace_id}")
        return workspace_id
    except Exception as e:
        print(f"Failed to seed workspaces: {e}")
        raise

def verify_workspace_exists(workspace_id):
    """Verify that the workspace_id exists in the workspaces table."""
    result = session.execute(text("""
        SELECT id FROM workspaces WHERE id = :id
    """), {"id": workspace_id}).fetchone()
    return result is not None

def seed_users(user_id, dry_run=False):
    """Seed the users table with idempotency."""
    try:
        existing_user = session.execute(text("""
            SELECT id FROM users WHERE id = :id
        """), {"id": user_id}).fetchone()

        if existing_user:
            print(f"User with ID {user_id} already exists. Skipping insertion.")
            return

        if dry_run:
            print(f"[Dry-Run] Would insert user with ID: {user_id}")
            return

        session.execute(text("""
            INSERT INTO users (id, email, full_name, mfa_status, created_at)
            VALUES (:id, :email, :full_name, :mfa_status, :created_at)
        """), {
            "id": user_id,
            "email": "user1@example.com",
            "full_name": "User One",
            "mfa_status": "disabled",
            "created_at": datetime.now(timezone.utc)
        })
        session.commit()
        print("Seeded users.")
    except Exception as e:
        print(f"Failed to seed users: {e}")
        raise

def seed_workspace_memberships(workspace_id, user_id):
    """Seed the workspace_memberships table."""
    session.execute(text("""
        INSERT INTO workspace_memberships (workspace_id, user_id, role, status, created_at)
        VALUES (:workspace_id, :user_id, :role, :status, :created_at)
        ON CONFLICT DO NOTHING
    """), {
        "workspace_id": workspace_id,
        "user_id": user_id,
        "role": "admin",
        "status": "active",
        "created_at": datetime.now(timezone.utc)
    })
    print("Seeded workspace memberships.")

def seed_accounts(workspace_id):
    """Seed the accounts table."""
    session.execute(text("""
        INSERT INTO accounts (id, workspace_id, institution_name, account_mask, import_format, status, created_at)
        VALUES (:id, :workspace_id, :institution_name, :account_mask, :import_format, :status, :created_at)
        ON CONFLICT (id) DO NOTHING
    """), {
        "id": str(uuid4()),
        "workspace_id": workspace_id,
        "institution_name": "Bank of Example",
        "account_mask": "1234",
        "import_format": "csv",
        "status": "active",
        "created_at": datetime.now(timezone.utc)
    })
    print("Seeded accounts.")

def seed_transactions(workspace_id):
    """Seed the transactions table."""
    session.execute(text("""
        INSERT INTO transactions (transaction_id, workspace_id, amount, currency, description_raw, occurred_at, created_at)
        VALUES (:transaction_id, :workspace_id, :amount, :currency, :description_raw, :occurred_at, :created_at)
        ON CONFLICT (transaction_id) DO NOTHING
    """), {
        "transaction_id": str(uuid4()),
        "workspace_id": workspace_id,
        "amount": 100.50,
        "currency": "USD",
        "description_raw": "Example transaction",
        "occurred_at": datetime.now(timezone.utc),
        "created_at": datetime.now(timezone.utc)
    })
    print("Seeded transactions.")

def main(dry_run=False):
    validate_environment()
    try:
        workspace_id = seed_workspaces(workspace_id)
        seed_users(user_id, dry_run=dry_run)
        if not dry_run:
            seed_workspace_memberships(workspace_id, user_id)
            seed_accounts(workspace_id)
            seed_transactions(workspace_id)
        session.commit()
        print("Seeding completed successfully.")
    except Exception as e:
        session.rollback()
        print(f"Error during seeding: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    main(dry_run=dry_run)