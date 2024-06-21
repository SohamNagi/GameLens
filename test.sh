#!/bin/bash

# Iterate over each SQL file matching the pattern
for sql_file in sample_sql/feature_*_test.sql; 
do 
    # Extract the base name of the SQL file without extension
    base_name=$(basename "$sql_file" _test.sql)
    
    # Construct the output file name
    output_file="sample_sql/${base_name}_test.out"
    
    # Execute the SQL file against the SQLite database and redirect the output
    sqlite3 SampleData.sqlite < "$sql_file" > "$output_file"
done
