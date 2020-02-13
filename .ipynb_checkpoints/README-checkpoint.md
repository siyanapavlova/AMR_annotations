# AMR_annotations
AMR Annotations Supervised Project - NLP Master - Université de Lorraine

__Authors__

* Kelvin Han
* Siyana Pavlova

__Supervisors__

* Bruno Guillaume
* Maxime Amblard

We present a system which takes sentences in natural language, parses them in the [Universal Dependencies (UD)](https://universaldependencies.org/) syntactic framework and applies a set of rewrite rules, using the [GREW](http://grew.fr/) rewriting system on the UD parses to produce semantic [Abstract Meaning Representation (AMR)](https://amr.isi.edu/) of the sentences.

Motivation, background, details on the design decisions and implementation, experiments and results can be found in the project [report](http://institut-sciences-digitales.fr/wp-content/uploads/2019/07/Going_from_UD_towards_AMR.pdf).

An outline of all of the above can be found in the project [poster](http://institut-sciences-digitales.fr/wp-content/uploads/2019/07/PosterM1TAL1819Going_from_UD_to_AMR_Poster.pdf).

### Requirements

[Install Grew](http://grew.fr/install/)
Make sure that you have installed opam v2+

Python packages

* grew
* smatch
* ufal.udpipe


### Running the System



