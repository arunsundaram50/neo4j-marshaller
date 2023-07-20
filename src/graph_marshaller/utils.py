#!/usr/bin/env python3


import os, sys
PWD = os.getcwd()


def log(*args, **kwargs):
  frame = sys._getframe(1)
  if frame.f_code.co_filename.startswith(PWD):
    rel_cwd = frame.f_code.co_filename[len(PWD):]
  else:
    rel_cwd = frame.f_code.co_filename
  print(f'File "{rel_cwd}", line {frame.f_lineno}', end=': ')
  print(*args, **kwargs)
  sys.stdout.flush()


if __name__ == "__main__":
  pass
