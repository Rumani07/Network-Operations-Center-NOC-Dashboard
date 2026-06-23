from django.db import models

# write class jaise us vid
class Sensing(models.Model):
    id = models.IntegerField(primary_key=True)
    ip = models.CharField(max_length=50)
    username = models.CharField(max_length=20, default="")
    passhash = models.CharField(max_length=20, default="")
    Site_name = models.CharField(max_length = 50)
    Type = models.CharField(max_length = 50)
    SensorID = models.JSONField(default=list)
    #This will store list of all the sensors on that IP address
    #eg - [1001,1002,1003]
    


    