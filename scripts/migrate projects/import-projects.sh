#!/bin/bash

# Set the path to the folder containing the .zip files
folder="/data/dataiku/data_dir/exported_projects"

# Loop over each .zip file in the folder
for file in "$folder"/*.zip
do
  # Extract the project ID from the filename
  project_id=$(basename "$file" .zip)
  /data/dataiku/data_dir/bin/dsscli project-import --project-key="$project_id" /data/dataiku/data_dir/exported_projects/"$project_id".zip
  echo "Done importing: $project_id"
done