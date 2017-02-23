# -*- coding: utf-8 -*-
import optparse


def main():

    parser = optparse.OptionParser()
    parser.add_option("-f", "--file", dest="filename",
                      help="write report to FILE", default='requirements.txt')
    (options, args) = parser.parse_args()
    with open(options.filename) as f:
        f.read()

if __name__ == '__main__':
    main()
