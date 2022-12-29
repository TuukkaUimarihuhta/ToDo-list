from datetime import datetime, timedelta

v = datetime.today()
z = v.strftime('%A %d.%m')
c = datetime.strptime(z, '%A %d.%m')

print(c)

print(z)

