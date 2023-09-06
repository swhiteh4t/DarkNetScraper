from datetime import datetime

def get_formatted_time():
    # Get the current time
    current_time = datetime.now()

    # Format the time as a string
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_time