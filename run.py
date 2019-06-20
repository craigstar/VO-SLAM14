from myslam import Config, VO
import sophus as sp


Config.setParameterFile('config/default.yaml')
# vo = VO()

dataset_dir = Config.get('dataset_dir')
print('dataset:', dataset_dir)

# with
