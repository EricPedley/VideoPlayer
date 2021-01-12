import cv2, numpy as np
import sys
from time import sleep,time

def flick(x):
    pass

cv2.namedWindow('image')
cv2.moveWindow('image',250,150)
cv2.namedWindow('controls')
cv2.moveWindow('controls',250,50)

controls = np.zeros((50,750),np.uint8)
cv2.putText(controls, "W/w: Play, S/s: Stay, A/a: Prev, D/d: Next, E/e: Fast, Q/q: Slow, Esc: Exit", (40,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)

video = sys.argv[1] 
cap = cv2.VideoCapture(video)

tots = cap.get(cv2.CAP_PROP_FRAME_COUNT)
i = 0
cv2.createTrackbar('S','image', 0,int(tots)-1, flick)
cv2.setTrackbarPos('S','image',0)

cv2.createTrackbar('F','image', 1, 100, flick)
frame_rate = 30
cv2.setTrackbarPos('F','image',frame_rate)

def process(im):
    return cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

status = 'stay'
prev_time=time()
while True:
  cv2.imshow("controls",controls)
  try:
    if i==tots-1:
      i=0
    cap.set(cv2.CAP_PROP_POS_FRAMES, i)
    ret, im = cap.read()
    r = 750.0 / im.shape[1]
    dim = (750, int(im.shape[0] * r))
    im = cv2.resize(im, dim, interpolation = cv2.INTER_AREA)
    if im.shape[0]>600:
        im = cv2.resize(im, (500,500))
        controls = cv2.resize(controls, (im.shape[1],25))
    #cv2.putText(im, status, )
    cv2.imshow('image', im)
    status = { ord('s'):'stay', ord('S'):'stay',
                ord('w'):'play', ord('W'):'play',
                ord('a'):'prev_frame', ord('A'):'prev_frame',
                ord('d'):'next_frame', ord('D'):'next_frame',
                ord('q'):'slow', ord('Q'):'slow',
                ord('e'):'fast', ord('E'):'fast',
                ord('c'):'snap', ord('C'):'snap',
                -1: status, 
                27: 'exit'}[cv2.waitKey(1)]

    if status == 'play':
      now=time()
      delta=now-prev_time
      print(delta)
      prev_time=now
      frame_rate = cv2.getTrackbarPos('F','image')
      if frame_rate<1:
          status='stay'
          continue
      diff = max(1,int(delta*frame_rate))#this fixes the video playing too slowly
      if diff==1:
          sleep(max(0,1/frame_rate-delta))#1/frame_rate is how long the frame should take, and delta is the time already spent, so it should sleep the remaining amount of time for the frame to avoid playing too fast
      i+=diff
      cv2.setTrackbarPos('S','image',i)
      continue
    elif status == 'stay':
      i = cv2.getTrackbarPos('S','image')
    elif status == 'exit':
        break
    elif status=='prev_frame':
        i-=1
        cv2.setTrackbarPos('S','image',i)
        status='stay'
    elif status=='next_frame':
        i+=1
        cv2.setTrackbarPos('S','image',i)
        status='stay'
    elif status=='slow':
        frame_rate = max(frame_rate - 5, 0)
        cv2.setTrackbarPos('F', 'image', frame_rate)
        status='play'
    elif status=='fast':
        frame_rate = min(100,frame_rate+5)
        cv2.setTrackbarPos('F', 'image', frame_rate)
        status='play'
    elif status=='snap':
        cv2.imwrite("./"+"Snap_"+str(i)+".jpg",im)
        print("Snap of Frame",i,"Taken!")
        status='stay'

  except KeyError:
      print("Invalid Key was pressed")
cv2.destroyWindow('image')
