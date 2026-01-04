# About Memory

**Theoretical 64-bit Address Space**: the complete, fixed range of virtual memory available to each process on a 64-bit system, spanning the full address range and defining the maximum possible memory a process could ever address.

**Virtual Memory (VIRT)**: the total size of all mapped regions (like program code, heap, stack, libraries, and memory-mapped files) that the process has actively claimed. *VIRT grows and shrinks as the process **allocates or frees memory***.

**Resident Set Size (RSS/RES)**: the physical memory actually allocated to a process.

**Shared Memory (SHR)**: the phisical memory shared with other processes, such as system libraries (```libc```).
