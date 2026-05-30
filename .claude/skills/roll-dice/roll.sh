#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: roll.sh <dice> [-a|-d] [+/-modifier]
  dice:  d4 d6 d8 d10 d12 d20 d100   (single die)
         NdX                           (multiple dice, e.g. 2d6 3d8)
  -a     advantage  — roll twice, keep higher (single die only)
  -d     disadvantage — roll twice, keep lower (single die only)
  +N/-N  flat modifier added to total
EOF
  exit 1
}

roll_die() {
  local sides=$1
  echo $(( (RANDOM % sides) + 1 ))
}

[[ $# -lt 1 ]] && usage

dice="$1"; shift
mode=""
modifier=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    -a) mode="adv" ;;
    -d) mode="dis" ;;
    -h|--help) usage ;;
    +*|-[0-9]*) modifier=$1 ;;
    *) usage ;;
  esac
  shift
done

if [[ "$dice" =~ ^([0-9]*)d([0-9]+)$ ]]; then
  count="${BASH_REMATCH[1]}"
  [[ -z "$count" ]] && count=1
  sides="${BASH_REMATCH[2]}"
else
  usage
fi

if [[ "$mode" != "" && "$count" -ne 1 ]]; then
  echo "Error: advantage/disadvantage requires single die (d20, not 2d20)" >&2
  exit 1
fi

if [[ "$mode" == "adv" ]]; then
  r1=$(roll_die "$sides")
  r2=$(roll_die "$sides")
  total=$(( r1 > r2 ? r1 : r2 ))
elif [[ "$mode" == "dis" ]]; then
  r1=$(roll_die "$sides")
  r2=$(roll_die "$sides")
  total=$(( r1 < r2 ? r1 : r2 ))
else
  total=0
  for (( i = 0; i < count; i++ )); do
    total=$(( total + $(roll_die "$sides") ))
  done
fi

echo $(( total + modifier ))
