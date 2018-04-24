#!/bin/bash
set -ex

rm db/critique.db;
sqlite3 db/critique.db ".databases"
sqlite3 db/critique.db ".read db/critique_schema_dump.sql"
sqlite3 db/critique.db ".read db/critique_data_dump.sql"
