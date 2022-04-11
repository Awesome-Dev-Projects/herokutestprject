import requests


class Fast2SMS:
    @staticmethod
    def send_sms(phone_number, message):
        url = "https://www.fast2sms.com/dev/bulkV2"
        payload = f"sender_id=Cghpet&message={message}&language=english&route=v3&numbers={phone_number}"
        headers = {
            'authorization': "S1Dycah6O245MJLYf8erkibXIFtANQ0H9PsUjdKTBmC3vuZGnlUz5QvIAmypqsSETaYHwCBkZ4ciX06l",
            'Content-Type': "application/x-www-form-urlencoded",
            'Cache-Control': "no-cache",
        }
        response = requests.request("POST", url, data=payload, headers=headers)
        print(response.text)
