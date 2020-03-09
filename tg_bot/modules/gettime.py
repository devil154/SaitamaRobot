import requests
import json
import datetime

from telegram import Bot, Update, ParseMode
from telegram.ext import run_async

from tg_bot import dispatcher, TIME_API_KEY
from tg_bot.modules.disable import DisableAbleCommandHandler


def generate_time(to_find: str, findtype: str):

    data = requests.get(f"http://api.timezonedb.com/v2.1/list-time-zone?key={TIME_API_KEY}&format=json&fields=countryCode,countryName,zoneName,gmtOffset,timestamp,dst").json()

    for zone in data["zones"]:
        if to_find in zone[findtype].lower():
            
            country_name = zone['countryName']
            country_zone = zone['zoneName']
            country_code = zone['countryCode']

            if zone['dst'] == 1:
                daylight_saving = "Yes"
            else:
                daylight_saving = "No"

            date_fmt = "%Y-%m-%d"
            time_fmt = "%H:%M:%S"
            gmt_offset = zone['gmtOffset']
            timestamp = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=gmt_offset)
            current_date = timestamp.strftime(date_fmt)
            current_time = timestamp.strftime(time_fmt)

            break
    
    try:
        result = "<b>Country :</b> {}\n" \
                 "<b>Zone Name :</b> {}\n" \
                 "<b>Country Code :</b> {}\n" \
                 "<b>DayLight saving :</b> {}\n" \
                 "<b>Current Date :</b> {}\n" \
                 "<b>Current Time :</b> {}".format(country_name, country_zone, country_code, daylight_saving, current_date, current_time)
    except:
        result = None

    return result


@run_async
def gettime(bot: Bot, update: Update):

    message = update.effective_message
    
    try:
        query_timezone = message.text.strip().split(" ", 1)[1]
    except:
        message.reply_text("Provide a country name/timezone to find.")
        return
        
    if len(query_timezone) == 2:
        result = generate_time(query_timezone, "countryCode")
    elif "/" in query_timezone:
        result = generate_time(query_timezone, "zoneName")
    else:
        result = generate_time(query_timezone, "countryName")

    if not result:
        message.reply_text(f"Timezone info not available for {query_timezone}")
        return

    message.reply_text(result, parse_mode=ParseMode.HTML)


__help__ = """
 - /time <query> : Gives information about a timezone.

Available queries : Country code/Country Name/TimeZone Name
"""

TIME_HANDLER = DisableAbleCommandHandler("time", gettime)

dispatcher.add_handler(TIME_HANDLER)

__mod_name__ = "Time"
__command_list__ = ["time"]
__handlers__ = [TIME_HANDLER]
