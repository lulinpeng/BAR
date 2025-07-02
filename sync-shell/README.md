# RUN
## sync-up
This script is used to ***overwrite-synchronize*** a local directory to a remote-end machine. *Note that if a file exists on the remote end but not locally, it will not be overwritten.*

```shell
./sync-up.sh /path/to/local/ [remote host]:/path/to/remote
./sync-up.sh A/ root@x.x.x.x:/root/A"
```
