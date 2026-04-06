import cv2
import numpy as np

def text_to_binary(text):
    return ''.join(format(ord(i), '08b') for i in text)

def binary_to_text(binary):
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join(chr(int(c, 2)) for c in chars)

def embed_data(image_path, data, output_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray, 100, 200)

    binary_data = text_to_binary(data) + '1111111111111110'
    data_index = 0

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if data_index >= len(binary_data):
                break

            pixel = image[i, j]

            if edges[i, j] > 0:
                for k in range(3):
                    if data_index < len(binary_data):
                        pixel[k] = int(format(pixel[k], '08b')[:-1] + binary_data[data_index], 2)
                        data_index += 1
            else:
                if data_index < len(binary_data):
                    pixel[0] = int(format(pixel[0], '08b')[:-1] + binary_data[data_index], 2)
                    data_index += 1

            image[i, j] = pixel

    cv2.imwrite(output_path, image)

def extract_data(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)

    binary_data = ""

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            pixel = image[i, j]

            if edges[i, j] > 0:
                for k in range(3):
                    binary_data += format(pixel[k], '08b')[-1]
            else:
                binary_data += format(pixel[0], '08b')[-1]

    end_marker = '1111111111111110'
    data = binary_data.split(end_marker)[0]

    return binary_to_text(data)
