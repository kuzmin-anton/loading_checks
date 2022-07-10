from django.db import models


class Check(models.Model):
    check_number = models.CharField(unique=True, max_length=20)
    check_issuance_time = models.DateTimeField()
    total = models.IntegerField()
    customer_id = models.CharField(max_length=20)
    pos_id = models.CharField(max_length=20)

    class Meta:
        db_table = 'checks'

    def __str__(self):
        return self.check_number
