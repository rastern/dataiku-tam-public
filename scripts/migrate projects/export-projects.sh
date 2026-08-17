#!/bin/bash

# Get the list of projects
projects=$(/data/dataiku/data_dir/bin/dsscli projects-list | awk '{if (NR!=1) {print $1}}')

# Export each project
for project in $projects
do
  echo "Exporting project $project ..."
  /data/dataiku/data_dir/bin/dsscli project-export "$project" /data/dataiku/data_dir/exported_projects/"$project".zip
done

echo "Done exporting all projects."