# -*- coding: utf-8 -*-
import optparse
from collections import namedtuple

Rules = namedtuple('Rules', ['rows','columns','ingredients_per_slice','max_cells_per_slice'])


def parse_rules(rules_line):
    rules_raw = rules_line.split(' ')
    rules_raw = [int(rule) for rule in rules_raw]
    rules = Rules(*rules_raw)
    return rules


def read_pizza(filename):
    done_slices = []
    with open(filename, 'r') as file:
        pizza = file.read().split('\n')
        rules = pizza[0]
        pizza = pizza[1:]
        print parse_rules(rules), pizza


def main():

    parser = optparse.OptionParser()
    parser.add_option("-f", "--file", dest="filename",
                      help="write report to FILE", default='requirements.txt')
    (options, args) = parser.parse_args()
    with open(options.filename, 'r') as f:
        data = f.read()
        print data
    read_pizza(options.filename)

if __name__ == '__main__':
    main()
