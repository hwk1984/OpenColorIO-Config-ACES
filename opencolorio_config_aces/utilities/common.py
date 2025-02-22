# SPDX-License-Identifier: BSD-3-Clause
# Copyright Contributors to the OpenColorIO Project.
"""
Common Utilities
================

Defines common utilities objects that don't fall in any specific category.
"""

import functools
import os
import re
import subprocess
from collections import defaultdict
from itertools import chain
from pprint import PrettyPrinter
from textwrap import TextWrapper

__author__ = "OpenColorIO Contributors"
__copyright__ = "Copyright Contributors to the OpenColorIO Project."
__license__ = "New BSD License - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "OpenColorIO Contributors"
__email__ = "ocio-dev@lists.aswf.io"
__status__ = "Production"

__all__ = [
    "DocstringDict",
    "first_item",
    "common_ancestor",
    "paths_common_ancestor",
    "vivification",
    "vivified_to_dict",
    "message_box",
    "is_colour_installed",
    "is_jsonpickle_installed",
    "is_networkx_installed",
    "REQUIREMENTS_TO_CALLABLE",
    "required",
    "is_string",
    "is_iterable",
    "git_describe",
    "matrix_3x3_to_4x4",
    "multi_replace",
]


# Monkey-patching the "PrettyPrinter" mapping to handle the "TypeError"
# exception raised with "instancemethod": https://bugs.python.org/issue33395
class _dispatch(dict):
    def get(self, key, default=None):
        try:
            return self.__get__(key, default)
        except Exception:
            pass


PrettyPrinter._dispatch = _dispatch()


class DocstringDict(dict):
    """
    A :class:`dict` sub-class that allows settings a docstring to :class:`dict`
    instances.
    """

    pass


def first_item(iterable, default=None):
    """
    Return the first item of given iterable.

    Parameters
    ----------
    iterable : iterable
        Iterable
    default : object
         Default value if the iterable is empty.

    Returns
    -------
    object
        First iterable item.
    """

    if not iterable:
        return default

    for item in iterable:
        return item


def common_ancestor(*args):
    """
    Return the common ancestor of given iterables.

    Other Parameters
    ----------------
    \\*args : list, optional
        Iterables to retrieve the common ancestor from.

    Returns
    -------
    iterable
        Common ancestor.

    Examples
    --------
    >>> common_ancestor(('1', '2', '3'), ('1', '2', '0'), ('1', '2', '3', '4'))
    ('1', '2')
    >>> common_ancestor('azerty', 'azetty', 'azello')
    'aze'
    """

    array = list(map(set, zip(*args)))
    divergence = list(filter(lambda i: len(i) > 1, array))

    if divergence:
        ancestor = first_item(args)[: array.index(first_item(divergence))]
    else:
        ancestor = min(args)

    return ancestor


def paths_common_ancestor(*args):
    """
    Return the common ancestor path from given paths.

    Parameters
    ----------
    \\*args : list, optional
        Paths to retrieve common ancestor from.

    Returns
    -------
    unicode
        Common path ancestor.

    Examples
    --------
    >>> paths_common_ancestor(  # doctest: +SKIP
    ...     '/Users/JohnDoe/Documents', '/Users/JohnDoe/Documents/Test.txt')
    '/Users/JohnDoe/Documents'
    """

    path_ancestor = os.sep.join(
        common_ancestor(*[path.split(os.sep) for path in args])
    )

    return path_ancestor


def vivification():
    """
    Implement supports for vivification of the underlying dict like
    data-structure, magical!

    Returns
    -------
    defaultdict

    Examples
    --------
    >>> vivified = vivification()
    >>> vivified['my']['attribute'] = 1
    >>> vivified['my']  # doctest: +SKIP
    defaultdict(<function vivification at 0x...>, {u'attribute': 1})
    >>> vivified['my']['attribute']
    1
    """

    return defaultdict(vivification)


