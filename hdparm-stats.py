#!/usr/bin/env python3

import re
import locale
import datetime

def read_file(file_path):
    with open(file_path) as f:
        speed = None

        for line in f:
            line = line.rstrip()
            if speed is not None:
                dt = datetime.datetime.strptime(line, '%a %b %d %H:%M:%S  CEST %Y')
                print(f'{dt}, {speed}')
                speed = None
            else:
                r = re.search('seconds = *([0-9.]+) (..)/sec$', line)

                if line.endswith('/secs'):
                    assert r

                if r:
                    speed = r.group(1)
                    unit = r.group(2)

                    if unit == 'MB':
                        speed = float(speed)
                    elif unit == 'kB':
                        speed = float(speed) / 8


def main():
    file_information = read_file('/home/carles/hdparm.log')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    locale.setlocale(locale.LC_TIME)
    main()
