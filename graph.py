import re
import sys
import scipy
import csv
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

FIELDS = ['[UPDATE]', '[INSERT]', '[READ]']
plt.ioff()


def throughput(log_files, save_or_show='show'):
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
                    r'(\d*) sec: (\d*) operations;', line)
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


def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i + n]


def publish_throughput():
    data = []
    with open('run_new_l.log') as f:
        for line in f:
            match = re.findall(
                r'(\d*) sec: (\d*) operations;', line)
            if match:
                data.append(match[0])
    data2 = [(chunk[0][0], (float(chunk[-1][1]) - float(chunk[0][1])) / 60)
             for chunk in chunks(data, 6)]
    tps = np.array([y for x, y in data2])
    mean = np.mean(tps)
    std = np.std(tps)
    data2 = [(time, tp) for time, tp in data2 if abs(tp - mean) < 2 * std]
    times = [float(time) / 60 for time, ops in data2]
    tps = [float(ops) for time, ops in data2]
    plt.plot(times, tps, label='TSX - 4 threads', color='pink',
             marker='D', linestyle='-', markevery=7, markersize=4)
    data = []
    with open('run_stock_l.log') as f:
        for line in f:
            match = re.findall(
                r'(\d*) sec: (\d*) operations;', line)
            if match:
                data.append(match[0])
    data2 = [(chunk[0][0], (float(chunk[-1][1]) - float(chunk[0][1])) / 60)
             for chunk in chunks(data, 6)]
    tps = np.array([y for x, y in data2])
    mean = np.mean(tps)
    std = np.std(tps)
    data2 = [(time, tp) for time, tp in data2 if abs(tp - mean) < 2 * std]
    times = [float(time) / 60 for time, ops in data2]
    tps = [float(ops) for time, ops in data2]
    plt.plot(times, tps, label='Stock - 4 threads', color='lightblue',
             marker='D', linestyle='-', markevery=13, markersize=4)
    plt.xlabel('Time (min)')
    plt.ylabel('Throughput (ops/min)')
    legend = plt.legend(loc='lower right')
    for label in legend.get_texts():
        label.set_fontsize('medium')
    plt.show()


def publish_ops():
    tsx_data = []
    with open('run_new_l.log') as f:
        for line in f:
            match = re.findall(
                r'(\d*) sec: (\d*) operations; \d*.?\d* current ops/sec', line)
            if match:
                tsx_data.append(match[0])
    # tsx_times = [float(time) for time, ops in tsx_data]
    # tsx_ops = [float(ops) for time, ops in tsx_data]
    # plt.plot(tsx_times, tsx_ops, label='TSX - 4 threads', color='pink',
    #          marker='D', linestyle='-', markevery=50, markersize=4)
    stock_data = []
    with open('run_stock_l.log') as f:
        for line in f:
            match = re.findall(
                r'(\d*) sec: (\d*) operations; \d*.?\d* current ops/sec', line)
            if match:
                stock_data.append(match[0])
    # stock_times = [float(time) for time, ops in stock_data]
    # stock_ops = [float(ops) for time, ops in stock_data]
    # plt.plot(
    #     stock_times, stock_ops, label='Stock - 4 threads', color='lightblue',
    #     marker='D', linestyle='-', markevery=30, markersize=4)
    tsx_data = dict([(int(x) / 10 * 10, float(y))
                    for x, y in tsx_data])
    stock_data = [(int(x) / 10 * 10, float(y)) for x, y in stock_data]
    delta = []
    for time, ops in stock_data:
        delta.append((time, tsx_data[time] - ops))
    plt.plot([x for x, y in delta][0::10],
             [y for x, y in delta][0::10], label='4 threads')

    delta = delta[0::6]
    delta = [((x - 10) / 60, y) for x, y in delta]
    with open('4.csv', 'wb') as f:
        wr = csv.writer(f, quoting=csv.QUOTE_ALL)
        for d in delta:
            wr.writerow(d)

    tsx_data = []
    with open('run_new_g.log') as f:
        for line in f:
            match = re.findall(
                r'(\d*) sec: (\d*) operations; \d*.?\d* current ops/sec', line)
            if match:
                tsx_data.append(match[0])
    # x = [float(time) for time, ops in tsx_data]
    # y = [float(ops) / 10000000 for time, ops in tsx_data]
    # plt.plot(x, y, label='TSX - 8 threads', color='red')
    stock_data = []
    with open('run_stock_g.log') as f:
        for line in f:
            match = re.findall(
                r'(\d*) sec: (\d*) operations; \d*.?\d* current ops/sec', line)
            if match:
                stock_data.append(match[0])
    # x = [float(time) for time, ops in stock_data]
    # y = [float(ops) / 10000000 for time, ops in stock_data]
    # plt.plot(x, y, label='Stock - 8 threads', color='blue')
    tsx_data = dict([(int(x) / 10 * 10, float(y))
                    for x, y in tsx_data])
    stock_data = [(int(x) / 10 * 10, float(y)) for x, y in stock_data]
    delta = []
    for time, ops in stock_data:
        if time in tsx_data:
            delta.append((time, tsx_data[time] - ops))
    plt.plot([x for x, y in delta][0::10],
             [y for x, y in delta][0::10], label='8 threads')

    delta = delta[0::6]
    delta = [((x - 10) / 60, y) for x, y in delta]
    with open('8.csv', 'wb') as f:
        wr = csv.writer(f, quoting=csv.QUOTE_ALL)
        for d in delta:
            wr.writerow(d)

    tsx_data = []
    with open('run_new_o.log') as f:
        for line in f:
            match = re.findall(
                r'(\d*) sec: (\d*) operations; \d*.?\d* current ops/sec', line)
            if match:
                tsx_data.append(match[0])
    # x = [float(time) for time, ops in tsx_data]
    # y = [float(ops) / 10000000 for time, ops in tsx_data]
    # plt.plot(x, y, label='TSX - 2 threads', color='green')
    stock_data = []
    with open('run_stock_o.log') as f:
        for line in f:
            match = re.findall(
                r'(\d*) sec: (\d*) operations; \d*.?\d* current ops/sec', line)
            if match:
                stock_data.append(match[0])
    # x = [float(time) for time, ops in stock_data]
    # y = [float(ops) / 10000000 for time, ops in stock_data]
    # plt.plot(x, y, label='Stock - 2 threads', color='orange')
    tsx_data = dict([(int(x) / 10 * 10, float(y))
                    for x, y in tsx_data])
    stock_data = [(int(x) / 10 * 10, float(y)) for x, y in stock_data]
    delta = []
    for time, ops in stock_data:
        if time in tsx_data:
            delta.append((time, tsx_data[time] - ops))
    plt.plot([x for x, y in delta][0::10],
             [y for x, y in delta][0::10], label='2 threads')

    delta = delta[0::6]
    delta = [((x - 10) / 60, y) for x, y in delta]
    with open('2.csv', 'wb') as f:
        wr = csv.writer(f, quoting=csv.QUOTE_ALL)
        for d in delta:
            wr.writerow(d)

    plt.xlabel('Time (sec)')
    plt.ylabel('Delta operations completed (TSX ops - Stock ops)')
    legend = plt.legend(loc='upper left')
    for label in legend.get_texts():
        label.set_fontsize('medium')
    plt.show()


