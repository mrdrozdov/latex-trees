# latex-trees

depends on python3.

usage:

```
$ python main.py --input 000110101 --tokens The,cat,on,the,mat

% tree
\draw [line width=0.25mm] (0, 0) -- (-3.0, -1.0);
\draw [line width=0.25mm] (-0.75, -0.75) -- (-1.5, -1.0);
\draw [line width=0.25mm] (-1.5, -0.5) -- (0.0, -1.0);
\draw [line width=0.25mm] (-0.75, -0.25) -- (1.5, -1.0);
\draw [line width=0.25mm] (0, 0) -- (3.0, -1.0);

% tokens
\node[text height=1.2cm] at (-3.0, -1.0) [fontscale=4] {The};
\node[text height=1.2cm] at (-1.5, -1.0) [fontscale=4] {cat};
\node[text height=1.2cm] at (0.0, -1.0) [fontscale=4] {sat};
\node[text height=1.2cm] at (1.5, -1.0) [fontscale=4] {on};
\node[text height=1.2cm] at (3.0, -1.0) [fontscale=4] {mat};
```

Recommended template for latex:

```
\documentclass{article}
\usepackage{tikz}

% I'm not completely sure the best way to change the font size and
% for now `fontscale' is a pretty hacky solution.
\usetikzlibrary{calc}
\usepackage{relsize}
\tikzset{fontscale/.style = {font=\relsize{#1}}
    }

\begin{document}

\resizebox{0.5\linewidth}{!}{
\begin{tikzpicture}
% tree
\draw [line width=0.25mm] (0, 0) -- (-3.0, -1.0);
\draw [line width=0.25mm] (-0.75, -0.75) -- (-1.5, -1.0);
\draw [line width=0.25mm] (-1.5, -0.5) -- (0.0, -1.0);
\draw [line width=0.25mm] (-0.75, -0.25) -- (1.5, -1.0);
\draw [line width=0.25mm] (0, 0) -- (3.0, -1.0);

% tokens
\node[text height=1.2cm] at (-3.0, -1.0) [fontscale=4] {The};
\node[text height=1.2cm] at (-1.5, -1.0) [fontscale=4] {cat};
\node[text height=1.2cm] at (0.0, -1.0) [fontscale=4] {sat};
\node[text height=1.2cm] at (1.5, -1.0) [fontscale=4] {on};
\node[text height=1.2cm] at (3.0, -1.0) [fontscale=4] {mat};
\end{tikzpicture}
}

\end{document}
```
