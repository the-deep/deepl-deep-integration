import enchant
from copy import copy
from typing import List, Dict
from collections import defaultdict
import json

EXAMPLE_ENTRY_STRUCTURE = [
    {"id": 1, "text": "vulnerability/pi->children with disabilitie"},
    {"id": 2, "text": "!health."},
    {"id": 3, "text": "Youth (18 to 24 years old)"},
    {"id": 4, "text": "test"},
    {"id": 5, "text": "CAPACITIES and response->national response capacity"},
    {"id": 6, "text": "national response capacity"},
]


def _clean_tag(tag: str):
    return (
        copy(tag)
        .lower()
        .replace("->->", "->")
        .replace("-> ", "->")
        .replace(" ->", "->")
        .replace("->none", "")
        .replace("->n/a", "")
        .replace("\t", "")
        .replace("•", "")
        .replace(".", "")
        .replace(",", "")
        .replace("!", "")
        .replace("?", "")
    )


def _short_distance_matching(tag, matching_dict: Dict[str, List[str]]):
    distances = defaultdict(list)
    for k, v in matching_dict.items():
        dist = enchant.utils.levenshtein(k, tag)
        min_distance = 1 + (len(k) // 10)
        if dist <= min_distance:
            distances[k].append(-dist)  # neg value so we get the min sum in the end

    if len(distances) == 0:
        return []
    else:
        distances = {k: sum(v) for k, v in distances.items()}
        min_key = min(distances, key=distances.get)
        return matching_dict[min_key]


def _one_tag2nlp_match(tag, matching_dict) -> List[str]:

    if type(tag) is str:
        clean_tag = _clean_tag(tag)
        mapped_tag = matching_dict.get(clean_tag)
        if mapped_tag is None:
            return _short_distance_matching(clean_tag, matching_dict)
        else:
            return mapped_tag
    else:
        return []


def af2nlp_matching(
    tags: List[Dict[int, str]],
    matching_dict_path="nlp_mapping_files/mapping_tags_nlp2original.json",
) -> List[List[str]]:
    with open(matching_dict_path, "r") as f:
        matching_dict = json.load(f)

    return {
        one_original_af_tag["id"]: _one_tag2nlp_match(
            one_original_af_tag["text"], matching_dict
        )
        for one_original_af_tag in tags
    }
