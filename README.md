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
<img src="https://github.com/skdltn210/Human-3D-AR-Interaction/assets/101277197/4ece3eaa-320f-4463-9ddf-fdcaeebed641" align="center" width="18%">
<img src="https://github.com/skdltn210/Human-3D-AR-Interaction/assets/101277197/df21214f-ca3a-49d9-926a-81d09e95c082" align="center" width="18%">
<img src="https://github.com/skdltn210/Human-3D-AR-Interaction/assets/101277197/2422d58b-b588-4f8c-868c-81d957fcb856" align="center" width="18%">
<img src="https://github.com/skdltn210/Human-3D-AR-Interaction/assets/101277197/8e31a440-e433-47df-b305-f76f96b40569" align="center" width="18%">
<img src="https://github.com/skdltn210/Human-3D-AR-Interaction/assets/101277197/7fd7e9cb-203b-4378-872b-6c950d89ddfd" align="center" width="18%">
</p>

This is the result of applying the masks to faces.

<p align="center">
<img src="https://github.com/skdltn210/Human-3D-AR-Interaction/assets/101277197/44d20bfa-91a8-4fd0-b6c2-35c9dd3bd587" align="center" width="18%">
<img src="https://github.com/skdltn210/Human-3D-AR-Interaction/assets/101277197/49d8069e-4d8e-4f6a-8c61-01a8fac8ef8b" align="center" width="18%">
</p>

### Style Transfer
I have utilized models within TensorFlow to transform the background style of a video.

The following images were chosen as the styles to be applied:

<p align="center">
<img src="https://github.com/skdltn210/Human-3D-AR-Interaction/assets/101277197/5c660015-0956-42ab-932f-a69b6f766217" align="center" width="18%">
<img src="https://github.com/skdltn210/Human-3D-AR-Interaction/assets/101277197/a3ef4bca-ac46-4ca5-ac23-42b89aa2f6dd" align="center" width="18%">
<img src="https://github.com/skdltn210/Human-3D-AR-Interaction/assets/101277197/39c5c5ad-0986-44ff-9a6d-b9b770b0ff03" align="center" width="18%">
<img src="https://github.com/skdltn210/Human-3D-AR-Interaction/assets/101277197/766fc3b4-1a4c-43ef-bf41-1ac34a84c98d" align="center" width="18%">
<img src="https://github.com/skdltn210/Human-3D-AR-Interaction/assets/101277197/c1e3fdba-7dc1-4b73-92fa-01a1f2691021" align="center" width="18%">
</p>
Here is the video with the applied style transfer:

- ![movie](https://github.com/skdltn210/Human-3D-AR-Interaction/assets/101277197/27797d86-980a-4f85-9693-deea228b2445)



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


