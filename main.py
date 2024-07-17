from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
import cv2
from image_recognizer import ImageRecognizer
from api_client import ApiClient

class CameraApp(App):
    def build(self):
        """
        Build the Kivy application layout.
        - Creates the main layout and image widget.
        - Sets the initial background color.
        - Initializes the camera and auxiliary classes.
        - Starts the process by taking the first picture.
        """
        self.img = Image()
        self.layout = BoxLayout(orientation='vertical')
        self.layout.add_widget(self.img)
        self.set_background_color(0, 1, 0, 1)  # Initial background color: green
        self.layout.bind(size=self.update_rect, pos=self.update_rect)
        self.capture = cv2.VideoCapture(0)  # Initialize camera
        self.image_recognizer = ImageRecognizer()  # Initialize ImageRecognizer
        self.api_client = ApiClient(base_url="https://poliskoll.se/fordon/")  # Initialize ApiClient with the base URL
        Clock.schedule_once(self.take_picture)  # Schedule first picture
        return self.layout

    def update_rect(self, instance, value):
        """
        Update the rectangle position and size.
        - Keeps the background rectangle in sync with the layout.
        """
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def take_picture(self, dt):
        """
        Capture a picture from the camera and process it.
        - Captures the current frame from the camera.
        - Updates the image widget with the captured frame.
        - Processes the image to detect text.
        - Updates the background color based on the API check result.
        - Schedules the next picture after a delay.
        """
        ret, frame = self.capture.read()  # Capture frame
        if ret:
            self.img.texture = self.frame_to_texture(frame)  # Update image widget
            registration_number = self.image_recognizer.recognize_text(frame)  # Recognize text
            if registration_number:
                is_police_vehicle = self.api_client.check_registration_number(registration_number)  # Check API
                if is_police_vehicle is True:
                    self.set_background_color(1, 0, 0, 1)  # Set background to green
                elif is_police_vehicle is False:
                    self.set_background_color(0, 1, 0, 1)  # Set background to red
                else:
                    self.set_background_color(0, 1, 0, 1)  # Set background to yellow for unknown results
        Clock.schedule_once(self.take_picture, 1)  # Schedule next picture

    def frame_to_texture(self, frame):
        """
        Convert a camera frame to a Kivy texture.
        - Flips the frame vertically and converts it to a texture.
        """
        buf = cv2.flip(frame, 0).tostring()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        return texture

    def set_background_color(self, r, g, b, a):
        """
        Set the background color of the layout.
        - Draws a rectangle with the specified color.
        """
        with self.layout.canvas.before:
            Color(r, g, b, a)
            self.rect = Rectangle(size=self.layout.size, pos=self.layout.pos)

    def on_stop(self):
        """
        Release the camera when the app is closed.
        """
        self.capture.release()

if __name__ == '__main__':
    CameraApp().run()
