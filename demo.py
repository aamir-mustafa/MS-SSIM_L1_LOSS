import torch
from PIL import Image, ImageFilter
import numpy as np

from MS_SSIM_L1_loss import MS_SSIM_L1_LOSS

def pil2tensor(im):  # in: [PIL Image with 3 channels]. out: [B=1, C=3, H, W] (0, 1)
    return torch.Tensor((np.float32(im) / 255).transpose(2, 0 ,1)).unsqueeze(0)


if __name__ == '__main__':
    '''Test of this loss function'''
    # load image

    im = Image.open('lena.png')
    gt = pil2tensor(im).cuda(0)
    blur_levels = [3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31]
    noise_levels = [5, 10 ,20, 40, 80, 160]
    im1 = np.float32(im)
    imgs = []
    imgs2 = []

    for bl in blur_levels:
        imgs.append(im.filter(ImageFilter.GaussianBlur(radius = bl)))
    for nl in noise_levels:
        nr = np.float32(Image.effect_noise((512, 512), nl)) - 128
        ng = np.float32(Image.effect_noise((512, 512), nl)) - 128
        nb = np.float32(Image.effect_noise((512, 512), nl)) - 128
        noise = np.stack((nr, ng, nb), 2)
        imn = Image.fromarray(np.uint8(np.clip(im1 + noise, 0, 255)))
        imgs2.append(imn)

    # test the loss
    LOSS = MS_SSIM_L1_LOSS()
    loss_blur = []
    loss_noise = []
    for img in imgs:
        img = pil2tensor(img).cuda(0)
        loss = LOSS(img, gt)
        loss_blur.append(loss)
    for img in imgs2:
        img = pil2tensor(img).cuda(0)
        loss = LOSS(img, gt)
        loss_noise.append(loss)