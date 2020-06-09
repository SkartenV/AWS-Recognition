import boto3
import os.path as path

def detect_text(photo, bucket):

    client = boto3.client('rekognition')

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
    NumCasoPrueba = 1

    while(True):

        print("\n -------------- Menu --------------")
        print("| 1 - Ingresar una imagen de prueba |")
        print("| 2 - Salir                         |")
        print(" ----------------------------------\n")

        print("Ingrese una opcion: ")
        opcion = input()

        if(opcion == '2'):
            break

        if(opcion == '1'):

            while(True):
                print("Ingrese el nombre de la imagen que quiere comparar con la Imagen de Control (alguna imagen dentro del bucket):")
                ImagenDePrueba = input()
                if(path.exists(ImagenDePrueba)):
                    break
                else:
                    print("No existe ese archivo, ingrese nuevamente.")

            TextoDeControl = detect_text(ImagenDeControl,bucket)
            TextoDePrueba = detect_text(ImagenDePrueba,bucket)

            Archivo_logs.write("Caso de prueba " + str(NumCasoPrueba) + ":\n\n")
            NumCasoPrueba += 1

            if(TextoDePrueba == False):
                Archivo_logs.write("Valor retornado: False. Una o mas palabras no superaron la probabilidad de reconocimiento (97%).\n")
                Archivo_logs.write("\n---------------------------------------------------------------------------------------------------------------\n\n")
            
            else:
                for i in range(len(TextoDeControl)):
                    TextoDeControl[i] = TextoDeControl[i].lower()

                for i in range(len(TextoDePrueba)):
                    TextoDePrueba[i] = TextoDePrueba[i].lower()

                Archivo_logs.write("Nombre imagen de control: \"" + ImagenDeControl + "\" - Palabras encontradas: " + str(TextoDeControl) + "\n")
                Archivo_logs.write("Nombre imagen de prueba: \"" + ImagenDePrueba + "\" - Palabras encontradas: " + str(TextoDePrueba) + "\n\n")

                if(set(TextoDeControl).issubset(set(TextoDePrueba))):
                    Archivo_logs.write("Valor retornado: True. Se encontraron las palabras de la imagen de control dentro de la imagen de prueba.")
                    Archivo_logs.write("\n\n---------------------------------------------------------------------------------------------------------------\n\n")
                
                else:
                    Archivo_logs.write("Valor retornado: False. No se encontraron las palabras de la imagen de control dentro de la imagen de prueba.")
                    Archivo_logs.write("\n\n---------------------------------------------------------------------------------------------------------------\n\n")

        else:
            print("\nOpcion invalida, seleccione nuevamente")

    Archivo_logs.close()

if __name__ == "__main__":
    main()