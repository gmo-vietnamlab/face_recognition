from crontab import CronTab

my_cron = CronTab(user='thanh')
job = my_cron.new(command='/home/thanh/erp/face_recognition/google_cloud.py')
cron = CronTab(tab="""0 0 * * * command""")

my_cron.write()
