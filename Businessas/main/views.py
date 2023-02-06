import json
from django.shortcuts import render
from django.http import HttpResponse

import smtplib as smtp
from email.header import Header
from email.mime.text import MIMEText

from .models import UsRequest, Services, Staff, Feedback


def index(request):
    txt = Services.objects.all()
    txt2 = Staff.objects.all()
    txt3 = Feedback.objects.all()
    return render(request, 'main/index.html', {'txt': txt, 'txt2': txt2, 'txt3': txt3})


def save_request(request):
    req = request.GET
    fname = request.GET.get('fname')
    phone = request.GET.get('phone')
    msg = request.GET.get('msg')
    if fname == "None" or phone == "None" or msg == "None":
        pass
    elif msg == "Необходимо перезвонить":
        send_ms(subject="Необходимо перезвонить", text=f"{fname}\n{phone}")
    else:
        send_ms(subject="Новая заявка", text=f"{fname}\n{phone}\n{msg}")
    print(f'{req=}')
    # Передача данных через HttpResponse в json
    data = {"header": "Hello Django"}
    # Create a new record using the model's constructor.
    a_record = UsRequest(fname=fname, phone=phone, msg=msg)
    # Save the object into the database.
    a_record.save()
    return HttpResponse(json.dumps(data), content_type='application/json')


def send_ms(subject, text):
    login = 'forsmtplib@gmail.com'
    password = 'mmhaavwsidqjbxja'

    server = smtp.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(login, password)

    mime = MIMEText(text, 'plain', 'utf-8')
    mime['Subject'] = Header(subject, 'utf-8')

    server.sendmail(login, 'b2b-as@yandex.ru', mime.as_string())
    server.sendmail(login, 'milk554@yandex.ru', mime.as_string())
