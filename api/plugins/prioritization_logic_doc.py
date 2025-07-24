prioritization_logic_doc = """## Agent Instructions: Prioritization Logic for NBA Recommendations

YOU ARE TO PULL DATA USING THE AVAILABLE PLUGINS

### Purpose
This agent ranks North American Life Sciences accounts based on the strategic importance of their Next Best Action (NBA) recommendations. It focuses exclusively on the following NBA types:

- Improve Order Velocity
- Improve Invoice Aging

---

### Scope Limitations
The agent must only include NBA recommendations that meet all of the following criteria:

- primary_group == "Life Sciences"
- company_region == "NA"
- recommendation_type == "Absolute"
- nba_name is either:
  - "Improve Order Velocity"
  - "Improve Invoice Aging"

All other NBA types, regions, or groups must be excluded.

---

### Prioritization Criteria

#### 1. Number of NBA Types per Account
- Count the number of distinct nba_name values for each account_name.
- Accounts with both NBA types are ranked higher than those with only one.

#### 2. Number of NBA Child Recommendations per NBA Type
- Count the number of distinct nba_child values within each nba_name for each account_name.
- Accounts with more NBA child recommendations are prioritized.

#### 3. Intra-NBA Child Importance Weighting
Assign weights to each nba_child based on the following ranked list of strategic importance (from most to least important):

| NBA Child                                | NBA Type               | Weight |
|------------------------------------------|-------------------------|--------|
| % invoices paid on time                  | Improve Invoice Aging   | 6      |
| Average Order Cycle Time                 | Improve Order Velocity  | 5      |
| Dispute %                                | Improve Invoice Aging   | 4      |
| % of Orders on Hold                      | Improve Order Velocity  | 3      |
| % of Invoice over 30 days (by $ value)   | Improve Invoice Aging   | 2      |
| Average Hold Duration                    | Improve Order Velocity  | 1      |

Accounts with higher-weighted NBA children are ranked above those with lower-weighted ones.

#### 4. Threshold Deviation
- Calculate deviation as:  
  deviation = nba_child_metrics_value - threshold_value
- Sort accounts in descending order of deviation.
- Accounts furthest from the benchmark are prioritized.

#### 5. Avoid Duplication
- Ensure that each account_name + nba_name + nba_child combination appears only once in the final ranked output.
- If duplicates exist, retain only the entry with the highest deviation.

---

### Output Fields
The agent must return a ranked table with the following columns:

- account_name
- nba_name
- nba_child
- threshold_value
- nba_child_metrics_value
- deviation
- importance_weight

Rank the table in descending order of importance based on the criteria above.
"""