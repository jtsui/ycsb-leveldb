import re
import sys
import math
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

FIELDS = ['[UPDATE]', '[INSERT]', '[READ]']
plt.ioff()


def throughput(log_files, save_or_show='show', hist=False):
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
        plt.plot(x, y, label=log_file.replace('.log', ''),
                 marker='o', ls='', ms=5, mec='white')
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


def latency(log_files, save_or_show='show'):
    for log_file in log_files:
        data = defaultdict(list)
        with open(log_file) as f:
            for line in f:
                match = re.findall(
                    r'(\[INSERT\]|\[READ\]|\[UPDATE\]), (\d*), (\d*)', line)
                if match:
                    op = match[0][0].replace('[', '').replace(']', '').lower()
                    data[op].append((float(match[0][1]), float(match[0][2])))
        for field, points in data.items():
            times = [point[0] for point in points]
            latencies = [point[1] for point in points]
            plt.plot(times, latencies, label='%s %s' %
                     (log_file.replace('.log', ''), field.strip('[]').lower()))
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


def ops(log_files, save_or_show='show', hist=False):
    for log_file in log_files:
        data = []
        with open(log_file) as f:
            for line in f:
                match = re.findall(
                    r'(\d*) sec: (\d*) operations; \d*.?\d* current ops/sec', line)
                if match:
                    data.append(match[0])
        x = [float(time) for time, ops in data]
        y = [float(ops) / 10000000 for time, ops in data]
        plt.plot(x, y, label=log_file.replace('.log', ''))
    plt.title('Cumulative Operations')
    plt.xlabel('time (ms)')
    plt.ylabel('operations (%)')
    legend = plt.legend()
    for label in legend.get_texts():
        label.set_fontsize('small')
    if save_or_show == 'show':
        plt.show()
    else:
        plt.savefig('cumulative_ops.pdf', bbox_inches=0)
        print 'Cumulative operations graph saved to cumulative_ops.pdf'


def publish_ops():
    data = []
    with open('run_new_l.log') as f:
        for line in f:
            match = re.findall(
                r'(\d*) sec: (\d*) operations; \d*.?\d* current ops/sec', line)
            if match:
                data.append(match[0])
    x = [float(time) for time, ops in data]
    y = [float(ops) / 10000000 for time, ops in data]
    plt.plot(x, y, label='TSX - 4 threads', color='pink',
             marker='D', linestyle='-', markevery=50, markersize=4)
    data = []
    with open('run_stock_l.log') as f:
        for line in f:
            match = re.findall(
                r'(\d*) sec: (\d*) operations; \d*.?\d* current ops/sec', line)
            if match:
                data.append(match[0])
    x = [float(time) for time, ops in data]
    y = [float(ops) / 10000000 for time, ops in data]
    plt.plot(x, y, label='Stock - 4 threads', color='lightblue',
             marker='D', linestyle='-', markevery=30, markersize=4)
    data = []
    with open('run_new_g.log') as f:
        for line in f:
            match = re.findall(
                r'(\d*) sec: (\d*) operations; \d*.?\d* current ops/sec', line)
            if match:
                data.append(match[0])
    x = [float(time) for time, ops in data]
    y = [float(ops) / 10000000 for time, ops in data]
    plt.plot(x, y, label='TSX - 8 threads', color='red')
    data = []
    with open('run_stock_g.log') as f:
        for line in f:
            match = re.findall(
                r'(\d*) sec: (\d*) operations; \d*.?\d* current ops/sec', line)
            if match:
                data.append(match[0])
    x = [float(time) for time, ops in data]
    y = [float(ops) / 10000000 for time, ops in data]
    plt.plot(x, y, label='Stock - 8 threads', color='blue')
    plt.xlabel('Time (ms)')
    plt.ylabel('Operations completed (%)')
    legend = plt.legend(loc='lower right')
    for label in legend.get_texts():
        label.set_fontsize('medium')
    plt.show()


def main():
    if len(sys.argv) == 2:
        option = sys.argv[1]
        if option == 'publish_ops' or option == 'po':
            publish_ops()
            return
    elif len(sys.argv) > 2:
        args = sys.argv
        option = args[1]
        save_or_show = 'show'
        if args[2] == 'save' or args[2] == 'show':
            save_or_show = args[2]
            log_files = args[3:]
        else:
            log_files = args[2:]
        if option == 'throughput' or option == 't':
            throughput(log_files, save_or_show)
            return
        elif option == 'latency' or option == 'l':
            latency(log_files, save_or_show)
            return
        elif option == 'clatency' or option == 'cl':
            clatency(log_files, save_or_show)
            return
        elif option == 'ops' or option == 'o':
            ops(log_files, save_or_show)
            return
    print 'Wrong number of arguments.'
    print 'Usage: python graph.py [throughput | latency | ops | clatency | publish_ops] [save | show(default)] [log files]'

if __name__ == '__main__':
    main()
