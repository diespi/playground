#calculate the angle between the watch hands of an analog clock

# read the time 
time = input( ' hour minute ' ).split()
minutes= int(time[1]) % 60 # we only consider 59 minutes
hours = int(time[0]) % 12   # analog has only 12 hours

largeangle = 360 / 60 * minutes # absolute angle of the large hand 6 degree per minute
smallangle =360 /60 * hours *5  # absolute angle of the small angle 30 degrees per hour
# in an analog clock the  small hand moves between the hour marks which is 0.5 degrees per minute
correction = 360 /60 *5 * minutes /60
# now e can calculate the angle and we don'like to see negative values 
# when the large hands absolute angle is bigger than the small hand's

angle = smallangle -largeangle  + correction
if angle < 0:
        angle += 360
print ("at", hours,":", minutes, "the angle is: ",angle)
