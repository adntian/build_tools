#!/usr/bin/env python

import sys
sys.path.append('../..')
import config
import base
import os
import subprocess

def clear_module():
  directories = ["glm", "libetonyek", "libodfgen", "librevenge", "mdds"]

  for dir in directories:
    if base.is_dir(dir):
      base.delete_dir_with_access_error(dir)

def make(use_gperf = True):
  old_cur_dir = os.getcwd()

  print("[fetch & build]: iwork")

  base_dir = base.get_script_dir() + "/../../core/Common/3dParty/apple"

  # Calculate PYTHONPATH before changing directory
  scripts_dir = base.get_script_dir() + "/../.."
  pythonpath = os.path.abspath(scripts_dir)

  os.chdir(base_dir)
  base.check_module_version("3", clear_module)
  os.chdir(old_cur_dir)

  cmd_args = ["fetch.py"]

  if use_gperf:
    cmd_args.append("--gperf")

  # Set PYTHONPATH to include build_tools scripts directory
  old_env = dict(os.environ)
  if "PYTHONPATH" in os.environ:
    pythonpath = pythonpath + os.pathsep + os.environ["PYTHONPATH"]
  os.environ["PYTHONPATH"] = pythonpath

  base.cmd_in_dir(base_dir, "python", cmd_args)

  # Restore environment
  os.environ.clear()
  os.environ.update(old_env)
  return

if __name__ == '__main__':
  # manual compile
  make(False)