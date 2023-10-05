from django.db import models
from ufls.celery import app as Celery

# Create your models here.
from multiselectfield import MultiSelectField


class Printer(models.Model):
    TYPES = (
        ("B", "Badge Printer [SP75+]"),
        ("R", "Receipt Printer [Epson TM88-x]"),
        ("L", "Label Printer [Brother]")
    )

    QUEUES = (
        ("mainqueue", "Badge Printer - Main Queue"),
        ("minor15queue", "Badge Printer - Minor 15+ Queue"),
        ("minor14queue", "Badge Printer - Minor 14-15 Queue"),
        ("daypassqueue", "Badge Printer - Day Pass Queue"),
        ("dealersdenqueue", "Badge Printer - Dealers Den Queue"),
        ("blackonly", "Badge Printer - Black Prints Only"),
        ("r-frontreg1", "Receipt Printer - Front of Reg Station 1 Queue"),
        ("r-frontreg2", "Receipt Printer - Front of Reg Station 2 Queue"),
        ("r-frontreg3", "Receipt Printer - Front of Reg Station 3 Queue"),
        ("r-frontreg4", "Receipt Printer - Front of Reg Station 4 Queue"),
        ("r-frontreg5", "Receipt Printer - Front of Reg Station 5 Queue"),
        ("r-frontreg", "Receipt Printer - Front of Reg Station General Queue"),
        ("r-backreg", "Receipt Printer - Back of Reg Picker Station Queue"),
        ("l-it", "Label Printer - IT Label Printer Queue")
    )

    address = models.CharField(max_length=100, help_text="Depending on the system, this will either be its IP address or Printer Queue Name")
    name = models.CharField(max_length=100)
    queues = MultiSelectField(choices=QUEUES, max_length=500)
    type = models.CharField(choices=TYPES, max_length=1)
    def save(self, *args, **kwargs):
        super(Printer, self).save(*args, **kwargs)
        Celery.send_task(name='receiptmanager.updatePrinterLocations')