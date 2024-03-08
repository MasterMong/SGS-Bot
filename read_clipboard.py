import clipboard

data = clipboard.paste()
lines = data.splitlines()
line_header = lines.pop(0)
line_columns = line_header.split('\t')

for line in lines:
    if (line != '' and line != line_header):
        cells = line.split('\t')
        for cell in cells:
            print(cell)
