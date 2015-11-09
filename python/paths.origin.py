""" Utility to expose all modules under src/ in the unittest directories."""

import os, sys
import os.path

file_path = os.path.abspath(os.path.dirname(__file__))
separator = os.sep
separated_file_path = file_path.split(separator)
top_level_index = separated_file_path.index('python')
top_level_path = os.path.abspath(separator.join(separated_file_path[:top_level_index+1]))

paths_to_insert = ['src/',
                   'unittest/',
                   'lib/'
                   ]

for p in paths_to_insert:
    path = os.path.join(top_level_path, p)
    if not path in sys.path:
        sys.path.insert(1, path)

print sys.path[:3]

del top_level_path, file_path, separated_file_path
