import imutils
import time
import cv2
import json

line_point1 = (250,0)
line_point2 = (250,500)


#in this case above the line and inbetween the two points is considered in

ENTERED_STRING = "ENTERED_THE_AREA"
LEFT_AREA_STRING = "LEFT_THE_AREA"
NO_CHANGE_STRING = "NOTHIN_HOMEBOY"

LOWEST_CLOSEST_DISTANCE_THRESHOLD = 100




class Person:

    positions = []

    def __init__(self, position):
        self.positions = [position]

    def update_position(self, new_position):
        self.positions.append(new_position)
        if len(self.positions) > 100:
            self.positions.pop(0)


    def on_opposite_sides(self):
        return ((self.positions[-2][0] > line_point1[0] and self.positions[-1][0] <= line_point1[0])
                or (self.positions[-2][0] <= line_point1[0] and self.positions[-1][0] > line_point1[0]))

    def did_cross_line(self):
        if self.on_opposite_sides():
            if self.positions[-1][0] > line_point1[0]:
                return ENTERED_STRING
            else:
                return LEFT_AREA_STRING
        else:
            return NO_CHANGE_STRING

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


def get_footage(vid_no=1):

    vid_no = str(vid_no)
    cam_no=f"video/vid{vid_no}.mp4"
    return cv2.VideoCapture(cam_no)

def find_foreground_objects(background_model):
    thresh = cv2.threshold(background_model, 25, 255, cv2.THRESH_BINARY)[1]

    thresh = cv2.dilate(thresh, None, iterations=3)
    thresh = cv2.erode(thresh, None, iterations=10)
    #cv2.imshow("Foreground Mfasdfaodel", thresh)


    (_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return cnts


class Cam():
    def __init__(self,cam_no, inside_count):
        self.cam_no = cam_no
        self.inside_count = inside_count


pythonDictionary = [
    {"lat": 21.413, "lng":39.897, "count": 1},
	{"lat": 21.423, "lng":39.897, "count": 2},
	{"lat": 21.421, "lng":39.897, "count": 3}
    ]

def zones(cams):
    print ("cams length:"+str(len(cams)))
    for i in range(len(pythonDictionary)-1):
        if i >= len(cams):
            break
        else:
            pythonDictionary[i]['count'] = cams[i].inside_count-cams[i+1].inside_count
            dictionaryToJson = json.dumps(pythonDictionary)

    with open ('test.josn', 'w') as data:
            json.dump(pythonDictionary, data)



cams=[]
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
                    if lowest_closest_distance < LOWEST_CLOSEST_DISTANCE_THRESHOLD:
                        people_list[i].update_position(rectangle_center)
                        change = people_list[i].did_cross_line()
                        if change == ENTERED_STRING:
                            inside_count += 1
                        elif change == LEFT_AREA_STRING:
                            inside_count -= 1
                    else:
                        new_person = Person(rectangle_center)
                        people_list.append(new_person)
                else:
                    new_person = Person(rectangle_center)
                    people_list.append(new_person)


            cv2.putText(frame, "Number of people inside: {}".format(inside_count), (10, 20),
    		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            cv2.line(frame, line_point1, line_point2, (255, 0, 0), 2)
            cv2.imshow("Security Feed", frame)


            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break

        cams.append(Cam(i,inside_count))
        camera.release()
        cv2.destroyAllWindows()
    camss = [Cam(1,3),Cam(2,3),Cam(3,5),Cam(4,3)]
    zones(cams)


main()
