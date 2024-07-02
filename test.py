from misc.astrology import Astrology

day = 6
month = 1
year = 2000
hour = 7
minute = 45
latitude = 19.2056
longitude = 25.2056
timezone = 5.5
language = "ru"

astrology = Astrology()


pdf_url = astrology.get_pdf_url(day=day, month=month, year=year, hour=hour, minute=minute, latitude=latitude, longitude=longitude, timezone=timezone, language=language)

print(pdf_url) 