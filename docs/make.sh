rm *.rst ||:
mkdir --parents _build _static _templates
touch index.rst
make clean html
sphinx-apidoc -f -o . .. 
rm modules.rst
mv e4client.rst index.rst
sphinx-build . _build/html/

