# Neural GEC Systems with Unsupervised Pre-Training on Synthetic Data

This repository contains models, system configurations and outputs of our
winning GEC systems in [the BEA 2019 shared
task](https://www.cl.cam.ac.uk/research/nl/bea2019st/) described in R.
Grundkiewicz, M. Junczys-Dowmunt, K. Heafield: [Neural Grammatical Error
Correction Systems with Unsupervised Pre-training on Synthetic
Data](https://www.aclweb.org/anthology/W19-4427), BEA 2019.

This subdirectory contains GEC systems developed for the BEA19 shared task:
- `model.restricted` is the system submitted to the main track
- `model.lowresource` is the system submitted to the low-resource track


## Instructions

1. Install requirements:
        - CUDA 8.0+ for the Marian toolkit
        - Python, SpaCy 1.9.0

1. Download required tools, including Marian:

        cd tools
        make all
        make marian-dev
        cd ..

    If Marian compilation fails, install it manually in `tools/marian-dev`
    following instructions from [the official
    documentation](https://marian-nmt.github.io/docs/) make sure to add `-DUSE_SENTENCEPIECE=on` to the cmake command.

1. Download models:

        cd model.restricted
        ./download.sh
        cd ..

1. Run the restricted system:

        mkdir -p example
        echo "Alice have a cats ." > example/test.in
        ./run.sh model.restricted example/test.in example/test.out -d 0 1
        cat example/test.out

    Options `-d 0 1` mean that translation is run on GPU 0 and 1.

1. To evaluate on common test sets, copy them into `data/` and name as
   listed in `data/README.md`, then run:

        ./evaluate.restricted.sh
        tail outputs.restricted/*.eval

    The generated files `*.out` and `*.eval` should be the same as files from
    `../outputs/restricted/`.

1. Similar steps can be performed to run the low-resource system. Use `./run.sh
   model.lowresource` and `./evaluate.lowresource.sh`.


## Files

After installing tools and downloading the models, there should be the
following files:

```
.
├── data
│   └── README.md
├── evaluate.lowresource.sh
├── evaluate.restricted.sh
├── model.lowresource
│   ├── config.yml
│   ├── download.sh
│   ├── lmbig.npz
│   ├── model{1-8}.npz
│   ├── rescore.ini
│   ├── rl{1-4}.npz
│   └── vocab.spm
├── model.restricted
│   ├── big{1-4}.npz
│   ├── config.yml
│   ├── download.sh
│   ├── lmbig.npz
│   ├── rescore.ini
│   ├── rl{1-4}.npz
│   └── vocab.spm
├── README.md
├── run.sh
└── tools
    ├── errant
    ├── jfleg
    ├── m2scorer
    ├── marian-dev
    ├── Makefile
    ├── rescore.py
    └── tc.py
```
