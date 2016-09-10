import sys, csv, json, re

YEAR='2015'
startLine = 6

def readHourBand(s):
    p = re.compile("(\d+)\-(\d+) \(Hour bands\)")
    m = p.match(s)
    if m is not None:
        return (int(m.group(1)), int(m.group(2)))
    
    p = re.compile("(\d+)\+ \(Hour bands\)")
    m = p.match(s)
    if m is not None:
        return (int(m.group(1)), )

    return None

def hourBandtoStr(hb):
    if len(hb) == 1:
        return str(hb[0])
    else:
        return '%s_to_%s' % (hb[0], hb[1])

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage:', sys.argv[0], 'inCSV outCSV', file=sys.stderr)
        exit(-1)
    
    newData = dict()

    with open(sys.argv[1], 'r') as f:
        data = csv.reader(f, delimiter=',')
        for i, row in enumerate(data):
            if i < startLine:
                continue
            elif i == startLine:
                field = { f: i for i,f in enumerate(row) }
            else:
                hourBand = readHourBand(row[field['Hour bands']])
                if hourBand is None:
                    continue
                
                country = row[field['Country']]
                thousands = float(row[field[YEAR]])
                print('%s-%s, %d' % (country, hourBandtoStr(hourBand), round(thousands*1000)))

