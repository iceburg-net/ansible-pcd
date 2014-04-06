#!/bin/bash

for db_table in `mysql -Bse "SELECT CONCAT(TABLE_SCHEMA, ':', TABLE_NAME) AS \
db_table FROM information_schema.TABLES WHERE TABLE_SCHEMA NOT IN ('information_schema','mysql') \
AND Data_free > 0 AND NOT ENGINE='MEMORY' ORDER BY Data_free DESC;"`; do
  DB=`echo $db_table | cut -d: -f1`; TB=`echo $db_table | cut -d: -f2`; mysqlcheck -o "$DB" "$TB"
done 