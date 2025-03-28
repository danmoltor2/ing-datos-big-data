USE entrega1;

-- Verify tables exist
SHOW TABLES;

-- Verify info_household data
SELECT COUNT(*) AS info_household_count FROM info_household;
SELECT * FROM info_household LIMIT 3;

-- Verify halfhourly data
SELECT COUNT(*) AS halfhourly_sample_count FROM halfhourly LIMIT 1000;
SELECT * FROM halfhourly LIMIT 3;
