# AMR_annotations
AMR Annotations Supervised Project - NLP Master - Université de Lorraine

__Authors__

* Kelvin Han
* Siyana Pavlova

__Supervisors__

* Bruno Guillaume
* Maxime Amblard

We present a system which takes sentences in natural language, parses them in the [Universal Dependencies (UD)](https://universaldependencies.org/) syntactic framework and applies a set of rewrite rules, using the [GREW](http://grew.fr/) rewriting system on the UD parses to produce semantic [Abstract Meaning Representation (AMR)](https://amr.isi.edu/) of the sentences.

![alt text](https://github.com/siyanapavlova/AMR_annotations/images/system_architecture.jpg "System Architecture")

Motivation, background, details on the design decisions and implementation, experiments and results can be found in the project [report](http://institut-sciences-digitales.fr/wp-content/uploads/2019/07/Going_from_UD_towards_AMR.pdf).

An outline of all of the above can be found in the project [poster](http://institut-sciences-digitales.fr/wp-content/uploads/2019/07/PosterM1TAL1819Going_from_UD_to_AMR_Poster.pdf).

### Requirements

* [Install Grew](http://grew.fr/install/)
* Python 3.x
* Python packages
    * `grew`
    * `smatch`
    * `ufal.udpipe`
    * `numpy` [for pattern_identification.py]
    * `sklearn` [for pattern_identification.py]

### Running the System

##### `main.py`
This script runs the main pipeline of the system and produces results to analyse.

__Parameters__

 * `sentence_nums` - a list of sentence numbers (corresponding to the trailing digits in any of the files in [dataset](https://github.com/siyanapavlova/AMR_annotations/tree/master/data/amr_bank_data/sentences))
 * `n` - number of times to perform the test 
 * `folder` - path to the folder where the results should be saved
 
__Data__

 * UD parses. In our experiments we used [these parses](https://github.com/siyanapavlova/AMR_annotations/tree/master/data/amr_bank_data/ud). UD parses can be produced by calling the `parse_files_in_folder(raw_sentences_folder, ud_save_folder)` function of the `parser.py` module, where `raw_sentences_folder` is the path to the folder where raw sentences are stored (one sentence per file) and `ud_save_folder` is the path to the folder where UD parses (in CoNNL-U format) should be stored. Example:
 ```parse_files_in_folder('./data/amr_bank_data/sentences/', './data/amr_bank_data/ud/')```
 * Gold AMR parses. We used parses for The Little Prince, as outlined in the report. Available [here](https://github.com/siyanapavlova/AMR_annotations/tree/master/data/amr_bank_data/amrs)
 
__Running the script__

 1. Initialise Grew.
     `grew.init()`
 2. Run `collect_scores(sentence_nums, n, folder)`. This will do the following:
     1. Call `calculate_scores()` on the given sentences. This, in turn, will:
           1. Call `run_pipeline()` on each sentence. This will:
               1. Load the UD graph for the given sentence
               2. Build all possible AMR graphs from the UD graph following the specified [rewrite rules](https://github.com/siyanapavlova/AMR_annotations/tree/master/grs) and compute their scores.
               3. Select the best scoring AMR graph and return its score
           2. Compute _precision_, _recall_ and _f1 score_ for each sentence.
           3. Print the max, min and average values for each measure.
           4. Return the measures.
     2. Write the computed score to files.
     
__Example__

```
#initiate Grew
grew.init()

#generate the numbers of the sentences to be processed
sentence_nums = list(range(1,101))

#process the sentences and collect scores
collect_scores(sentence_nums, 1, './results/final_100')
```

##### Visualisations

[`Result_Visualisations.ipynb`](https://github.com/siyanapavlova/AMR_annotations/blob/master/results/Result%20Visualisations.ipynb) is a Jupyter notebook that can be used to analyse and visualise the stored scores.

### Possible alterations

Here we outline how to run the system on a different dataset. Furthermore, the coverage of the rewriting rules and lexicon can be significantly extended to improve the AMR parsing performance. We outline how these can be extended.

1. To run the code on your own dataset, starting from raw sentences:
    1. Add your raw sentences (one sentence per file) to a folder and number them accordingly (with 4 digits at the end of the filename).
    2. Call the `parse_files_in_folder(raw_sentences_folder, ud_save_folder)` function of the `parser.py` module, as outlined above.
    3. Add Gold AMR parses for your dataset to a folder.
    4. Run `main.py`, specifying `sentence_nums`, `n` and `folder`.
2. To use a different model for the UD parser:
    1. Save your model to `./models/`
    2. Change the model path in `line 37` in `parser.py`.
3. To extend the GRS rulebase, you can add rules to the main [grs file](https://github.com/siyanapavlova/AMR_annotations/tree/master/grs). Please refer to [Application of Graph Rewriting to Natural Language Processing](https://www.wiley.com/en-fr/Application+of+Graph+Rewriting+to+Natural+Language+Processing-p-9781119522348) and the [GREW documentation](http://grew.fr/) for a guide on how to do so.
4. You can add to the lexicons, by manually annotating the PropBank predicates on the proto-roles of these predicates. The lexicon we used can be found [here](https://github.com/siyanapavlova/AMR_annotations/blob/master/grs/lexicons/subcat/test_lexicon.lp). An annotation tool for adding these proto-roles can be found [here](https://github.com/siyanapavlova/AMR_annotations/blob/master/create_lexicon.py).
