"""
6.1010 Spring '23 Lab 9: Autocomplete
"""

# NO ADDITIONAL IMPORTS!
import doctest
from text_tokenize import tokenize_sentences


class PrefixTree:
    def __init__(self):
        self.value = None
        self.children = {}

    def __setitem__(self, key, value):
        """
        Add a key with the given value to the prefix tree,
        or reassign the associated value if it is already present.
        Raise a TypeError if the given key is not a string.
        """
        if not isinstance(key, str):
            raise TypeError

        new_node = PrefixTree()
        if len(key) == 1:
            # might need a new_node, but if it already had a value, then
            # just change the value
            if key in self.children.keys():
                self.children[key].value = value

            else:
                new_node.value = value
                self.children[key] = new_node

        else:
            if key[0] in self.children.keys():
                node_of_element = self.children[key[0]]
                node_of_element[key[1:]] = value

            else:
                new_node[key[1:]] = value
                self.children[key[0]] = new_node

    def __getitem__(self, key):
        """
        Return the value for the specified prefix.
        Raise a KeyError if the given key is not in the prefix tree.
        Raise a TypeError if the given key is not a string.
        """
        if not isinstance(key, str):
            raise TypeError

        if key[0] not in self.children.keys():
            raise KeyError

        else:
            baby_tree = self.children[key[0]]
            if len(key) == 1:
                if baby_tree.value is None:
                    raise KeyError
                return baby_tree.value

            else:
                if baby_tree[key[1:]] is None:
                    raise KeyError

                return baby_tree[key[1:]]

    def __delitem__(self, key):
        """
        Delete the given key from the prefix tree if it exists.
        Raise a KeyError if the given key is not in the prefix tree.
        Raise a TypeError if the given key is not a string.
        """
        if not isinstance(key, str):
            raise TypeError

        if key not in self:
            raise KeyError

        self[key] = None

    def __contains__(self, key):
        """
        Is key a key in the prefix tree?  Return True or False.
        Raise a TypeError if the given key is not a string.
        """
        if not isinstance(key, str):
            raise TypeError

        if key == "":
            return False

        try:
            self[key]
            return True

        except KeyError:
            return False

    def __iter__(self, current_str=""):
        """
        Generator of (key, value) pairs for all keys/values in this prefix tree
        and its children.  Must be a generator!
        """
        # find the values that are actually contained within the PrefixTree using
        # contains dunder method

        # option_1: find all possible strings to be made and then return the
        # ones that are actually contained with their values

        if self.value is not None:
            yield (current_str, self.value)

        for letter in self.children:
            new_word = current_str + letter

            yield from self.children[letter].__iter__(new_word)


def word_frequencies(text):
    """
    Given a piece of text as a single string, create a prefix tree whose keys
    are the words in the text, and whose values are the number of times the
    associated word appears in the text.
    """
    sentences = tokenize_sentences(text)
    scrambled_word_dict = {}

    for sentence in sentences:
        for word in sentence.split():
            if word not in scrambled_word_dict.keys():
                scrambled_word_dict[word] = 1

            else:
                scrambled_word_dict[word] += 1

    my_tree = PrefixTree()
    for word in scrambled_word_dict.keys():
        my_tree[word] = scrambled_word_dict[word]

    return my_tree


