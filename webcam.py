import cv2
import redis

class WebCam:

    def __init__(self):
        self.redis = RedisClient()

    def start(self):
        wcam = cv2.VideoCapture(0)

        while (True) :
            ret, frame = wcam.read()

            _, buffer = cv2.imencode('.jpg', frame)

            buffer = buffer.tostring()

            if buffer is not None :
                self.redis.sendImg(buffer)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        wcam.release()
        cv2.destroyAllWindows()


class RedisClient:

    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379 , db=0)

    def sendImg(self,  img):

        self.r.set('image', img)

    def getImg(self):

        return self.r.get("image")
