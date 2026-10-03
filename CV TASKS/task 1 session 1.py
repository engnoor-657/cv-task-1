import numpy as np
import cv2 as cv
from datetime import datetime


class MiniPainter:
    window_name = 'Mini Painter'
    radius = 30
    shape_size = 50  # half-size of the rectangle / triangle
    colors = {
        "1": ("Red", (0, 0, 255)),
        "2": ("Green", (0, 255, 0)),
        "3": ("Blue", (255, 0, 0)),
        "4": ("Yellow", (0, 255, 255)),
        "5": ("Magenta", (255, 0, 255)),
    }
    modes = {
        "c": "circle",
        "r": "rectangle",
        "p": "polygon",
    }

    def __init__(self):
        self.canvas = np.full((500, 500, 3), 255, dtype=np.uint8)
        self.color_name, self.color = self.colors["1"]
        self.mode = "circle"

    def on_mouse(self, event, x, y, flags, param):
        if event != cv.EVENT_LBUTTONDOWN:
            return

        s = self.shape_size
        if self.mode == "circle":
            cv.circle(self.canvas, (x, y), self.radius, self.color, -1)
        elif self.mode == "rectangle":
            cv.rectangle(self.canvas, (x - s, y - s), (x + s, y + s), self.color, -1)
        else:  # polygon
            points = np.array([[x, y - s], [x - s, y + s], [x + s, y + s]], np.int32)
            cv.fillPoly(self.canvas, [points], self.color)

    def run(self):
        cv.namedWindow(self.window_name)
        cv.setMouseCallback(self.window_name, self.on_mouse)

        while True:
            display = self.canvas.copy()
            cv.putText(display, f"Mode: {self.mode}, Color: {self.color_name}", (10, 30),
                       cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
            cv.imshow(self.window_name, display)

            key = chr(cv.waitKey(1) & 0xFF).lower()
            if key == 'q':
                break
            elif key in self.colors:
                self.color_name, self.color = self.colors[key]
            elif key in self.modes:
                self.mode = self.modes[key]
            elif key == 'w':
                filename = f"canvas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                cv.imwrite(filename, self.canvas)
                print(f"Canvas saved as {filename}")

        cv.destroyAllWindows()


if __name__ == "__main__":
    MiniPainter().run()