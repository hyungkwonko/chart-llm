<p align="center">
  <h2 align="center">NL generation pipeline using Vega-Lite specifications and LLMs</h2>
</p>

![img](https://github.com/hyungkwonko/chart-llm/blob/main/docs/static/img/fig3.png?raw=true)

We introduce a Large Language Model (LLM) framework that generates rich and diverse NL datasets using only Vega-Lite specifications as input, thereby streamlining the development of Natural Language Interfaces (NLIs) for data visualization. We propose two techniques to synthesize relevant chart semantics accurately and enhance syntactic diversity in each NL dataset, respectively: 1) a guided discovery incorporated into prompting so that LLMs can steer themselves to create varying NL datasets in a self-directed manner; 2) a score-based paraphrasing to augment NL syntax along with four well-defined language axes. We also present a new chart collection of 1,981 real-world Vega-Lite specifications that have increased diversity and complexity compared to benchmarks, to demonstrate the generalizability of our framework. The experimental results show that our framework accurately extracts chart semantics and generates L1/L2 captions with 89.4\% and 76.0\% accuracy, respectively, while generating and paraphrasing utterances and questions with greater diversity than benchmarks.


## [Chart Dataset: 1,981 Vega-Lite Specifications](https://github.com/hyungkwonko/chart-llm/tree/main/docs/data/chart)

![img](https://github.com/hyungkwonko/chart-llm/blob/main/docs/static/img/teaser.png?raw=true)

We introduce a new set of human-generated Vega-Lite specifications, which is more diverse and complex than previous datasets. You can find the dataset [here](https://github.com/hyungkwonko/chart-llm/tree/main/docs/data/chart). Also refer to [our website](https://hyungkwonko.info/chart-llm/explorer.html) to see the charts.


## Examples NL Dataset Generation
Please prepare [Open-AI API](https://openai.com/blog/openai-api) and locate the `.env` file in the root:
```
OPENAI_API_KEY= example-openai-code
```

To run the example codes, refer to below:
```python
# L1 Caption Generation (Caption)
python -m pipeline_sample.task1_L1

# L2 Caption Generation (Caption)
python -m pipeline_sample.task1_L2

# Utterance (NL to Chart Generation)
python -m pipeline_sample.task2

# Question (Chart Question Answering)
python -m pipeline_sample.task3
```


## NL Dataset Paraphrasing

![img](https://github.com/hyungkwonko/chart-llm/blob/main/docs/static/img/paraphrase.png?raw=true)

Our paraphrasing technique is inspired by a linear interpolation in the latent space for image generation and manipulation as demonstrated in many system and application papers. It enables a smooth transition from one expression to another by focusing on creating controllable and meaningful variations of a single sentence. We employ a five-point Likert-scale and assign one of the axes to each. Here, we focus on altering only the sentence's syntax, while maintaining its meaning. In detail, we provide LLMs with a sentence (i.e., Example Sentence) and an explanation about one of the defined axes (i.e., Axis) and its two directions (i.e., Direction-1, Direction-2). We assign a specific value on a Likert scale ranging from one to five, to paraphrase the sentence as if it were spoken by a person using a language with a certain degree indicated by the score.

## Examples NL Dataset Paraphrasing
```python
# Paraphrasing with Random one or two Axis
python -m pipeline_sample.task4_1

# Paraphrasing with two Axex and print them all (5*5=25)
python -m pipeline_sample.task4_all
```

## Citation

You can use the following bibtex to cite our work:

```bibtex
@inproceedings{,
  title={},
  author={},
  pages={},
  year={}
}
```