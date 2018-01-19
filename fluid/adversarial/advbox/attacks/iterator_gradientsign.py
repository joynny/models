"""
This module provide the attack method for Iterator FGSM's implement.
"""
from __future__ import division
import numpy as np
from collections import Iterable
from .base import Attack


class IteratorGradientSignAttack(Attack):
    """
    This attack was originally implemented by Alexey Kurakin(Google Brain).
    Paper link: https://arxiv.org/pdf/1607.02533.pdf
    """

    def _apply(self, image_label, epsilons=100, steps=10):
        """
        Apply the iterative gradient sign attack.
        Args:
            image_label(list): The image and label tuple list of one element.
            epsilons(list|tuple|int): The epsilon (input variation parameter).
            steps(int): The number of iterator steps.
        Return:
            numpy.ndarray: The adversarail sample generated by the algorithm.
        """
        assert len(image_label) == 1
        pre_label = np.argmax(self.model.predict(image_label))
        gradient = self.model.gradient(image_label)
        min_, max_ = self.model.bounds()

        if not isinstance(epsilons, Iterable):
            epsilons = np.linspace(0, 1, num=epsilons + 1)

        for epsilon in epsilons:
            adv_img = image_label[0][0].reshape(gradient.shape)
            for _ in range(steps):
                gradient = self.model.gradient([(adv_img, image_label[0][1])])
                gradient_sign = np.sign(gradient) * (max_ - min_)
                adv_img = adv_img + epsilon * gradient_sign
                adv_img = np.clip(adv_img, min_, max_)
                adv_label = np.argmax(self.model.predict([(adv_img, 0)]))
                if pre_label != adv_label:
                    return adv_img
