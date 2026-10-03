import cv2 as cv

class Object_Counter:
    window_name = 'Image'

    def __init__(self, path):
        self.image = cv.imread(path)
        if self.image is None:
            raise FileNotFoundError(path)
        self.hsv = cv.cvtColor(self.image, cv.COLOR_BGR2HSV)
        self.copy = self.image.copy()

    def on_clicking(self, event, x, y, *_):
        if event != cv.EVENT_LBUTTONDOWN:
            return
        h = int(self.hsv[y, x, 0])
        output = cv.inRange(self.hsv, (max(h - 10, 0), 50, 50), (min(h + 10, 179), 255, 255))
        contours, _ = cv.findContours(output, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        contours = [c for c in contours if cv.contourArea(c) > 100]
        self.copy = self.image.copy()
        for c in contours:
            bx, by, bw, bh = cv.boundingRect(c)
            cv.rectangle(self.copy, (bx, by), (bx + bw, by + bh), (0, 0, 0), 2)
        cv.putText(self.copy, f"Count: {len(contours)}", (10, 25),
                   cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
        print(f"Number of objects detected: {len(contours)}")

    def run(self):
        cv.namedWindow(self.window_name)
        cv.setMouseCallback(self.window_name, self.on_clicking)
        while cv.waitKey(30) != ord('q'):
            cv.imshow(self.window_name, self.copy)
        cv.destroyAllWindows()

if __name__ == "__main__":
    Object_Counter('img4.jpg').run()