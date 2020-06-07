import boto3
import os.path as path

def detect_text(photo, bucket):

    client=boto3.client('rekognition')
    Arreglo_Texto = []

    with open(photo, 'rb') as image:
        response=client.detect_text(Image={'Bytes': image.read()})
                        
    textDetections=response['TextDetections']
    print ('Detected text\n----------')
    for text in textDetections:
            print ('Detected text:' + text['DetectedText'])
            if(text['Type'] == "WORD"):
                Arreglo_Texto.append(text['DetectedText'])
            print ('Confidence: ' + "{:.2f}".format(text['Confidence']) + "%")
            print ('Id: {}'.format(text['Id']))
            if 'ParentId' in text:
                print ('Parent Id: {}'.format(text['ParentId']))
            print ('Type:' + text['Type'])
            print()
    return Arreglo_Texto

def main():

    bucket='bucket'
    ImagenDeControl='Control.png'

    while(True):
        print("Ingrese el nombre de la imagen que quiere comparar con la Imagen de Control (alguna imagen dentro de la misma carpeta):")
        ImagenDePrueba = input()
        if(path.exists(ImagenDePrueba)):
            break
        else:
            print("No existe ese archivo, ingrese nuevamente.")

    TextoDeControl = detect_text(ImagenDeControl,bucket)
    TextoDePrueba = detect_text(ImagenDePrueba,bucket)
    
    for i in range(len(TextoDeControl)):
        TextoDeControl[i] = TextoDeControl[i].lower()

    for i in range(len(TextoDePrueba)):
        TextoDePrueba[i] = TextoDePrueba[i].lower()

    print(TextoDeControl)
    print(TextoDePrueba)

    if(TextoDeControl == TextoDePrueba):
        return True


if __name__ == "__main__":
    main()