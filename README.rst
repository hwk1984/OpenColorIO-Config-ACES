..
  SPDX-License-Identifier: CC-BY-4.0
  Copyright Contributors to the OpenColorIO Project.

OpenColorIO Configuration for ACES
==================================

..  image:: https://via.placeholder.com/720x320.png?text=WARNING: This+repository+is+under+construction!

The `OpenColorIO Configuration for ACES <https://github.com/AcademySoftwareFoundation/OpenColorIO-Config-ACES/>`__
is an open-source `Python <https://www.python.org/>`__ package implementing
support for the generation of the *OCIO* configurations for the
`Academy Color Encoding System <https://www.oscars.org/science-technology/sci-tech-projects/aces>`__
(ACES).

It is freely available under the
`New BSD License <https://opensource.org/licenses/BSD-3-Clause>`__ terms.

.. contents:: **Table of Contents**
    :backlinks: none
    :depth: 2

.. sectnum::

Features
--------

The following features are available:

-   Automatic *OCIO* **Reference** configuration generation for *aces-dev*
    *CTL* reference implementation.

    - Discovery of *aces-dev* *CTL* transforms.
    - Generation of the *CTL* transforms graph.

-   Configurable generator producing the *OCIO* **CG** and **Studio**
    configurations.
-   Included *CLF* transforms along with generator and discovery support.

User Guide
----------

Installation
^^^^^^^^^^^^

Cloning the Repository
~~~~~~~~~~~~~~~~~~~~~~

The *OpenColorIO Configuration for ACES* repository uses `Git submodules <https://git-scm.com/book/en/v2/Git-Tools-Submodules>`__
thus cloning the repository requires initializing them::

    git clone --recursive https://github.com/AcademySoftwareFoundation/OpenColorIO-Config-ACES.git

If you have already cloned the repository and forgot the `--recursive`
argument, it is possible to initialize the submodules as follows::

    git submodule update --init --recursive

Poetry
~~~~~~

The *OpenColorIO Configuration for ACES* repository adopts `Poetry <https://poetry.eustace.io>`__
to help managing its dependencies, this is the recommended way to get started
with development.

Assuming `python >= 3.8 <https://www.python.org/download/releases/>`__ is
available on your system along with `OpenColorIO <https://opencolorio.org/>`__,
the development dependencies are installed with `Poetry <https://poetry.eustace.io>`__
as follows::

    git clone --recursive https://github.com/AcademySoftwareFoundation/OpenColorIO-Config-ACES.git
    cd OpenColorIO-Config-ACES
    poetry install --extras "optional"

The *aces-dev* *CTL* reference graph can be plotted but it requires `Graphviz <https://graphviz.org/>`__
to be installed on the system and having installed the optional `pygraphviz <https://pypi.org/project/pygraphviz/>`__:
python package::

    poetry install --extras "optional graphviz"

Docker
~~~~~~

Installing the dependencies for the `previous config generator <https://github.com/imageworks/OpenColorIO-Configs>`__
was not a trivial task. For ease of use an `aswf-docker <https://github.com/AcademySoftwareFoundation/aswf-docker>`__
based container is now available.

Creating the container from the `Dockerfile <https://docs.docker.com/engine/reference/builder/>`__
is done as follows::

    docker build -t aswf/opencolorio-config-aces:latest .

or alternatively, if the dependencies described in the next section are
satisfied::

    invoke docker build

Then, to run *bash* in the container::

    docker run -it -v ${PWD}:/home/aswf/OpenColorIO-Config-ACES aswf/opencolorio-config-aces:latest /bin/bash

Pypi
~~~~

The **OpenColorIO Configuration for ACES** package requires various
dependencies in order to run and be able to generate the *OCIO* configurations:

Primary Dependencies
********************

-   `python >= 3.8, < 3.11 <https://www.python.org/download/releases/>`__
-   `OpenColorIO <https://opencolorio.org/>`__

Optional Dependencies
*********************

-   `colour <https://www.colour-science.org/>`__
-   `graphviz <https://www.graphviz.org/>`__
-   `jsonpickle <https://jsonpickle.github.io/>`__
-   `networkx <https://pypi.org/project/networkx/>`__
-   `pygraphviz <https://pypi.org/project/pygraphviz/>`__

Development Dependencies
************************

