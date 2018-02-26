#!/bin/bash
set -ex

python -m tests.database_api_tests_user;
python -m tests.database_api_tests_ratings;
