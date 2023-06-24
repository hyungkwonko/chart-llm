# Answering Questions about Charts and Generating Visual Explanations

This repository includes code and data for the CHI 2020 submission **Answering Questions about Charts and Generating Visual Explanations**.

## Code

We include the code for the 3-stage pipeline for automatically answering questions about a chart specified in [Vega-Lite](https://vega.github.io/vega-lite/) and providing explanations about how the answer was obtained.
Each of the three stages of the pipeline can be run in separation.

### Requirements

- [Sempre](https://github.com/percyliang/sempre) 
  - Recompiled with `Server.java` from our code 
  - With parameters from [Macro Grammars and Holistic Triggering for Efficient Semantic Parsing (Zhang et al.)](https://nlp.stanford.edu/pubs/zhang2017macro.pdf) (available [here](https://worksheets.codalab.org/worksheets/0xca1104da2ecb42c2b9c0cde07256e033/))
  - Run on port `8400`
- [Stanford CoreNLP](https://stanfordnlp.github.io/CoreNLP/)
  - Run on port `9000`.
- Word2Vec
  - With trained vectors on the Google News dataset from [Distributed Representations of Words and Phrases and their Compositionality (Mikolov et al.)](https://arxiv.org/abs/1310.4546) (available [here](https://code.google.com/archive/p/word2vec/))
  - Run `word2vec.py` on port `5005`.
- Python packages (Requires Python3)
  - flask
  - nltk
  - bidict
  - gensim
  
### Running Stage 1: Extract Data Table and Encodings

Note: the code has only been tested on Google Chrome.
1. Set `curr_visualization` parameter in `js/index.js` to point to the desired visualization.
2. Run local host on the root code directory and open `index.html`
3. Extracted table will show underneath the chart. Save the table as CSV for next steps. (You may want to change line 153 of `js/index.js` to save to a file instead of printing to console.)

### Running Stage 2: Visual to Non-Visual Question Conversion & Running Sempre for answers

1. Run `QAServer.py`. You may have to modify the directories the file depending on where you have the relevant data. This will run on port `5000`.
2. You can provide: `sessionId`, `question_id`, `dataset_name`, `spec_file_name`, `runtime_file_name` (name of the CSV table extracted from Stage 1) to localhost:5000/query-vis-sempre with GET method to obtain the converted question, answer given by system, and the lambda expression.

### Running Stage 3: Explanation Generation

1. Run `GenerateExplanation.py` with the CSV including the lambda expression and the chart metadata.

## Dataset

We include the 52 Vega-Lite charts and the 629 human-generated questions, along with 748 explanations they gave for their answers.
We collected these questions and explanations through Amazon Mechanical Turk, and manually annotated each of the questions with the correct answers.
We used these questions to evaluate our automatic pipeline.

### Chart Metadata
`chart-list.json` includes the metadata about the 52 charts present in the dataset. This includes the title of the chart, as well as the dataset name and the name of the Vega-Lite specification file.

### Chart Specifications
Inside the `dataset` directory, the Vega-Lite specification files can be found in `[dataset-name]/specs/[file-name]`.

### Human-Generated Questions and Explanations
`qadata.json` includes the human-generated questions with correct answers, and answer-explanation pairs generated by humans.
For each question id, the question, the correct answer, and the turkers' answers and explanations (if the provided explanation was meaningful) are given, along with the metadata about the chart that the question and the explanations refer to.