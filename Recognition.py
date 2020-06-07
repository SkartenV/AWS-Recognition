


import boto3

def detect_text(photo, bucket):

    client=boto3.client('rekognition')

    with open(photo, 'rb') as image:
        response=client.detect_text(Image={'Bytes': image.read()})
                        
    textDetections=response['TextDetections']
    print ('Detected text\n----------')
    for text in textDetections:
            print ('Detected text:' + text['DetectedText'])
            print ('Confidence: ' + "{:.2f}".format(text['Confidence']) + "%")
            print ('Id: {}'.format(text['Id']))
            if 'ParentId' in text:
                print ('Parent Id: {}'.format(text['ParentId']))
            print ('Type:' + text['Type'])
            print()
    return len(textDetections)

def main():

    bucket='bucket'
    photo='Monday.png'
    text_count=detect_text(photo,bucket)
    print("Text detected: " + str(text_count))


if __name__ == "__main__":
    main()