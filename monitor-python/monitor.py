import psutil
import time
import argparse
import sys
from datetime import datetime
import os
from typing import Optional, Dict, List
import signal
import json

class ProcessMonitor:
    def __init__(self, interval: float = 1.0):
        self.interval = interval
        self.monitoring = False
        self.monitored_pids = set()
        self.current_pid = os.getpid()  # Get current process PID
        self.current_monitor_filename = None
        self.bar_length = 110
        return
    
    def find_processes_by_name(self, process_name: str, exclude_self: bool = True) -> List[psutil.Process]:
        matching_processes = []
        current_process = psutil.Process(self.current_pid) if exclude_self else None
        for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'create_time']):
            try:
                # skip the current process if exclude_self is True
                if exclude_self and (proc.pid == self.current_pid or current_process and proc.create_time() == current_process.create_time()):
                    continue
                proc_name = proc.info.get('name', '')
                if process_name.lower() in proc_name.lower(): # check process name
                    matching_processes.append(proc)
                elif proc.info.get('cmdline'): # check command line
                    cmdline = ' '.join(proc.info['cmdline'])
                    if process_name.lower() in cmdline.lower():
                        matching_processes.append(proc)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        return matching_processes
    
    def get_process_resource_usage(self, pid: int) -> Optional[Dict]:
        try:
            proc = psutil.Process(pid)
            # Get additional process info
            with proc.oneshot():
                cpu_percent = proc.cpu_percent(interval=0.1)  # Get CPU usage
                memory_info = proc.memory_info() # Get memory information
                memory_percent = proc.memory_percent()
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                io_counters = proc.io_counters()
                return {'current_time':timestamp, 'pid': pid, 'name': proc.name(),
                    'cmdline': ' '.join(proc.cmdline()) if proc.cmdline() else proc.name(),
                    'cpu_percent': round(cpu_percent, 2),
                    'memory_rss': memory_info.rss, 'memory_rss_mb': round(memory_info.rss / (1024 * 1024), 2),
                    'memory_percent': round(memory_percent, 2),
                    'memory_vms': memory_info.vms, 'memory_vms_mb': round(memory_info.vms / (1024 * 1024), 2),
                    'num_threads': proc.num_threads(),
                    'create_time': datetime.fromtimestamp(proc.create_time()).strftime('%Y-%m-%d %H:%M:%S'),
                    'status': proc.status(),
                    'read_chars':io_counters.read_chars, 'write_chars':io_counters.write_chars,
                    'read_bytes': io_counters.read_bytes, 'write_bytes': io_counters.write_bytes,
                    'read_count': io_counters.read_count, 'write_count': io_counters.write_count
                }
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            print('get_process_resource_usage error')
            return None
    
    def get_system_usage(self) -> Dict:
        return {'system_cpu_percent': psutil.cpu_percent(interval=0.1), 'system_memory_percent': psutil.virtual_memory().percent, 'system_memory_available_gb': round(psutil.virtual_memory().available / (1024**3), 2), 'system_memory_used_gb': round(psutil.virtual_memory().used / (1024**3), 2), 'system_memory_total_gb': round(psutil.virtual_memory().total / (1024**3), 2)}
    
    def display_header(self):
        print("="*self.bar_length)
        print(f"{'Timestamp':<20} {'PID':<8} {'Process Name':<20} {'CPU %':<8} {'Memory %':<10} {'Memory VMS (MB)':<15} {'Memory RSS (MB)':<15} {'Threads':<8} {'Status':<10}")
        print("-"*self.bar_length)
    
    def display_usage(self, process_info: Dict):
        timestamp = datetime.now().strftime("%m-%d %H:%M:%S")
        print(f"{timestamp:<20} {process_info['pid']:<8} {process_info['name'][:18]:<20} {process_info['cpu_percent']:<8.1f} {process_info['memory_percent']:<10.2f} {process_info['memory_vms_mb']:<15.2f} {process_info['memory_rss_mb']:<15.2f} {process_info['num_threads']:<8} {process_info['status']:<10}")
    
    def display_system_summary(self, system_info: Dict):
        print("\n" + "-"*self.bar_length)
        print("SYSTEM SUMMARY:")
        print(f"  CPU Usage: {system_info['system_cpu_percent']:.1f}%")
        print(f"  Memory Usage: {system_info['system_memory_percent']:.1f}% ({system_info['system_memory_used_gb']} GB / {system_info['system_memory_total_gb']} GB)")
        print(f"  Available Memory: {system_info['system_memory_available_gb']} GB")
        print("-"*self.bar_length)
    
    def monitor_process_by_name(self, process_name: str, duration: Optional[float] = None):
        self.monitoring = True
        start_time = time.time()
        # Find initial processes
        processes = self.find_processes_by_name(process_name)
        if not processes:
            print(f"No processes found matching: {process_name}")
            return
        print(f"Found {len(processes)} process(es) matching: {process_name}")
        # self.display_header()
        cnt = 0
        process_infos = []
        try:
            while self.monitoring:
                if cnt % 5 == 0:
                    self.display_header()
                    cnt = 0
                    timestamp = datetime.now().strftime("%m_%d_%H_%M")
                    self.current_monitor_filename = f'monitor_{process_name}_{timestamp}.txt' if self.current_monitor_filename is None else self.current_monitor_filename
                    with open(self.current_monitor_filename, 'w') as f:
                        f.write(str(json.dumps(process_infos)))
                    if os.path.getsize(self.current_monitor_filename) > 100*1024*1024:
                        timestamp = datetime.now().strftime("%m_%d_%H_%M")
                        self.current_monitor_filename = f'monitor_{process_name}_{timestamp}.txt'
                        process_infos = []
                current_processes = self.find_processes_by_name(process_name)
                for proc in current_processes:
                    process_info = self.get_process_resource_usage(proc.pid)
                    if process_info:
                        process_infos.append(process_info)
                        self.display_usage(process_info)
                if not current_processes:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] No processes found matching: {process_name}")
                    break
                # check duration
                if duration and (time.time() - start_time) >= duration:
                    break
                time.sleep(self.interval)
                cnt += 1
                print()  # Add blank line between intervals
        except KeyboardInterrupt:
            print("\n\nMonitoring interrupted by user")
        finally:
            self.monitoring = False
            system_info = self.get_system_usage()
            self.display_system_summary(system_info)
    
        def monitor_single_process(self, pid: int, duration: Optional[float] = None):
            self.monitoring = True
            start_time = time.time()
            self.display_header()
            try:
                while self.monitoring:
                    process_info = self.get_process_resource_usage(pid) # Get process info
                    system_info = self.get_system_usage()
                    if process_info:
                        self.display_usage(process_info)
                    else:
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] Process {pid} not found or terminated")
                        break
                    if duration and (time.time() - start_time) >= duration: # Check duration
                        break
                    time.sleep(self.interval)
            except KeyboardInterrupt:
                print("\n\nMonitoring interrupted by user")
            finally:
                self.monitoring = False
                self.display_system_summary(system_info)

