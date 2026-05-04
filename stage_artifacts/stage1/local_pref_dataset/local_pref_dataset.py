import datasets


class LocalPrefDataset(datasets.GeneratorBasedBuilder):
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
            ("hello", "Say hello.", "Hello there.", "Goodbye."),
            ("color", "Give a color.", "Blue.", "Stone."),
            ("brief", "Answer briefly.", "Hello.", "Goodbye."),
            ("again", "Say hello.", "Hello.", "Stone."),
        ]
        test_rows = [
            ("eval-hello", "Say hello.", "Hello there.", "Goodbye."),
            ("eval-color", "Give a color.", "Blue.", "Stone."),
        ]
        rows = train_rows if split == "train" else test_rows
        for idx, (key, prompt, chosen, rejected) in enumerate(rows):
            yield idx, {
                "prompt": [{"role": "user", "content": prompt}],
                "chosen": [{"role": "assistant", "content": chosen}],
                "rejected": [{"role": "assistant", "content": rejected}],
            }
