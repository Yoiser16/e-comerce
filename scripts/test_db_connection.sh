#!/bin/bash
export PGPASSWORD="ecommerce_dev_2026!"
psql -h 72.61.73.245 -U ecommerce_user -d ecommerce_db -c "SELECT current_database(), current_user;"
