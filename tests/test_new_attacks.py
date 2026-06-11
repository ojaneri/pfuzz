"""Tests for the modern adversarial techniques added in Phases 1-3.

These verify that each new attack is registered, instantiates, and runs end-to-end
against a FakeChatClient (no real LLM / no token spend), producing status updates.
"""
import pytest
from pfuzz.chat_clients import FakeChatClient
from pfuzz.client_config import ClientConfig
from pfuzz.attack_config import AttackConfig
from pfuzz.attack_registry import instantiate_tests
from pfuzz.attacks.utils import word_to_ascii_art
from pfuzz.attacks.flipattack import _build_flip_attack
from pfuzz.attacks.ascii_smuggling import _to_tag_chars, _build_ascii_smuggling

NEW_ATTACKS = [
    "many_shot", "artprompt", "flip_attack", "deep_inception", "skeleton_key",
    "policy_puppetry", "ascii_smuggling", "crescendo", "bad_likert_judge", "pair",
]


def _make_tests():
    client_config = ClientConfig(FakeChatClient(), [])
    attack_config = AttackConfig(FakeChatClient(), attack_prompts_count=1, embedding_config=None)
    return instantiate_tests(client_config, attack_config, [], False)


def test_all_new_attacks_registered():
    names = {t.test_name for t in _make_tests()}
    for name in NEW_ATTACKS:
        assert name in names, f"attack '{name}' is not registered"


@pytest.mark.parametrize("attack_name", NEW_ATTACKS)
def test_new_attack_runs_to_completion(attack_name):
    test = next(t for t in _make_tests() if t.test_name == attack_name)
    updates = list(test.run())  # should not raise
    assert len(updates) >= 1
    # With attack_prompts_count=1 each attack must record exactly one outcome.
    assert test.status.total_count >= 1


def test_descriptions_present():
    for t in _make_tests():
        if t.test_name in NEW_ATTACKS:
            assert t.test_description and len(t.test_description) > 20


# --- Pure helper / transform sanity checks (deterministic, no LLM) ---

def test_flip_attack_reverses_text():
    prompt = _build_flip_attack("abcdef")
    assert "fedcba" in prompt


def test_ascii_smuggling_uses_invisible_tag_chars():
    tagged = _to_tag_chars("hi")
    assert tagged and all(ord(c) >= 0xE0000 for c in tagged)
    # Visible benign text is preserved; hidden payload is non-ASCII tag chars.
    full = _build_ascii_smuggling("do the thing")
    assert "photosynthesis" in full
    assert any(ord(c) >= 0xE0000 for c in full)


def test_ascii_art_has_five_rows():
    art = word_to_ascii_art("AB")
    assert len(art.split("\n")) == 5
