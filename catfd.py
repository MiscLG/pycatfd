#!/usr/bin/env python3

import argparse
import cv2
import glob
import os
from PIL import Image
from lib.CatFaceLandmark import *
from lib.Detector import Detector
from skimage import io
import dlib


def main():
    def formatter(prog): return argparse.HelpFormatter(prog,
                                                       max_help_position=36)
    desc = '''
    Detects cat faces and facial landmarks
    '''
    parser = argparse.ArgumentParser(description=desc,
                                     formatter_class=formatter)

    parser.add_argument('-i', '--input-image',
                        help='input image',
                        metavar='<file>')

    parser.add_argument('-f', '--input-folder',
                        help='input folder',
                        metavar='<path>')

    parser.add_argument('-o', '--output_path',
                        help='output location',
                        default='.',
                        metavar='<path>')

    parser.add_argument('-j', '--json',
                        help='output face and landmark information to JSON',
                        action='store_true')

    parser.add_argument('-c', '--save-chip',
                        help='save a cropped version of each detected cat face',
                        action='store_true')

    parser.add_argument('-a', '--annotate-faces',
                        help='draw a square around each detected cat face',
                        action='store_true')

    parser.add_argument('-l', '--annotate-landmarks',
                        help='''
                        draw lines between detected facial landmarks
                        ''',
                        action='store_true')

    parser.add_argument('-ac', '--face-color',
                        help='face square color',
                        type=int,
                        default=[25, 255, 100],
                        nargs=3)

    parser.add_argument('-lc', '--landmark-color',
                        help='facial landmark line color',
                        type=int,
                        default=[255, 50, 100],
                        nargs=3)

    args = vars(parser.parse_args())
    use_dlib = False

    if not args['input_image'] and not args['input_folder']:
        parser.error("must specify either -i or -f")

    if args['input_image']:
        if use_dlib:
            dlib_detect(args['input_image'])
        else:
            detect(args['input_image'],
                   args['output_path'],
                   args['json'],
                   args['annotate_faces'],
                   args['annotate_landmarks'],
                   args['face_color'],
                   args['landmark_color'],
                   args['save_chip'])

    if args['input_folder']:
        for f in glob.glob(os.path.join(args['input_folder'], '*.jp*g')):
            if use_dlib:
                dlib_detect(f)
            else:
                detect(f,
                       args['output_path'],
                       args['json'],
                       args['annotate_faces'],
                       args['annotate_landmarks'],
                       args['face_color'],
                       args['landmark_color'],
                       args['save_chip'])


def dlib_detect(filename):
    """Applies the detector on a given file and uses dlib to show the results"""
    print("Showing detections and predictions on the images in the faces folder...")
    win = dlib.image_window()
    print("Processing file: {}".format(filename))
    img = dlib.load_rgb_image(filename)

    win.clear_overlay()
    win.set_image(img)

    # Ask the detector to find the bounding boxes of each face. The 1 in the
    # second argument indicates that we should upsample the image 1 time. This
    # will make everything bigger and allow us to detect more faces.
    d = Detector(filename)
    d.detect()
    dets = d.result.face_count
    print("Number of faces detected: {}".format(dets))
    for k, face in enumerate(d.result.faces):
        print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
            k, face.left(), face.top(), face.right(), face.bottom()))
        # Get the landmarks/parts for the face in box d.
        shape = d.predictor(img, face)
        print("Part 0: {}, Part 1: {} ...".format(shape.part(0),
                                                  shape.part(1)))
        # Draw the face landmarks on the screen.
        win.add_overlay(shape)

    win.add_overlay(d.result.faces)
    dlib.hit_enter_to_continue()


