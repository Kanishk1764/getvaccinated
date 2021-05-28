import requests
from datetime import datetime


base_cowin_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict"
now = datetime.now()
today_date=now.strftime("%d-%m-%Y")
api_url_telegram = "https://api.telegram.org/bot1632490270:AAFWSQZyqQOWSU2BqCj5n6L2ZB4XfpSMBPM/sendMessage?chat_id=@__groupid__&text="
group_id = "VaccineNotifier_Saitan"
faridabad_district_ids = [186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207]

def fetch_data_from_cowin(district_id):
  query_params = "?district_id={}&date={}".format(district_id,today_date)
  headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
  final_url = base_cowin_url+query_params
  response=requests.get(final_url,headers=headers)
  extract_availability_data(response)
  # print(response.text)

def fetch_data_for_state(district_ids):
    for district_id in district_ids:
        fetch_data_from_cowin(district_id)

def extract_availability_data(response):
    response_json = response.json()
    for center in response_json["sessions"]:
        if center["available_capacity_dose1"] >0 and center["min_age_limit"]== 45:
            message = "Pincode:{},Name:{},Slots:{},Minimum Age:{}".format(center["pincode"], center["name"],center["available_capacity_dose1"],center["min_age_limit"])
            send_message_telegram(message)

def send_message_telegram(message):
    final_telegram_url = api_url_telegram.replace("__groupid__",group_id)
    final_telegram_url = final_telegram_url + message
    response = requests.get(final_telegram_url)
    print(response)
        
if __name__ == "__main__":
  fetch_data_for_state(faridabad_district_ids)
