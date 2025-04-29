"""
@author: shinich39
@title: comfyui-nothing-happened
@nickname: comfyui-nothing-happened
@version: 1.0.0
@description: Save image and keep metadata.
"""

from .nodes import NothingHappened

NODE_CLASS_MAPPINGS = {
  "NothingHappened": NothingHappened,
}

NODE_DISPLAY_NAME_MAPPINGS = {
  "NothingHappened": "Nothing Happened",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]