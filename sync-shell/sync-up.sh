echo "Usage: ./up-sync.sh A/ root@x.x.x.x:/root/A"
set_terminal_title() { echo -ne "\033]0;$*\007"; }
local=$1 remote=$2
set_terminal_title "$local=>$remote"
while true; do
  echo "$(date "+%Y-%m-%d %H:%M:%S") $local -> $remote"
  rsync -aztH --progress --rsh=ssh "$local" "$remote"
  sleep 1
done