def vivified_to_dict(vivified):
    """
    Convert given vivified data-structure to dictionary.

    Parameters
    ----------
    vivified : defaultdict
        Vivified data-structure.

    Returns
    -------
    dict

    Examples
    --------
    >>> vivified = vivification()
    >>> vivified['my']['attribute'] = 1
    >>> vivified_to_dict(vivified)  # doctest: +SKIP
    {u'my': {u'attribute': 1}}
    """

    if isinstance(vivified, defaultdict):
        vivified = {
            key: vivified_to_dict(value) for key, value in vivified.items()
        }
    return vivified


def message_box(message, width=79, padding=3, print_callable=print):
    """
    Print a message inside a box.

    Parameters
    ----------
    message : unicode
        Message to print.
    width : int, optional
        Message box width.
    padding : unicode, optional
        Padding on each sides of the message.
    print_callable : callable, optional
        Callable used to print the message box.

    Returns
    -------
    bool
        Definition success.

    Examples
    --------
    >>> message = ('Lorem ipsum dolor sit amet, consectetur adipiscing elit, '
    ...     'sed do eiusmod tempor incididunt ut labore et dolore magna '
    ...     'aliqua.')
    >>> message_box(message, width=75)
    ===========================================================================
    *                                                                         *
    *   Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do       *
    *   eiusmod tempor incididunt ut labore et dolore magna aliqua.           *
    *                                                                         *
    ===========================================================================
    True
    >>> message_box(message, width=60)
    ============================================================
    *                                                          *
    *   Lorem ipsum dolor sit amet, consectetur adipiscing     *
    *   elit, sed do eiusmod tempor incididunt ut labore et    *
    *   dolore magna aliqua.                                   *
    *                                                          *
    ============================================================
    True
    >>> message_box(message, width=75, padding=16)
    ===========================================================================
    *                                                                         *
    *                Lorem ipsum dolor sit amet, consectetur                  *
    *                adipiscing elit, sed do eiusmod tempor                   *
    *                incididunt ut labore et dolore magna                     *
    *                aliqua.                                                  *
    *                                                                         *
    ===========================================================================
    True
    """

    ideal_width = width - padding * 2 - 2

    def inner(text):
        """Format and pads inner text for the message box."""

        return "*{0}{1}{2}{0}*".format(
            " " * padding, text, (" " * (width - len(text) - padding * 2 - 2))
        )

    print_callable("=" * width)
    print_callable(inner(""))

    wrapper = TextWrapper(
        width=ideal_width, break_long_words=False, replace_whitespace=False
    )

    lines = [wrapper.wrap(line) for line in message.split("\n")]
    lines = [" " if len(line) == 0 else line for line in lines]
    for line in chain(*lines):
        print_callable(inner(line.expandtabs()))

    print_callable(inner(""))
    print_callable("=" * width)

    return True


def is_colour_installed(raise_exception=False):
    """
    Return if *Colour* is installed and available.

    Parameters
    ----------
    raise_exception : bool
        Raise exception if *Colour* is unavailable.

    Returns
    -------
    bool
        Is *Colour* installed.

    Raises
    ------
    ImportError
        If *Colour* is not installed.
    """

    try:  # pragma: no cover
        import colour  # noqa

        return True
    except ImportError as error:  # pragma: no cover
        if raise_exception:
            raise ImportError(
                (
                    '"Colour" related API features ' 'are not available: "{}".'
                ).format(error)
            )
        return False


def is_jsonpickle_installed(raise_exception=False):
    """
    Return if *jsonpickle* is installed and available.

    Parameters
    ----------
    raise_exception : bool
        Raise exception if *jsonpickle* is unavailable.

    Returns
    -------
    bool
        Is *jsonpickle* installed.

    Raises
    ------
    ImportError
        If *jsonpickle* is not installed.
    """

    try:  # pragma: no cover
        import jsonpickle  # noqa

        return True
    except ImportError as error:  # pragma: no cover
        if raise_exception:
            raise ImportError(
                (
                    '"jsonpickle" related API features, e.g. serialization, '
                    'are not available: "{}".'
                ).format(error)
            )
        return False