def detect(input_image, output_path, use_json, annotate_faces,
           annotate_landmarks, face_color, landmark_color, save_chip):
    """
        Applies the detector on a given file and uses opencv to show the results
    """
    img = io.imread(input_image)
    d = Detector(input_image)
    d.detect()

    if use_json:
        json = []
    else:
        print(('\nImage: {}'.format(input_image)))
        print(('Number of cat faces detected: {}'.format(d.result.face_count)))

    if annotate_faces or annotate_landmarks:
        w = img.shape[1]

    for i, face in enumerate(d.result.faces):
        shape = d.predictor(img, face)

        if save_chip:
            cropped = Image.open(input_image)
            cropped = cropped.crop((face.left(),
                                    face.top(),
                                    face.right(),
                                    face.bottom()))

            chip_path = get_output_file(output_path,
                                        input_image,
                                        '_face_{}'.format(i),
                                        'jpg')
            cropped.save(chip_path)

        if annotate_landmarks:
            draw_landmark_annotation(img, shape, landmark_color, 1)
            #  int(w * 0.0025))

        if annotate_faces:
            draw_face_annotation(img, face, face_color, int(w * 0.005))

        if use_json:
            json.append(get_face_json(face, shape))
        else:
            print_face_info(i, face, shape)

    if d.result.face_count > 0:
        if annotate_faces or annotate_landmarks:
            filename = get_output_file(output_path,
                                       input_image,
                                       '_annotated',
                                       'jpg')

            cv2.imshow(filename, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
            cv2.waitKey()

    if use_json:
        print(json)


def get_output_file(output_path, input_image, extra, ext):
    """ Gets output filepath from input path """
    if not os.path.isdir(output_path):
        os.makedirs(output_path)

    basename = os.path.splitext(os.path.basename(input_image))[0]
    return os.path.join(output_path, basename + str(extra) + '.' + ext)


def print_face_info(i, face, shape):
    """ Prints the landmark and bounding box coordinates"""
    print(('Face #{}: ({}, {}), ({}, {})'.format(
        i,
        face.top(),
        face.left(),
        face.right(),
        face.bottom()
    )))

    for landmark in CatFaceLandmark.all():
        print(('   {}: ({}, {})'.format(
            landmark['name'],
            shape.part(landmark['value']).x,
            shape.part(landmark['value']).y
        )))


def get_face_json(face, shape):
    landmarks = {}
    for landmark in CatFaceLandmark.all():
        landmarks[landmark['name']] = [shape.part(landmark['value']).x,
                                       shape.part(landmark['value']).y]

    return {
        "face": {
            'left': face.left(),
            'top': face.top(),
            'right': face.right(),
            'bottom': face.bottom(),
            'height': face.bottom() - face.top(),
            'width': face.right() - face.left(),
            'landmarks': landmarks
        }
    }


def draw_face_annotation(img, face, color, width):
    """draws bounding box of face on given image"""
    cv2.rectangle(img,
                  (face.left(), face.top()),
                  (face.right(), face.bottom()),
                  color,
                  width)


def draw_landmark_annotation(img, shape, color, width):
    """ Draws face landmarks of given image"""
    lines = [
        [CatFaceLandmark.LEFT_EYE, CatFaceLandmark.RIGHT_EYE],
        [CatFaceLandmark.RIGHT_EYE, CatFaceLandmark.MOUTH],
        [CatFaceLandmark.MOUTH, CatFaceLandmark.LEFT_EYE],
        [CatFaceLandmark.MOUTH, CatFaceLandmark.LEFT_OF_LEFT_EAR],
        [CatFaceLandmark.LEFT_OF_LEFT_EAR, CatFaceLandmark.TIP_OF_LEFT_EAR],
        [CatFaceLandmark.TIP_OF_LEFT_EAR, CatFaceLandmark.RIGHT_OF_LEFT_EAR],
        [CatFaceLandmark.RIGHT_OF_LEFT_EAR, CatFaceLandmark.LEFT_OF_RIGHT_EAR],
        [CatFaceLandmark.LEFT_OF_RIGHT_EAR, CatFaceLandmark.TIP_OF_RIGHT_EAR],
        [CatFaceLandmark.TIP_OF_RIGHT_EAR, CatFaceLandmark.RIGHT_OF_RIGHT_EAR],
        [CatFaceLandmark.RIGHT_OF_RIGHT_EAR, CatFaceLandmark.MOUTH],
    ]

    for i in lines:
        draw_line(img, shape.part(i[0]), shape.part(i[1]), color, width)


def draw_line(img, shape1, shape2, color, width):
    """draws line connecting landmarks"""
    pt1 = (shape1.x, shape1.y)
    pt2 = (shape2.x, shape2.y)
    cv2.circle(img, pt1, radius=5, color=(0, 0, 255), thickness=-1)
    cv2.circle(img, pt2, radius=5, color=(0, 0, 255), thickness=-1)
    cv2.line(img, pt1, pt2, color, width, cv2.LINE_AA)


main()
