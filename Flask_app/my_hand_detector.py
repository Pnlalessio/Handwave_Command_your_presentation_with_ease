import math
import cv2
import mediapipe as mp

# HandDetector class definition.
class HandDetector:
    def __init__(self, use_static_mode=False, max_num_hands=2, model_complexity=1, detection_confidence=0.5, tracking_confidence=0.5):
        # Initialize HandDetector with parameters.
        self.use_static_mode = use_static_mode
        self.max_num_hands = max_num_hands
        self.model_complexity = model_complexity
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence

        # Initialize Mediapipe Hands module.
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=self.use_static_mode,
                                         max_num_hands=self.max_num_hands,
                                         model_complexity=self.model_complexity,
                                         min_detection_confidence=self.detection_confidence,
                                         min_tracking_confidence=self.tracking_confidence)
        self.mp_draw = mp.solutions.drawing_utils
        self.tip_ids = [4, 8, 12, 16, 20]
        self.fingers = []
        self.landmarks_list = []

    # Function to find hands and draw landmarks on the image.
    def find_hands(self, image, enable_draw=True, flip_image=True):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(image_rgb)
        all_hands = []
        height, width, channels = image.shape
        if self.results.multi_hand_landmarks:
            for hand_type, hand_landmarks in zip(self.results.multi_handedness, self.results.multi_hand_landmarks):
                my_hand = {}
                my_landmarks_list = []
                x_list = []
                y_list = []
                for id, landmark in enumerate(hand_landmarks.landmark):
                    px, py, pz = int(landmark.x * width), int(landmark.y * height), int(landmark.z * width)
                    my_landmarks_list.append([px, py, pz])
                    x_list.append(px)
                    y_list.append(py)
                
                x_min, x_max = min(x_list), max(x_list)
                y_min, y_max = min(y_list), max(y_list)
                box_width, box_height = x_max - x_min, y_max - y_min
                bbox = x_min, y_min, box_width, box_height
                center_x, center_y = bbox[0] + (bbox[2] // 2), bbox[1] + (bbox[3] // 2)

                my_hand["landmarks_list"] = my_landmarks_list
                my_hand["bbox"] = bbox
                my_hand["center"] = (center_x, center_y)

                if flip_image:
                    if hand_type.classification[0].label == "Right":
                        my_hand["type"] = "Left"
                    else:
                        my_hand["type"] = "Right"
                else:
                    my_hand["type"] = hand_type.classification[0].label
                all_hands.append(my_hand)

                if enable_draw:
                    self.mp_draw.draw_landmarks(image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                    cv2.rectangle(image, (bbox[0] - 20, bbox[1] - 20), (bbox[0] + bbox[2] + 20, bbox[1] + bbox[3] + 20),
                                  (255, 0, 255), 2)
                    cv2.putText(image, my_hand["type"], (bbox[0] - 30, bbox[1] - 30), cv2.FONT_HERSHEY_PLAIN,
                                2, (255, 0, 255), 2)

        return all_hands, image

    # Function to count fingers up based on hand landmarks.
    def count_fingers_up(self, my_hand):
        fingers = []
        my_hand_type = my_hand["type"]
        my_landmarks_list = my_hand["landmarks_list"]
        if self.results.multi_hand_landmarks:
            if my_hand_type == "Right":
                fingers.append(1) if my_landmarks_list[self.tip_ids[0]][0] > my_landmarks_list[self.tip_ids[0] - 1][0] else fingers.append(0)
            else:
                fingers.append(1) if my_landmarks_list[self.tip_ids[0]][0] < my_landmarks_list[self.tip_ids[0] - 1][0] else fingers.append(0)

            for id in range(1, 5):
                fingers.append(1) if my_landmarks_list[self.tip_ids[id]][1] < my_landmarks_list[self.tip_ids[id] - 2][1] else fingers.append(0)
        return fingers
    
    # Function to find distance between two points and visualize on the image.
    def find_distance(self, point1, point2, image=None, color=(255, 0, 255), scale=5):
        x1, y1 = point1
        x2, y2 = point2
        center_x, center_y = (x1 + x2) // 2, (y1 + y2) // 2
        length = math.hypot(x2 - x1, y2 - y1)
        info = (x1, y1, x2, y2, center_x, center_y)
        if image is not None:
            cv2.circle(image, (x1, y1), scale, color, cv2.FILLED)
            cv2.circle(image, (x2, y2), scale, color, cv2.FILLED)
            cv2.line(image, (x1, y1), (x2, y2), color, max(1, scale // 3))
            cv2.circle(image, (center_x, center_y), scale, color, cv2.FILLED)
        return length, info, image

def main():
    cap = cv2.VideoCapture(0) # Initialize video capture and HandDetector.
    detector = HandDetector(use_static_mode=False, max_num_hands=2, model_complexity=1, detection_confidence=0.5, tracking_confidence=0.5)

    while True:
        success, img = cap.read() # Read video frames.
        hands, img = detector.find_hands(img, enable_draw=True, flip_image=True) # Find hands and draw landmarks on the image.

        if hands:
            hand1 = hands[0] # Extract hand information for the first hand.
            lm_list1 = hand1["landmarks_list"]
            fingers1 = detector.fingers_up(hand1)

            length, info, img = detector.find_distance(lm_list1[8][0:2], lm_list1[12][0:2], img, color=(255, 0, 255), scale=10) # Find distance between specific landmarks on the first hand.

            if len(hands) == 2:
                hand2 = hands[1]
                lm_list2 = hand2["landmarks_list"]
                fingers2 = detector.fingers_up(hand2)
                length, info, img = detector.find_distance(lm_list1[8][0:2], lm_list2[8][0:2], img, color=(255, 0, 0), scale=10)

        cv2.imshow("Image", img) # Display the processed image
        cv2.waitKey(1)

if __name__ == "__main__":
    main()
