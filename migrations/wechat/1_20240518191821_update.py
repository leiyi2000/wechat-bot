from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "weather" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "to" VARCHAR(64) NOT NULL,
    "is_room" INT NOT NULL,
    "adcode" VARCHAR(32) NOT NULL,
    "at_hour" INT NOT NULL  DEFAULT 0,
    "address" VARCHAR(128) NOT NULL,
    "type" VARCHAR(32) NOT NULL,
    "error" INT NOT NULL  DEFAULT 0,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "uid_weather_to_98a753" UNIQUE ("to", "is_room", "adcode")
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "weather";"""
