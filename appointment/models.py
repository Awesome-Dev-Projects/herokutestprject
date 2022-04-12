from django.db import models

from doctor.models import DoctorTimeSlot
# Create your models here.


class DailySlotBooking(models.Model):
    date = models.DateField()
    doctor_time_slot = models.ForeignKey(
        DoctorTimeSlot, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.date} {self.doctor_time_slot.doctor} {self.doctor_time_slot.time_slot} {self.status}"