def reach_prefix_part_of_tree(tree, prefix, curr=""):
    """


    Parameters
    ----------
    tree : TYPE
        DESCRIPTION.
    prefix : TYPE
        DESCRIPTION.
    curr : TYPE, optional
        DESCRIPTION. The default is ''.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    if len(prefix) == 1:
        if prefix in tree.children:
            return tree.children[prefix].__iter__(curr + prefix)
        else:
            return []

    else:
        if prefix[0] in tree.children:
            curr += prefix[0]
            return reach_prefix_part_of_tree(tree.children[prefix[0]], prefix[1:], curr)

        else:
            return []


def autocomplete(tree, prefix, max_count=None):
    """
    Return the list of the most-frequently occurring elements that start with
    the given prefix.  Include only the top max_count elements if max_count is
    specified, otherwise return all.

    Raise a TypeError if the given prefix is not a string.
    """
    if not isinstance(prefix, str):
        raise TypeError

    if prefix == "":
        all_words = []
        for word, count in tree.__iter__():
            all_words.append(word)

        if max_count:
            return all_words[:max_count]

        else:
            return all_words

    if max_count is None:
        all_words = []
        for word, count in reach_prefix_part_of_tree(tree, prefix):
            all_words.append(word)

        return all_words

    prefix_words = []

    for word, count in reach_prefix_part_of_tree(tree, prefix):
        prefix_words.append((word, count))

    prefix_words.sort(key=lambda tup: tup[1], reverse=True)

    last_last = []
    for word, count in prefix_words:
        last_last.append(word)

    return last_last[:max_count]


def deletion_edit(prefix):
    """


    Parameters
    ----------
    prefix : TYPE
        DESCRIPTION.

    Returns
    -------
    possibles : TYPE
        DESCRIPTION.

    """
    possibles = []
    for i in range(len(prefix)):
        possibles.append(prefix[:i] + prefix[i + 1 :])

    return possibles


def replacement_and_insertion_edit(prefix):
    """


    Parameters
    ----------
    prefix : TYPE
        DESCRIPTION.

    Returns
    -------
    possibles : TYPE
        DESCRIPTION.

    """
    alphabet = [
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
    ]
    possibles = []
    for i in range(len(prefix)):
        for letter in alphabet:
            # possibles.append(prefix[:i] + letter + prefix[i+1:]) #replacement
            possibles.append(prefix[:i] + letter + prefix[i:])  # insertion

    for i in range(len(prefix)):
        for letter in alphabet:
            possibles.append(prefix[:i] + letter + prefix[i + 1 :])  # replacement

    return possibles


def transpose_edit(prefix):
    """


    Parameters
    ----------
    prefix : TYPE
        DESCRIPTION.

    Returns
    -------
    possibles : TYPE
        DESCRIPTION.

    """
    possibles = []
    for i in range(len(prefix) - 1):
        possibles.append(prefix[:i] + prefix[i + 1] + prefix[i] + prefix[i + 2 :])

    return possibles


def possible_edits(prefix):
    """


    Parameters
    ----------
    prefix : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    cash = list(
        set(
            deletion_edit(prefix)
            + replacement_and_insertion_edit(prefix)
            + transpose_edit(prefix)
        )
    )

    if prefix in cash:
        cash.remove(prefix)

    return cash


def autocorrect(tree, prefix, max_count=None):
    """
    Return the list of the most-frequent words that start with prefix or that
    are valid words that differ from prefix by a small edit.  Include up to
    max_count elements from the autocompletion.  If autocompletion produces
    fewer than max_count elements, include the most-frequently-occurring valid
    edits of the given word as well, up to max_count total elements.
    """
    words_for_now = autocomplete(tree, prefix, max_count)

    if len(words_for_now) == max_count:
        return words_for_now

    else:
        testing = possible_edits(prefix)
        possible_words = [word for word in testing if word in tree]
        possible_words.sort(key=lambda word: tree[word], reverse=True)

        if max_count is None:
            return list(set(words_for_now + possible_words))

        return words_for_now + possible_words[: max_count - len(words_for_now)]


def word_filter(tree, pattern, curr=""):
    """
    Return list of (word, freq) for all words in the given prefix tree that
    match pattern.  pattern is a string, interpreted as explained below:
         * matches any sequence of zero or more characters,
         ? matches any single character,
         otherwise char in pattern char must equal char in word.
    """
    full_list = []
    if len(pattern) == 0:
        if tree.value is not None:
            full_list.append((curr, tree.value))

    else:
        head = pattern[0]
        rest = pattern[1:]
        if head == "?":
            for child in tree.children:
                full_list.extend(word_filter(tree.children[child], rest, curr + child))

        if head == "*":
            ##matching one or more
            for child in tree.children:
                full_list.extend(
                    word_filter(tree.children[child], pattern, curr + child)
                )

            ##matching 0
            full_list.extend(word_filter(tree, rest, curr))

        if head in tree.children:
            full_list.extend(word_filter(tree.children[head], rest, curr + head))

    return list(set(full_list))


# you can include test cases of your own in the block below.
if __name__ == "__main__":
    doctest.testmod()
