import sys, os, pdb, time, json, importlib

from tqdm import tqdm

import torch
import numpy as np
from PIL import Image

### Model
from model import SSD300, MultiBoxLoss

### Dataset
from datasets import KAISTPed, LoadBox

### Evaluation
from eval import *

from utils.utils import *

args = importlib.import_module('config').args

# random seed fix 
set_seed(seed=9)


def main():
    """
    Training and validation.
    """
    global epochs_since_improvement, start_epoch, label_map, best_loss, epoch

    train_conf = args.train
    checkpoint = train_conf.checkpoint
    start_epoch = train_conf.start_epoch
    epochs_since_improvement = train_conf.epochs_since_improvement
    best_loss = train_conf.best_loss
    epochs = train_conf.epochs

    # Initialize model or load checkpoint
    if checkpoint is None:
        model = SSD300(n_classes=args.n_classes)
        # Initialize the optimizer, with twice the default learning rate for biases, as in the original Caffe repo
        biases = list()
        not_biases = list()
        for param_name, param in model.named_parameters():
            if param.requires_grad:
                if param_name.endswith('.bias'):
                    biases.append(param)
                else:
                    not_biases.append(param)
        optimizer = torch.optim.SGD(params=[{'params': biases, \
                                            'lr': 2 * train_conf.lr},
                                            {'params': not_biases}],
                                            lr=train_conf.lr,
                                            momentum=train_conf.momentum,
                                            weight_decay=train_conf.weight_decay,
                                            nesterov=False)

        optim_scheduler = torch.optim.lr_scheduler.MultiStepLR(optimizer, milestones=[ int(epochs*0.5), int(epochs*0.9)], gamma=0.1)

    else:
        checkpoint = torch.load(checkpoint)
        start_epoch = checkpoint['epoch'] + 1
        train_loss = checkpoint['loss']
        print('\nLoaded checkpoint from epoch %d. Best loss so far is %.3f.\n' % (start_epoch, train_loss))
        model = checkpoint['model']
        optimizer = checkpoint['optimizer']
        optim_scheduler = torch.optim.lr_scheduler.MultiStepLR(optimizer, milestones=[ int(epochs*0.5)], gamma=0.1)

    # Move to default device
    model = model.to(args.device)
    criterion = MultiBoxLoss(priors_cxcy=model.priors_cxcy).to(args.device)

    train_dataset = KAISTPed(args, condition='train')
        
    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=train_conf.batch_size, shuffle=True,
                                               num_workers=args.dataset.workers,
                                               collate_fn=train_dataset.collate_fn, 
                                               pin_memory=True)  # note that we're passing the collate function here

    test_dataset = KAISTPed(args, condition='test')

    test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=args["test"].eval_batch_size, shuffle=False,
                                               num_workers=args.dataset.workers,
                                               collate_fn=test_dataset.collate_fn, 
                                               pin_memory=True)    
    #############################################################################################################################
    
    ### Set job directory
    if args.exp_time is None:
        from datetime import datetime
        args.exp_time        = datetime.now().strftime('%Y-%m-%d_%Hh%Mm')
    
    exp_name        = ('_' + args.exp_name) if args.exp_name else '_' 
    jobs_dir        = os.path.join( 'jobs', args.exp_time + exp_name )
    args.jobs_dir   = jobs_dir

    if not os.path.exists(jobs_dir):        os.makedirs(jobs_dir)

    ### Make logger
    logger = make_logger(args)

    # Epochs
    for epoch in range(start_epoch, epochs):
        # Paper describes decaying the learning rate at the 80000th, 100000th, 120000th 'iteration', i.e. model update or batch
        # The paper uses a batch size of 32, which means there were about 517 iterations in an epoch
        # Therefore, to find the epochs to decay at, you could do,
        # if epoch in {80000 // 517, 100000 // 517, 120000 // 517}:
        #     adjust_learning_rate(optimizer, 0.1)

        # In practice, I just decayed the learning rate when loss stopped improving for long periods,
        # and I would resume from the last best checkpoint with the new learning rate,
        # since there's no point in resuming at the most recent and significantly worse checkpoint.
        # So, when you're ready to decay the learning rate, just set checkpoint = 'BEST_checkpoint_ssd300.pth.tar' above
        # and have adjust_learning_rate(optimizer, 0.1) BEFORE this 'for' loop

        # One epoch's training
        train_loss = train(args=args,
                           train_loader=train_loader,
                           model=model,
                           criterion=criterion,
                           optimizer=optimizer,
                           epoch=epoch,
                           logger=logger)

        optim_scheduler.step()
        
        # Save checkpoint
        save_checkpoint(epoch, model, optimizer, train_loss, jobs_dir)
        
        if epoch >= 3 :
            rstFile = os.path.join(jobs_dir, './COCO_TEST_det_{:d}.json'.format(epoch)) 
            
            evaluate_coco(test_loader, model, rstFile=rstFile)
        

def train(args, train_loader, model, criterion, optimizer, epoch, logger):
    """
    One epoch's training.

    :param train_loader: DataLoader for training data
    :param model: model
    :param criterion: MultiBox loss
    :param optimizer: optimizer
    :param epoch: epoch number
    """
    model.train()  # training mode enables dropout

    batch_time = AverageMeter()  # forward prop. + back prop. time
    data_time = AverageMeter()  # data loading time
    losses = AverageMeter()  # loss_sum
    losses_loc = AverageMeter()  # loss_loc
    losses_cls = AverageMeter()  # loss_cls

    start = time.time()
    
    # Batches
    for batch_idx, (image_vis, image_lwir, boxes, labels, _) in enumerate(train_loader):

        data_time.update(time.time() - start)

        # Move to default device
        image_vis = image_vis.to(args.device) 
        image_lwir = image_lwir.to(args.device) 

        boxes = [b.to(args.device) for b in boxes]
        labels = [l.to(args.device) for l in labels]

        # Forward prop.
        predicted_locs, predicted_scores = model(image_vis, image_lwir)  # (N, 8732, 4), (N, 8732, n_classes)

        # Loss
        loss,cls_loss,loc_loss,n_positives = criterion(predicted_locs, predicted_scores, boxes, labels)  # scalar

        # Backward prop.
        optimizer.zero_grad()
        loss.backward()

        if np.isnan(loss.item()):
            import pdb; pdb.set_trace()
            loss,cls_loss,loc_loss = criterion(predicted_locs, predicted_scores, boxes, labels)  # scalar

        # Clip gradients, if necessary
        if args["train"].grad_clip is not None:
            clip_gradient(optimizer, args["train"].grad_clip)

        # Update model
        optimizer.step()

        # losses.update(loss.item(), images.size(0))
        losses.update(loss.item())
        losses_loc.update(loc_loss)
        losses_cls.update(cls_loss)
        batch_time.update(time.time() - start)

        start = time.time()

               # Print status
        if batch_idx % args["train"].print_freq == 0:

            logger.info('Epoch: [{0}][{1}/{2}]\t'
                  'Batch Time {batch_time.val:.3f} ({batch_time.avg:.3f})\t'
                  'Data Time {data_time.val:.3f} ({data_time.avg:.3f})\t'
                  'Loss {loss.val:.4f} ({loss.avg:.4f})\t'
                  'num of Positive {Positive}\t'.format(epoch, batch_idx, len(train_loader),
                                                                  batch_time=batch_time,
                                                                  data_time=data_time, loss=losses, Positive=n_positives))

    del predicted_locs, predicted_scores, image_vis, image_lwir, boxes, labels  # free some memory since their histories may be stored

    return  losses.avg

if __name__ == '__main__':

    main()
