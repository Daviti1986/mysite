from BlackListApp.models import blacklist

def my_job():

    data = blacklist(ip='123456')
    data.save()