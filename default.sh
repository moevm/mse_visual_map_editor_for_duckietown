# before u need: docker build -t map .
docker run -it  --net="host"  -v /tmp/.X11-unix:/tmp/.X11-unix  -e DISPLAY=$DISPLAY  -u qtuser  map python3 /main.py