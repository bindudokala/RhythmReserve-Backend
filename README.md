
# RhythmReserve Backend

Backend for P465 project RhythmReserve

**How to run**

clone repo
```git clone https://github.com/bindudokala/RhythmReserve-Backend/```

get into repo directory
```cd P465-Backend```

start python virtual environment depending on your operating system

- **MAC/LINUX**
```source venv/bin/activate```

- **WINDOWS**
```winvenv\Scripts\activate```

*NOTE: there may be differences in python packages installed between the 2 virtual environments, REFER TO REQUIREMENTS.TXT*

get into django directory
```cd RhythmReserve```

start server
```python manage.py runserver```
OR 
```uvicorn RhythmReserve.asgi:application``` for the chat support implementation

**How to interact with postgreSQL database**

download [pgAdmin](https://www.pgadmin.org/download/)

once open, click `Add New Server`

1. Name it whatever you want
2. go to the **Connection** tab
- Host name/address: ```ep-delicate-cherry-a5827apg.us-east-2.aws.neon.tech```
- Port: ```5432```
- Maintenance database: ```master```
- Username: ```tipb47```
- Password: ```m8OqSEQnAb5D```
3. Save

backend admin dashboard user:
email: admin@admin.com
username: admin
password: password16
