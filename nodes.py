import os
import json

import folder_paths
import numpy as np

from comfy.cli_args import args

from PIL import Image, ImageOps, ImageSequence
from PIL.PngImagePlugin import PngInfo

# ComfyUI/nodes.py/SaveImage

class NothingHappened:
  def __init__(self):
    self.output_dir = folder_paths.get_output_directory()
    self.type = "output"
    self.prefix_append = ""
    self.compress_level = 4

  @classmethod
  def INPUT_TYPES(s):
    return {
      "required": {
        "images": ("IMAGE", {"tooltip": "The images to save."}),
        "filename_prefix": ("STRING", {"default": "ComfyUI", "tooltip": "The prefix for the file to save. This may include formatting information such as %date:yyyy-MM-dd% or %Empty Latent Image.width% to include values from nodes."}),
        "prompt": ("STRING", {"placeholder": "prompt", "multiline": True,}),
        "workflow": ("STRING", {"placeholder": "workflow", "multiline": True,}),
      },
      "hidden": {
        # "prompt": "PROMPT", 
        "extra_pnginfo": "EXTRA_PNGINFO"
      },
    }

  RETURN_TYPES = ()
  FUNCTION = "save_images"

  OUTPUT_NODE = True

  CATEGORY = "image"
  DESCRIPTION = "Saves the input images to your ComfyUI output directory."

  def save_images(self, images, filename_prefix="ComfyUI", prompt = None, workflow = None, extra_pnginfo = None, ):
    filename_prefix += self.prefix_append
    full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(filename_prefix, self.output_dir, images[0].shape[1], images[0].shape[0])
    results = list()
    for (batch_number, image) in enumerate(images):
      i = 255. * image.cpu().numpy()
      img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))

      metadata = None
      if not args.disable_metadata:
        metadata = PngInfo()

        if prompt is not None:
          metadata.add_text("prompt", prompt)

        if extra_pnginfo is not None:
          for x in extra_pnginfo:
            metadata.add_text(x, json.dumps(extra_pnginfo[x]))

        if workflow is not None:
          metadata.add_text("workflow", workflow)

      filename_with_batch_num = filename.replace("%batch_num%", str(batch_number))
      file = f"{filename_with_batch_num}_{counter:05}_.png"
      img.save(os.path.join(full_output_folder, file), pnginfo=metadata, compress_level=self.compress_level)
      results.append({
        "filename": file,
        "subfolder": subfolder,
        "type": self.type
      })
      counter += 1

    return { "ui": { "images": results } }