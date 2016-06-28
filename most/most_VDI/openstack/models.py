from django.db import models


class VmModel(models.Model):
    name = models.CharField(u'Name', max_length=50)

    def __unicode__(self):
        return self.name
