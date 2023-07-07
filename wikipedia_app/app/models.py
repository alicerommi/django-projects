from django.db import models

class Wikipedia_keyword(models.Model):

    keyword = models.CharField(max_length=200)
    keyword_description = models.TextField(max_length=500)
    keyword_timedate = models.DateTimeField(auto_now_add=True)
    def __str(self):
        return self.keyword
#
# class Folders(models.Model):
#     folder_title = models.CharField(max_length=200)
#     folder_upload_timedate = models.DateTimeField(auto_now_add=True)
#     folder_name = models.FileField(upload_to='uploads/')
#     folder_description = models.TextField()
#     def __str__(self):
#         return self.folder_title
#
# class Topics(models.Model):
#
#
#     DigitalDocument = models.ForeignKey(Documents, on_delete=models.CASCADE)
#     topic_name = models.CharField(max_length=50)
#     Folders = models.ForeignKey(Folders, on_delete=models.CASCADE)
#     def __str__(self):
#         return self.topic_name

# class User(models.Model):
#     username = models.CharField(max_length=50)
#     user_email = models.CharField(max_length=50)
#     password = models.CharField(max_length=50)
#
#     def __str__(self):
#         return self.user_email

