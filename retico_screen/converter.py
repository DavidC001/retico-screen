from retico_vision.vision import ImageIU, DetectedObjectsIU
from retico_core.abstract import AbstractModule
import retico_core

from PIL import Image, ImageDraw

class Convert_DetectedObjectsIU_ImageIU(AbstractModule):
    """
    A module that converts DetectedObjectsIU to ImageIU for display.
    """
    @staticmethod
    def name():
        return "Convert_DetectedObjectsIU_ImageIU"
    
    @staticmethod
    def description():
        return "Converts DetectedObjectsIU to ImageIU for display."
    
    @staticmethod
    def input_ius():
        return [DetectedObjectsIU]
    
    @staticmethod
    def output_iu():
        return ImageIU
    
    def __init__(self, num_obj_to_display=1):
        super().__init__()
        self.num_obj_to_display = num_obj_to_display
        
    def process_update(self, update_message):
        for iu, ut in update_message:
            if ut != retico_core.UpdateType.ADD:
                continue
            elif isinstance(iu, DetectedObjectsIU):
                # Convert DetectedObjectsIU to ImageIU and draw bounding boxes
                image : Image = iu.image
                
                output_iu = self.create_iu(iu)
                
                obj_type = iu.object_type
                num_objs = min(self.num_obj_to_display, iu.num_objects)
                
                if obj_type == 'bb':
                    valid_boxes = iu.payload
                    for i in range(num_objs):
                        box = valid_boxes[i]
                        if box is not None:
                            x1, y1, x2, y2 = box
                            # Draw bounding box on the image
                            img_draw = ImageDraw.Draw(image)
                            img_draw.rectangle([x1, y1, x2, y2], outline='red', width=2)
                            # put a label on the box
                            img_draw.text((x1, y1), f'Object {i+1}', fill='red')
                elif obj_type == 'seg':
                    valid_segs = iu.payload
                    for i in range(num_objs):
                        seg_mask = valid_segs[i]
                        # seg_mask is expected to be a binary mask
                        if seg_mask is not None:
                            # Convert the mask to a PIL Image and apply it to the original with transparency
                            seg_mask_image = Image.fromarray(seg_mask.astype('uint8') * 255)
                            # blend the mask with the original image
                            image = Image.composite(image, Image.new('RGB', image.size, (255, 0, 0)), seg_mask_image)
                            # put a label on the image
                            img_draw = ImageDraw.Draw(image)
                            img_draw.text((10, 10 + i * 20), f'Segmented Object {i+1}', fill='red')
                else: 
                    print('Object type is invalid. Can\'t retrieve segmented object.')
                    exit()
                    
                output_iu.image = image
                um = retico_core.UpdateMessage.from_iu(output_iu, retico_core.UpdateType.ADD) 
                self.append(um)
                
            