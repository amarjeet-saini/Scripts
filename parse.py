import sys
import os
import onnx
from tvm.contrib.download import download_testdata
from PIL import Image
import numpy as np
import tvm.relay as relay
import tvm
from tvm.contrib import graph_executor
from tvm.contrib import utils, graph_executor as runtime
from scipy.special import softmax

directory = "/home/nvidianx/data_clean"
engine_no = sys.argv[1]


# Downloading and Loading the ONNX Model

model_url = "".join(
    [
        "https://github.com/onnx/models/tree/",
        "master/vision/classification/squeezenet/model/",
        "squeezenet1.1-7.onnx", 
    ]
)

model_path = download_testdata(model_url, "squeezenet1.1-7.onnx", module="onnx")

onnx_model = onnx.load(model_path)


# Load engine file
tmp = "/home/nvidianx/TVM/tvm/engine"+str(engine_no)+"_cpu_opt_squeezenet.tar"
lib: tvm.runtime.Module = tvm.runtime.load_module(tmp)


# Create output globally so it only open once 
try:
    file = open("output"+str(engine_no)+".txt", "a+")
except:
    print("unable to open file")


labels_url = "https://s3.amazonaws.com/onnx-model-zoo/synset.txt"
labels_path = download_testdata(labels_url, "synset.txt", module="data")

with open(labels_path, "r") as f:
    labels = [l.rstrip() for l in f]


def model(img_path,engine_no):
    
    # Downloading, Preprocessing, and Loading the Test Image

    # write image path to output file
    
    path = img_path[img_path.find("/")+1:]
    path = path[path.find("n0"):path.find("-")]+ " "
       
    file.write(path)
    
    resized_image = Image.open(img_path).resize((224, 224))
   
    print(resized_image.mode)

    if(resized_image.mode != "RGB"):
        resized_image = resized_image.convert("RGB")
    
    img_data = np.asarray(resized_image).astype("float32")

    print(img_path,end = " ")
    print(img_data.shape)
    # Our input image is in HWC layout while ONNX expects CHW input, so convert the array
    
    img_data = np.transpose(img_data, (2, 0, 1))

    # Normalize according to the ImageNet input specification
    imagenet_mean = np.array([0.485, 0.456, 0.406]).reshape((3, 1, 1))
    imagenet_stddev = np.array([0.229, 0.224, 0.225]).reshape((3, 1, 1))
    norm_img_data = (img_data / 255 - imagenet_mean) / imagenet_stddev

    # Add the batch dimension, as we are expecting 4-dimensional input: NCHW.
    img_data = np.expand_dims(norm_img_data, axis=0)

    # Compile the Model With Relay

    target = "llvm"

  
    # .. admonition:: Defining the Correct Target

    input_name = "data"
    shape_dict = {input_name: img_data.shape}

    mod, params = relay.frontend.from_onnx(onnx_model, shape_dict)

    dev = tvm.device(str(target), 0)
    module = graph_executor.GraphModule(lib["default"](dev))


    # Execute on the TVM Runtime
    
    dtype = "float32"
    module.set_input(input_name, img_data)
    
    module.run()
    
    output_shape = (1, 1000)
    tvm_output = module.get_output(0, tvm.nd.empty(output_shape)).numpy()


    # Postprocess the output


    # from scipy.special import softmax

    # Download a list of labels
    # labels_url = "https://s3.amazonaws.com/onnx-model-zoo/synset.txt"
    # labels_path = download_testdata(labels_url, "synset.txt", module="data")

    # with open(labels_path, "r") as f:
    #     labels = [l.rstrip() for l in f]

    # Open the output and read the output tensor
    scores = softmax(tvm_output)
    scores = np.squeeze(scores)
    ranks = np.argsort(scores)[::-1]
    
    out = "%s"%(labels[ranks[0]])
    out = out[:out.find(" ")] + "\n" 
    file.write(out)
    
    print("complete")


def main():
    for root, dirs, files in os.walk(directory):
        for img in files:
            model(os.path.join(root,img), engine_no)
    
    print("*******************")
    print(f"completed for engine{engine_no}")
    print("*******************")
    file.close()


if __name__ == "__main__":
    main()