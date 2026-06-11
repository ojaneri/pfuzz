from .attacks import (
    dynamic_test,
    translation,
    typoglycemia,
    dan,
    aim,
    self_refine,
    ethical_compliance,
    ucar,
    complimentary_transition,
    harmful_behavior,
    base64_injection,
    custom_benchmark,
    rag_poisoning,
    # Modern adversarial techniques (2024-2026)
    many_shot,          # Phase 1: single-turn
    artprompt,
    flipattack,
    deep_inception,
    skeleton_key,
    policy_puppetry,
    ascii_smuggling,
    crescendo,          # Phase 2: multi-turn
    bad_likert_judge,
    pair                # Phase 3: automated iterative refinement (PAIR/TAP)
)
