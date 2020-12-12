""" Mail-Attachment """

#Attachment - Picture
picture_folder = Path("E:/Bilder/Cars/Toyota/Supra/MK4 - A80")
filename = picture_folder / "Screenshot_20191124-161132.jpg"


""" Copy & Paste """
# Open PDF file in binary mode
with open(filename, "rb") as attachment:
    # Add file as application/octet-stream
    # Email client can usually download this automatically as attachment
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())

# Encode file in ASCII characters to send by email
encoders.encode_base64(part)

# Add header as key/value pair to attachment part
part.add_header(
    "Content-Disposition",
    f"attachment; filename= {filename}",
)


""" Copy & Paste """
# Add attachment to message and convert message to string
message.attach(part)












""" #Paths
absFilePath = os.path.abspath(__file__)
print(absFilePath)
fileDir = os.path.dirname(os.path.abspath(__file__))
print(fileDir)
parentDir = os.path.dirname(fileDir)
print(parentDir)
"""





with open(path_of_request_file, 'w') as file_request:
        file_request.write(json.dumps(data_url_quote, indent=4))
        
        
        
        
        
        
        
#unixTime_now = []
#unixTime_ago = []
#calculation_time_days_ago = 5

"""
# doesn't work    
def get_data_from_stock_candle(calculation_time_days_ago):
    global url_finnhub, unixTime_ago, unixTime_now
    resolution="D"
    
    # get unixtime for finnhub-api
    # datetime.datetime(year=2020,month=12,day=1,hour=00,minute=00,second=00)
    unixTime_ago = time.mktime((datetime.datetime.now() - datetime.timedelta(minutes=calculation_time_days_ago)).timetuple())
    from_params = int(unixTime_ago)
    
    unixTime_now = time.mktime(datetime.datetime.now().timetuple())
    unixTime_now = time.mktime((datetime.datetime(year=2020,month=12,day=3,hour=00,minute=00,second=00)).timetuple())
    to_params=int(unixTime_now)
    url_candle = url_finnhub + f"stock/candle?symbol={symbol}&resolution={resolution}&from={from_params}&to={to_params}&token={api_token}"
    params_for_request = dict() #Leere Parameter, da schon in URL eingefügt
    
    data_of_url_candle = requests.get(url_candle).json()
    print(data_of_url_candle)
"""

#get_data_from_stock_candle(calculation_time_days_ago)









#r_currency = json.dumps(r_currency.json(), indent=4)    # Umwandlung zu schöner geformtem .json-formattiertem String
    #r_currency = json.loads(r_currency) # 