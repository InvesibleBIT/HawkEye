
# Importing the Open-cv and imutils libraries and the built-in library json
import imutils
import cv2
import json


# setting the point we will use to draw the line we will start countinon on
line_bottom_point = (250,0)
line_top_point = (250,500)

# we will use these later
Crossed_from_Left_to_Right = "entered"
Crossed_from_Right_to_Left = "left"
still_there = "no change"

# shortest distance between Person and Camera
shortest_distance = 100



# Class Person contain all functions we need to detect people and count them
class Person:

    # set empty list for positions
    positions = []

    # take the position and added to positions list
    def __init__(self, position):
        self.positions = [position]

    ''' update the position and appending it to positions list
      and check if the list contain more than 100 so remove the oldest position
      so we can control it so we dnt run out of memory '''
    def update_position(self, new_position):
        self.positions.append(new_position)
        if len(self.positions) > 100:
            self.positions.pop(0)

    # this function returns if the person is on the opposite side or not
    def on_opposite_sides(self):
        return ((self.positions[-2][0] > line_bottom_point[0] and self.positions[-1][0] <= line_bottom_point[0])
                or (self.positions[-2][0] <= line_bottom_point[0] and self.positions[-1][0] > line_bottom_point[0]))

    # this function return if person entered or left  or didn't move
    def did_cross_line(self):
        if self.on_opposite_sides():
            if self.positions[-1][0] > line_bottom_point[0]:
                return Crossed_from_Left_to_Right
            else:
                return Crossed_from_Right_to_Left
        else:
            return still_there

    def distance_from_last_x_positions(self, new_position, x):
        total = [0,0]
        z = x
        while z > 0:
            if (len(self.positions) > z):
                total[0] +=  self.positions[-(z+1)][0]
                total[1] +=  self.positions[-(z+1)][1]
            else:
                x -= 1
            z -= 1
        if total[0] < 1 or total[1] < 1:
            return abs(self.positions[0][0] - new_position[0]) + abs(self.positions[0][1] - new_position[1])
        total[0] = total[0] / x
        total[1] = total[1] / x

        return abs(new_position[0] - total[0]) + abs(new_position[1] - total[1])

# this function capture the video or "the stream video from live camera"
def get_footage(vid_no=1):
    vid_no = str(vid_no)
    cam_no=f"video/vid{vid_no}.mp4"
    return cv2.VideoCapture(cam_no)

# this function return the counters
def find_foreground_objects(background_model):
    thresh = cv2.threshold(background_model, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=3)
    thresh = cv2.erode(thresh, None, iterations=10)
    (_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return cnts

# this class saves the number of people camera did count and camera id
class Cam():
    def __init__(self,cam_no, inside_count):
        self.cam_no = cam_no
        self.inside_count = inside_count

# setting the fixed zone's cordinates and the number of people did count
ZonesDictionary = [
    {"lat": 21.413, "lng":39.897, "count": 1},
	{"lat": 21.423, "lng":39.897, "count": 2},
	{"lat": 21.421, "lng":39.897, "count": 3}
    ]

# this function dump dictionary we made to json file
def zones(cams):
    for i in range(len(ZonesDictionary)-1):
        if i >= len(cams):
            break
        else:
            ZonesDictionary[i]['count'] = cams[i].inside_count-cams[i+1].inside_count
            dictionaryToJson = json.dumps(ZonesDictionary)

    with open ('templates/FrontEnd/assets/js/pages/data.josn', 'w') as data:
            json.dump(ZonesDictionary, data)



cams=[]

# this the main function that calculate and set the out put inside the list cams
def main():
    for i in range(1,4):
        camera = get_footage(i)
        fgbg = cv2.createBackgroundSubtractorMOG2()
        frame_count = 0
        people_list = []
        inside_count = 0

        while True:

            (grabbed, frame) = camera.read()

            if not grabbed:
                break

            frame = imutils.resize(frame, width=500)

            frame_count += 1

            filtered_frame = cv2.GaussianBlur(frame, (21, 21), 0)
            fgmask = fgbg.apply(filtered_frame)

            foreground_objects = find_foreground_objects(fgmask)

            for c in foreground_objects:
                if cv2.contourArea(c) < 5000:
                    continue

                (x, y, w, h) = cv2.boundingRect(c)

                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                lowest_closest_distance = float("inf")
                rectangle_center = (int( ((2 * x) + w)/2) ,int( ((2 * y) + h)/2)  )
                cv2.circle(frame, rectangle_center, 2, (0, 0, 255))
                closest_person_index = None


                for i in range(0, len(people_list)):
                    if people_list[i].distance_from_last_x_positions(rectangle_center, 5) < lowest_closest_distance:
                        lowest_closest_distance = people_list[i].distance_from_last_x_positions(rectangle_center, 5)
                        closest_person_index = i
                if closest_person_index is not None:
                    if lowest_closest_distance < shortest_distance:
                        people_list[i].update_position(rectangle_center)
                        change = people_list[i].did_cross_line()
                        if change == Crossed_from_Left_to_Right:
                            inside_count += 1
                        elif change == Crossed_from_Right_to_Left:
                            inside_count -= 1
                    else:
                        new_person = Person(rectangle_center)
                        people_list.append(new_person)
                else:
                    new_person = Person(rectangle_center)
                    people_list.append(new_person)


            cv2.putText(frame, "Number of people inside: {}".format(inside_count), (10, 20),
    		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            cv2.line(frame, line_bottom_point, line_top_point, (255, 0, 0), 2)
            cv2.imshow("Security Feed", frame)


            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break

        cams.append(Cam(i,inside_count))
        camera.release()
    zones(cams)


main()
