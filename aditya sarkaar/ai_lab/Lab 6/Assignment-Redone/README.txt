Assignment-Redone
=================

This directory is an independent second implementation of the Genetic Algorithm
painter-robot lab. The original deliverables folder has not been used as an
output location for this run.

Run the experiment from this directory with:

    python code/redone_painter_ga.py --output outputs

The script recreates the plots, CSV files, and summary JSON in outputs/. The
experiment uses a fixed seed (40731), so the saved results are reproducible.

Files
-----

code/redone_painter_ga.py   Independent GA implementation
report.tex                  LaTeX source for the written report
report.pdf                  Compiled report, when generated locally
outputs/                    Plots, trajectories, CSV data, and summary JSON

To regenerate the report, open report.tex in Overleaf or compile it with
XeLaTeX, pdfLaTeX, or Tectonic while keeping the outputs/ folder beside it.
The image paths in the report are relative to Assignment-Redone/.
