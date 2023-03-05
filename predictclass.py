import torch
from model import resnet34, resnet101
from torchvision import transforms
import json

# read class_indict
try:
    json_file = open('./class_indices.json', 'r')
    class_indict = json.load(json_file)
    print('class_indict:{}'.format(class_indict))
    print('class_indict:{}type'.format(type(class_indict)))
except Exception as e:
    print(e)
    exit(-1)
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

data_transform = transforms.Compose(
    [transforms.Resize(256),
     transforms.CenterCrop(224),
     transforms.ToTensor(),
     transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])
# create model
model = resnet101(num_classes=25)
# load model weights
model_weight_path = "./resNet101.pth"
model.load_state_dict(torch.load(model_weight_path, map_location=device))
model.eval()


def predict(img):
    with torch.no_grad():
        # [N, C, H, W]
        img = data_transform(img)
        # expand batch dimension
        img = torch.unsqueeze(img, dim=0)
        # predict class
        output = torch.squeeze(model(img))
        predictResult = torch.softmax(output, dim=0)
        predict_cla = torch.argmax(predictResult).numpy()
        # print('type(predict_cla):{}'.format(type(predict_cla)))
        # print('predict_cla:{}'.format(predict_cla))
        # print(class_indict[str(predict_cla)], predictResult[predict_cla].numpy())
        return class_indict[str(predict_cla)], str(predictResult[predict_cla].numpy())
