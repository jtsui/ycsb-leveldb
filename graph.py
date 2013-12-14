import re
import sys
import matplotlib.pyplot as plt
from collections import defaultdict

FIELDS = ['[UPDATE]', '[INSERT]', '[READ]']
plt.ioff()


def str_to_num(s):
    try:
        return float(s)
    except ValueError:
        return False


def throughput(log_files, save_or_show):
    for log_file in log_files:
        data = []
        with open(log_file) as f:
            for line in f:
                match = re.findall(
                    r'(\d*) sec: \d* operations; (\d*.?\d*) current ops/sec', line)
                if match:
                    data.append(match[0])
        x = [int(time) for time, tp in data]
        y = [float(tp) for time, tp in data]
        plt.plot(x, y, label=log_file.replace('.log', ''), marker='o', ls='', ms=5, mec='white')
        # plt.plot(x, y, label=log_file.replace('.log', ''))
    plt.title('Throughput')
    plt.xlabel('time (s)')
    plt.ylabel('ops/sec')
    legend = plt.legend()
    for label in legend.get_texts():
        label.set_fontsize('small')
    if save_or_show == 'show':
        plt.show()
    else:
        plt.savefig('throughput.pdf', bbox_inches=0)
        print 'Throughput graph saved to throughput.pdf'


def latency(log_files, save_or_show):
    for log_file in log_files:
        data = defaultdict(list)
        with open(log_file) as f:
            for line in f:
                vals = [x.strip() for x in line.split(',')]
                if len(vals) == 3 and vals[0] in FIELDS:
                    time = str_to_num(vals[1])
                    latency = str_to_num(vals[2])
                    if time is not False and time != 0 and latency is not False:
                        data[vals[0]].append((time, latency))
        for field, points in data.items():
            x = [point[0] for point in points]
            y = [point[1] for point in points]
            plt.plot(x, y, label='%s %s' %
                     (log_file.replace('.log', ''), field.strip('[]').lower()))
            # plt.plot(x, y, label='%s' %
            #          ('TSX Accelerated' if 'new' in log_file else 'Stock LevelDB'))
    plt.title('Latency')
    plt.xlabel('time (ms)')
    plt.ylabel('latency (us)')
    legend = plt.legend()
    for label in legend.get_texts():
        label.set_fontsize('small')
    if save_or_show == 'show':
        plt.show()
    else:
        plt.savefig('latency.pdf', bbox_inches=0)
        print 'Latency graph saved to latency.pdf'


def ops(log_files, save_or_show):
    for log_file in log_files:
        data = []
        with open(log_file) as f:
            for line in f:
                match = re.findall(
                    r'(\d*) sec: (\d*) operations; \d*.?\d* current ops/sec', line)
                if match:
                    data.append(match[0])
        x = [float(time) for time, ops in data]
        y = [float(ops) for time, ops in data]
        plt.plot(x, y, label=log_file.replace('.log', ''))
    plt.title('Cumulative Operations')
    plt.xlabel('time (ms)')
    plt.ylabel('ops')
    legend = plt.legend()
    for label in legend.get_texts():
        label.set_fontsize('small')
    if save_or_show == 'show':
        plt.show()
    else:
        plt.savefig('cumulative_ops.pdf', bbox_inches=0)
        print 'Cumulative operations graph saved to cumulative_ops.pdf'


def main():
    if len(sys.argv) < 3:
        print 'Wrong number of arguments.'
        print 'Usage: python graph.py [throughput | latency] [save | show(default)] [log files]'
    else:
        args = sys.argv
        option = args[1]
        save_or_show = 'show'
        if args[2] == 'save' or args[2] == 'show':
            save_or_show = args[2]
            log_files = args[3:]
        else:
            log_files = args[2:]
        if option == 'throughput':
            throughput(log_files, save_or_show)
        elif option == 'latency':
            latency(log_files, save_or_show)
        elif option == 'ops':
            ops(log_files, save_or_show)


if __name__ == '__main__':
    main()
