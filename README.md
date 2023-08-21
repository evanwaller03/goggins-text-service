# goggins-text-service
Sends a daily David Goggins motivational text to users who sign up to my google forms.


Process: 
  - Users submit their phone number and carrier to my google forms which automatically updates a google sheet.
  - My program chooses a random quote from a "config.py" file, connects to the google sheets api, and then sends each person the same daily motivational quote using python's SMTPLIB.

What I would like to add:
  - Task Scheduler to automatically execute this every day without my manual execution of the file
  - Increased API rate limits via the google cloud project console interface