def stats(log_files):
    for log_file in log_files:
        print log_file
        f = open(log_file).read()
        print 'OVERALL'
        for field, num in re.findall(r'\[OVERALL\], ([a-zA-Z()/]*), (\d*)', f):
            print '%s\t%s' % (field.rjust(20), num)
        print 'READ'
        for field, num in re.findall(r'\[READ\], ([a-zA-Z()/]*), (\d*)', f):
            print '%s\t%s' % (field.rjust(20), num)
        read_lat = [float(x)
                    for x in re.findall(r'\[READ\], \d*, ([\d.]*)', f)]
        c = scipy.percentile(read_lat, 25)
        o = scipy.percentile(read_lat, 75)
        h = scipy.percentile(read_lat, 99)
        l = scipy.percentile(read_lat, 1)
        print '%s\t%s' % ('open'.rjust(20), o)
        print '%s\t%s' % ('high'.rjust(20), h)
        print '%s\t%s' % ('low'.rjust(20), l)
        print '%s\t%s' % ('close'.rjust(20), c)
        print 'INSERT'
        for field, num in re.findall(r'\[INSERT\], ([a-zA-Z()/]*), (\d*)', f):
            print '%s\t%s' % (field.rjust(20), num)
        insert_lat = [float(x)
                      for x in re.findall(r'\[INSERT\], \d*, ([\d.]*)', f)]
        c = scipy.percentile(insert_lat, 25)
        o = scipy.percentile(insert_lat, 75)
        h = scipy.percentile(insert_lat, 90)
        l = scipy.percentile(insert_lat, 10)
        print '%s\t%s' % ('open'.rjust(20), o)
        print '%s\t%s' % ('high'.rjust(20), h)
        print '%s\t%s' % ('low'.rjust(20), l)
        print '%s\t%s' % ('close'.rjust(20), c)


def main():
    if len(sys.argv) == 2:
        option = sys.argv[1]
        if option == 'publish_ops' or option == 'po':
            publish_ops()
            return
        if option == 'publish_throughput' or option == 'pt':
            publish_throughput()
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
        elif option == 'ops' or option == 'o':
            ops(log_files, save_or_show)
            return
        elif option == 'stats' or option == 's':
            stats(log_files)
            return
    print 'Wrong number of arguments.'
    print 'Usage: python graph.py [throughput | latency | ops | clatency | publish_ops] [save | show(default)] [log files]'

if __name__ == '__main__':
    main()
