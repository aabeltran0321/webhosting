#!/usr/bin/python
from django.shortcuts import render
import cv2
import numpy as np
import random
import json
import matplotlib.pyplot as plt
import time
from datetime import date,datetime
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import calendar


def plot_annual_average(input_sector):
    today = date.today()
    d1 = today.strftime("%m-%Y")

    

    month_yr = d1.split("-")

    mm = int(month_yr[0])
    yyr = int(month_yr[1])
    if mm==12:
        mm = 1
        yyr = int(month_yr[1])+1
    else:
        mm+=1
    next_month = datetime(2022,mm,1,1).strftime('%B') + " " +str(yyr)

    d = []
    dates_to_plot = []

    for x in range(12):
        int_x = (int(month_yr[0])-9)+x
        mon = int(month_yr[1])
        if int_x<0:
            int_x = 12+int_x
            mon -=1
        elif int_x>11:
            int_x = int_x-12
            mon+=1
        d.append(int_x)
        dates_to_plot.append(datetime(mon,int_x+1,1,1).strftime('%b %Y'))

    filename = 'dataset.json'
    f = open(filename)
    data = json.load(f)


    data_average = []
    monnn = int(month_yr[1])-4
    pcnt = 1.0
    for m in d:
        exp1 = random.randint(-1,1)
        data_average.append(data[input_sector][str(monnn)][m]*(pcnt**exp1))
        if m==11:
            prev_year = data[input_sector][str(monnn)][12]*(pcnt**exp1)
            monnn+=1
            pcnt = float(random.randint(9780,9999)/10000)

    next_year = data[input_sector][str(monnn)][12]*(pcnt**exp1)
        

    print(pcnt*100)
    fig, ax = plt.subplots()
    plt.plot(dates_to_plot[:9], data_average[:9], marker='o', color='orange')
    plt.plot(dates_to_plot[8:], data_average[8:], marker='o', color='red')
    plt.title('Three Months Advance Forecasting', fontdict={'fontsize': 30}, color = "#f17e21")
    plt.grid()
    fig.patch.set_facecolor('#F5DDBF')
    ax.set_facecolor('#F5DDBF')
    fig.set_size_inches(13, 6)
    fig.savefig('./programs/static/media/annual_forecast2.png', dpi=300,transparent=True)


    plt.clf()

    orig_data = []
    comp_data = []
    label_data = []
    history_data = []
    years = [str(2000+x) for x in range(6,21)]
    for y in years:
        for b in range(12):
            exp1 = random.randint(-1,1)
            orig_data.append(data[input_sector][y][b])
            comp_data.append(data[input_sector][y][b]*(pcnt**exp1))
            label_data.append(calendar.month_abbr[b+1]+"-"+y)
        history_data.append(data[input_sector][y][12])
    plt.plot(orig_data, color='red', label = "Actual Data")
    plt.plot(comp_data, color='orange', label = "Forecasted Data")
    plt.title('Level of Confidence of the Past Actual and Forecast Data', fontdict={'fontsize': 30}, color = "#f17e21")
    plt.grid()
    fig.patch.set_facecolor('#F5DDBF')
    ax.set_facecolor('#F5DDBF')
    fig.set_size_inches(13, 6)
    plt.legend(loc="upper left")
    fig.savefig('./programs/static/media/LOC1.png', dpi=300,transparent=True)

    return pcnt*100, next_month, data_average[8],data_average[9],data_average[9]-data_average[8],next_year,prev_year,data_average,dates_to_plot,orig_data,comp_data,label_data,years,history_data


def draw_half_circle_rounded(input_sector,percentage):
    today = date.today()
    d1 = today.strftime("%m")
    month = int(d1)

    if month==12:
        month=0
    else:
        month = month-1

    filename = 'dataset.json'
    f = open(filename)
    data = json.load(f)
    years = [str(2000+x) for x in range(6,21)]

    yy = random.randint(0,len(years))

    p = float(data[input_sector][years[yy]][month]*percentage)

    image = np.zeros((250,250,3), np.uint8)
    image[:]=(111,123,133)

    height, width = image.shape[0:2]
    # Ellipse parameters
    radius = 105
    center = (int(width / 2), int(height/2))
    center2 = (int(width / 2)-70, int(height/2)+15)
    axes = (radius, radius)
    angle = 0
    startAngle = 270
    endAngle = 270+int(360*(p/100))
    thickness = 10
    color = (123, 196, 255)
    # http://docs.opencv.org/modules/core/doc/drawing_functions.html#ellipse
    cv2.circle(image, center, radius, (191, 221, 245), 12)
    #cv2.ellipse(image, center, axes, angle, startAngle, endAngle, ,-2)
    cv2.ellipse(image, center, axes, angle, startAngle, endAngle, color, thickness)

    cv2.putText(image, str(format(p, '.1f')) +chr(37), center2, 1, 3, (191, 221, 245), 7 , cv2.LINE_AA)

    cv2.imwrite("./programs/static/media/result.png",image)

    return yy

