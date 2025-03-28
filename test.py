# # import tensorflow as tf

# # # Check if TensorFlow is using the GPU
# # print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))


# import torch

# # Check if CUDA is available
# print("Is CUDA available: ", torch.cuda.is_available())

# # If CUDA is available, you can also check the current device
# if torch.cuda.is_available():
#     print("Current CUDA device: ", torch.cuda.current_device())
#     print("Current CUDA device name: ", torch.cuda.get_device_name(torch.cuda.current_device()))