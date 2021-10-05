# HWM2
*Author : Wen-Ling Chi*
*10/04/2021*

1. Execute `preprocessing.py`
Output: `dating.csv` and the following result

```
Quotes removed from 8316 cells.
=============================================
Standardized 5707 cells to lower case.
=============================================
Value assigned for male in column gender: 1.
Value assigned for European/Caucasian-American in column race: 2.
Value assigned for Latino/Hispanic American in column race o: 3.
Value assigned for law in column field: 121.
=============================================
Mean of attractive_important: 0.22.
Mean of sincere_important: 0.17.
Mean of intelligence_important: 0.20.
Mean of funny_important: 0.17.
Mean of ambition_important: 0.11.
Mean of shared_interests_important: 0.12.
Mean of pref_o_attractive: 0.22.
Mean of pref_o_sincere: 0.17.
Mean of pref_o_intelligence: 0.20.
Mean of pref_o_funny: 0.17.
Mean of pref_o_ambitious: 0.11.
Mean of pref_o_shared_interests: 0.12.
```

2. Execute `2_1.py`
Output: `img/gender_attributes.jpg` and the following result
```
Male data
Mean of pref_o_attractive : 0.27
Mean of pref_o_sincere : 0.17
Mean of pref_o_intelligence : 0.20
Mean of pref_o_funny : 0.18
Mean of pref_o_ambitious : 0.08
Mean of pref_o_shared_interests : 0.11
==================================
Female data
Mean of pref_o_attractive : 0.18
Mean of pref_o_sincere : 0.18
Mean of pref_o_intelligence : 0.21
Mean of pref_o_funny : 0.17
Mean of pref_o_ambitious : 0.13
Mean of pref_o_shared_interests : 0.13
==================================
```

3. Execute `2_2.py`
Output : you will get six images which locate at `ima/`
* attractive_partner_success_rate.jpg
* ambition_partner_success_rate.jpg
* funny_partner_success_rate.jpg
* intelligence_parter_success_rate.jpg
* shared_interests_partner_success_rate.jpg
* sincere_partner_success_rate.jpg

4. Execute `deicretize.py`
Output : `dating-binned.csv` and the following result
```
age: [3710, 2932, 97, 0, 5]
age_o: [3704, 2899, 136, 0, 5]
importance_same_race: [2980, 1213, 977, 1013, 561]
importance_same_religion: [3203, 1188, 1110, 742, 501]
pref_o_attractive: [4333, 1987, 344, 51, 29]
pref_o_sincere: [1416, 4378, 865, 79, 6]
pref_o_intelligence: [666, 3935, 1873, 189, 81]
pref_o_funny: [1255, 4361, 1048, 55, 25]
pref_o_ambitious: [1963, 2352, 2365, 42, 22]
pref_o_shared_interests: [1506, 2068, 1981, 1042, 147]
attractive_important: [4323, 2017, 328, 57, 19]
sincere_important: [546, 2954, 2782, 377, 85]
intelligence_important: [630, 3976, 1861, 210, 67]
funny_important: [1282, 4306, 1070, 58, 28]
ambition_important: [1913, 2373, 2388, 49, 21]
shared_interests_important: [1464, 2197, 1950, 1007, 126]
attractive: [131, 726, 899, 4122, 866]
sincere: [57, 228, 352, 2715, 3392]
intelligence: [127, 409, 732, 3190, 2286]
funny: [19, 74, 1000, 2338, 3313]
ambition: [225, 697, 559, 2876, 2387]
attractive_partner: [284, 948, 2418, 2390, 704]
sincere_partner: [94, 353, 1627, 3282, 1388]
intelligence_parter: [36, 193, 1509, 3509, 1497]
funny_partner: [279, 733, 2296, 2600, 836]
ambition_partner: [119, 473, 2258, 2804, 1090]
shared_interests_partner: [701, 1269, 2536, 1774, 464]
sports: [650, 961, 1369, 2077, 1687]
tvsports: [2151, 1292, 1233, 1383, 685]
exercise: [619, 952, 1775, 2115, 1283]
dining: [39, 172, 1118, 2797, 2618]
museums: [117, 732, 1417, 2737, 1741]
art: [224, 946, 1557, 2500, 1517]
hiking: [963, 1386, 1575, 1855, 965]
gaming: [2565, 2338, 1598, 168, 75]
clubbing: [912, 1068, 1668, 2193, 903]
reading: [331, 633, 2953, 2778, 49]
tv: [1188, 1216, 1999, 1642, 699]
theater: [288, 811, 1585, 2300, 1760]
movies: [144, 462, 530, 2783, 2825]
concerts: [222, 777, 1752, 2282, 1711]
music: [62, 196, 1106, 2583, 2797]
shopping: [1093, 1098, 1709, 1643, 1201]
yoga: [2285, 1392, 1369, 1056, 642]
interests_correlate: [75, 985, 2312, 2597, 773]
expected_happy_with_sd_people: [321, 1262, 3292, 1596, 273]
like: [273, 865, 2539, 2560, 507]
```

5. Execute `split.py`
Output : `trainingSet.csv` and `testSet.csv.`

6. Execute `5_1.py`
Output : 
```
Training Accuracy: 0.76
Testing Accuracy: 0.75
```

7. Execute `5_2.py`
Output : `img/(5_2)different_bins.jpg`

    When you execute this code, it will take at least 10 minutes.

8. Execute `5_3.py`
Output : `img/(5_3)different_fraction.jpg`
