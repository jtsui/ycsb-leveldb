import re
import sys
import numpy


def get_variance(file_name):
    latencies = []
    with open(file_name) as f:
        for line in f:
            latencies.extend([float(x)
                             for x in re.findall(r'; (.*?) current ops/sec', line)])
    print numpy.std(latencies)


def main():
    if len(sys.argv) == 2:
        this_file, file_name = sys.argv
        get_variance(file_name)
        return
    print 'Wrong usage.'


if __name__ == '__main__':
    main()
