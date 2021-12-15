import xml.etree.ElementTree as et
import numpy as np
from dlib import rectangle


class CatFace:
    """ 
    creates an object that holds the landmark and bounding box data for a cat face in 
    the image that filename points to
    """

    def __init__(self, filename, feat_str, bb_str):
        features = feat_str.split()
        num_features = features[0]
        self.file = filename
        self.features = {
            "LEFT_EYE": (features[1], features[2]),
            "RIGHT_EYE": (features[3], features[4]),
            "MOUTH": (features[5], features[6]),
            "LEFT_OF_LEFT_EAR": (features[7], features[8]),
            "TIP_OF_LEFT_EAR": (features[9], features[10]),
            "RIGHT_OF_LEFT_EAR": (features[11], features[12]),
            "LEFT_OF_RIGHT_EAR": (features[13], features[14]),
            "TIP_OF_RIGHT_EAR": (features[15], features[16]),
            "RIGHT_OF_RIGTH_EAR": (features[17], features[18]),
        }
        bb = bb_str.split()
        features = np.array(features).astype(int)[1:].reshape((-1, 2))
        bb = np.array([np.min(features, axis=0),
                      np.max(features, axis=0)]).flatten()
        # print(bb.flatten())
        width = int(bb[2]) - int(bb[0])
        height = int(bb[3]) - int(bb[1])
        sqr_dim = max(width, height)
        self.box = {
            'left': bb[0],
            'top': bb[1],
            # TODO: check that width and height are not supposed to just be left and bottom
            'width': sqr_dim,  # left-right
            'height': sqr_dim,  # bottom-top
        }
        self.rect = [rectangle(left=bb[0], top=bb[1],
                               right=bb[0]+sqr_dim, bottom=bb[1]+sqr_dim)]

    def GenerateXML(self):
        """Creates the XML annotation fo this face in the format for dlib"""
        image = et.Element("image")
        image.set('file', self.file)
        box = et.SubElement(image, "box")
        for key, val in self.box.items():
            box.set(key, "%s" % val)

        landmarks = ["LEFT_EYE", "RIGHT_EYE", "MOUTH", "LEFT_OF_LEFT_EAR", "TIP_OF_LEFT_EAR",
                     "RIGHT_OF_LEFT_EAR", "LEFT_OF_RIGHT_EAR", "TIP_OF_RIGHT_EAR", "RIGHT_OF_RIGTH_EAR"]

        for landmark in landmarks:
            point = self.features[landmark]
            part = et.SubElement(box, "part")
            part.set('name', landmark)
            part.set('x', point[0])
            part.set('y', point[1])

        return image


def main():
    dataset = et.Element("dataset")
    root = et.ElementTree(dataset)
    name = et.SubElement(dataset, "name")
    name.text = "imglab dataset"
    comment = et.SubElement(dataset, "comment")
    comment.text = "Created by imglab tool."
    images = et.SubElement(dataset, "images")
    face = CatFace(
        "example.jpg", "9 175 160 239 162 199 199 149 121 137 78 166 93 281 101 312 96 296 133")
    image = face.GenerateXML()
    images.append(face.GenerateXML())
    et.indent(dataset)
    et.dump(dataset)
    # dataset.write("hello", encoding="utf-8")
    # print(et.tostring(images, pretty_print=True).decode())


if __name__ == "__main__":
    main()
