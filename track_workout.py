



def convert_lap_time_to_mile_pace(lap_length_in_m: int, time_in_seconds: int):
    multiple_factor = 1609/lap_length_in_m
    return time_in_seconds*multiple_factor

def print_time_in_readable_format(time_in_seconds: str):
    minutes = int(time_in_seconds/60)
    seconds = int(time_in_seconds % 60)
    print(f"{minutes:02d}:{seconds:02d}")


print_time_in_readable_format(convert_lap_time_to_mile_pace(400, 104))