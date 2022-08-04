# cal_test.py
# Calendar test
# Kevin McAleer
# 18 August 2021

from skills.calendar import Calendar, Calendar_skill

mycal = Calendar_skill()
mycal.load()
mycal.add_event(begin="2021-07-18 20:00:00", name="test", description="this is a test")
mycal.add_event(begin="2021-08-20 20:00:00", name="launch YouTube Video",description="New vid dropping")
# mycal.list_events()
# mycal.remove_event("launch YouTube Video")
# mycal.list_events()
# mycal.remove_event("test")
print("this week:",mycal.list_events())
mycal.save()