#!/usr/bin/bash

md2pdf README.md summary.pdf

for task in task*; do
   cd $task
   md2pdf README.md $task.pdf
   cd ..
done
