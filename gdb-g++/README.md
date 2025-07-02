# Test Environment
```shell
# ubuntu:22.04
apt update
apt install g++ gdb -y
```

# Quick Start
GDB is a command-line debugger ***primarily for C/C++*** that enables setting breakpoints, stepping through code, and examining variables in **running programs or core dumps**, *with limited support for other compiled languages like **Go and Rust***.

##  ​Launch-Mode Debugging 
Starting the program directly from **within GDB** to control execution **from the very beginning**.
```shell
g++ demo_launch.cpp
# g++ -g demo_launch.cpp
gdb ./a.out
(gdb) run
(gdb) bt
(gdb) quit
```

## Attach-Mode Debugging
**Connecting** GDB to an **already running process** to inspect its current execution state.
```shell
g++ demo_attach.cpp
nohup ./a.out > /dev/null & # start the process

ps aux # find the target process id
gdb -p [process id] 
# now the target process is paused
(gdb) bt
(gdb) info threads # show all threads
(gdb) thread 1 # enter thread 1
(gdb) continue # continue running
(gdb) detach
```
# Demo
Debugging **with '-g'** provides source-level information like ***variable names and line numbers***, while **without '-g'** you only see ***raw memory addresses and assembly code***.​
## Launch-Mode (without '-g')
```shell
g++ demo_launch.cpp
gdb ./a.out
```
```console
(gdb) run
Starting program: /xxx/gdb-demo/a.out
Program received signal SIGSEGV, Segmentation fault.
0x0000aaaacbd009e4 in g(int*) ()

(gdb) bt
#0  0x0000aaaacbd009e4 in g(int*) ()
#1  0x0000aaaacbd00a2c in f(int*) ()
#2  0x0000aaaacbd00a4c in main ()
```
## Launch-Mode (with '-g')
```console
g++ -g demo_launch.cpp
gdb ./a.out
```
```
(gdb) run
Starting program: /xxx/gdb-demo/a.out
Program received signal SIGSEGV, Segmentation fault.
0x0000aaaac8e309e4 in g (q=0x0) at demo.cpp:4
4	void g(int *q) { cout << *q << endl; }

(gdb) bt
#0  0x0000aaaac8e309e4 in g (q=0x0) at demo.cpp:4
#1  0x0000aaaac8e30a2c in f (p=0x0) at demo.cpp:6
#2  0x0000aaaac8e30a4c in main () at demo.cpp:10
```
## Attach-Mode
```shell
g++ -g demo_attach.cpp
nohup ./a.out > /dev/null &
ps aux # find the target process id
gdb -p 5718
```
```console
(gdb) bt
#0  0x0000ffff96e7bb20 in __GI___libc_write (fd=1, buf=buf@entry=0xaaaaeee95eb0, nbytes=nbytes@entry=10)
    at ../sysdeps/unix/sysv/linux/write.c:26
#1  0x0000ffff96e17d8c in _IO_new_file_write (f=0xffff96f425d8 <_IO_2_1_stdout_>, data=0xaaaaeee95eb0,
    n=10) at ./libio/fileops.c:1180
#2  0x0000ffff96e1713c in new_do_write (fp=0xffff96f425d8 <_IO_2_1_stdout_>,
    data=0xaaaaeee95eb0 "here is g\n", to_do=to_do@entry=10) at ./libio/libioP.h:947
#3  0x0000ffff96e18e40 in _IO_new_do_write (to_do=10, data=<optimized out>, fp=0xa)
    at ./libio/fileops.c:422
#4  _IO_new_do_write (fp=fp@entry=0xffff96f425d8 <_IO_2_1_stdout_>, data=<optimized out>, to_do=10)
    at ./libio/fileops.c:422
#5  0x0000ffff96e1926c in _IO_new_file_overflow (f=0xffff96f425d8 <_IO_2_1_stdout_>, ch=10)
    at ./libio/fileops.c:783
#6  0x0000ffff970821f8 in std::ostream::put(char) () from /lib/aarch64-linux-gnu/libstdc++.so.6
#7  0x0000ffff97082878 in std::basic_ostream<char, std::char_traits<char> >& std::endl<char, std::char_traits<char> >(std::basic_ostream<char, std::char_traits<char> >&) ()
   from /lib/aarch64-linux-gnu/libstdc++.so.6
#8  0x0000aaaace650a0c in g(int*) ()
#9  0x0000aaaace650a38 in f(int*) ()
#10 0x0000aaaace650a58 in main ()
```