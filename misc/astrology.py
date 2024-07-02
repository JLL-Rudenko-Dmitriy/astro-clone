import requests

from config import ASTROLOGY_API_ID, ASTROLOGY_API_KEY

class Astrology:
    def __init__(self):
        self.api_endpoint = "https://pdf.astrologyapi.com/v1/natal_horoscope_report/tropical"
        self.user_id = ASTROLOGY_API_ID
        self.api_key = ASTROLOGY_API_KEY

    def get_pdf_url(self, day: int, month: int, year: int, hour: int, minute: int, latitude: float, longitude: float, timezone: str, language: str) -> str:
        data = {
            "day": day,
            "month": month,
            "year": year,
            "hour": hour,
            "minute": minute,
            "latitude": latitude,
            "longitude": longitude,
            "timezone": timezone,
            "language": language
        }
        try:
            response = requests.post(self.api_endpoint, data=data, auth=('628901', 'bc5870530c8a93a476a4824db9dbb145'))
        except:
            pass
        else:
            if response.status_code == 200:
                data = response.json()
                url = data.get('pdf_url')
                
                return url
            
        return None