def is_networkx_installed(raise_exception=False):
    """
    Return if *NetworkX* is installed and available.

    Parameters
    ----------
    raise_exception : bool
        Raise exception if *NetworkX* is unavailable.

    Returns
    -------
    bool
        Is *NetworkX* installed.

    Raises
    ------
    ImportError
        If *NetworkX* is not installed.
    """

    try:  # pragma: no cover
        # pylint: disable=W0612
        import networkx  # noqa

        return True
    except ImportError as error:  # pragma: no cover
        if raise_exception:
            raise ImportError(
                (
                    '"NetworkX" related API features '
                    'are not available: "{}".'
                ).format(error)
            )
        return False


REQUIREMENTS_TO_CALLABLE = DocstringDict(
    {
        "Colour": is_colour_installed,
        "jsonpickle": is_jsonpickle_installed,
        "NetworkX": is_networkx_installed,
    }
)
REQUIREMENTS_TO_CALLABLE.__doc__ = """
Mapping of requirements to their respective callables.

_REQUIREMENTS_TO_CALLABLE : CaseInsensitiveMapping
    **{'Colour', 'jsonpickle', 'NetworkX', 'OpenImageIO'}**
"""


def required(*requirements):
    """
    Decorate a function to check whether various ancillary package requirements
    are satisfied.

    Other Parameters
    ----------------
    \\*requirements : list, optional
        Requirements to check whether they are satisfied.

    Returns
    -------
    object
    """

    def wrapper(function):
        """Wrap given function wrapper."""

        @functools.wraps(function)
        def wrapped(*args, **kwargs):
            """Wrap given function."""

            for requirement in requirements:
                REQUIREMENTS_TO_CALLABLE[requirement](raise_exception=True)

            return function(*args, **kwargs)

        return wrapped

    return wrapper


def is_string(a):
    """
    Return if given :math:`a` variable is a *string* like variable.

    Parameters
    ----------
    a : object
        Data to test.

    Returns
    -------
    bool
        Is :math:`a` variable a *string* like variable.

    Examples
    --------
    >>> is_string("I'm a string!")
    True
    >>> is_string(["I'm a string!"])
    False
    """

    return True if isinstance(a, str) else False


def is_iterable(a):
    """
    Return if given :math:`a` variable is iterable.

    Parameters
    ----------
    a : object
        Variable to check the iterability.

    Returns
    -------
    bool
        :math:`a` variable iterability.

    Examples
    --------
    >>> is_iterable([1, 2, 3])
    True
    >>> is_iterable(1)
    False
    """

    return is_string(a) or (True if getattr(a, "__iter__", False) else False)


def git_describe():
    """
    Describe the current *OpenColorIO Configuration for ACES* *git* version.

    Returns
    -------
    >>> git_describe()  # doctest: +SKIP
    '0.1.0'
    """

    import opencolorio_config_aces

    try:  # pragma: no cover
        version = subprocess.check_output(
            ["git", "describe"],
            cwd=opencolorio_config_aces.__path__[0],
            stderr=subprocess.STDOUT,
        ).strip()
        version = version.decode("utf-8")
    except Exception:  # pragma: no cover
        version = opencolorio_config_aces.__version__

    return version


# TODO: Numpy currently comes via "Colour", we might want that to be an
# explicit dependency in the future.
@required("Colour")
def matrix_3x3_to_4x4(M):
    """
    Convert given 3x3 matrix :math:`M` to a raveled 4x4 matrix.

    Parameters
    ----------
    M : array_like
        3x3 matrix :math:`M` to convert.

    Returns
    -------
    list
        Raveled 4x4 matrix.
    """

    import numpy as np

    M_I = np.identity(4)
    M_I[:3, :3] = M

    return np.ravel(M_I).tolist()


def multi_replace(name, patterns):
    """
    Update given name by applying in succession the given patterns and
    substitutions.

    Parameters
    ----------
    name : unicode
        Name to update.
    patterns : dict
        Dictionary of regular expression patterns and substitution to apply
        onto the name.

    Returns
    -------
    unicode
        Updated name.

    Examples
    --------
    >>> multi_replace(
    ...     'Canon Luke Skywalker was weak and powerless.',
    ...     {'Canon': 'Legends', 'weak': 'strong', '\\w+less': 'powerful'})
    'Legends Luke Skywalker was strong and powerful.'
    """

    for pattern, substitution in patterns.items():
        name = re.sub(pattern, substitution, name)

    return name
