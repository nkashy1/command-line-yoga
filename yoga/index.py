"""
Build indices of words from a document or a corpus of documents
"""

from typing import Dict, List

def index_document(document: str) -> Dict[str, List[int]]:
    """
    Build an index of words in a single document
    """
    words = document.split()
    word_index: Dict[str, List[int]] = {}
    for i, raw_word in enumerate(words):
        word = raw_word.lower()
        if word_index.get(word) is None:
            word_index[word] = []
        word_index[word].append(i)

    return word_index
