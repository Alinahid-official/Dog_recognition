#from asyncio.windows_events import NULL
from io import BytesIO
from django.shortcuts import render
from numpy import imag
import numpy as np
import os
from PIL import Image
from .feature_extractor import FeatureExtractor
from datetime import datetime
from pathlib import Path
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from .models import Dog
from .serializers import TaskSerializer
from django.conf import settings
from offline import renu
# renu()

# fe = FeatureExtractor()
# for img_path in sorted(Path("./static/img").glob("*.jpg")):
#     print(img_path)  # e.g., ./static/img/xxx.jpg
#     feature = fe.extract(img=Image.open(img_path))
#     print(feature)
#     feature_path = Path(settings.STATIC_ROOT+"\\feature\\"+img_path.stem + ".npy")  # e.g., ./static/feature/xxx.npy
#     print(feature_path)
#     np.save(feature_path, feature)

fe = FeatureExtractor()
features = []
img_paths = []
fp=os.path.join(settings.MEDIA_ROOT,'feature')
# ip=os.path.join(settings.STATIC_ROOT,'img')
for feature_path in Path(fp).glob("*.npy"):
    features.append(np.load(feature_path))
    img_paths.append(Path("./media/img") / (feature_path.stem + ".jpg"))
features = np.array(features)


def handle_uploaded_file(f): 
    print(f.name) 
    with open('dog/static/img/'+f.name, 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk) 

# Create your views here.
@api_view(['GET', 'POST'])
def petList(req):
    if req.method =='POST':
        query=req.POST.items()
        query=dict(query)
        query.pop('csrfmiddlewaretoken')
        print(query)
        if(query['age']==  '' and query['breed']=='' and query['size']==''):
            dogs=Dog.objects.all()
        elif(query['age']!=  '' and query['breed']=='' and query['size']==''):
            print('age')
            dogs=Dog.objects.filter(age=query['age'])
        elif(query['age']==  '' and query['breed']!='' and query['size']==''):
            dogs=Dog.objects.filter(breed=query['breed'])
        elif(query['age']==  '' and query['breed']=='' and query['size']!=''):
            dogs=Dog.objects.filter(size=query['size'])
        elif(query['age']!= '' and query['breed']!='' and query['size']==''):
            dogs=Dog.objects.filter(age=query['age'],breed=query['breed'])
        elif(query['age']!=  '' and query['breed']=='' and query['size']!=''):
            dogs=Dog.objects.filter(size=query['size'],age=query['age'])
        elif(query['age']==  '' and query['breed']=='' and query['size']!=''):
            dogs=Dog.objects.filter(size=query['size'],breed=query['breed'])
        else:
            dogs=Dog.objects.filter(size=query['size'],breed=query['breed'],age=query['age'])

        print(dogs)
        return render(req,'list.html',{'dogs':dogs})
    # pet_list=Dog.objects.all()
    return render(req, 'petList.html')
    # serializer = TaskSerializer(pet_list,many=True)
    # return Response(serializer.data)

# @api_view(['GET', 'POST'])
def uploadPet(req):
    if req.method == 'POST':
        breed=req.POST['breed']
        size=req.POST['size']
        age=req.POST['age']
        img=req.FILES['dog_pic']

        Dog(breed=breed,size=size,age=age,image=img).save()
        # handle_uploaded_file(img) 
        
        renu()
        return render(req,'uploadPet.html')

    return render(req, 'uploadPet.html')


def index(request):
    if request.method == 'POST':
        file = request.FILES['query_img']
        
        # Save query image
        img = Image.open(file)  # PIL image
        # uploaded_img_path = settings.STATIC_ROOT +  "\\uploaded\\" + datetime.now().isoformat().replace(":", ".") + "_" + file.name
        # print(uploaded_img_path)
        # i_io = BytesIO()
        # file.save(i_io,uploaded_img_path)

        # Run search
        query = fe.extract(img)
        dists = np.linalg.norm(features-query, axis=1)  # L2 distances to features
        ids = np.argsort(dists)[:10]  # Top 30 results
        # scores = [(dists[id], img_paths[id]) for id in ids ]
        scores=[]
        for id in ids:
            if(dists[id]<1):
                scores.append([dists[id],img_paths[id]])

        print(scores)
        return render(request,'index.html',{'scores':scores})
                               
    else:
        return render(request,'index.html')

