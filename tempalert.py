import conf,json,time
from boltiot import Sms,Bolt


minimum_limit=500
maximum_limit=600

config = {
"consumer_key"        : conf.consumer_key,
"consumer_secret"     : conf.consumer_secret,
"access_token"        : conf.access_token,
"access_token_secret" : conf.access_token_secret
}

def get_api_object(cfg):
    auth =tweepy.OAuthHandler(cfg['consumer_key'],
                                  cfg['consumer_secret'])
    auth.set_access_token(cfg['access_token'],
                              cfg['access_token_secret'])
    return tweepy.API(auth)

mybolt=Bolt(conf.API_KEY,conf.DEVICE_ID)
sms=Sms(conf.SSID,conf.AUTH_TOKEN,conf.TO_NUMBER,conf.FROM_NUMBER)
mailerone=Email(email_conf.MAILGUN_API_KEY,email_conf.SANDBOX_URL,email_conf.SENDER_EMAIL,email_conf.RECIPIENT_EMAIL)
mailersec=Email(email_conf.MAILGUN_API_KEY,email_conf.SANDBOX_URL,email_conf.SENDER_EMAIL,email_conf.RECIPIENT_EMAIL_SEC)

#To set the threshold to 25 deg celcius (since the Lm35 sensor gives a analog value it must be divided by 10.24 to convert to deg celcius.)
temperature_threshold = 100*256/1024


while True:
        response=mybolt.analogRead('A0')
        data=json.loads(response)
        print(data['value'])
        try:
                sensor_value=int(data['value'])
                Temperature=(100*sensor_value)/1024
                print(sensor_value)
                if temperature > temperature_threshold:
                        print ("Temperature has crossed the threshold of "+str(temperature_threshold)+"in deg Celcius and It is now : " + str(temperature)+"in deg celcius")


                        api_object=get_api_object(config)

                        tweet = "Temperature has crossed the threshold of " + str(temperature_threshold)+"in deg Celcius and It is now :"+ str(temperature)+"in deg celcius"


                        status = api_object.update_status(status=tweet)
                        response=mailerone.send_email("Alert! - Warning!","The Current temperature sensor value is " + str(sensor_value) +" And in Deg Celius is " + str(Temperature))
                        response=mailersec.send_email("Alert! - Warning!","The Current temperature sensor value is " + str(sensor_value) +" And in Deg Celcius is " + str(Temperature))

                        response = sms.send_sms("The Current temperature sensor value is " +str(sensor_value))
        except Exception as e:
                print("An error ocurred ", e)
         time.sleep(10)
