#!/bin/bash
schematool -dbType mysql -initSchema
hive --service metastore
