from PIL import Image
from app.feature_extractor import FeatureExtractor
from pathlib import Path
import numpy as np

def renu():
    fe = FeatureExtractor()

    for img_path in sorted(Path("./media/img").glob("*.jpg")):
        print(img_path)  # e.g., ./static/img/xxx.jpg
        feature = fe.extract(img=Image.open(img_path))
        feature_path = Path("./media/feature") / (img_path.stem + ".npy")  # e.g., ./static/feature/xxx.npy
        np.save(feature_path, feature)

# if __name__ == '__main__':
#     fe = FeatureExtractor()

#     for img_path in sorted(Path("./static/img").glob("*.jpg")):
#         print(img_path)  # e.g., ./static/img/xxx.jpg
#         feature = fe.extract(img=Image.open(img_path))
#         feature_path = Path("./app/static/feature") / (img_path.stem + ".npy")  # e.g., ./static/feature/xxx.npy
#         np.save(feature_path, feature)
