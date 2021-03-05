
# 수정중
## transforms.py pair=None 다 떼어 낼 것.
- pair가 필요한 trasforms.. -> args.upaired_augmentation에서 정의함.
  - TT_RandomHorizontalFlip
  - TT_FixedHorizontalFlip
  - TT_RandomResizedCrop
  - config.py로 정리 완료함.
- ~~train에서 사용하는 transfoms 함수에 모두 pair 인자가 적용된 상태~~
  - args.upaired_augmentation 에 필요한 인자에만 적용되도록 변경.
- SynthFail -> FusionDeadZone으로 변경하여 구성 및 원복 실험 예정.
  - Blackout_{R, T}
  - SidesBlackout_{R, T}
  - SurroundingBlackout_{R, T}

## model.py 
 - 모델 파라미터도 config로 꺼내?
 - 모델 구조 Modulelist로 변환??? 

## utils.py : torchcv 사용 x

## 추가로 할 작업.
- 필요없는 torchcv 코드 정리.

# 수정 완료.
## train_eval.py
- 수정 완료.

## eval.py
- ~~3가지 eval 중 무엇으로 할지 선정할 것!~~
  - COCO tool 기반의 evaluate_coco, Matlab 기반의 evaluate_matlab으로 구성함.
- 코드 정리는 완료.
- 논문 성능 7.58, 성능 원복이 가능한 checkpoint를 구해야할 듯. (MR 7.75????, checkpoint_ssd300.pth.tar024) 

## dataset.py
- transform : pair, ARCNN - train 종속 제거
- Paired annotation : train 단일로 변경 완료.
- test: santized??? original???
- 글로벌 변수 정리 완료.




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
