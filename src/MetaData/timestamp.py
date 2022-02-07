from datetime import datetime

def to_timestamp(input: str):
    input_split = input.strip().split(' ')
    date = input_split[0]
    time = input_split[1]
    date_split = date.split('/')
    time_split = time.split(':')
    dt = datetime(int(date_split[2]), int(date_split[1]), int(date_split[0]), int(time_split[0]), int(time_split[1]), int(time_split[2]))
    return datetime.timestamp(dt)

def to_str(input):
    dt = str(datetime.fromtimestamp(input))
    print(dt)
    dt_split = dt.split(' ')
    date = dt_split[0]
    time = dt_split[1]
    date_split = date.split('-')
    result = f"{date_split[2]}/{date_split[1]}/{date_split[0]} {time}"
    return result


if __name__ == "__main__":
    print(to_timestamp("12/08/2018 11:58:30"))
    print(to_str(1534067910.0))