from django.db import models

class Elementsalaire(models.Model):
  
  intitule_element=models.CharField(max_length=20)
  description=models.CharField(max_length=255)

  def __str__(self):
    return self.intitule_element
  
  class Meta:
        db_table="elementSal"
       


