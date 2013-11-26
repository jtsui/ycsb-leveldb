import sys
from collections import defaultdict
import matplotlib.pyplot as plt

FIELDS = ['[UPDATE]', '[INSERT]', '[READ]']
LINE_TYPES = {'[READ]': '',
              '[UPDATE]': '',
              '[INSERT]': '',
              }


def str_to_num(s):
    try:
        return float(s)
    except ValueError:
        return False


def throughput(log_file):
    data = []
    text = {}
    with open(log_file) as f:
        for line in f:
            if line.startswith('Command line:'):
                line_split = line.split(' ')
                workload = 'unkown'
                for i in range(len(line_split)):
                    if line_split[i] == '-P':
                        workload = line_split[i + 1]
                title = 'Throughput for %s from %s' % (
                    workload, log_file)
            split_line = line.strip().split(' ')
            if len(split_line) == 7 and split_line[1] == 'sec:' and split_line[3] == 'operations;':
                data.append((split_line[0], split_line[4]))
            vals = [x.strip() for x in line.split(',')]
            if len(vals) == 3 and vals[0] == '[OVERALL]':
                if vals[1] == 'RunTime(ms)':
                    text[vals[1]] = str_to_num(vals[2])
                elif vals[1] == 'Throughput(ops/sec)':
                    text[vals[1]] = str_to_num(vals[2])
    fig, ax = plt.subplots()
    # line
    x = [time for time, tp in data]
    y = [tp for time, tp in data]
    ax.plot(x, y)
    plt.title(title)
    plt.xlabel('time (sec)')
    plt.ylabel('throughput (ops/sec)')
    # table
    row_labels = ['Overall']
    col_labels = text.keys()
    table_vals = []
    row = []
    for col in col_labels:
        row.append(text[col])
    table_vals.append(row)
    table = ax.table(cellText=table_vals,
             rowLabels=row_labels,
             colLabels=col_labels,
             loc='lower right')
    table.set_fontsize(8)
    table.scale(0.85, 1.1)
    plt.show()


def latency(log_file):
    data = defaultdict(list)
    text = defaultdict(dict)
    title = ''
    with open(log_file) as f:
        for line in f:
            if line.startswith('Command line:'):
                line_split = line.split(' ')
                workload = 'unkown'
                for i in range(len(line_split)):
                    if line_split[i] == '-P':
                        workload = line_split[i + 1]
                title = 'Latency for %s from %s' % (
                    workload, log_file)
            vals = [x.strip() for x in line.split(',')]
            if len(vals) == 3 and vals[0] in FIELDS:
                time = str_to_num(vals[1])
                latency = str_to_num(vals[2])
                if time is not False and time != 0 and latency is not False:
                    data[vals[0]].append((time, latency))
                elif time is False:
                    text[vals[0]][vals[1]] = vals[2]
    fig, ax = plt.subplots()
    # table
    row_labels = text.keys()
    col_labels = text.items()[0][1].keys()
    table_vals = []
    for row in row_labels:
        table_vals.append([text[row][param] for param in col_labels])
    table = ax.table(cellText=table_vals,
             rowLabels=row_labels,
             colLabels=col_labels,
             loc='upper right')
    table.set_fontsize(8)
    table.scale(0.85, 1.1)
    # lines
    for field, points in data.items():
        x = [point[0] for point in points]
        y = [point[1] for point in points]
        ax.plot(x, y, LINE_TYPES[field], label=field.strip('[]').lower())
    plt.xlabel('time (ms)')
    plt.ylabel('latency (us)')
    plt.title(title).set_y(1.2)
    legend = ax.legend(loc='right')
    for label in legend.get_texts():
        label.set_fontsize('medium')
    plt.title(title)
    plt.show()


def main():
    if len(sys.argv) == 3:
        this_file, log_file, option = sys.argv
        if option == 'throughput':
            throughput(log_file)
            return
        elif option == 'latency':
            latency(log_file)
            return
    print 'Wrong number of arguments.'
    print 'Usage: python graph.py [log file] [throughput | latency]'
    return


if __name__ == '__main__':
    main()
