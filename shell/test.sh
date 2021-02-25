#!/bin/bash
set -u

# Check if script is run non-interactively (e.g. CI)
# If it is run non-interactively we should not prompt for passwords.
if [[ ! -t 0 || -n "${CI-}" ]]; then
  NONINTERACTIVE=1
fi

abort() {
  printf "%s\n" "$1"
  exit 1
}

# First check OS.
OS="$(uname)"
if [[ "$OS" == "Linux" ]]; then
  HOMEBREW_ON_LINUX=1
elif [[ "$OS" != "Darwin" ]]; then
  abort "Homebrew is only supported on macOS and Linux."
fi

ohai "start install abd"
execute "adb -h"
ohai "start install scrcpy"
execute "scrcpy --help"