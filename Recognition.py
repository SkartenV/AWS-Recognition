import boto3
import os.path as path

def detect_text(photo, bucket):

    client = boto3.client(
        'rekognition',
        aws_access_key_id = "ASIAZD5Z3NSCMLQHS26T",
        aws_secret_access_key = "F8AjmZwdUXtpQ3cO9sjspjSwbNdOGxcL5dSBSvwL",
        aws_session_token = "FwoGZXIvYXdzEJ7//////////wEaDKm85UX0Y7ZwCNxclCLNAf8uOWoe96SOIsECoGBqcSOUtiY91bwXdn0uJMzG2HFxGC7pNfm9xYRfuKxAeW1+PQTmQXooM6Yo8leho/TAIzjoMHuCLNO/iflin4RTPPYE8cV143fT+gwAPD7qmfHqNzrUXous+8TLWnXarTBX/z2+fNxjJb+pCI57FC//pyKjXF3jjVzwEgGL4ig51yo/En74UVfeg2Ep+pDCBlrPi5PlVU4vCK74PHKgy7F1V3JHfUBbDgC1RtxNUA0GROuf7DW4R5yJx05SV8TTp6AosLX69gUyLcOJQIV6Nl9YVo2n/woBDcJaZYzwya0m7lMY/pwpIaFtXJIjNVUhW8fSnbpzSw=="
    )

    Arreglo_Texto = []

    response=client.detect_text(Image={'S3Object':{'Bucket':bucket,'Name':photo}})
                        
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

        if(text['Type'] == "WORD" and float("{:.2f}".format(text['Confidence'])) >= 97.00):
            Arreglo_Texto.append(text['DetectedText'])
        elif(text['Type'] == "WORD" and float("{:.2f}".format(text['Confidence'])) < 97.00):
            return False

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

    if(TextoDePrueba == False):
        Archivo_logs.write("Valor retornado: False. Una o mas palabras no superaron la probabilidad de reconocimiento (97%).")
        Archivo_logs.close()
        print("False")
        return False
    
    for i in range(len(TextoDeControl)):
        TextoDeControl[i] = TextoDeControl[i].lower()

    for i in range(len(TextoDePrueba)):
        TextoDePrueba[i] = TextoDePrueba[i].lower()

    Archivo_logs.write("Nombre imagen de control: \"" + ImagenDeControl + "\" - Palabras encontradas: " + str(TextoDeControl) + "\n")
    Archivo_logs.write("Nombre imagen de prueba: \"" + ImagenDePrueba + "\" - Palabras encontradas: " + str(TextoDePrueba) + "\n\n")

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