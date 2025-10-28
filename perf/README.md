# Test Machine
Intel(R) Xeon(R) Platinum 8163 CPU @ 2.50GHz
# Version
```shell
yum install perf -y # perf-3.10.0
# for flame graph
git clone https://github.com/brendangregg/FlameGraph.git
cd FlameGraph/
export PATH=$PATH:$(pwd)
```
# Quick Start
Perf is a tool that assesses the performance of a target program by **sampling** various CPU events and call stack information at a specified frequency. *The core principle is straightforward: **if a particular function or instruction is time-consuming, it will be sampled more frequently**.*

```shell
g++ -g demo.cpp -std=c++11 # -g for 'debug'
perf stat ./a.out > /dev/null
#  Performance counter stats for './a.out':

#            1008.54 msec task-clock:u              #    0.999 CPUs utilized
#                  0      context-switches:u        #    0.000 K/sec
#                  0      cpu-migrations:u          #    0.000 K/sec
#                818      page-faults:u             #    0.811 K/sec
#         2699856533      cycles:u                  #    2.677 GHz
#         4651208407      instructions:u            #    1.72  insn per cycle
#          909140971      branches:u                #  901.443 M/sec
#             123741      branch-misses:u           #    0.01% of all branches

#        1.009379135 seconds time elapsed

#        1.009070000 seconds user
#        0.000000000 seconds sys

perf record -g -F 999 ./a.out # -g for 'call-graph', -F for 'sample freq 999Hz'
# [ perf record: Woken up 2 times to write data ]
# [ perf record: Captured and wrote 0.418 MB perf.data (3583 samples) ]

perf report
# Samples: 3K of event 'cycles:uppp', Event count (approx.): 2311489875
#   Children      Self  Command  Shared Object        Symbol
# +   99.88%     0.00%  a.out    libc-2.17.so         [.] __libc_start_main
# +   99.88%     0.00%  a.out    a.out                [.] main
# +   77.90%    77.90%  a.out    a.out                [.] f3
# +   77.90%     0.00%  a.out    a.out                [.] f
# +   77.90%     0.00%  a.out    a.out                [.] f0
# +   77.90%     0.00%  a.out    a.out                [.] f1
# +   77.90%     0.00%  a.out    a.out                [.] f2
# +   13.00%    13.00%  a.out    a.out                [.] mat_mul
# +    8.98%     8.98%  a.out    a.out                [.] fibonacci

cd FlameGraph/ && export PATH=$PATH:$(pwd) # for 'stackcollapse-perf.pl' and 'flamegraph.pl'
perf script | stackcollapse-perf.pl | flamegraph.pl > flamegraph.svg
ls -al flamegraph.svg
```

# FYI
```shell
perf list # list all available events
# List of pre-defined events (to be used in -e):

#   branch-instructions OR branches                    [Hardware event]
#   branch-misses                                      [Hardware event]
#   bus-cycles                                         [Hardware event]
#   cache-misses                                       [Hardware event]
#   cache-references                                   [Hardware event]
#   cpu-cycles OR cycles                               [Hardware event]
#   instructions                                       [Hardware event]
#   ref-cycles                                         [Hardware event]

#   alignment-faults                                   [Software event]
#   bpf-output                                         [Software event]
#   context-switches OR cs                             [Software event]
#   cpu-clock                                          [Software event]
#   cpu-migrations OR migrations                       [Software event]
#   dummy                                              [Software event]

perf top # show top hot functions or instructions
# Samples: 11M of event 'cycles:ppp', 4000 Hz, Event count (approx.): 1296274621165 lost: 0/0 drop: 0/0
# Overhead  Shared Object                                             Symbol
#   28.47%  [kernel]                                                  [k] mwait_idle_with_hints.constprop.0
#    3.50%  [kernel]                                                  [k] native_queued_spin_lock_slowpath.part.0
#    1.45%  [kernel]                                                  [k] copy_pte_range
#    1.43%  [kernel]                                                  [k] zap_pte_range
#    1.31%  [kernel]                                                  [k] __update_blocked_fair
#    0.70%  [kernel]                                                  [k] _raw_spin_lock
#    0.55%  [kernel]                                                  [k] __update_load_avg_cfs_rq
#    0.53%  [kernel]                                                  [k] filemap_map_pages
#    0.52%  [kernel]                                                  [k] page_remove_rmap
#    0.52%  [kernel]                                                  [k] __d_lookup_rcu
#    0.50%  perf                                                      [.] ordered_events__queue
#    0.46%  [kernel]                                                  [k] native_irq_return_iret
#    0.45%  [kernel]                                                  [k] release_pages
#    0.45%  perf                                                      [.] 0x0000000000182a85
```
