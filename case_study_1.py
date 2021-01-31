import csv
import jdatetime
import json
import os

DATETIME_STRING_FORMAT = '%Y/%m/%d %H:%M'
NUMBER_OF_ROWS = 10 * 365 * 24
NUMBER_OF_DAYS = 10 * 365

PATH_DATASET = 'datasets/'
if not os.path.exists(PATH_DATASET):
    os.makedirs(PATH_DATASET)


def json_reader(jsonfile):
    print("reading " + jsonfile)
    f = open(jsonfile, "r")
    contents = ""
    if f.mode == 'r':
        contents = f.read()
    print("parsing to json")
    return json.loads(contents)


def test_day_by_day():
    json_data = json_reader('load.json')
    for i in json_data.keys():
        the_day = jdatetime.datetime.strptime(i, DATETIME_STRING_FORMAT)
        next_day = the_day + jdatetime.timedelta(hours=1)
        if next_day.strftime(DATETIME_STRING_FORMAT) not in json_data.keys():
            print(next_day.strftime(DATETIME_STRING_FORMAT))


# test_day_by_day()
# load.json day by day, time by time is correct


# These days:
# 1389/01/02 00:00
# 1391/01/02 00:00
# 1394/01/02 00:00
# 1395/01/02 00:00
# 1396/01/02 00:00
# 1397/01/02 00:00
# 1398/01/02 00:00
# are ZERO Load


json_data = json_reader('load.json')

field_names = ['calc', 'Load_t',
               'L_t-1', 'L_t-2', 'L_t-3',
               'L_d_t', 'L_d_t-1', 'L_d_t+1',
               'L_w_t', 'L_w_t-1', 'L_w_t+1',
               'L_m_t', 'L_m_t-1', 'L_m_t+1',
               'L_y_t', 'L_y_t-1', 'L_y_t+1']

first_date = jdatetime.datetime(year=1388, month=1, day=1)

final_data = [field_names]
for i in range(NUMBER_OF_DAYS):
    the_day = first_date + jdatetime.timedelta(days=i)
    the_day_str = the_day.strftime("%Y/%m/%d")
    print('making ' + the_day_str)

    for j in range(0, 24):
        datetime_day = jdatetime.datetime(year=the_day.year, month=the_day.month, day=the_day.day, hour=j)
        day_hour_load = json_data.get(datetime_day.strftime(DATETIME_STRING_FORMAT))

        a_row_data = [
            datetime_day.strftime('%Y/%m/%d %H:%M'),
            day_hour_load,
            json_data.get((datetime_day - jdatetime.timedelta(hours=1)).strftime('%Y/%m/%d %H:%M')),  # t-1
            json_data.get((datetime_day - jdatetime.timedelta(hours=2)).strftime('%Y/%m/%d %H:%M')),  # t-2
            json_data.get((datetime_day - jdatetime.timedelta(hours=3)).strftime('%Y/%m/%d %H:%M')),  # t-3

            json_data.get((datetime_day - jdatetime.timedelta(days=1)).strftime('%Y/%m/%d %H:%M')),  # d-t
            json_data.get((datetime_day - jdatetime.timedelta(days=1) - jdatetime.timedelta(hours=1)).strftime('%Y/%m/%d %H:%M')),  # d-t-1
            json_data.get((datetime_day - jdatetime.timedelta(days=1) + jdatetime.timedelta(hours=1)).strftime('%Y/%m/%d %H:%M')),  # d-t+1

            json_data.get((datetime_day - jdatetime.timedelta(days=7)).strftime('%Y/%m/%d %H:%M')),  # w-t
            json_data.get((datetime_day - jdatetime.timedelta(days=7) - jdatetime.timedelta(hours=1)).strftime('%Y/%m/%d %H:%M')),  # w-t-1
            json_data.get((datetime_day - jdatetime.timedelta(days=7) + jdatetime.timedelta(hours=1)).strftime('%Y/%m/%d %H:%M')),  # w-t+1

            json_data.get((datetime_day - jdatetime.timedelta(days=28)).strftime('%Y/%m/%d %H:%M')),  # m-t
            json_data.get((datetime_day - jdatetime.timedelta(days=28) - jdatetime.timedelta(hours=1)).strftime('%Y/%m/%d %H:%M')),  # m-t-1
            json_data.get((datetime_day - jdatetime.timedelta(days=28) + jdatetime.timedelta(hours=1)).strftime('%Y/%m/%d %H:%M')),  # m-t+1

            json_data.get((datetime_day - jdatetime.timedelta(days=364)).strftime('%Y/%m/%d %H:%M')),  # y-t
            json_data.get((datetime_day - jdatetime.timedelta(days=364) - jdatetime.timedelta(hours=1)).strftime('%Y/%m/%d %H:%M')),  # y-t-1
            json_data.get((datetime_day - jdatetime.timedelta(days=364) + jdatetime.timedelta(hours=1)).strftime('%Y/%m/%d %H:%M')),  # y-t+1
        ]

        # NoneTypes
        for i in range(a_row_data.__len__()):
            if type(a_row_data[i]) is NoneType:
                a_row_data[i] = day_hour_load

        final_data.append(a_row_data)

with open('datasets/final_cs1.csv', 'w') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerows(final_data)
csvFile.close()
