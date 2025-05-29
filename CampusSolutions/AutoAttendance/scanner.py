# AutoAttendance/scanner.py
import face_recognition
import cv2
import numpy as np
import os
import datetime
import logging
import threading
import time
from .models import RegisteredFace, Attendance
from Home.models import Students, subjects, sections

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('attendance_scanner.log'),
        logging.StreamHandler()
    ]
)

class FaceAttendanceScanner:
    def __init__(self):
        self.running = False
        self.video = None
        self.scan_thread = None

    def load_known_faces(self):
        known_encodings = []
        student_map = {}
        
        os.makedirs("face_encodings", exist_ok=True)
        
        for face in RegisteredFace.objects.all().select_related('user'):
            encoding_path = f"face_encodings/{face.roll_number}.npy"
            if os.path.exists(encoding_path):
                try:
                    encoding = np.load(encoding_path)
                    if encoding.size == 128:
                        encoding = encoding.reshape(128,)  # Ensure 1D
                        known_encodings.append(encoding)
                        student_map[len(known_encodings) - 1] = face
                        logging.info(f"Loaded encoding for {face.roll_number}")
                except Exception as e:
                    logging.error(f"Error loading encoding for {face.roll_number}: {str(e)}")
        
        if known_encodings:
            known_encodings = np.array(known_encodings)  # Ensure it's a 2D NumPy array

        return known_encodings, student_map
    


    def scan_faces(self, subject_id, section_id):
        today = datetime.date.today()
        known_encodings, student_map = self.load_known_faces()
        recognized_ids_today = set()

        if not known_encodings.any():
            logging.error("No valid face encodings found")
            return {"marked": 0, "skipped": 0}

        # Initialize camera
        for i in range(3):
            self.video = cv2.VideoCapture(i)
            if self.video.isOpened():
                logging.info(f"Camera opened at index {i}")
                break
        else:
            logging.error("Could not open any camera")
            return {"marked": 0, "skipped": len(student_map)}

        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        self.running = True
        last_cleanup = time.time()

        try:
            while self.running:
                ret, frame = self.video.read()
                if not ret:
                    logging.warning("Failed to capture frame")
                    time.sleep(0.1)
                    continue

                # Periodic cleanup
                if time.time() - last_cleanup > 30:
                    recognized_ids_today = set()
                    last_cleanup = time.time()

                # Resize & convert color
                small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
                rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

                face_locations = face_recognition.face_locations(
                    rgb_frame, model="hog", number_of_times_to_upsample=1
                )

                if face_locations:
                    try:
                        encodings = face_recognition.face_encodings(
                            rgb_frame, face_locations, num_jitters=1, model="small"
                        )

                        for encoding, (top, right, bottom, left) in zip(encodings, face_locations):
                            top, right, bottom, left = [x*2 for x in (top, right, bottom, left)]

                            face_distances = face_recognition.face_distance(
                                known_encodings, encoding
                            )
                            best_match_index = np.argmin(face_distances)

                            if face_distances[best_match_index] < 0.6:
                                face = student_map.get(best_match_index)
                                if face and face.student_id not in recognized_ids_today:
                                    self.mark_attendance(
                                        face.student_id, subject_id, section_id, today
                                    )
                                    recognized_ids_today.add(face.student_id)
                                    logging.info(f"Marked attendance for {face.roll_number}")

                                    # ✅ Draw box and name
                                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                                    display_text = f"{face.roll_number} - Marked"
                                    cv2.putText(
                                        frame,
                                        display_text,
                                        (left, top - 10),
                                        cv2.FONT_HERSHEY_SIMPLEX,
                                        0.8,
                                        (0, 255, 0),
                                        2,
                                        cv2.LINE_AA
                                    )

                    except Exception as e:
                        logging.error(f"Face processing error: {str(e)}")

                cv2.imshow("Attendance Scanner - Press q to quit", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

        except Exception as e:
            logging.error(f"Scanner error: {str(e)}")
        finally:
            self.cleanup()
        
        return {
            "marked": len(recognized_ids_today),
            "skipped": len(student_map) - len(recognized_ids_today),
        }





    def mark_attendance(self, student_id, subject_id, section_id, date):
        try:
            student = Students.objects.get(id=student_id)
            subj = subjects.objects.get(id=subject_id)
            sect = sections.objects.get(id=section_id)

            if not Attendance.objects.filter(
                student=student, subject=subj, section=sect, date=date
            ).exists():
                Attendance.objects.create(
                    student=student,
                    subject=subj,
                    section=sect,
                    status="Present",
                    date=date,
                )
        except Exception as e:
            logging.error(f"Attendance marking error: {str(e)}")

    def cleanup(self):
        self.running = False
        if self.video and self.video.isOpened():
            self.video.release()
        cv2.destroyAllWindows()

def run_face_attendance(subject_id, section_id):
    scanner = FaceAttendanceScanner()
    try:
        return scanner.scan_faces(subject_id, section_id)
    except Exception as e:
        logging.error(f"Fatal scanner error: {str(e)}")
        return {"marked": 0, "skipped": 0}
    finally:
        scanner.cleanup()
