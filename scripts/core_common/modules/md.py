#!/usr/bin/env python

import sys
sys.path.append('../..')
import config
import base
import os
import subprocess

def make():
  print("[fetch]: md")

  base_dir = base.get_script_dir() + "/../../core/Common/3dParty/md"

  # Set PYTHONPATH to include build_tools scripts directory
  old_env = dict(os.environ)
  scripts_dir = base.get_script_dir() + "/../.."
  pythonpath = os.path.abspath(scripts_dir)
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