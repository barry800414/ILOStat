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

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage:', sys.argv[0], 'inCSV outJson', file=sys.stderr)
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
                if hourBand not in newData:
                    newData[hourBand] = dict()
                country = row[field['Country']]
                assert country not in newData[hourBand]
                thousands = float(row[field[YEAR]])
                newData[hourBand][country] = thousands

    # slightly change structure
    newData2 = list()
    for hourBand, values in newData.items():
        newData2.append([hourBand, values])

    with open(sys.argv[2], 'w') as f:
        json.dump(newData2, f, indent=1)      

    # print some statistics
    for d in newData2:
        print(d[0], round(sum(d[1].values())*1000), sep=',')

#Country,Sex,Hour bands,Source,Series footnotes,2015
