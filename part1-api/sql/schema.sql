CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS clans (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL,
  region TEXT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT (now() AT TIME ZONE 'utc')
);


CREATE INDEX IF NOT EXISTS idx_clans_region ON clans(region);
CREATE INDEX IF NOT EXISTS idx_clans_created_at ON clans(created_at DESC);