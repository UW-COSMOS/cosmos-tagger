"""
File: xml_to_json.py
Author: Keshav Balaji
Description: Standalone Python script to parse an xml file of annotations and write
the data to a corresponding json file
"""

import os
import glob
import json
import xmltodict
import sys
from pydantic import BaseModel, Field
from typing import List
from numpy import arange

DEFAULT_REGION_TYPES = ["Figure", "Equation", "Table"]
# BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),'../..'))

class AnnotationBounds(BaseModel):
    page_num: int = Field(description="Page Number")
    postprocess_cls: str = Field(description="The label assigned to the region by Cosmos")
    postprocess_score: float = 0 # for internal use only
    bounding_box: List[int] = Field(description="Region bounds (x0, y0, x1, y1)")

    def area(self):
        """ Get the area of a bounding box"""
        (x0, y0, x1, y1) = self.bounding_box
        return (x1 - x0) * (y1 - y0)

    def intersection(self, other: 'AnnotationBounds'):
        """ Get the intersecting area of two rectangles """
        # via https://stackoverflow.com/a/27162334

        (my_x0, my_y0, my_x1, my_y1) = self.bounding_box
        (their_x0, their_y0, their_x1, their_y1) = other.bounding_box

        dx = min(my_x1, their_x1) - max(my_x0, their_x0)
        dy = min(my_y1, their_y1) - max(my_y0, their_y0)

        return dx * dy if dx > 0 and dy > 0 else 0


    def union(self, other: 'AnnotationBounds'):
        """ Get the union area of two rectangles """
        return self.area() + other.area() - self.intersection(other)


    def intersection_over_union(self, other: 'AnnotationBounds'):
        """ Get the intersection-over-union of two rectangles """
        return self.intersection(other) / self.union(other)

def parse_xml() -> list[AnnotationBounds]:
    annotations = []

    # for xml_path in glob.glob(annotations_path):
    with open(sys.argv[1]) as xml_data:
        xml_dict = xmltodict.parse(xml_data.read())
        page_num = int(xml_dict['annotation']['page'])
        objects = xml_dict['annotation']['object']
        annotations.extend(_cosmos_obj_from_manual_obj(page_num, obj) for obj in objects)

    return annotations, xml_data.name[:-4]

def _cosmos_obj_from_manual_obj(page_num, obj):
        """Convert the extracted XML of a manual annotation to use the same keys/data types as 
        those included in the cosmos parquet
        """
        bbox = obj['bndbox']
        bounds = [int(float(b)) 
            for b in [bbox['xmin'],bbox['ymin'],bbox['xmax'],bbox['ymax']]]
        
        return AnnotationBounds(
            page_num = page_num,
            postprocess_cls = obj['name'],
            bounding_box= bounds
        )

def create_json(xml_annotations, filename):
    with open(filename + '.json','w') as json_out:
        data = [a.dict() for a in xml_annotations]
        data.sort(key=lambda x: x['page_num'])
        json_out.write(json.dumps(data, indent=2))

annotations, filename = parse_xml()
create_json(annotations, filename)
