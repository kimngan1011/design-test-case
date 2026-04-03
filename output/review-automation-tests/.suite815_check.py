import json

RUN_CASE_IDS = set([
    661, 664, 666, 667, 668, 673, 674, 675, 676, 708, 711, 712, 713, 715, 717, 719,
    731, 735, 736, 737, 738, 739, 747, 748, 749, 750, 758, 759, 761, 785, 786,
    1013, 1014, 1015, 1016, 1022, 1023, 1039, 1216, 1218, 1263, 1265, 1377, 1456, 1919,
    3144, 3155, 3170, 3171, 3172, 3173, 3178, 3391, 3396, 3495, 3498, 3506, 3510,
    3570, 3571, 3574, 3575, 3585, 3587, 3597, 3787, 6931,
    8293, 8294, 8447, 8451, 8493, 8494, 8497, 8498, 8501, 8502, 8509, 8510, 8513, 8514, 8517, 8518,
    9672, 9673, 9674, 9675, 9676, 9677, 9678, 9680, 9681,
    9734, 9735, 9736, 9737,
    9745, 9746, 9747, 9748, 9749, 9750, 9752, 9753, 9754, 9755, 9756, 9757,
    9763, 9764, 9765, 9766, 9767, 9768, 9770, 9771, 9772, 9773, 9774, 9775,
    9786, 9788, 9789, 9790, 9791,
    10072, 10073, 10074, 10075, 10076, 10077, 10078, 10079,
    11285, 11538, 13747, 13748, 13749, 13750
])

SUITE96 = set(range(10072, 10080))

SUITE815_FILE = "/Users/manabie/Library/Application Support/Code/User/workspaceStorage/c6d55808ef8e9cd506d8bc5970c3e4d1/GitHub.copilot-chat/chat-session-resources/383d2ac7-7b21-4725-ad68-655411f35fe6/toolu_vrtx_01TzrbMsonmQPAmPZkuURTSg__vscode-1775200276113/content.json"
with open(SUITE815_FILE) as f:
    d = json.load(f)

suite815_cases = {c['id']: c for c in d['entities']}
suite815_ids = set(suite815_cases.keys())
print(f"Suite 815 total cases in Qase: {len(suite815_ids)}")

in_run_suite815 = suite815_ids & RUN_CASE_IDS
print(f"\nSuite 815 cases IN this run ({len(in_run_suite815)}):")
for cid in sorted(in_run_suite815):
    case = suite815_cases[cid]
    print(f"  PX-{cid} | auto={case['automation']} | {case['title'][:65]}")

remaining = RUN_CASE_IDS - in_run_suite815 - SUITE96
print(f"\nRemaining cases (-> Automated, not Suite815, not Suite96): {len(remaining)}")
print(f"  {sorted(remaining)}")
