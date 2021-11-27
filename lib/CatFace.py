import xml.etree.ElementTree as et


class CatFace:
    def __init__(self, filename, feat_str):
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
        x_values = [int(x) for x in features[1::2]]
        y_values = [int(x) for x in features[2::2]]
        left = min(x_values)
        right = max(x_values)
        top = min(y_values)
        bottom = max(y_values)
        self.box = {'top': top, 'left': left,
                    "width": right - left, "height": bottom-top}

    def GenerateXML(self):
        image = et.Element("image")
        image.set('file', self.file)
        box = et.SubElement(image, "box")
        for key, val in self.box.items():
            box.set(key, "%s" % val)
        for key, val in self.features.items():
            part = et.SubElement(box, "part")
            part.set('name', key)
            part.set('x', val[0])
            part.set('y', val[1])
        # et.dump(image)
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
