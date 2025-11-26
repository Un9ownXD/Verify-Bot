import aiosqlite

async def setup_db():
    async with aiosqlite.connect("data.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS entries (
                user_id INTEGER,
                first TEXT,
                second TEXT,
                third TEXT
            )
        """)
        await db.commit()

# Save user data
async def save_entries(user_id, first, second, third):
    async with aiosqlite.connect("data.db") as db:
        await db.execute("""
            INSERT INTO entries (user_id, first, second, third)
            VALUES (?, ?, ?, ?)
        """, (user_id, first, second, third))
        await db.commit()

