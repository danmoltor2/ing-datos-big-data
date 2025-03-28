#!/bin/bash
echo "Running verification queries..."
cd /opt/hive/bin
./hive -e "
USE entrega1;
SELECT 'info_household' as table_name, COUNT(*) as record_count FROM info_household;
SELECT 'halfhourly' as table_name, COUNT(*) FROM halfhourly LIMIT 10;
SELECT * FROM info_household LIMIT 3;
SELECT * FROM halfhourly LIMIT 3;
"
