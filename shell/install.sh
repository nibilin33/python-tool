#!/bin/bash
echo "welcome ~"
# string formatters
if [[ -t 1 ]]; then
  tty_escape() { printf "\033[%sm" "$1"; }
else
  tty_escape() { :; }
fi
tty_mkbold() { tty_escape "1;$1"; }
tty_underline="$(tty_escape "4;39")"
tty_blue="$(tty_mkbold 34)"
tty_red="$(tty_mkbold 31)"
tty_bold="$(tty_mkbold 39)"
tty_reset="$(tty_escape 0)"
shell_join() {
  local arg
  printf "%s" "$1"
  shift
  for arg in "$@"; do
    printf " "
    printf "%s" "${arg// /\ }"
  done
}
ohai() {
  printf "${tty_blue}==>${tty_bold} %s${tty_reset}\n" "$(shell_join "$@")"
}

warn() {
  printf "${tty_red}Warning${tty_reset}: %s\n" "$(chomp "$1")"
}

execute() {
  if ! "$@"; then
    abort "$(printf "Failed during: %s" "$(shell_join "$@")")"
  fi
}
catch()
{
    export ex_code=$?
    (( $SAVED_OPT_E )) && set +e
    return $ex_code
}
set -e
trap 'catch $? $LINENO' EXIT
brew -v || (
  ohai "start install homebrew"
  bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
)
adb version || (
ohai "start install abd"
execute "brew" "install" "adb"
)
scrcpy -v || (
  ohai "start install scrcpy"
  execute "brew" "install" "scrcpy"
)
ohai "download lique"
execute "cd" "${HOME}"
rm -rf Liquebin
execute "curl" "-L" "-o" "Liquebin.zip" "--output" "~/" "https://gw.alipayobjects.com/os/bmw-prod/91039fc3-8c1c-4796-90fd-bc4880fb124c.zip"
unzip "Liquebin.zip"
ln -fs ${HOME}/Liquebin/lique /usr/local/bin/lique
ohai "start download neblula"
execute "curl"  "https://gw.alipayobjects.com/os/bmw-prod/a897bece-e6c3-4892-a5a1-a10ccf5d6869.apk" "--output" "${HOME}/Liquebin/NebulaApplication-debug.apk"
ohai "start download bugless"
execute "curl" "https://gw-office.alipayobjects.com/bmw-prod/e0c27d89-a3aa-4212-853e-aba8b0b1306a.apk" "--output" "${HOME}/Liquebin/bugless.apk"
ohai "start download smile"
execute "curl" "http://scmcenterclient.cn-hangzhou.alipay.aliyun-inc.com/vending/sdk/common/2020/07/16/11/5f0fc6e16aa4000001760bdb/signed_app-vending-debug.apk" "--output" "${HOME}/Liquebin/signed_app-vending-debug.apk"
ohai "start download drangfly"
execute "curl" "https://gw-office.alipayobjects.com/bmw-prod/cc78d0c9-d3bd-42f8-937d-eb865dc77e00.apk" "--output" "${HOME}/Liquebin/dragonfly.apk"
ohai "start download unisetting-debug"
execute "curl" "https://gw-office.alipayobjects.com/bmw-prod/5298bc70-5663-4412-bbe4-d6328560a20a.apk" "--output" "${HOME}/Liquebin/unisetting-debug.apk"
echo "- Run \`lique\` to get started"
