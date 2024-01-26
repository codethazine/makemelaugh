mkdir pretrainedModels

# Download pretrained model to detect smile
curl -o pretrainedModels/haarcascade_smile.xml https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_smile.xml

# Download pretrained model to detect face
curl -o pretrainedModels/haarcascade_face.xml https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml
