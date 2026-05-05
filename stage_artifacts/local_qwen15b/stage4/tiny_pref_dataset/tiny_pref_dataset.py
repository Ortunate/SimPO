import datasets


class TinyPrefDataset(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("0.0.1")

    def _info(self):
        message_features = [
            {
                "role": datasets.Value("string"),
                "content": datasets.Value("string"),
            }
        ]
        return datasets.DatasetInfo(
            features=datasets.Features(
                {
                    "prompt": message_features,
                    "chosen": message_features,
                    "rejected": message_features,
                }
            )
        )

    def _split_generators(self, dl_manager):
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"split": "train"}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"split": "test"}),
        ]

    def _generate_examples(self, split):
        train_rows = [
            (
                "train-brief-capital",
                "Answer in one short sentence: what is the capital of France?",
                "The capital of France is Paris.",
                "France is a country in Europe with many cities.",
            ),
            (
                "train-sort",
                "Sort these numbers from smallest to largest: 3, 1, 2.",
                "1, 2, 3.",
                "3, 2, 1.",
            ),
            (
                "train-safety",
                "Give a safe way to clean a laptop screen.",
                "Power it off and wipe the screen gently with a microfiber cloth.",
                "Spray household cleaner directly onto the screen.",
            ),
            (
                "train-math",
                "Compute 7 plus 5.",
                "7 plus 5 equals 12.",
                "7 plus 5 equals 10.",
            ),
        ]
        test_rows = [
            (
                "test-color",
                "Name one primary color.",
                "Red is a primary color.",
                "Triangle is a primary color.",
            ),
            (
                "test-brief",
                "Answer briefly: what do bees make?",
                "Bees make honey.",
                "Bees make steel.",
            ),
        ]
        rows = train_rows if split == "train" else test_rows
        for idx, (key, prompt, chosen, rejected) in enumerate(rows):
            yield idx, {
                "prompt": [{"role": "user", "content": prompt}],
                "chosen": [{"role": "assistant", "content": chosen}],
                "rejected": [{"role": "assistant", "content": rejected}],
            }
