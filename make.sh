#!/usr/bin/env bash

clean () {
    find . -name *.egg-info -exec rm -rf {} +
    find . -name '*.pyc' -exec rm -f {} +
    find . -name '*.pyo' -exec rm -f {} +
    find . -name '*~' -exec rm -f {} +
    rm -rf dist build
}

build () {
    python setup.py ${*:-sdist bdist_wheel}
}

case $1 in
    clean)
        clean
        ;;
    upload)
        twine upload dist/* --skip-existing ${@:2}
        ;;
    build)
        build ${@:2}
        ;;
    install)
        pip install .
        ;;
    *)
        build $@
        ;;
esac
