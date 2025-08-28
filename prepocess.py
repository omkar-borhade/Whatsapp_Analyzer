import re
import pandas as pd
import unicodedata
from datetime import datetime

def parse_whatsapp_chat(text):
    text = unicodedata.normalize("NFKC", text)  # normalize spaces

    # WhatsApp datetime regex
    pattern = r'(\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s*(?:am|pm)\s-\s)'

    matches = list(re.finditer(pattern, text))
    records = []

    for i in range(len(matches)):
        start = matches[i].end()  # message starts after timestamp
        end = matches[i+1].start() if i+1 < len(matches) else len(text)
        ts = matches[i].group(1).strip(" -")
        msg = text[start:end].strip()

        # Parse datetime
        try:
            dt = datetime.strptime(ts, "%d/%m/%y, %I:%M %p")
        except ValueError:
            # Some exports use yyyy instead of yy
            dt = datetime.strptime(ts, "%d/%m/%Y, %I:%M %p")

        records.append((dt, msg))

    df = pd.DataFrame(records, columns=["datetime", "message"])

    users = []
    messages = []
    for message in df['message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])
    df['user'] = users
    df['message'] = messages   

    df['only_date'] = df['datetime'].dt.date
    df['day']=df['datetime'].dt.day
    df['time']=df['datetime'].dt.time
    df['month_num']=df['datetime'].dt.month
    df['month'] = df['datetime'].dt.month_name()
    df['year']=df['datetime'].dt.year
    df['day_name'] = df['datetime'].dt.day_name()
    df['hour']=df['datetime'].dt.hour
    df['minute']=df['datetime'].dt.minute
    df.drop(columns=['datetime'], inplace=True)  

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period   
    return df