import boto3
import os.path as path

def detect_text(photo, bucket):

    client=boto3.client('rekognition')
    Arreglo_Texto = []

    response=client.detect_text(Image={'S3Object':{'Bucket':bucket,'Name':photo}})
                        
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

    Archivo_logs = open("logs.txt","w")
    bucket='bucketskartenv1'
    ImagenDeControl='Control.png'

    while(True):
        print("Ingrese el nombre de la imagen que quiere comparar con la Imagen de Control (alguna imagen dentro del bucket):")
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

    Archivo_logs.write("Nombre imagen: \"" + ImagenDeControl + "\" - Palabras encontradas: " + str(TextoDeControl) + "\n")
    Archivo_logs.write("Nombre imagen: \"" + ImagenDePrueba + "\" - Palabras encontradas: " + str(TextoDePrueba) + "\n\n")

    if(set(TextoDePrueba).issubset(set(TextoDeControl))):
        Archivo_logs.write("Valor retornado: True. Se encontraron las palabras de la imagen de prueba dentro de la imagen de control.")
        Archivo_logs.close()
        print("True")
        return True
    
    else:
        Archivo_logs.write("Valor retornado: False. No se encontraron las palabras de la imagen de prueba dentro de la imagen de control.")
        Archivo_logs.close()
        print("False")
        return False


if __name__ == "__main__":
    main()