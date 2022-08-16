import wget
import os 
import boto3
import cv2
from mtcnn import MTCNN
from botocore.exceptions import ClientError
link = 'https://videotofotos.s3.us-west-2.amazonaws.com/registrationVideo/example1.mp4'
empId = 'e1'
tempName = 'tmp.mp4'
tempFolderName = 'tmp'
wget.download(link,'./'+tempName)



# Playing video from file:
cap = cv2.VideoCapture(tempName)
frms = cap.get(cv2.CAP_PROP_FRAME_COUNT)
#print(frames)
fps = cap.get(cv2.CAP_PROP_FPS)
#print(type(fps))
time = round(frms/fps)
os.mkdir(tempFolderName)
detector = MTCNN()

currentFrame = 0
while(currentFrame<=frms):
#while(300):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Saves image of the current frame in jpg file
    name = './'+tempFolderName+'/' + str(empId) + str(currentFrame) + '.jpg'
    faces = detector.detect_faces(frame)
    print ('Creating...' + name)
    if faces != []:
        for person in faces:
            bounding_box = person['box']
            if person['confidence']>0.98:
                cv2.rectangle(frame,(bounding_box[0],bounding_box[1]), (bounding_box[0]+bounding_box[2],bounding_box[1]+bounding_box[3]),(255,0,0),2)
                frames = cv2.resize(frame[bounding_box[1]:bounding_box[1]+bounding_box[3],bounding_box[0]:bounding_box[0]+bounding_box[2]],(256,256))
                cv2.imwrite(name, frames)

    # To stop duplicate images
    #currentFrame += (time//4)
    currentFrame += 5

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()





s3_client = boto3.client('s3', region_name='us-east-2', aws_access_key_id = 'AKIAQVWCUMEC62WL74BI',
                        aws_secret_access_key = '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')
folder_name = empId
s3_client.put_object(Bucket='videotofotos', Key=('datasets/'+empId+'/'), )


def upload_my_file(bucket, folder, file_to_upload, file_name):
    key = folder+"/"+file_name
    try:
        response = s3_client.upload_file(file_to_upload, bucket, key)
    except ClientError as e:
        print(e)
        return False
    except FileNotFoundError as e:
        print(e)
        return False
    return True

#Upload file
for i in os.listdir('./'+tempFolderName):
    upload_my_file("videotofotos", "datasets/"+empId, "./"+tempFolderName+"/"+str(i), str(i)) 