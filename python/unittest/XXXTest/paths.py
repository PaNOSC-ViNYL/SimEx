""" Utility to expose all modules under src/ in the unittest directories."""

import os, sys
import os.path

file_path = os.path.dirname(__file__)
#separator = os.pathsep
separator = '/'
separated_file_path = file_path.split(separator)
top_level_index = separated_file_path.index('python')
separated_top_level_path = separated_file_path[:top_level_index+1]
separated_top_level_path.append('src')

top_level_path = separator.join(separated_top_level_path)

if not top_level_path in sys.path:
    sys.path.insert(1, top_level_path)
del top_level_path, file_path, separated_file_path, separated_top_level_path
