import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.dates as mdates

file = 'monitor.txt'
with open(file) as f:
    raw_data = eval(f.read())

start = round(len(raw_data) * 0)
end  = round(len(raw_data) * 1)
print(f'start {start}, end {end}, total {len(raw_data)}')
data = list(raw_data)[start:end]

timestamps = []
memory_rss_values = []
memory_vms_values = []
for record in data:
    if record['memory_rss']/1024/1024 > 100:
        timestamps.append(datetime.strptime(record['current_time'], "%Y-%m-%d %H:%M:%S.%f"))
        memory_rss_values.append(int(round(record['memory_rss']/1024/1024)))
        memory_vms_values.append(int(round(record['memory_vms']/1024/1024)))

with open('result.txt', 'w') as f:
    tt = ''
    for i in range(len(timestamps)):
        tt += f'{str(timestamps[i])}\t{str(memory_rss_values[i])}\t{str(memory_vms_values[i])}\n'
    f.write(tt)

plt.figure(figsize=(12, 6))
plt.plot(timestamps, memory_rss_values, marker='o', linewidth=1, markersize=2, color='steelblue', label='RSS Mem')
plt.plot(timestamps, memory_vms_values, marker='o', linewidth=1, markersize=2, color='green', label='VIRT Mem')
plt.title(f'{timestamps[0].strftime("%Y-%m-%d %H:%M:%S")}   -   {timestamps[-1].strftime("%Y-%m-%d %H:%M:%S")}', fontsize=16, fontweight='bold')
plt.xlabel('Time', fontsize=12)
plt.ylabel('Memory', fontsize=12)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3, linestyle='--')
plt.tight_layout()
plt.legend()
plt.savefig('time_series_plot.png', dpi=300, bbox_inches='tight')
plt.savefig('time_series_plot.svg', format='svg', bbox_inches='tight')
plt.show()
