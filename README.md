# 수정중


## model.py 
 - 모델 파라미터도 config로 꺼내?
 - 모델 구조 Modulelist로 변환??? 
 - vis
  - conv1-1 3 64 Batch
  - conv1-2 64 64 Batch Max

  - conv2-1 64 128 Batch
  - conv2-2 128 128 Batch Max

  - conv3-1 128 256 Batch
  - conv3-2 256 256 Batch Max

  - conv4-1 256 512 Batch
  - conv4-2 512 512 Batch
  - conv4-3 512 512 Batch

 - lwir
  - conv1-1 1 64 Batch
  - conv1-2 64 64 Batch Max

  - conv2-1 64 128 Batch
  - conv2-2 128 128 Batch Max

  - conv3-1 128 256 Batch
  - conv3-2 256 256 Batch Max

  - conv4-1 256 512 Batch
  - conv4-2 512 512 Batch
  - conv4-3 512 512 Batch

## transforms.py pair=None 다 떼어 낼 것.
- SynthFail -> FusionDeadZone으로 변경하여 구성 및 원복 실험 중.
  - 논문에 기재된 체크포인트 좀 주세요.
  - Blackout
  - SidesBlackout_{R, L} R:right cutoff L:left cutoff
  - SurroundingBlackout

  |         | 논문 MR | 측정 MR |
  |--------|--|--|
  |Original| 7.58  | 7.75 |
  |Blackout_R| 16.34 | 17.83 |
  |Blackout_T| 25.60 | 26.28 |
  |streo_A| 21.56 | 27.62 |
  |Streo_B| 15.40 | 23.06 |
  |EOIR| 16.40 | 19.13 |

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

## utils
- 필요한 파일과 함수만 선별하여 utils dir에 넣어둠.
- transforms.py
 - pair가 필요한 trasforms.. -> args.upaired_augmentation에서 정의함.
  - TT_RandomHorizontalFlip
  - TT_FixedHorizontalFlip
  - TT_RandomResizedCrop
  - config.py로 정리 완료함.
  - ~~train에서 사용하는 transfoms 함수에 모두 pair 인자가 적용된 상태~~
    - args.upaired_augmentation 에 필요한 인자에만 적용되도록 변경.

## 수정된 파일 구조
```
.
├── README.md
├── docker
│   ├── Dockerfile
│   ├── Makefile
│   └── requirements.txt
└── src
    ├── config.py
    ├── datasets -> /raid/datasets/
    ├── datasets.py
    ├── eval.py
    ├── jobs
    │   └── checkpoint_ssd300.pth.tar024
    ├── model.py
    ├── result
    │   ├── COCO_TEST_det_all.jpg
    │   └── COCO_TEST_det_all.json
    ├── train_eval.py
    └── utils
        ├── __init__.py
        ├── coco.py
        ├── eval_MR_multisetup.py
        ├── functional.py
        ├── trace_error.py
        ├── transforms.py
        └── utils.py
```

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
