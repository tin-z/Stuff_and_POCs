import sys
import os
import argparse
import re

import subprocess


### 
## Utils
#

repo_folder = "repo_folder"

class WrapExp(Exception):
  pass


def check_output(cmd):
  return subprocess.check_output([
    "/bin/sh", 
    "-c",
    cmd
  ]).decode('utf-8').strip()


def check_tool(tool):
  """
    Check if 'tool' is present

  """
  rets = check_output("which {}".format(tool)).strip()
  if rets == '' :
    raise WrapExp("Can't find '{}' command".format(tool))


def do_git_clone(url, remove_folder=False):
  """
    Do git clone on 'repo_folder'

  """
  if remove_folder :
    _ = check_output("rm -rf {}".format(repo_folder))
  if os.path.isdir(repo_folder) :
    return
  rets = check_output("git clone {} {}; echo $?".format(url, repo_folder))
  ret_code = int(rets.split("\n")[-1])
  if ret_code :
    raise WrapExp("Can't git clone on '{}'".format(url))


def do_save_git_diff(pre_version, post_version, fmts_file=''):
  """
    Return the diff outputs
     - diff on pre and post versions (tag or commit)
     - skip those not matching file formats

  """
  cmd = f"git --no-pager diff {pre_version} {post_version}; echo $?"
  rets = check_output(cmd).split("\n")
  ret_code = int(rets[-1])
  if ret_code :
    raise WrapExp(f"Can't git diff on '{pre_version}' and '{post_version}'")
  #
  starts_with = lambda x : x.startswith("diff --git ")
  ends_with = lambda x : True
  if fmts_file :
    fmts = "\.({})$".format(
      "|".join([x.strip() for x in fmts_file.lower().split(",")])
    )
    ends_with = lambda x : re.search(fmts,x) != None
  #
  prev_index = -1
  output = []
  for i,x in enumerate(rets):
    if starts_with(x) :
      if prev_index == -1 :
        prev_index = 0
      else :
        diff_now = rets[prev_index]
        if ends_with(diff_now.split(" ")[2].lower()) :
          output.append("\n".join(rets[prev_index:i]))
        prev_index = i

  diff_now = rets[prev_index]
  if ends_with(diff_now.split(" ")[2]) :
    output.append("\n".join(rets[prev_index:i]))

  return output



if __name__ == "__main__" :
  parser = argparse.ArgumentParser(
    description="%s: Downloader Tool" % sys.argv[0]
  )
  parser.add_argument(
    "-g",
    "--git",
    required=True,
    help="Git url repository to git clone"
  )
  parser.add_argument(
    "--cve",
    required=True,
    help="Insert CVE number. The files are saved based on that"
  )
  parser.add_argument(
    "--pre",
    required=True,
    help="Software version still unpatched"
  )
  parser.add_argument(
    "--post",
    required=True,
    help="Software version patched"
  )
  parser.add_argument(
    "--formats",
    default="",
    help="File formats that we're interested in with ',' as separator for multiple choices (e.g. py, c,cpp,h,hpp)"
  )
  parser.add_argument(
    "--remove",
    default=False,
    action="store_true",
    help=
      "Delete the temporary folder before git cloning on it '{}' (default:False)".format(
        repo_folder
      )
  )
  parser.add_argument(
    "--output",
    default="output",
    help="Folder where results are saved"
  )

  args = parser.parse_args()
  pre_version = args.pre
  post_version = args.post
  fmts_file = args.formats
  cve = args.cve

  if not os.path.isdir(args.output) :
    os.mkdir(args.output)

  try :
    check_tool("git")
    do_git_clone(args.git, args.remove)
    os.chdir(repo_folder)
    output = do_save_git_diff(pre_version, post_version, fmts_file)
    os.chdir("..")

    for i,x in enumerate(output) :
      with open(f"{args.output}/{cve}_{str(i).rjust(2,'0')}.txt","w") as fp:
        fp.write(x)
    print("[+] Done")

  except WrapExp as ex :
    print("[x] Exception: {}".format(ex))