def main():
    parser = argparse.ArgumentParser(
        description="Process Monitor - Monitor CPU and Memory usage of processes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --pid 1234                    Monitor process with PID 1234
  %(prog)s --name python                 Monitor all python processes
  %(prog)s --pid 1234 --duration 30     Monitor for 30 seconds
  %(prog)s --pid 1234 --interval 0.5     Monitor with 0.5 second interval
        """
    )
    
    # Monitoring target arguments
    target_group = parser.add_argument_group('Monitoring Target')
    target_group.add_argument("--pid", type=int, help="Process ID to monitor")
    target_group.add_argument("--name", type=str, help="Process name to monitor (supports partial names)")
    
    # Monitoring parameters
    param_group = parser.add_argument_group('Monitoring Parameters')
    param_group.add_argument("--interval", type=float, default=1.0, help="Monitoring interval in seconds (default: 1.0)")
    param_group.add_argument("--duration", type=float, help="Monitoring duration in seconds (default: infinite)")
        
    args = parser.parse_args()
    
    # validate arguments
    if not any([args.pid, args.name]):
        parser.error("Please specify --pid, --name")
    
    if args.pid and args.name:
        parser.error("Please specify either --pid or --name, not both")
    
    # create monitor instance
    monitor = ProcessMonitor(interval=args.interval)
    
    # handle signal for graceful shutdown
    def signal_handler(sig, frame):
        print("\n\nshutting down monitor...")
        monitor.monitoring = False
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    try:        
        # monitor by PID
        if args.pid:
            # verify process exists
            if not psutil.pid_exists(args.pid):
                print(f"Error: Process with PID {args.pid} not found")
                sys.exit(1)
            process_info = monitor.get_process_resource_usage(args.pid)
            if process_info:
                print(f"Monitoring process: {process_info['name']} (PID: {args.pid})")
                print(f"Command: {process_info['cmdline']}")
                print(f"Started: {process_info['create_time']}")
                print()
            monitor.monitor_single_process(args.pid, args.duration)
        elif args.name: # Monitor by name
            monitor.monitor_process_by_name(args.name, args.duration)
    except PermissionError:
        print("Error: Permission denied. Try running with sudo/administrator privileges.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()