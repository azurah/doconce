#!/bin/bash
set -x

function system {
  "$@"
  if [ $? -ne 0 ]; then
    echo "make.sh: unsuccessful command $@"
    echo "abort!"
    exit 1
  fi
}

# Main document lives in test directory
cp ../../../test/math_test.do.txt .

rm -f *.aux
name=math_test

# Because we exemplify all math blocks with latex code blocks,
# we get multiple defined lables and need --no_abort
options="--no_abort"

system doconce format pdflatex $name --no_abort --latex_code_style=pyg $options
system pdflatex -shell-escape $name
pdflatex -shell-escape $name

system doconce format html $name --html_output=${name}_html $options
exit

system doconce format sphinx $name $options
system doconce sphinx_dir $name
system python automake_sphinx.py

system doconce format pandoc $name $options
# Do not use pandoc directly because it does not support MathJax sufficiently well
system doconce md2html $name.md
cp $name.html ${name}_pandoc.html