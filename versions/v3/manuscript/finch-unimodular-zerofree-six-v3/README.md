# Finch's balanced zerofree matrices

The note refutes Conjecture 4 in Steven Finch's *Small Matrices with Small
Inverses: Unimodular Zerofree Cases*, arXiv:2605.03691v4, Section 5, page 7.
It gives explicit integral matrices `A`, `B` of order six with `AB=BA=I`,
`det(A)=-1`, no zero entries and entrywise absolute maxima `alpha=beta=3`.
The written proof characterizes the unimodular matrices in the family
`diag(s_1,...,s_n)+cJ`, for signs `s_i` and integers `n>=2`, `c>=2`.
It also supplies positive order-six matrices with `(alpha,beta)=(3,4)`
and `(3,5)`, and relates Finch's later extremal bounds to Conjecture 6.
The rank-one determinant and inverse identities are prior constructions
recorded by Christopher Towse and Eric Campbell, *Constructing Integer
Matrices with Integer Eigenvalues*, manuscript dated March 25, 2016,
Section 2, Theorem 1 and Corollaries 1–2, page 2:
https://ericthewry.github.io/pdfs/imies.pdf.
The note specializes these identities to positive zerofree matrices with
equal prescribed entry maxima; these conclusions are not stated there.

## Contents

- `note.tex`: the complete mathematical note and its bibliography.
- `witness.json`: the two matrices displayed in the note.
- `sibling-witnesses.json`: the two neighbouring inverse pairs.
- `verify.py`: a standard-library Python exact-arithmetic checker.
- `verification.json`: expected checker output, including finite ranges.
- Cited lower-bound families are also checked for each integer height from 3 to 20.
- `metadata.json`: title, authors, license, problem identity and scientific scope.

The separately supplied `note.pdf` is the typeset note.

## Typeset the note

Use Tectonic 0.17.0:

```sh
tectonic note.tex
```

Alternatively, use a standard LaTeX installation with the listed packages:

```sh
pdflatex -interaction=nonstopmode -halt-on-error note.tex
pdflatex -interaction=nonstopmode -halt-on-error note.tex
```

The bibliography is included in `note.tex`; no BibTeX database is needed.

## Check the matrices

Python 3.10 or later, with its standard library, is sufficient:

```sh
python3 verify.py > calculated.json
cmp calculated.json verification.json
```

The checker computes both matrix products, determinants by rational Gaussian
elimination and the inverse by rational Gauss--Jordan elimination. It also
compares all six displayed LaTeX matrices with the witness data and
tests the rank-one determinant and inverse identities over the ranges recorded
in `verification.json`. All calculations use exact integers or rational
numbers. The finite ranges are checks of instances; the general theorem has
the complete written proof in `note.tex`.

The pinned scientific formalization is
https://github.com/the-omega-institute/trureturing/blob/3ede1d0bfa6d3c063b82234699d279136b6f0c42/D5/S3/QuadraticForms/FinchBalancedZerofreeRefutation.lean.
The declaration `Trureturing.OpenProblems.FinchUnimodularZerofree.result`
states the negation of the order-six nonexistence claim, with the displayed
matrices as witnesses. The general family is the written theorem of the note.

## Authors and license

Haobo Ma — ChronoAI Pte Ltd, Singapore.

Wenlin Zhang — National University of Singapore; ChronoAI Pte Ltd, Singapore.

CC BY 4.0 (`cc-by-4.0`): https://creativecommons.org/licenses/by/4.0/.
