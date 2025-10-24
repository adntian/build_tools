#!/usr/bin/env python

import sys
sys.path.append('../..')
import config
import base
import os
import subprocess

def clear_module():
  directories = ["gumbo-parser", "katana-parser"]

  for dir in directories:
    if base.is_dir(dir):
      base.delete_dir_with_access_error(dir)

def make():
  old_cur_dir = os.getcwd()

  print("[fetch]: html")

  base_dir = base.get_script_dir() + "/../../core/Common/3dParty/html"

  # Calculate PYTHONPATH before changing directory
  scripts_dir = base.get_script_dir() + "/../.."
  pythonpath = os.path.abspath(scripts_dir)

  os.chdir(base_dir)
  base.check_module_version("2", clear_module)
  os.chdir(old_cur_dir)

  # Set PYTHONPATH to include build_tools scripts directory
  # so that fetch.py can import config module
  old_env = dict(os.environ)
  if "PYTHONPATH" in os.environ:
    pythonpath = pythonpath + os.pathsep + os.environ["PYTHONPATH"]
  os.environ["PYTHONPATH"] = pythonpath

  base.cmd_in_dir(base_dir, "python", ["fetch.py"])

  # Restore environment
  os.environ.clear()
  os.environ.update(old_env)
  return

if __name__ == '__main__':
  # manual compile
  make()
