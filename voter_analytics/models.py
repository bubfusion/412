from django.db import models

# Create your models here.

class Voter(models.Model):
  # Personal info
  last_name = models.TextField()
  first_name = models.TextField()
  street_number = models.IntegerField()
  street_name = models.TextField()
  apartment_number = models.TextField()
  zip_code = models.IntegerField()
  dob = models.DateField()
  registration_date = models.DateField()
  party_affiliation = models.CharField(max_length=2)
  precinct_number = models.TextField()
  
  # Voting history
  v20state = models.BooleanField()
  v21town = models.BooleanField()
  v21primary = models.BooleanField()
  v22general = models.BooleanField()
  v23town = models.BooleanField()
  voter_score = models.IntegerField()

  def __str__(self):
      '''Return a string representation of this model instance.'''
      return f'{self.first_name} {self.last_name} {self.dob}, {self.party_affiliation}'
    
def load_data():
    '''Function to load data records from CSV file into Django model instances.'''
    filename = '/Users/bubfusion/Downloads/newton_voters.csv'
    f = open(filename)
    f.readline()
    for line in f:
        fields = line.split(',')
        # show which value in each field
                
        # create a new instance of Result object with this record from CSV
        try:
          voter = Voter(
                        last_name = fields[1].strip(),
                        first_name = fields[2].strip(),
                        street_number = fields[3].strip(),
                        street_name = fields[4].strip(),
                        apartment_number = fields[5].strip(),
                        zip_code = fields[6].strip(),
                        dob = fields[7].strip(),
                        registration_date = fields[8].strip(),
                        party_affiliation = fields[9].strip(),
                        precinct_number = fields[10].strip(),
                        
                        # Voting history
                        v20state=fields[11].strip().lower() in ['true'],
                        v21town = fields[12].strip().lower() in ['true'],
                        v21primary = fields[13].strip().lower() in ['true'],
                        v22general = fields[14].strip().lower() in ['true'],
                        v23town = fields[15].strip().lower() in ['true'],
                        voter_score = fields[16],
          )
          voter.save()
          print(f'Created result: {voter}')
        except:
          print(f"Skipped: {fields}")