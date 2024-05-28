import argparse

import librosa
import librosa.display
import matplotlib.pyplot as plt
import dlib
import cv2

def face_detection():
    """
    """
    cap = cv2.VideoCapture('path_to_your_video.mp4')
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        # Dibujar rectángulos alrededor de los rostros detectados
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Muestra el frame resultante
        cv2.imshow('Frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def face_features():
    """
    """
    # Cargar el detector de rostros y el predictor de puntos faciales
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("path_to_shape_predictor_68_face_landmarks.dat")

    # Suponiendo que 'frame' es un frame del vídeo que ya ha sido cargado y convertido a escala de grises
    faces = detector(frame)
    for face in faces:
        landmarks = predictor(frame, face)

def audio_features():
    """
    """
    # Cargar archivo de audio
    y, sr = librosa.load('output_audio.mp3')

    # Extraer MFCCs
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)

    # Visualizar MFCCs
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(mfccs, x_axis='time')
    plt.colorbar()
    plt.title('MFCC')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract features from preprocessed data.")
    parser.add_argument("-icsv", "--input_csv", required=True, help="CSV with raw data.")
    parser.add_argument("-ocsv", "--output_csv", required=True, help="Output where to save csv with features.")
    parser.add_argument("-d","--processed_data", default = '..\data\processed')

    args = parser.parse_args()
    _input = args.input_csv
    _output = args.output_csv
    _data_path = args.processed_data

    


    