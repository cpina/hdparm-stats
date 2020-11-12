#!/usr/bin/env python3
import os
import re
import locale
import datetime
import argparse

def read_file(file_path):
    data = []
    with open(file_path) as f:
        speed = None

        for line in f:
            line = line.rstrip()
            if speed is not None:
                if 'CEST' in speed:
                    dt = datetime.datetime.strptime(line, '%a %b %d %H:%M:%S  CEST %Y')
                elif 'CET' in speed:
                    dt = datetime.datetime.strptime(line, '%a %b %d %H:%M:%S CET %Y')

                data.append(str(dt) + ',' + str(speed) + '\n')
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

    return data

def write_csv(html_output, hdparm_speeds):
    with open(os.path.join(html_output, 'data.csv'), 'w') as f:
        f.writelines(hdparm_speeds)


def main(hdparm_log, html_output):
    hdparm_speeds = read_file(hdparm_log)

    write_csv(html_output, hdparm_speeds)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    locale.setlocale(locale.LC_TIME)

    parser = argparse.ArgumentParser()
    parser.add_argument('hdparm_log')
    parser.add_argument('html_directory_output')

    options = parser.parse_args()

    main(options.hdparm_log, options.html_directory_output)
