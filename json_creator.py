import json
import jdatetime
import xlrd


book = xlrd.open_workbook("Load/load.xlsx")
sh1 = book.sheet_by_index(0)


json_data = {}
for i in range(1, sh1.nrows):
    datestr = sh1.cell_value(i, 1)

    hour = 0
    for j in range(2, 2+24):
        datetimestr = datestr + ' ' + str(hour) + ':00'
        mdatetime = jdatetime.datetime.strptime(datetimestr, '%Y/%m/%d %H:%M')

        json_data.update({mdatetime.strftime('%Y/%m/%d %H:%M'): sh1.cell_value(i, j)})
        hour += 1

file = open("load.json", "w")
file.write(json.dumps(json_data, sort_keys=True, indent=5))
file.close()
