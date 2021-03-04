# create_data_lists.py VOC 리스트 툴 # 제거 
# detect.py, image_to_video 시각화 툴 # 제거 고려 중

# eval_coco.py COCO_Tool을 이용한 평가 방법 : 심플하게 한다면 제거 할 것
# eval_for_matlab.py : 메인 평가. 트레인을 공개하지 않는다면 해당 방법만 사용해서 평가 고려 중. -> 추후 eval.py로 수정 할 것.
# eval.py : printing만 하는 평가 코드 <-util.py의 calculate_mAP를 이용한 평가 방법. 심플하게 한다면 제거 할 것

# model.py : main, torchcv 사용 x


# train_eval.py : main2,  torchcv -> datasets, utils, evaluation 사용함.

# utils.py : torchcv 사용 x




# Multi-Label-Pedestrian-Detection Backup

This code is based on [a-PyTorch-Tutorial-to-Object-Detection](https://github.com/sgrvinod/a-PyTorch-Tutorial-to-Object-Detection). 


### Paper : [Paper](./MLPD/MLPD.pdf)
### Latex : [Latex](./MLPD/MLPD_Latex_Image_X.zip)
### Cover Letter : [Cover Letter](./MLPD/Cover_letter.pdf)


### Installation

#### Git clone

```
git clone https://github.com/sejong-rcv/MLPD-Multi-Label-Pedestrian-Detection.git
cd Multi-Lable-Pedestrian-Detection/docker
```

#### Build docker 

```
make docker-make
```

#### Make Contianer (example)

```
nvidia-docker run -it --name mlpd -p 8810:8810 -w /home/jwkim/workspace -v /home/jwkim/workspace:/home/jwkim/workspace -v /data/:/raid -e NVIDIA_VISIBLE_DEVICES=ALL --shm-size=32G mlpd /bin/bash
```

### Dataset

For Multispectral pedestrian detection, we train and test our model on [Multispectral Pedestrian Detection: Benchmark Dataset and Baselines](https://github.com/SoonminHwang/rgbt-ped-detection), you should firstly download the dataset. By default, we assume the dataset is stored in `./data/kaist-rgbt`. Please see details below

``` 
<DATA_PATH>

+-- data
|   +-- kaist-rgbt
|   |   +-- kaist_annotations_test20.json
|   |   +-- annotations-xml-15
|   |   |   +-- set00
|   |   |   |   +-- V000
|   |   |   |   |   +-- I00000.xml
|   |   +-- images
|   |   |   +-- set00
|   |   |   |   +-- V000
|   |   |   |   |   +-- lwir
|   |   |   |   |   |   +-- I00000.jpg
|   |   |   |   |   +-- visible
|   |   |   |   |   |   +-- I00000.jpg
|   |   +-- imageSets
|   |   |   +-- train-all-02.txt
|   |   |   +-- test-all-20.txt

```


### Citation

```
@INPROCEEDINGS{ACCV2020,
  author = {JIWON KIM*, HYEONGJUN KIM*, TAEJOO KIM*, NAMIL KIM, AND YUKYUNG CHOI*},
  title = {Multi-Label-Pedestrian-Detection},
  booktitle = {-},
  year = {2021}
}
```
