import math
import sys
from pathlib import Path
from types import MethodType, SimpleNamespace

import torch
from torch import nn


REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from simpo_trainer import SimPOTrainer


def build_trainer(**overrides):
    trainer = object.__new__(SimPOTrainer)
    trainer.beta = overrides.get("beta", 2.0)
    trainer.gamma_beta_ratio = overrides.get("gamma_beta_ratio", 0.5)
    trainer.dynamic_gamma_similarity_scale = overrides.get("dynamic_gamma_similarity_scale", 0.5)
    trainer.dynamic_gamma_min = overrides.get("dynamic_gamma_min", 0.0)
    trainer.dynamic_gamma_max = overrides.get("dynamic_gamma_max", 0.5)
    trainer.label_smoothing = overrides.get("label_smoothing", 0.0)
    trainer.loss_type = overrides.get("loss_type", "sigmoid")
    trainer.label_pad_token_id = overrides.get("label_pad_token_id", -100)
    trainer.sft_weight = overrides.get("sft_weight", 0.0)
    trainer.is_encoder_decoder = False
    trainer.accelerator = SimpleNamespace(device=torch.device("cpu"))
    trainer._captured_lm_head_hidden_states = None
    return trainer


def assert_close(actual, expected, name, atol=1e-6):
    if not torch.allclose(actual, expected, atol=atol, rtol=0.0):
        raise AssertionError(f"{name}: expected {expected}, got {actual}")


def test_static_loss_matches_full_gamma_tensor():
    trainer = build_trainer(gamma_beta_ratio=0.5)
    chosen_logps = torch.tensor([-1.0, -2.0, -3.0])
    rejected_logps = torch.tensor([-2.0, -1.5, -4.0])
    scalar_losses, scalar_chosen, scalar_rejected = trainer.simpo_loss(chosen_logps, rejected_logps)
    tensor_losses, tensor_chosen, tensor_rejected = trainer.simpo_loss(
        chosen_logps,
        rejected_logps,
        gamma_beta_ratio=torch.full_like(chosen_logps, 0.5),
    )
    assert_close(tensor_losses, scalar_losses, "static loss equivalence")
    assert_close(tensor_chosen, scalar_chosen, "chosen reward equivalence")
    assert_close(tensor_rejected, scalar_rejected, "rejected reward equivalence")


def test_response_pooling_ignores_masked_tokens():
    trainer = build_trainer()
    hidden_states = torch.tensor(
        [
            [[1000.0, 1000.0], [1.0, 0.0], [500.0, 500.0]],
            [[1000.0, 1000.0], [0.0, 1.0], [500.0, 500.0]],
            [[-999.0, -999.0], [1.0, 0.0], [-500.0, -500.0]],
            [[-999.0, -999.0], [0.0, -1.0], [-500.0, -500.0]],
        ]
    )
    labels = torch.tensor(
        [
            [-100, 7, -100],
            [-100, 7, -100],
            [-100, 7, -100],
            [-100, 7, -100],
        ]
    )
    similarities = trainer._response_embedding_similarity(hidden_states, labels, len_chosen=2)
    assert_close(similarities, torch.tensor([1.0, -1.0]), "masked pooling similarities")


def test_dynamic_gamma_mapping_and_clamp():
    trainer = build_trainer(
        gamma_beta_ratio=0.5,
        dynamic_gamma_similarity_scale=2.0,
        dynamic_gamma_min=0.1,
        dynamic_gamma_max=0.4,
    )
    hidden_states = torch.tensor(
        [
            [[1.0, 0.0]],
            [[0.0, 1.0]],
            [[1.0, 0.0]],
            [[0.0, -1.0]],
        ]
    )
    labels = torch.tensor([[1], [1], [1], [1]])
    gamma, similarity = trainer._compute_dynamic_gamma_beta_ratio(hidden_states, labels, len_chosen=2)
    assert_close(similarity, torch.tensor([1.0, -1.0]), "dynamic similarity")
    assert_close(gamma, torch.tensor([0.1, 0.4]), "dynamic gamma clamp")


def test_lm_head_hook_detaches_and_removes():
    class DummyModel(nn.Module):
        def __init__(self):
            super().__init__()
            self.output = nn.Linear(2, 2, bias=False)

        def get_output_embeddings(self):
            return self.output

        def forward(self, x):
            return self.output(x)

    trainer = build_trainer()
    model = DummyModel()
    hidden = torch.ones(1, 2, requires_grad=True)
    with trainer._capture_lm_head_hidden_states(model):
        model(hidden)
    if trainer._captured_lm_head_hidden_states is None:
        raise AssertionError("LM-head hook did not capture hidden states")
    if trainer._captured_lm_head_hidden_states.requires_grad:
        raise AssertionError("Captured hidden states must be detached")

    trainer._captured_lm_head_hidden_states = None
    model(hidden * 2.0)
    if trainer._captured_lm_head_hidden_states is not None:
        raise AssertionError("LM-head hook was not removed after context exit")


def test_metric_key_contract_static_and_dynamic():
    trainer = build_trainer()
    chosen_logps = torch.tensor([-2.0, -1.0])
    rejected_logps = torch.tensor([-2.5, -1.5])
    chosen_logits = torch.zeros(2, 3, 4)
    rejected_logits = torch.zeros(2, 3, 4)
    chosen_labels = torch.ones(2, 3, dtype=torch.long)

    def static_forward(self, model, batch):
        return chosen_logps, rejected_logps, chosen_logits, rejected_logits, chosen_labels, None, None

    trainer.concatenated_forward = MethodType(static_forward, trainer)
    _, static_metrics = trainer.get_batch_loss_metrics(None, {}, train_eval="train")
    if any(key.startswith("gamma_beta_ratio/") or key.startswith("similarity/") for key in static_metrics):
        raise AssertionError(f"Static metrics unexpectedly include dynamic keys: {static_metrics.keys()}")

    gamma = torch.tensor([0.25, 0.35])
    similarity = torch.tensor([0.75, 0.25])

    def dynamic_forward(self, model, batch):
        return chosen_logps, rejected_logps, chosen_logits, rejected_logits, chosen_labels, gamma, similarity

    trainer.concatenated_forward = MethodType(dynamic_forward, trainer)
    _, dynamic_metrics = trainer.get_batch_loss_metrics(None, {}, train_eval="train")
    expected_keys = {
        "gamma_beta_ratio/mean",
        "gamma_beta_ratio/min",
        "gamma_beta_ratio/max",
        "similarity/mean",
        "similarity/min",
        "similarity/max",
    }
    missing = expected_keys.difference(dynamic_metrics)
    if missing:
        raise AssertionError(f"Dynamic metrics missing expected keys: {sorted(missing)}")
    if not all(math.isfinite(float(dynamic_metrics[key])) for key in expected_keys):
        raise AssertionError("Dynamic metric values must be finite")


def main():
    checks = [
        test_static_loss_matches_full_gamma_tensor,
        test_response_pooling_ignores_masked_tokens,
        test_dynamic_gamma_mapping_and_clamp,
        test_lm_head_hook_detaches_and_removes,
        test_metric_key_contract_static_and_dynamic,
    ]
    for check in checks:
        check()
        print(f"PASS {check.__name__}")
    print("LOCAL_DYNAMIC_GAMMA_UNIT_CHECKS PASS")


if __name__ == "__main__":
    main()