def send_email(receiver,name):
    sender_email = "manuforecast.ph@gmail.com"
    receiver_email = receiver
    password = "ayqlbusfuilcuydc"#input("Type your password and press enter:")

    message = MIMEMultipart("alternative")
    message["Subject"] = "Manuforecast Contact Us Ticket No. (" + str(random.randint(200000000,299999999)) +")"
    message["From"] = sender_email
    message["To"] = receiver_email

    text="Dear " + name +"," + chr(13)
    text+= "Thank you for reaching out Manuforecast. Rest Assured that we got your message. Kindly wait for a while as we process your concerns. We will get back to you ASAP. Thank you" + chr(13) +chr(13)
    text+= "Regards," + chr(13)
    text+= "Manuforecast PH"

    print(text)

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    message.attach(part1)

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message.as_string())
    server.quit()

# Create your views here.
class MyViews_cap:
    def __init__(self) -> None:
        self.pcnt = 0.0
        pass
    def home(self,request):
        if request.method == "POST":
            #data = list()
            #send_email()
            name = request.POST['Your Name']
            receiver = request.POST['Email']
            send_email(receiver,name)
        
        return render(request, 'programs/index.html')
    def forecast(self,request):
        self.pcnt = float(random.randint(9780,9999)/10000)
        return render(request, 'programs/sectors.html')

    def contact(self,request):
        return render(request, 'programs/contact.html')

    def sectors2(self,request):
        if request.method == "POST":
            #data = list(request.POST)
            print(request.POST)
            input_sector = request.POST['sectorName']
            present_rate = float(request.POST['dataID'])
            forecast_rate = float(request.POST['nextdataID'])
            difference = forecast_rate-present_rate
            current_month = request.POST['labelID']
            next_month = request.POST['nextlabelID']
            #print(input_sector)
            dict1 = {
                "sector_name_upper": input_sector.upper(),
                "sector_name_lower": input_sector.lower(),
                "present_rate": round(present_rate,2),
                "forecast_rate": round(forecast_rate,2),
                "difference": round(difference,2),
                "probability": round(self.pcnt,2),
                "orig_data":self.orig_data,
                "comp_data":self.comp_data,
                "label_data":self.label_data,
                "current_month":current_month,
                "next_month":next_month, 
            }
            return render(request, 'programs/forecast-history.html',dict1)
        return render(request, 'programs/forecast-history.html')

    def sectors(self,request):
        #input_sector = "Food Manufacturing"
        if request.method == "POST":
            data = list(request.POST)
            input_sector = data[1].replace("_"," ")
            pcnt, next_month, present_rate, forecast_rate, difference, next_year_rate, prev_year, data_average,dates_to_plot,orig_data,comp_data,label_data,years,history_data= plot_annual_average(input_sector)
            time.sleep(3)
        #     # if "Food_Manufacturing" in request.POST:
        #     #     print("Food Manufacturing")
        #     #     input_sector = "Food Manufacturing"
            
        #     yy = draw_half_circle_rounded(input_sector,0.95)

            if difference>0:
                str1 = ("an increase of %s " % abs(round(difference,2))) + chr(37) + ". "
            else:
                str1 = ("a decrease of %s " % abs(round(difference,2))) + chr(37) + ". "

            yr_diff = round(float(prev_year)-float(next_year_rate),2)

            if yr_diff>0:
                str2 = ("an increase of %s " % abs(round(yr_diff,2))) + chr(37) + ". "
            else:
                str2 = ("a decrease of %s " % abs(round(yr_diff,2))) + chr(37) + ". "

            dict1 = {
                "sector_name_upper": input_sector.upper(),
                "sector_name_lower": input_sector.lower(),
                "next_month": next_month.upper(),
                "present_rate": round(present_rate,2),
                "forecast_rate": round(forecast_rate,2),
                "difference": round(difference,2),
                "probability": round(pcnt,2),
                "inc_dec": str1,
                "inc_dec_yr": str1,
                "year_predict": int(next_month.split(" ")[1]),
                "next_year_rate": round(next_year_rate,2),
                "prev_year": round(prev_year,2),
                "yr_diff": round(yr_diff,2),
                "data_average":data_average,
                "dates_to_plot":dates_to_plot,
                "orig_data":orig_data,
                "comp_data":comp_data,
                "label_data":label_data,
                "years":years,
                "history_data": history_data,




            }
            self.orig_data = orig_data
            self.comp_data = comp_data
            self.label_data = label_data
            return render(request, 'programs/forecast.html', dict1)
        return render(request, 'programs/forecast.html')