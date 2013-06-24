class FakeSubprocess():
   def __init__(self):
      self.pid = 1
      self.status = 'RUN'
      
   def poll(self):
      if self.status == 'RUN':
         return None
      elif self.status == 'DIE':
         return 0
      elif self.status == 'KILL':
         return -1
   
   def kill(self):
      self.status = 'KILL'
   
   def wait(self):
      # TODO Wait some time.
      self.status = 'DIE'
