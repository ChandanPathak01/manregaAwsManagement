modelPath = 'face_rec_model.h5'

def predict_image(image_path):
    from mtcnn import MTCNN
    from keras.models import load_model
    import cv2
    import numpy as np

    classes = []
    present_employees_id = []
    detector = MTCNN()
    model = load_model(modelPath)
    img = cv2.imread(image_path)
    faces = detector.detect_faces(img)
    if faces!= []:
        for j in faces:
            if j['confidence'] > 0.98:
                bounding_box = j['box']
                img_ = img[bounding_box[1]:bounding_box[1]+bounding_box[3],bounding_box[0]:bounding_box[0]+bounding_box[2]]
                x = cv2.resize(img_,(256,256))
    #img = image.load_img(image_path, target_size=(256,256,3))
    #plt.imshow(img)
    #plt.show()
                x = img_/255
    #print(x)
                x = np.expand_dims(x, axis=0)
    #images = np.vstack([x])
                pred = model.predict(x, batch_size=32)
                if pred[0][np.argmax(pred)] >= 0.75:
                    present_employees_id += classes[np.argmax(pred)]
    return present_employees_id