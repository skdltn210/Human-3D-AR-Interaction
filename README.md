# Human-3D-AR-Interaction

## About Projects

In traditional platforms like Instagram, filters simply add assets to the background or have basic effects like petals floating. In this project, however, we apply 3D models to the face using AR and apply style transfer to the background, enabling more advanced interactions.

## Contents

* public : free 3d model examples from [sketchfab](https://sketchfab.com/)
* styles : example images of style transfers that match 3D models
* 1.html : client-side part that displays the AR-applied face on the web
* server.py : server-side part that applies style transfer and sends the processed video to the client

## Getting Started 

You need 2 terminals, and run the following in each terminal respectively.
> server
  ```
  python server.py
  ```

> client
  ```
  npm install --global http-server
  cd ..
  http-server 
  find 1.html and run
  ```

## Features

## How This Works

Both the client and the server are using the same webcam to capture video. When a rotating 3D model is clicked on the client side, it gets applied over the face in the browser, and the corresponding index of that model is sent to the server. The server captures the video with the applied 3D model and applies style transfer to the video corresponding to that index. Then, it sends the processed video back to the client. The client places the received video underneath the 3D model.

## Components

### 3D Models

Face recognition is used to apply these 3D models as masks on faces.

<p align="center">
  <img src="./images/5" align="center" width="50%">
  <img src="./images/6" align="center" width="50%">
  <img src="./images/10" align="center" width="18%">
  <img src="./images/11" align="center" width="18%">
  <img src="./images/12" align="center" width="18%">
</p>

This is the result of applying the masks to faces.

<p align="center">
  <img src="./images/8" align="center" width="18%">
  <img src="./images/9" align="center" width="18%">
</p>


### Style Transfer
I have utilized models within TensorFlow to transform the background style of a video.

The following images were chosen as the styles to be applied:

<p align="center">
  <img src="./images/0" align="center" width="18%">
  <img src="./images/1" align="center" width="18%">
  <img src="./images/2" align="center" width="18%">
  <img src="./images/3" align="center" width="18%">
  <img src="./images/4" align="center" width="18%">
</p>

Here is the video with the applied style transfer:

- `./images/7`




## Limitations

For now, this project only works on Mac. I attempted to try it on a Windows environment with a better GPU. However, unlike on Mac, Windows didn't allow me to use one webcam across multiple applications. So, I tried to solve this by using a virtual webcam or implementing [WebRTC](https://webrtc.org/), or by having the server process and transmit the video without using the webcam on the client side. However, due to time constraints, I couldn't finish it.

## Future Enhancements

With a more powerful GPU and more realistic models and images, this could be practically usable. This technology could also be applied to body parts and joints, making it useful for virtual reality games.

## License

MIT. see License.txt for more information.

## Dependences

server
* written in [Python3](https://www.python.org/)
* [OpenCV](https://opencv.org/) for process video
* [FastAPI](https://fastapi.tiangolo.com/) for video transmission
* [Tensorflow](https://tensorflow.org/) for style-transfer

client
* [MindAR](https://hiukim.github.io/mind-ar-js-doc/) and [Aframe](https://aframe.io/) for AR interaction
* [ThreeJS](https://threejs.org/) for rotating 3D models

## References

* [MindAR](https://hiukim.github.io/mind-ar-js-doc/)


