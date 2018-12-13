# © All rights reserved.
# ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland,
# Space Center (eSpace), 2018
# See the LICENSE.TXT file for more details.

from torch import autograd
import numpy as np
import torch as th

from practical_deep_stereo import matching


def mockup_operation(concatenated_embedding):
    return th.max(concatenated_embedding, dim=1, keepdim=True)[0]


def test_matching():
    network = matching.Matching(
        maximum_disparity=2, operation=mockup_operation)
    left_embedding = autograd.Variable(
        th.Tensor([0, 2, 1, 2]).view(1, 1, 1, 4))
    right_embedding = autograd.Variable(
        th.Tensor([3, 4, 2, 4]).view(1, 1, 1, 4))
    expected_output = np.array([[3, 4, 2, 4], [0, 3, 4, 2],
                                [0, 2, 3, 4]]).reshape(1, 1, 3, 1, 4)
    network_output = network(left_embedding, right_embedding)
    assert np.all(np.isclose(network_output.data.numpy(), expected_output))