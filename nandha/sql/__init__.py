from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base

# Define the database URL
DB_URL = "postgresql+asyncpg://postgres.lfxzalulgmqdalctysxe:PkAkZwH2yHnweNsT@aws-0-ap-south-1.pooler.supabase.com:6543/postgres"

# Create the async engine
engine = create_async_engine(DB_URL, echo=True)

# Define the base class for declarative models
Base = declarative_base()
