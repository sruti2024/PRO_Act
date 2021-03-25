from django.db import models

class Project_add(models.Model):
    pid = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=200)
    desc = models.CharField(max_length=700)
    link = models.CharField(max_length=200)
    stack = models.CharField(max_length=300)
    date = models.CharField(max_length=100)
    status= models.IntegerField(null=True)

    def save(self, *args, **kwargs):
        self.pid = str(str(self.name[0:3])+'_'+str(self.date).split(' ')[0].split('-')[2])
        super(Project_add, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


# For OTP
class OTPModel(models.Model):
    user = models.EmailField(max_length=127)
    timestamp = models.DateTimeField(auto_now_add=True)
    otp = models.IntegerField()

    class Meta:
        verbose_name = 'OTP'


 # For Subtask
class modules_add(models.Model):
    task_id= models.CharField(max_length=50, primary_key=True)
    #super_id= models.ForeignKey(modules_add, on_delete=models.CASCADE)
    project_id= models.ForeignKey(Project_add, on_delete=models.CASCADE)
    task_desc= models.CharField(max_length=500)
    task_status = models.IntegerField(null=True)
    
    def saves(self, *args, **kwargs):
        self.task_id = str(str(self.task_desc[0:3])+'_'+str(self.project_id))
        super(modules_add, self).save(*args, **kwargs)


    def _str_(self):
        return self.task_desc