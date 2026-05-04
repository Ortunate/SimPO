from pathlib import Path

from tokenizers import Tokenizer
from tokenizers.models import WordLevel
from tokenizers.pre_tokenizers import Whitespace
from transformers import GPT2Config, GPT2LMHeadModel, PreTrainedTokenizerFast


def main() -> None:
    output_dir = Path(__file__).resolve().parent / "local_tiny_gpt2"
    tokens = [
        "[UNK]",
        "<pad>",
        "<bos>",
        "<eos>",
        "<|user|>",
        "<|assistant|>",
        "<|system|>",
        "Say",
        "hello",
        "Give",
        "a",
        "color",
        "Answer",
        "briefly",
        "Hello",
        "there",
        "Goodbye",
        "Blue",
        "Stone",
        ".",
    ]
    vocab = {token: idx for idx, token in enumerate(tokens)}
    tokenizer = Tokenizer(WordLevel(vocab=vocab, unk_token="[UNK]"))
    tokenizer.pre_tokenizer = Whitespace()
    fast = PreTrainedTokenizerFast(
        tokenizer_object=tokenizer,
        unk_token="[UNK]",
        pad_token="<pad>",
        bos_token="<bos>",
        eos_token="<eos>",
    )
    fast.model_max_length = 64

    config = GPT2Config(
        vocab_size=len(fast),
        n_positions=64,
        n_ctx=64,
        n_embd=32,
        n_layer=2,
        n_head=4,
        bos_token_id=fast.bos_token_id,
        eos_token_id=fast.eos_token_id,
        pad_token_id=fast.pad_token_id,
    )
    model = GPT2LMHeadModel(config)

    output_dir.mkdir(parents=True, exist_ok=True)
    fast.save_pretrained(output_dir)
    model.save_pretrained(output_dir)
    print(output_dir)


if __name__ == "__main__":
    main()
