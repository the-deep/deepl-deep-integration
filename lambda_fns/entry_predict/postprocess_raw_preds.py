pillars_1d_tags = [
    "Covid-19",
    "Casualties",
    "Context",
    "Displacement",
    "Humanitarian Access",
    "Shock/Event",
    "Information And Communication",
]

pillars_2d_tags = [
    "At Risk",
    "Priority Interventions",
    "Capacities & Response",
    "Humanitarian Conditions",
    "Impact",
    "Priority Needs",
]

output_columns = [
    "sectors",
    "subpillars_2d",
    "subpillars_1d",
    "gender",
    "age",
    "severity",
    "specific_needs_groups",
    "affected_groups",
]

primary_tags = ["sectors", "subpillars_2d", "subpillars_1d"]
secondary_tags = ["age", "gender", "affected_groups", "specific_needs_groups"]


def get_predictions_all(
    ratio_proba_threshold,
    output_columns=output_columns,
    pillars_2d=pillars_2d_tags,
    pillars_1d=pillars_1d_tags,
    nb_entries: int = 1,
    ratio_nb: int = 1,
):

    predictions = {column: [] for column in output_columns}
    for entry_nb in range(nb_entries):
        returns_sectors = ratio_proba_threshold["sectors"][entry_nb]

        returns_subpillars = ratio_proba_threshold["subpillars"][entry_nb]

        subpillars_2d_tags = {
            key: value
            for key, value in returns_subpillars.items()
            if key.split("->")[0] in pillars_2d
        }
        subpillars_1d_tags = {
            key: value
            for key, value in returns_subpillars.items()
            if key.split("->")[0] in pillars_1d
        }

        ratios_sectors_subpillars_2d = list(returns_sectors.values()) + list(
            subpillars_2d_tags.values()
        )

        if any([item >= ratio_nb for item in ratios_sectors_subpillars_2d]):
            preds_2d = get_preds_entry(subpillars_2d_tags, True, ratio_nb)
            preds_sectors = get_preds_entry(returns_sectors, True, ratio_nb)

        else:
            preds_2d = []
            preds_sectors = []

        predictions["sectors"].append(preds_sectors)
        predictions["subpillars_2d"].append(preds_2d)

        preds_1d = get_preds_entry(subpillars_1d_tags, False, ratio_nb)
        predictions["subpillars_1d"].append(preds_1d)

        returns_sec_tags = ratio_proba_threshold["secondary_tags"][entry_nb]
        preds_entry = get_preds_entry(returns_sec_tags, False, ratio_nb)

        for secondary_tag in [
            "age",
            "gender",
            "affected_groups",
            "specific_needs_groups",
        ]:
            preds_sec_tag = [
                item.split("->")[1]
                for item in preds_entry
                if item.split("->")[0] == secondary_tag
            ]
            predictions[secondary_tag].append(preds_sec_tag)

        severity_tags = {
            key: value
            for key, value in returns_sec_tags.items()
            if key.split("->")[0] == "severity"
        }
        if any(["Humanitarian Conditions" in item for item in preds_2d]):
            preds_severity = get_preds_entry(severity_tags, True, ratio_nb, True)
            preds_severity = [item.split("->")[1] for item in preds_severity]
        else:
            preds_severity = []
        predictions["severity"].append(preds_severity)

    return predictions


def get_preds_entry(
    preds_column, return_at_least_one=True, ratio_nb=1, return_only_one=False
):
    preds_entry = [
        sub_tag
        for sub_tag in list(preds_column.keys())
        if preds_column[sub_tag] > ratio_nb
    ]
    if return_only_one:
        preds_entry = [
            sub_tag
            for sub_tag in list(preds_column.keys())
            if preds_column[sub_tag] == max(list(preds_column.values()))
        ]
    if return_at_least_one:
        if len(preds_entry) == 0:
            preds_entry = [
                sub_tag
                for sub_tag in list(preds_column.keys())
                if preds_column[sub_tag] == max(list(preds_column.values()))
            ]
    return preds_entry


def get_clean_thresholds(
    thresholds,
    output_columns=output_columns,
    pillars_2d=pillars_2d_tags,
    pillars_1d=pillars_1d_tags,
    primary_tags=primary_tags,
    secondary_tags=secondary_tags,
):

    final_thresholds = {name: {} for name in output_columns}
    final_thresholds["sectors"] = thresholds["sectors"]
    subpillars_thresholds = thresholds["subpillars"]

    subpillars_2d_thresholds = {
        key: value
        for key, value in subpillars_thresholds.items()
        if key.split("->")[0] in pillars_2d
    }
    subpillars_1d_thresholds = {
        key: value
        for key, value in subpillars_thresholds.items()
        if key.split("->")[0] in pillars_1d
    }
    final_thresholds["subpillars_2d"] = subpillars_2d_thresholds
    final_thresholds["subpillars_1d"] = subpillars_1d_thresholds

    secondary_tags_thresholds = thresholds["secondary_tags"]
    for secondary_tag in ["age", "gender", "affected_groups", "specific_needs_groups"]:
        final_thresholds[secondary_tag] = {
            key.split("->")[1]: value
            for key, value in secondary_tags_thresholds.items()
            if key.split("->")[0] == secondary_tag
        }

    output_ratios = {
        "primary_tags": {key: final_thresholds[key] for key in primary_tags},
        "secondary_tags": {key: final_thresholds[key] for key in secondary_tags},
    }
    return output_ratios


def get_clean_ratios(
    ratios,
    output_columns=output_columns,
    pillars_2d=pillars_2d_tags,
    pillars_1d=pillars_1d_tags,
    primary_tags=primary_tags,
    secondary_tags=secondary_tags,
    nb_entries: int = 1,
):

    final_ratios = {name: [] for name in output_columns}
    final_ratios["sectors"] = ratios["sectors"]

    subpillars_ratios = ratios["subpillars"]
    secondary_tags_ratios = ratios["secondary_tags"]

    for i in range(nb_entries):
        subpillars_2d_ratio_tmp = {
            key: value
            for key, value in subpillars_ratios[i].items()
            if key.split("->")[0] in pillars_2d
        }

        subpillars_1d_ratio_tmp = {
            key: value
            for key, value in subpillars_ratios[i].items()
            if key.split("->")[0] in pillars_1d
        }

        final_ratios["subpillars_2d"].append(subpillars_2d_ratio_tmp)
        final_ratios["subpillars_1d"].append(subpillars_1d_ratio_tmp)

        for secondary_tag in secondary_tags:
            secondary_tags_ratios_tmp = {
                key.split("->")[1]: value
                for key, value in secondary_tags_ratios[i].items()
                if key.split("->")[0] == secondary_tag
            }
            final_ratios[secondary_tag].append(secondary_tags_ratios_tmp)

    output_ratios = {
        "primary_tags": {key: final_ratios[key] for key in primary_tags},
        "secondary_tags": {key: final_ratios[key] for key in secondary_tags},
    }
    return output_ratios
