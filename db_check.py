from sqlalchemy import create_engine, text

DB_URL = "postgresql+psycopg://petuser:petpass@localhost:5432/petdb"

engine = create_engine(DB_URL, pool_pre_ping=True)

with engine.connect() as conn:
    result = conn.execute(text("select 1")).scalar_one()
    print("DB OK:", result)