-   `black <https://pypi.org/project/black/>`__
-   `coverage <https://pypi.org/project/coverage/>`__
-   `coveralls <https://pypi.org/project/coveralls/>`__
-   `flake8 <https://pypi.org/project/flake8/>`__
-   `invoke <https://pypi.org/project/invoke/>`__
-   `mypy <https://pypi.org/project/mypy/>`__
-   `pre-commit <https://pypi.org/project/pre-commit/>`__
-   `pydata-sphinx-theme <https://pypi.org/project/pydata-sphinx-theme/>`__
-   `pydocstyle <https://pypi.org/project/pydocstyle/>`__
-   `pytest <https://pypi.org/project/pytest/>`__
-   `pyupgrade <https://pypi.org/project/pyupgrade/>`__
-   `restructuredtext-lint <https://pypi.org/project/restructuredtext-lint/>`__
-   `sphinx >= 4, < 5 <https://pypi.org/project/Sphinx/>`__
-   `twine <https://pypi.org/project/twine/>`__

Once the dependencies are satisfied, the **OpenColorIO Configuration for ACES**
package can be installed from the `Python Package Index <http://pypi.python.org/pypi/opencolorio-config-aces>`__
by issuing this command in a shell::

    pip install --user opencolorio-config-aces

Components Status
^^^^^^^^^^^^^^^^^

+-------------------------------+----------------+----------------------------------------------------------------------------------+
| Component                     | Status         | Notes                                                                            |
+-------------------------------+----------------+----------------------------------------------------------------------------------+
| *aces-dev* Discovery          | Complete       | Minor updates might be required when *aces-dev* is updated.                      |
+-------------------------------+----------------+----------------------------------------------------------------------------------+
| Common Config Generator       | Complete       |                                                                                  |
+-------------------------------+----------------+----------------------------------------------------------------------------------+
| *Reference* Config Generation | Complete       |                                                                                  |
+-------------------------------+----------------+----------------------------------------------------------------------------------+
| *CG* Config Generation        | Complete       |                                                                                  |
+-------------------------------+----------------+----------------------------------------------------------------------------------+
| Custom Config Generation      | In-Progress    | We are designing the components so that one can generate a custom *ACES* config. |
+-------------------------------+----------------+----------------------------------------------------------------------------------+
| *Studio* Config Generation    | In-Progress    |                                                                                  |
+-------------------------------+----------------+----------------------------------------------------------------------------------+
| *CLF* Transforms Discovery    | Complete       | Minor updates will be required if classification changes.                        |
+-------------------------------+----------------+----------------------------------------------------------------------------------+
| *CLF* Transforms Generation   | In-Progress    | The *CG* Config *CLF* transforms are implemented                                 |
+-------------------------------+----------------+----------------------------------------------------------------------------------+
| Public API Surfacing          | In-Progress    | What is part of the Public API is not well defined currently.                    |
+-------------------------------+----------------+----------------------------------------------------------------------------------+
| Unit Tests                    | In-Progress    |                                                                                  |
+-------------------------------+----------------+----------------------------------------------------------------------------------+
| API Documentation             | In-Progress    |                                                                                  |
+-------------------------------+----------------+----------------------------------------------------------------------------------+
| Continuous Integration        | Complete       |                                                                                  |
+-------------------------------+----------------+----------------------------------------------------------------------------------+
| CLI                           | In-Progress    |                                                                                  |
+-------------------------------+----------------+----------------------------------------------------------------------------------+
| Containerisation              | Complete       | Minor updates will be required as the CLI evolves.                               |
+-------------------------------+----------------+----------------------------------------------------------------------------------+

Usage
^^^^^

Tasks
~~~~~

Various tasks are currently exposed via `invoke <https://pypi.org/project/invoke/>`__.

This is currently the recommended way to build the configuration until a
dedicated CLI is provided.

Listing the tasks is done as follows::

    invoke --list

Assuming the dependencies are satisfied, the task to build the **Reference**
configuration is::

    invoke build-config-reference

Alternatively, with the docker container built::

    invoke docker-run-build-config-reference

Likewise, for the **CG** configuration::

    invoke build-config-cg

Or::

    invoke docker-run-build-config-cg

API Reference
-------------

The main technical reference for `OpenColorIO Configuration for ACES <https://github.com/AcademySoftwareFoundation/OpenColorIO-Config-ACES>`__
is the `API Reference <https://opencolorio-config-aces.readthedocs.io/>`__.

About
-----

| **OpenColorIO Configuration for ACES** by OpenColorIO Contributors
| Copyright Contributors to the OpenColorIO Project – `ocio-dev@lists.aswf.io <ocio-dev@lists.aswf.io>`__
| This software is released under terms of New BSD License: https://opensource.org/licenses/BSD-3-Clause
| `https://github.com/AcademySoftwareFoundation/OpenColorIO-Config-ACES <https://github.com/AcademySoftwareFoundation/OpenColorIO-Config-ACES>`__
