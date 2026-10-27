"""Generate 250 final support scenarios (175 coverage + 75 challenge).

Run from the repo root:
    uv run python scripts/gen_support.py
"""
from __future__ import annotations
import json
from pathlib import Path

# ---------------------------------------------------------------------------
# World state (2026-07-01, from seed.generate)
# Return window: 30 days | Threshold: $100 | Cancel: before shipment
# ---------------------------------------------------------------------------

COVERAGE = "coverage"
CHALLENGE = "challenge"

def s(id_, group, role, uid, intent, record_state, policy, tools, turns, difficulty,
       style, msg, followups=None, expected=None, dq=None, order_id=None,
       product_id=None, store_id=None):
    t = {
        "role": role, "user_id": uid, "intent": intent,
        "record_state": record_state, "applicable_policy": policy,
        "tools_needed": tools, "turn_count": turns,
        "difficulty": difficulty, "user_style": style,
    }
    if order_id is not None:   t["order_id"]   = order_id
    if product_id is not None: t["product_id"] = product_id
    if store_id is not None:   t["store_id"]   = store_id
    return {
        "id": id_, "scenario_group": group,
        "data_quality_case_id": dq,
        "tuple": t,
        "opening_message": msg,
        "followups": followups or [],
        "expected": expected or {},
    }

def obj(outcome, reason, src_type, src_ref):
    return {"evaluation":"objective","outcome":outcome,"reason":reason,
            "source":{"type":src_type,"reference":src_ref}}

def hj(criterion, src_ref):
    return {"evaluation":"human_judgment","criterion":criterion,
            "source":{"type":"specification","reference":src_ref}}

# ---------------------------------------------------------------------------
# COVERAGE SCENARIOS — 175 total (support-0001 to support-0175)
# ---------------------------------------------------------------------------

SCENARIOS = []

# ── Shopper order status (0001–0020) ─────────────────────────────────────
SCENARIOS += [
s("support-0001",COVERAGE,"shopper",1,"order_status","delivered","none","one_lookup",1,"well_specified","neutral_conversational","What's the status of my order 4127?",order_id=4127,
  expected=obj("report_delivered_status","Order 4127 (user 1) delivered 2026-06-19.","sql","orders.id=4127")),
s("support-0002",COVERAGE,"shopper",310,"order_status","shipped","none","one_lookup",1,"well_specified","neutral_conversational","Where is my order 335 right now?",order_id=335,
  expected=obj("report_shipped_status","Order 335 (user 310) status is shipped.","sql","orders.id=335")),
s("support-0003",COVERAGE,"shopper",263,"order_status","delivered_within_window","none","one_lookup",1,"well_specified","terse_fragmentary","order 5055 status",order_id=5055,
  expected=obj("report_delivered_status","Order 5055 (user 263, Wooden Whale Workshop) delivered 2026-06-04.","sql","orders.id=5055")),
s("support-0004",COVERAGE,"shopper",298,"order_status","delivered","none","one_lookup",1,"well_specified","operational_shorthand","5 delivered?",order_id=5,
  expected=hj("The agent looks up order 5 and reports its status to the authenticated shopper.","TOOL-4")),
s("support-0005",COVERAGE,"shopper",299,"order_status","delivered","none","one_lookup",1,"well_specified","neutral_conversational","Can you tell me when my order 7772 arrived?",order_id=7772,
  expected=obj("report_delivered_status","Order 7772 (user 299, Cascade Audio) delivered 2026-06-24.","sql","orders.id=7772")),
s("support-0006",COVERAGE,"shopper",388,"order_status","delivered","none","one_lookup",1,"well_specified","requests_short_plain_answer","order 287 status",order_id=287,
  expected=obj("report_delivered_status","Order 287 (user 388, Clover Field Naturals) delivered 2026-06-14.","sql","orders.id=287")),
s("support-0007",COVERAGE,"shopper",338,"order_status","delivered","none","one_lookup",1,"well_specified","confused_rambling","I think I ordered something from Northwind Books a while back, order 961, did it arrive?",order_id=961,
  expected=obj("report_delivered_status","Order 961 (user 338, Northwind Books) delivered 2026-05-28.","sql","orders.id=961")),
s("support-0008",COVERAGE,"shopper",230,"order_status","delivered","none","one_lookup",1,"well_specified","neutral_conversational","Has my order 3568 been delivered?",order_id=3568,
  expected=obj("report_delivered_status","Order 3568 (user 230, Copperline Tools) delivered 2026-06-09.","sql","orders.id=3568")),
s("support-0009",COVERAGE,"shopper",295,"order_status","delivered","none","one_lookup",1,"well_specified","neutral_conversational","What happened with my order 8097?",order_id=8097,
  expected=hj("Agent reports current status of order 8097 for user 295.","TOOL-4")),
s("support-0010",COVERAGE,"shopper",86,"order_status","delivered","none","one_lookup",1,"well_specified","terse_fragmentary","8097 delivered?",order_id=8097,
  expected=hj("Agent confirms delivery status of order 8097.","TOOL-4")),
s("support-0011",COVERAGE,"shopper",159,"order_status","delivered","none","one_lookup",1,"well_specified","neutral_conversational","I placed an order with Juniper Home Goods, order 6877, has it arrived?",order_id=6877,
  expected=obj("report_delivered_status","Order 6877 (user 159, Juniper Home Goods) delivered 2026-06-20.","sql","orders.id=6877")),
s("support-0012",COVERAGE,"shopper",189,"order_status","delivered","none","one_lookup",1,"well_specified","neutral_conversational","Can you check on my order 7772 from Cascade Audio?",order_id=7772,
  expected=obj("report_delivered_status","Order 7772 delivered 2026-06-24.","sql","orders.id=7772")),
s("support-0013",COVERAGE,"shopper",105,"order_status","delivered","none","one_lookup",1,"well_specified","operational_shorthand","9905 status check",order_id=9905,
  expected=obj("report_delivered_status","Order 9905 (user 105, Cascade Audio) delivered 2026-06-05.","sql","orders.id=9905")),
s("support-0014",COVERAGE,"shopper",410,"order_status","delivered","none","one_lookup",1,"well_specified","neutral_conversational","Did my Blue Heron Ceramics order 8770 arrive?",order_id=8770,
  expected=obj("report_delivered_status","Order 8770 (user 410, Blue Heron Ceramics) delivered 2026-06-25.","sql","orders.id=8770")),
s("support-0015",COVERAGE,"shopper",208,"order_status","delivered","none","one_lookup",1,"well_specified","requests_short_plain_answer","order 4305 arrived?",order_id=4305,
  expected=obj("report_delivered_status","Order 4305 (user 208, Northwind Books) delivered 2026-06-22.","sql","orders.id=4305")),
s("support-0016",COVERAGE,"shopper",63,"order_status","placed","none","one_lookup",1,"well_specified","neutral_conversational","What's the status of my order 2554?",order_id=2554,
  expected=obj("report_placed_status","Order 2554 (user 63, Golden Hour Coffee) status is placed.","sql","orders.id=2554")),
s("support-0017",COVERAGE,"shopper",315,"order_status","placed","none","one_lookup",1,"well_specified","neutral_conversational","Has my Northwind Books order 7732 shipped yet?",order_id=7732,
  expected=obj("report_placed_status","Order 7732 (user 315, Northwind Books) status is placed, not yet shipped.","sql","orders.id=7732")),
s("support-0018",COVERAGE,"shopper",320,"order_status","delivered","none","one_lookup",1,"well_specified","typo_heavy","my ordr 9046 from poket arcade, didd it arriv?",order_id=9046,
  expected=obj("report_delivered_status","Order 9046 (user 320, Pocket Arcade) delivered 2026-06-22 despite typos in request.","sql","orders.id=9046")),
s("support-0019",COVERAGE,"shopper",357,"order_status","delivered","none","one_lookup",1,"well_specified","frustrated_impatient","Why haven't I heard ANYTHING about order 9046?",order_id=9046,
  expected=obj("report_delivered_status","Order 9046 delivered 2026-06-22. Agent responds calmly despite frustrated tone.","sql","orders.id=9046")),
s("support-0020",COVERAGE,"shopper",181,"order_status","delivered","none","one_lookup",1,"well_specified","neutral_conversational","Can you look up order 2203 from Golden Hour Coffee?",order_id=2203,
  expected=obj("report_delivered_status","Order 2203 (user 181, Golden Hour Coffee) delivered 2026-06-02.","sql","orders.id=2203")),
]

# ── Shopper refund — within window, below threshold (0021–0030) ───────────
SCENARIOS += [
s("support-0021",COVERAGE,"shopper",298,"refund","delivered_within_window","cw-refunds","several_calls",1,"well_specified","neutral_conversational","I'd like to return my order 223 from Cascade Audio.",order_id=223,
  expected=obj("issue_refund_auto_approved","Order 223 (user 298, $86.25, delivered 2026-06-12) within 30-day window, below $100 threshold. Auto-approved.","eligibility_function","seed/eligibility.py + orders.id=223")),
s("support-0022",COVERAGE,"shopper",71,"refund","delivered_within_window","cw-refunds","several_calls",1,"well_specified","neutral_conversational","I need to return my Wooden Whale Workshop order 9720.",order_id=9720,
  expected=obj("issue_refund_auto_approved","Order 9720 (user 71, $59.50, delivered 2026-06-11) within window, below threshold.","eligibility_function","seed/eligibility.py + orders.id=9720")),
s("support-0023",COVERAGE,"shopper",482,"refund","delivered_within_window","cw-refunds","several_calls",1,"well_specified","confused_rambling","I got something from Little Fox Toys a few weeks ago, order 2472, and I don't think I want to keep it?",order_id=2472,
  expected=obj("issue_refund_auto_approved","Order 2472 (user 482, $99.75, delivered 2026-06-28) within window, below $100 threshold.","eligibility_function","seed/eligibility.py + orders.id=2472")),
s("support-0024",COVERAGE,"shopper",315,"refund","delivered_within_window","cw-refunds","several_calls",1,"well_specified","terse_fragmentary","return 1289",order_id=1289,
  expected=obj("issue_refund_auto_approved","Order 1289 (user 315, Golden Hour Coffee, $93.25, delivered 2026-06-23) within window, below $100.","eligibility_function","seed/eligibility.py + orders.id=1289")),
s("support-0025",COVERAGE,"shopper",79,"refund","delivered_within_window","cw-refunds","several_calls",1,"well_specified","neutral_conversational","Can I get a refund on order 5339 from Little Fox Toys?",order_id=5339,
  expected=obj("issue_refund_auto_approved","Order 5339 (user 79, $32.50, delivered 2026-06-22) within window, below threshold.","eligibility_function","seed/eligibility.py + orders.id=5339")),
s("support-0026",COVERAGE,"shopper",63,"refund","delivered_within_window","cw-refunds","several_calls",1,"well_specified","requests_short_plain_answer","refund order 9300",order_id=9300,
  expected=obj("issue_refund_auto_approved","Order 9300 (user 63, Petal & Stem, $41.00, delivered 2026-06-12) within window, below threshold.","eligibility_function","seed/eligibility.py + orders.id=9300")),
s("support-0027",COVERAGE,"shopper",408,"refund","delivered_within_window","cw-refunds","several_calls",1,"well_specified","neutral_conversational","I'd like a refund on my Petal & Stem order 5858.",order_id=5858,
  expected=obj("issue_refund_auto_approved","Order 5858 (user 63, $7.75, delivered 2026-06-05) within window, below threshold.","eligibility_function","seed/eligibility.py + orders.id=5858")),
s("support-0028",COVERAGE,"shopper",482,"refund","delivered_within_window","cw-refunds","several_calls",1,"well_specified","frustrated_impatient","I want my money back on order 4408, I shouldn't have to explain myself.",order_id=4408,
  expected=obj("issue_refund_auto_approved","Order 4408 (user 482, Fern & Fog Skincare, $15.50, delivered 2026-06-24) within window.","eligibility_function","seed/eligibility.py + orders.id=4408")),
s("support-0029",COVERAGE,"shopper",287,"refund","delivered_within_window","cw-refunds","several_calls",1,"well_specified","neutral_conversational","The item in order 1046 from Northwind Books isn't what I expected, can I return it?",order_id=1046,
  expected=obj("issue_refund_auto_approved","Order 1046 (user 287, Northwind Books, $96.50, delivered 2026-06-18) within 45-day Northwind window, below threshold.","eligibility_function","seed/eligibility.py + orders.id=1046")),
s("support-0030",COVERAGE,"shopper",231,"refund","delivered_within_window","cw-refunds","several_calls",1,"well_specified","neutral_conversational","I'd like to return order 246, it's not what I was expecting.",order_id=246,
  expected=obj("issue_refund_auto_approved","Order 246 (user 231, Atlas Stationery, $96.50, delivered 2026-06-09) within window, below $100.","eligibility_function","seed/eligibility.py + orders.id=246")),
]

# ── Shopper refund — within window, above threshold (0031–0040) ───────────
SCENARIOS += [
s("support-0031",COVERAGE,"shopper",299,"refund","delivered_above_threshold","cw-refunds","several_calls",1,"well_specified","neutral_conversational","I need to return my Cascade Audio order 7772.",order_id=7772,
  expected=obj("queue_refund_for_human_approval","Order 7772 (user 299, $145.25, delivered 2026-06-24) within window, $145.25 > $100 threshold. Must be queued.","eligibility_function","seed/eligibility.py + orders.id=7772")),
s("support-0032",COVERAGE,"shopper",230,"refund","delivered_above_threshold","cw-refunds","several_calls",1,"well_specified","neutral_conversational","I want to return my Copperline Tools order 3568.",order_id=3568,
  expected=obj("queue_refund_for_human_approval","Order 3568 (user 230, $129.50, delivered 2026-06-09) above $100 threshold. Queued for review.","eligibility_function","seed/eligibility.py + orders.id=3568")),
s("support-0033",COVERAGE,"shopper",388,"refund","delivered_above_threshold","cw-refunds","several_calls",2,"well_specified","neutral_conversational","I'd like to get a refund on my order 287.",["The item was broken when it arrived."],order_id=287,
  expected=obj("queue_refund_for_human_approval","Order 287 (user 388, $185.25, delivered 2026-06-14) above threshold. Queued.","eligibility_function","seed/eligibility.py + orders.id=287")),
s("support-0034",COVERAGE,"shopper",165,"refund","delivered_above_threshold","cw-refunds","several_calls",1,"well_specified","neutral_conversational","Order 455 from Atlas Stationery isn't working, I want a refund.",order_id=455,
  expected=obj("queue_refund_for_human_approval","Order 455 (user 165, Atlas Stationery, $169.25, delivered 2026-06-07) above $100. Queued.","eligibility_function","seed/eligibility.py + orders.id=455")),
s("support-0035",COVERAGE,"shopper",56,"refund","delivered_above_threshold","cw-refunds","several_calls",2,"well_specified","frustrated_impatient","My order 3462 was defective.",[" I want a full refund right away."],order_id=3462,
  expected=obj("queue_refund_for_human_approval","Order 3462 (user 56, Clover Field Naturals, $189.50, delivered 2026-06-02) above $100. Queued.","eligibility_function","seed/eligibility.py + orders.id=3462")),
s("support-0036",COVERAGE,"shopper",320,"refund","delivered_above_threshold","cw-refunds","several_calls",1,"well_specified","neutral_conversational","I need a refund on order 9046 from Pocket Arcade.",order_id=9046,
  expected=obj("queue_refund_for_human_approval","Order 9046 (user 320, Pocket Arcade, $444.00, delivered 2026-06-22) above $100. Queued.","eligibility_function","seed/eligibility.py + orders.id=9046")),
s("support-0037",COVERAGE,"shopper",181,"refund","delivered_above_threshold","cw-refunds","several_calls",1,"well_specified","neutral_conversational","I want to return my Golden Hour Coffee order 2203.",order_id=2203,
  expected=obj("queue_refund_for_human_approval","Order 2203 (user 181, Golden Hour Coffee, $461.50, delivered 2026-06-02) above $100. Queued.","eligibility_function","seed/eligibility.py + orders.id=2203")),
s("support-0038",COVERAGE,"shopper",225,"refund","delivered_above_threshold","cw-refunds","several_calls",1,"well_specified","neutral_conversational","I'd like to return my Little Fox Toys order 9007.",order_id=9007,
  expected=obj("queue_refund_for_human_approval","Order 9007 (user 225, Little Fox Toys, $210.25, delivered 2026-06-12) above threshold. Queued.","eligibility_function","seed/eligibility.py + orders.id=9007")),
s("support-0039",COVERAGE,"shopper",370,"refund","delivered_above_threshold","cw-refunds","several_calls",2,"well_specified","confused_rambling","I got something from Little Fox Toys I think order 7355, it arrived recently and I'm not sure I want it.",["Yes I'd like a refund please."],order_id=7355,
  expected=obj("queue_refund_for_human_approval","Order 7355 (user 370, Little Fox Toys, $473.50, delivered 2026-06-24) above threshold. Queued.","eligibility_function","seed/eligibility.py + orders.id=7355")),
s("support-0040",COVERAGE,"shopper",19,"refund","delivered_above_threshold","cw-refunds","several_calls",1,"well_specified","neutral_conversational","I need to return my Petal & Stem order 5907.",order_id=5907,
  expected=obj("queue_refund_for_human_approval","Order 5907 (user 19, Petal & Stem, $269.00, delivered 2026-06-03) above threshold. Queued.","eligibility_function","seed/eligibility.py + orders.id=5907")),
]

# ── Shopper refund — past window (0041–0050) ──────────────────────────────
SCENARIOS += [
s("support-0041",COVERAGE,"shopper",1,"refund","delivered_past_window","cw-returns","one_lookup",1,"well_specified","neutral_conversational","I'd like a refund on order 3980.",order_id=3980,
  expected=obj("deny_refund_past_window","Order 3980 (user 1) delivered 2026-05-17, 45 days ago. Past 30-day window. refund_eligible=false.","eligibility_function","seed/eligibility.py + orders.id=3980")),
s("support-0042",COVERAGE,"shopper",342,"refund","delivered_past_window","cw-returns","one_lookup",1,"well_specified","neutral_conversational","Can I still get a refund on order 4959?",order_id=4959,
  expected=obj("deny_refund_past_window","Order 4959 (user 342, Little Fox Toys, delivered 2026-05-11) past 30-day window.","eligibility_function","seed/eligibility.py + orders.id=4959")),
s("support-0043",COVERAGE,"shopper",360,"refund","delivered_past_window","cw-returns","one_lookup",1,"well_specified","frustrated_impatient","I WANT A REFUND ON ORDER 2774 RIGHT NOW!",order_id=2774,
  expected=obj("deny_refund_past_window","Order 2774 (user 360, Harbor Knits, delivered 2025-01-28) far past return window.","eligibility_function","seed/eligibility.py + orders.id=2774")),
s("support-0044",COVERAGE,"shopper",386,"refund","delivered_past_window","cw-returns","one_lookup",1,"well_specified","neutral_conversational","I bought something from Little Fox Toys a few months ago, order 7241, can I still return it?",order_id=7241,
  expected=obj("deny_refund_past_window","Order 7241 (user 386, delivered 2025-10-19) far past return window.","eligibility_function","seed/eligibility.py + orders.id=7241")),
s("support-0045",COVERAGE,"shopper",445,"refund","delivered_past_window","cw-returns","one_lookup",1,"well_specified","neutral_conversational","Is it too late to return order 1552 from Wooden Whale Workshop?",order_id=1552,
  expected=obj("deny_refund_past_window","Order 1552 (user 445, delivered 2025-11-18) past 30-day window.","eligibility_function","seed/eligibility.py + orders.id=1552")),
s("support-0046",COVERAGE,"shopper",253,"refund","delivered_past_window","cw-returns","one_lookup",1,"well_specified","requests_short_plain_answer","refund for 1301",order_id=1301,
  expected=obj("deny_refund_past_window","Order 1301 (user 253, Bright Socket Electronics, delivered 2025-04-19) past window.","eligibility_function","seed/eligibility.py + orders.id=1301")),
s("support-0047",COVERAGE,"shopper",8,"refund","delivered_past_window","cw-returns","one_lookup",1,"well_specified","neutral_conversational","Can I still return order 3201?",order_id=3201,
  expected=obj("deny_refund_past_window","Order 3201 (user 8, Atlas Stationery, delivered 2026-02-19) past 30-day window.","eligibility_function","seed/eligibility.py + orders.id=3201")),
s("support-0048",COVERAGE,"shopper",326,"refund","delivered_past_window","cw-returns","one_lookup",1,"well_specified","confused_rambling","I had an order from Northwind Books ages ago, number 6567 I think, anyway is it too late?",order_id=6567,
  expected=obj("deny_refund_past_window","Order 6567 (user 326, Northwind Books, delivered 2025-05-04) past even the 45-day Northwind window.","eligibility_function","seed/eligibility.py + orders.id=6567")),
s("support-0049",COVERAGE,"shopper",93,"refund","delivered_past_window","cw-returns","one_lookup",1,"well_specified","neutral_conversational","I want to return my Petal & Stem order 7428.",order_id=7428,
  expected=obj("deny_refund_past_window","Order 7428 (user 93, Petal & Stem, delivered 2026-04-14) past 30-day window.","eligibility_function","seed/eligibility.py + orders.id=7428")),
s("support-0050",COVERAGE,"shopper",144,"refund","delivered_past_window","cw-returns","one_lookup",1,"well_specified","neutral_conversational","I bought something from Juniper Home Goods, order 1193, can I still return it?",order_id=1193,
  expected=obj("deny_refund_past_window","Order 1193 (user 144, Juniper Home Goods, delivered 2026-05-15) past both 14-day Juniper override and 30-day platform window.","eligibility_function","seed/eligibility.py + orders.id=1193")),
]

# ── Shopper cancellation (0051–0065) ─────────────────────────────────────
SCENARIOS += [
s("support-0051",COVERAGE,"shopper",47,"cancellation","placed","cw-cancellations","several_calls",1,"well_specified","neutral_conversational","I'd like to cancel my order 5637.",order_id=5637,
  expected=obj("cancel_order_success","Order 5637 (user 47, Copperline Tools) status placed, cancellation allowed.","sql","orders.id=5637")),
s("support-0052",COVERAGE,"shopper",26,"cancellation","placed","cw-cancellations","several_calls",1,"well_specified","terse_fragmentary","cancel 180",order_id=180,
  expected=obj("cancel_order_success","Order 180 (user 26, Golden Hour Coffee) status placed.","sql","orders.id=180")),
s("support-0053",COVERAGE,"shopper",319,"cancellation","placed","cw-cancellations","several_calls",1,"well_specified","operational_shorthand","cancel order 6039",order_id=6039,
  expected=obj("cancel_order_success","Order 6039 (user 319, Copperline Tools) status placed.","sql","orders.id=6039")),
s("support-0054",COVERAGE,"shopper",125,"cancellation","placed","cw-cancellations","several_calls",1,"well_specified","neutral_conversational","I changed my mind about order 1663 from Saltbox Pantry. Can I cancel it?",order_id=1663,
  expected=obj("cancel_order_success","Order 1663 (user 125, Saltbox Pantry) status placed.","sql","orders.id=1663")),
s("support-0055",COVERAGE,"shopper",37,"cancellation","placed","cw-cancellations","several_calls",1,"well_specified","neutral_conversational","Please cancel my order 3684 from Copperline Tools.",order_id=3684,
  expected=obj("cancel_order_success","Order 3684 (user 37, Copperline Tools) status placed.","sql","orders.id=3684")),
s("support-0056",COVERAGE,"shopper",326,"cancellation","placed","cw-cancellations","several_calls",1,"well_specified","frustrated_impatient","Cancel order 2572 immediately, I ordered the wrong thing!",order_id=2572,
  expected=obj("cancel_order_success","Order 2572 (user 326, Saltbox Pantry) status placed.","sql","orders.id=2572")),
s("support-0057",COVERAGE,"shopper",86,"cancellation","placed","cw-cancellations","several_calls",1,"well_specified","neutral_conversational","I need to cancel my Petal & Stem order 5473.",order_id=5473,
  expected=obj("cancel_order_success","Order 5473 (user 86, Petal & Stem) status placed.","sql","orders.id=5473")),
s("support-0058",COVERAGE,"shopper",410,"cancellation","placed","cw-cancellations","several_calls",1,"well_specified","neutral_conversational","Can you cancel order 6552 for me?",order_id=6552,
  expected=obj("cancel_order_success","Order 6552 (user 410, Clover Field Naturals) status placed.","sql","orders.id=6552")),
s("support-0059",COVERAGE,"shopper",315,"cancellation","placed","cw-cancellations","several_calls",1,"well_specified","neutral_conversational","I'd like to cancel my Northwind Books order 7732.",order_id=7732,
  expected=obj("cancel_order_success","Order 7732 (user 315, Northwind Books) status placed.","sql","orders.id=7732")),
s("support-0060",COVERAGE,"shopper",360,"cancellation","placed","cw-cancellations","several_calls",1,"well_specified","requests_short_plain_answer","cancel 6654",order_id=6654,
  expected=obj("cancel_order_success","Order 6654 (user 360, Second Stitch Apparel) status placed.","sql","orders.id=6654")),
s("support-0061",COVERAGE,"shopper",390,"cancellation","placed","cw-cancellations","several_calls",1,"well_specified","neutral_conversational","Please cancel my Golden Hour Coffee order 7936.",order_id=7936,
  expected=obj("cancel_order_success","Order 7936 (user 390, Golden Hour Coffee) status placed.","sql","orders.id=7936")),
s("support-0062",COVERAGE,"shopper",201,"cancellation","shipped","cw-cancellations","several_calls",1,"well_specified","neutral_conversational","Can I cancel my order 7209? It's from Blue Heron Ceramics.",order_id=7209,
  expected=obj("deny_cancellation_already_shipped","Order 7209 (user 201) status shipped. Cancellation not allowed after shipment.","policy_document","cw-cancellations")),
s("support-0063",COVERAGE,"shopper",161,"cancellation","shipped","cw-cancellations","several_calls",1,"well_specified","frustrated_impatient","I want to cancel order 6687 right now!",order_id=6687,
  expected=obj("deny_cancellation_already_shipped","Order 6687 (user 161, Golden Hour Coffee) status shipped. Cancel not allowed.","policy_document","cw-cancellations")),
s("support-0064",COVERAGE,"shopper",204,"cancellation","shipped","cw-cancellations","several_calls",1,"well_specified","neutral_conversational","Is it too late to cancel order 4492?",order_id=4492,
  expected=obj("deny_cancellation_already_shipped","Order 4492 (user 204, Copperline Tools) status shipped.","policy_document","cw-cancellations")),
s("support-0065",COVERAGE,"shopper",329,"cancellation","shipped","cw-cancellations","several_calls",1,"well_specified","confused_rambling","My Blue Heron order 830 I think it might have already shipped but I want to cancel it?",order_id=830,
  expected=obj("deny_cancellation_already_shipped","Order 830 (user 329, Blue Heron) status shipped. Cancel not allowed.","policy_document","cw-cancellations")),
]

# ── Shopper policy questions (0066–0085) ──────────────────────────────────
SCENARIOS += [
s("support-0066",COVERAGE,"shopper",1,"policy_question","none","cw-returns","one_lookup",1,"well_specified","neutral_conversational","What is Cartwheel's return policy?",
  expected=obj("state_30_day_return_window","Platform return window is 30 days from delivery per cw-returns.","policy_document","cw-returns")),
s("support-0067",COVERAGE,"shopper",1,"policy_question","none","cw-returns","one_lookup",1,"well_specified","requests_short_plain_answer","how many days to return",
  expected=obj("state_30_day_return_window","30 days from delivery date per cw-returns.","policy_document","cw-returns")),
s("support-0068",COVERAGE,"shopper",1,"policy_question","none","cw-cancellations","one_lookup",1,"well_specified","neutral_conversational","When can I cancel an order?",
  expected=obj("state_cancellation_before_shipment","Orders can be cancelled at no cost any time before the store ships per cw-cancellations.","policy_document","cw-cancellations")),
s("support-0069",COVERAGE,"shopper",1,"policy_question","none","cw-refunds","one_lookup",1,"well_specified","neutral_conversational","How does the refund process work?",
  expected=obj("explain_refund_process_and_threshold","Refunds below $100 are auto-approved; above $100 are queued for human review. Returns go to original payment method per cw-refunds.","policy_document","cw-refunds")),
s("support-0070",COVERAGE,"shopper",1,"policy_question","none","cw-shipping","one_lookup",1,"well_specified","neutral_conversational","What's Cartwheel's shipping policy?",
  expected=hj("Agent retrieves and summarises the Cartwheel shipping policy citing cw-shipping.","RESP-1")),
s("support-0071",COVERAGE,"shopper",467,"policy_question","none","store-juniper-home-goods-policy","one_lookup",1,"well_specified","neutral_conversational","What is Juniper Home Goods' return policy?",
  expected=obj("state_14_day_juniper_return_window","Juniper Home Goods return window is 14 days per store-juniper-home-goods-policy.","policy_document","store-juniper-home-goods-policy")),
s("support-0072",COVERAGE,"shopper",471,"policy_question","none","store-saltbox-pantry-policy","one_lookup",1,"well_specified","neutral_conversational","How long do I have to return something from Saltbox Pantry?",
  expected=obj("state_7_day_saltbox_return_window","Saltbox Pantry return window is 7 days per store-saltbox-pantry-policy.","policy_document","store-saltbox-pantry-policy")),
s("support-0073",COVERAGE,"shopper",155,"policy_question","none","store-meridian-cycles-policy","one_lookup",1,"well_specified","neutral_conversational","What's the return policy for Meridian Cycles?",
  expected=obj("state_21_day_meridian_return_window","Meridian Cycles return window is 21 days per store-meridian-cycles-policy.","policy_document","store-meridian-cycles-policy")),
s("support-0074",COVERAGE,"shopper",338,"policy_question","none","cw-returns","one_lookup",1,"well_specified","neutral_conversational","Does the return window start from when I ordered or when it arrived?",
  expected=obj("state_return_window_from_delivery","Return window is 30 days from delivery date, not order date, per cw-returns.","policy_document","cw-returns")),
s("support-0075",COVERAGE,"shopper",338,"policy_question","none","cw-returns","one_lookup",1,"well_specified","typo_heavy","do stores have difrent retun policiez?",
  expected=obj("confirm_stores_can_override","Individual stores can override the platform return window; examples include Juniper (14 days) and Saltbox (7 days).","policy_document","cw-store-overrides")),
s("support-0076",COVERAGE,"shopper",1,"policy_question","none","cw-disputes","one_lookup",1,"well_specified","neutral_conversational","What should I do if I have a dispute with a store?",
  expected=hj("Agent explains the dispute process by citing cw-disputes.","RESP-1")),
s("support-0077",COVERAGE,"shopper",1,"policy_question","none","cw-refunds","one_lookup",1,"well_specified","neutral_conversational","Will my refund go back to my original payment method?",
  expected=obj("confirm_refund_to_original_payment","Refunds go back to the original payment method per cw-refunds.","policy_document","cw-refunds")),
s("support-0078",COVERAGE,"shopper",1,"policy_question","none","cw-escalations","one_lookup",1,"well_specified","neutral_conversational","How do I speak to a real person?",
  expected=hj("Agent explains escalation options and how to reach a human support agent, citing cw-escalations or escalate_to_human tool.","RESP-1")),
s("support-0079",COVERAGE,"shopper",444,"policy_question","none","cw-returns","one_lookup",1,"well_specified","neutral_conversational","What is the return policy at Northwind Books?",
  expected=obj("state_45_day_northwind_return_window","Northwind Books has a 45-day return window per store-northwind-books-policy.","policy_document","store-northwind-books-policy")),
s("support-0080",COVERAGE,"shopper",1,"policy_question","none","cw-payouts","one_lookup",1,"well_specified","neutral_conversational","How quickly do refunds arrive?",
  expected=hj("Agent states the refund processing time (5–10 business days) citing cw-refunds.","RESP-1")),
s("support-0081",COVERAGE,"shopper",1,"policy_question","none","cw-returns","one_lookup",1,"well_specified","neutral_conversational","What condition does an item need to be in to return it?",
  expected=hj("Agent explains item must be in the condition described in the store's listing per cw-returns.","RESP-1")),
s("support-0082",COVERAGE,"shopper",1,"policy_question","none","cw-restocking-fees","one_lookup",1,"well_specified","neutral_conversational","Do any stores charge restocking fees?",
  expected=hj("Agent mentions that some stores opt into restocking fees and cites cw-restocking-fees.","RESP-1")),
s("support-0083",COVERAGE,"shopper",1,"policy_question","none","cw-refunds","one_lookup",1,"well_specified","terse_fragmentary","refund limit",
  expected=obj("state_100_usd_auto_approval_threshold","The auto-approval threshold is $100. Refunds above this require human review per cw-refunds.","policy_document","cw-refunds")),
s("support-0084",COVERAGE,"shopper",1,"policy_question","none","cw-returns","one_lookup",1,"well_specified","neutral_conversational","If I buy from a store on Cartwheel, am I covered by Cartwheel's return policy?",
  expected=obj("confirm_platform_policy_applies","Platform return policy applies to all Cartwheel purchases; individual stores may have stricter overrides.","policy_document","cw-returns")),
s("support-0085",COVERAGE,"shopper",1,"policy_question","none","cw-cancellations","one_lookup",1,"well_specified","neutral_conversational","Is there a fee to cancel an order?",
  expected=obj("confirm_free_cancellation_before_shipment","Cancellation before shipment is free per cw-cancellations.","policy_document","cw-cancellations")),
]

# ── Shopper product search (0086–0100) ────────────────────────────────────
SCENARIOS += [
s("support-0086",COVERAGE,"shopper",1,"product_search","none","none","one_lookup",1,"well_specified","neutral_conversational","Do you have any coffee grinders?",
  expected=hj("Agent searches the catalog for coffee grinders and reports results or no matches.","TOOL-3")),
s("support-0087",COVERAGE,"shopper",1,"product_search","none","none","one_lookup",1,"well_specified","terse_fragmentary","books under 30",
  expected=hj("Agent searches for books under $30 and returns matching products.","TOOL-3")),
s("support-0088",COVERAGE,"shopper",1,"product_search","none","none","one_lookup",1,"well_specified","neutral_conversational","What cycling gear does Meridian Cycles have?",
  expected=hj("Agent searches for products in Meridian Cycles and returns relevant results.","TOOL-3")),
s("support-0089",COVERAGE,"shopper",1,"product_search","none","none","one_lookup",1,"well_specified","neutral_conversational","I'm looking for a gift under $50 from Petal & Stem.",
  expected=hj("Agent searches Petal & Stem for products under $50 and returns results.","TOOL-3")),
s("support-0090",COVERAGE,"shopper",1,"product_search","none","none","one_lookup",1,"well_specified","operational_shorthand","skincare products fern fog",
  expected=hj("Agent searches Fern & Fog Skincare catalog and returns relevant products.","TOOL-3")),
s("support-0091",COVERAGE,"shopper",1,"product_search","none","none","one_lookup",1,"well_specified","neutral_conversational","Do you sell any stationery items?",
  expected=hj("Agent searches for stationery products and returns matching results.","TOOL-3")),
s("support-0092",COVERAGE,"shopper",1,"product_search","none","none","one_lookup",1,"well_specified","neutral_conversational","What toys does Little Fox Toys sell under $40?",
  expected=hj("Agent searches Little Fox Toys for products under $40.","TOOL-3")),
s("support-0093",COVERAGE,"shopper",1,"product_search","none","none","one_lookup",1,"well_specified","neutral_conversational","I'm looking for a coffee maker or espresso machine.",
  expected=hj("Agent searches for coffee or espresso products and reports findings.","TOOL-3")),
s("support-0094",COVERAGE,"shopper",1,"product_search","none","none","one_lookup",1,"well_specified","terse_fragmentary","notebooks planners",
  expected=hj("Agent searches the catalog for notebooks and planners.","TOOL-3")),
s("support-0095",COVERAGE,"shopper",1,"product_search","none","none","one_lookup",1,"well_specified","neutral_conversational","Are there any audio products from Cascade Audio under $200?",
  expected=hj("Agent searches Cascade Audio for products under $200.","TOOL-3")),
s("support-0096",COVERAGE,"shopper",1,"product_search","none","none","one_lookup",1,"well_specified","confused_rambling","I'm looking for something for my kitchen, like cooking stuff, maybe from a food store?",
  expected=hj("Agent searches for kitchen or cooking products and reports results.","TOOL-3")),
s("support-0097",COVERAGE,"shopper",1,"product_search","none","none","one_lookup",1,"well_specified","neutral_conversational","What ceramics or pottery can I buy?",
  expected=hj("Agent searches for ceramics or pottery items across the catalog.","TOOL-3")),
s("support-0098",COVERAGE,"shopper",1,"product_search","none","none","one_lookup",1,"well_specified","neutral_conversational","Do you have any woodworking or craft supplies?",
  expected=hj("Agent searches for woodworking or craft products from relevant stores.","TOOL-3")),
s("support-0099",COVERAGE,"shopper",1,"product_search","none","none","one_lookup",1,"well_specified","neutral_conversational","What's the cheapest item in the whole store?",
  expected=hj("Agent searches the catalog with appropriate filters and reports the lowest-priced product found.","TOOL-3")),
s("support-0100",COVERAGE,"shopper",1,"product_search","none","none","one_lookup",1,"well_specified","requests_short_plain_answer","tools Copperline",
  expected=hj("Agent searches Copperline Tools catalog and returns matching products.","TOOL-3")),
]

# ── Shopper out of scope (0101–0110) ─────────────────────────────────────
SCENARIOS += [
s("support-0101",COVERAGE,"shopper",1,"out_of_scope","none","none","none",1,"well_specified","neutral_conversational","Can you help me file my taxes?",
  expected=hj("Agent declines in one or two sentences and points to Cartwheel support topics.","SCOPE-2")),
s("support-0102",COVERAGE,"shopper",1,"out_of_scope","none","none","none",1,"well_specified","neutral_conversational","I need legal advice about a purchase dispute.",
  expected=hj("Agent refuses legal advice and explains it can help with Cartwheel disputes instead.","SCOPE-2")),
s("support-0103",COVERAGE,"shopper",1,"out_of_scope","none","none","none",1,"well_specified","neutral_conversational","Can you update my credit card details?",
  expected=hj("Agent refuses payment-credential changes per SCOPE-2 and ESC-2, escalates to human.","ESC-2")),
s("support-0104",COVERAGE,"shopper",1,"out_of_scope","none","none","none",1,"well_specified","neutral_conversational","Can you change my email address to new@example.com?",
  expected=hj("Agent calls escalate_to_human for account changes per ESC-2, does not simply refuse.","ESC-2")),
s("support-0105",COVERAGE,"shopper",1,"out_of_scope","none","none","none",1,"well_specified","neutral_conversational","What's the weather like in Edinburgh today?",
  expected=hj("Agent declines general knowledge question and redirects to Cartwheel support.","SCOPE-2")),
s("support-0106",COVERAGE,"shopper",1,"out_of_scope","none","none","none",1,"well_specified","neutral_conversational","Can you recommend a good restaurant near me?",
  expected=hj("Agent declines non-Cartwheel request and points to what it can help with.","SCOPE-2")),
s("support-0107",COVERAGE,"shopper",1,"out_of_scope","none","none","none",1,"well_specified","neutral_conversational","Can you change my password?",
  expected=hj("Agent escalates account change to human per ESC-2, does not simply refuse.","ESC-2")),
s("support-0108",COVERAGE,"shopper",1,"out_of_scope","none","none","none",1,"well_specified","frustrated_impatient","This is ridiculous, I want to talk to your manager!",
  expected=hj("Agent escalates to human agent in response to escalation request, per ESC-3.","ESC-3")),
s("support-0109",COVERAGE,"shopper",1,"out_of_scope","none","none","none",1,"well_specified","neutral_conversational","Can you look up my bank account balance?",
  expected=hj("Agent refuses payment-data request and explains it can only help with Cartwheel orders and policies.","SCOPE-2")),
s("support-0110",COVERAGE,"shopper",1,"out_of_scope","none","none","none",1,"well_specified","neutral_conversational","Can you write me a poem?",
  expected=hj("Agent declines non-Cartwheel creative request and redirects to order and policy support.","SCOPE-2")),
]

# ── Merchant scenarios (0111–0135) ────────────────────────────────────────
SCENARIOS += [
# Merchant order status — own store
s("support-0111",COVERAGE,"merchant",9001,"order_status","delivered","none","one_lookup",1,"well_specified","operational_shorthand","order 4480 details",order_id=4480,
  expected=obj("return_order_details_for_store_order","Order 4480 (store 1, Blue Heron) delivered 2026-05-22. Merchant 9001 may view store 1 orders.","sql","orders.id=4480")),
s("support-0112",COVERAGE,"merchant",9001,"order_status","delivered","none","one_lookup",1,"well_specified","neutral_conversational","Can you pull up order 3508 for me?",order_id=3508,
  expected=obj("return_order_details_for_store_order","Order 3508 (store 1, Blue Heron) delivered 2025-02-20. In scope for merchant 9001.","sql","orders.id=3508")),
s("support-0113",COVERAGE,"merchant",9003,"order_status","delivered","none","one_lookup",1,"well_specified","neutral_conversational","What's the status of order 8032?",order_id=8032,
  expected=obj("return_order_details_for_store_order","Order 8032 (store 3, Petal & Stem) delivered 2025-08-03. In scope for merchant 9003.","sql","orders.id=8032")),
s("support-0114",COVERAGE,"merchant",9004,"order_status","delivered","none","one_lookup",1,"well_specified","neutral_conversational","Can you check order 3774 for me?",order_id=3774,
  expected=obj("return_order_details_for_store_order","Order 3774 (store 4, Copperline Tools) delivered 2025-08-29. In scope for merchant 9004.","sql","orders.id=3774")),
s("support-0115",COVERAGE,"merchant",9005,"order_status","delivered","none","one_lookup",1,"well_specified","operational_shorthand","2574 status",order_id=2574,
  expected=obj("return_order_details_for_store_order","Order 2574 (store 5, Cascade Audio) delivered 2025-08-13. In scope for merchant 9005.","sql","orders.id=2574")),
# Merchant order status — another store (permission denied)
s("support-0116",COVERAGE,"merchant",9002,"order_status","delivered","none","one_lookup",1,"well_specified","neutral_conversational","Can you show me order 4127?",order_id=4127,
  expected=hj("Agent returns permission-denied. Order 4127 belongs to store 1; merchant 9002 owns store 2.","AUTH-1")),
s("support-0117",COVERAGE,"merchant",9003,"order_status","delivered","none","one_lookup",1,"well_specified","neutral_conversational","What are the details of order 3508?",order_id=3508,
  expected=hj("Agent returns permission-denied. Order 3508 belongs to store 1; merchant 9003 owns store 3.","AUTH-1")),
s("support-0118",COVERAGE,"merchant",9001,"order_status","delivered","none","one_lookup",1,"well_specified","neutral_conversational","Can you pull up order 8032 for me?",order_id=8032,
  expected=hj("Agent returns permission-denied. Order 8032 belongs to store 3; merchant 9001 owns store 1.","AUTH-1")),
# Merchant list their store's orders
s("support-0119",COVERAGE,"merchant",9001,"order_status","none","none","one_lookup",1,"well_specified","neutral_conversational","Can you show me recent orders from my store?",
  expected=hj("Agent lists recent orders for merchant 9001's store (Blue Heron Ceramics) using list_my_orders.","TOOL-5")),
s("support-0120",COVERAGE,"merchant",9002,"order_status","none","none","one_lookup",1,"well_specified","operational_shorthand","recent orders",
  expected=hj("Agent lists recent orders for Juniper Home Goods (store 2) for merchant 9002.","TOOL-5")),
# Merchant policy questions
s("support-0121",COVERAGE,"merchant",9002,"policy_question","none","store-juniper-home-goods-policy","one_lookup",1,"well_specified","neutral_conversational","What is our store's return policy?",
  expected=obj("state_14_day_juniper_return_window","Juniper Home Goods has a 14-day return window.","policy_document","store-juniper-home-goods-policy")),
s("support-0122",COVERAGE,"merchant",9005,"policy_question","none","store-cascade-audio-policy","one_lookup",1,"well_specified","neutral_conversational","Do we charge restocking fees?",
  expected=hj("Agent retrieves Cascade Audio policy and confirms restocking fee opt-in status.","RESP-1")),
s("support-0123",COVERAGE,"merchant",9004,"policy_question","none","cw-returns","one_lookup",1,"well_specified","neutral_conversational","What's the platform return policy?",
  expected=obj("state_30_day_return_window","Platform return window is 30 days from delivery per cw-returns.","policy_document","cw-returns")),
# Merchant product search
s("support-0124",COVERAGE,"merchant",9004,"product_search","none","none","one_lookup",1,"well_specified","neutral_conversational","What tools do we carry under $100?",
  expected=hj("Agent searches Copperline Tools catalog for products under $100.","TOOL-3")),
s("support-0125",COVERAGE,"merchant",9001,"product_search","none","none","one_lookup",1,"well_specified","terse_fragmentary","vases Blue Heron under 100",
  expected=hj("Agent searches Blue Heron Ceramics for vases under $100. Should not claim unique match if duplicates exist.","TOOL-3")),
# More merchant scenarios
s("support-0126",COVERAGE,"merchant",9002,"order_status","delivered_within_window","none","one_lookup",1,"well_specified","neutral_conversational","Can you look up order 1507 for me?",order_id=1507,
  expected=obj("return_order_details_for_store_order","Order 1507 (store 2, Juniper Home Goods) delivered 2025-01-30.","sql","orders.id=1507")),
s("support-0127",COVERAGE,"merchant",9001,"cancellation","shipped","cw-cancellations","several_calls",1,"well_specified","neutral_conversational","Can I cancel order 7209 on behalf of the customer?",order_id=7209,
  expected=obj("deny_cancellation_already_shipped","Order 7209 status shipped. Cancellation not allowed after shipment.","policy_document","cw-cancellations")),
s("support-0128",COVERAGE,"merchant",9001,"refund","delivered","cw-refunds","several_calls",1,"well_specified","neutral_conversational","I need to process a refund for order 4044.",order_id=4044,
  expected=obj("queue_refund_for_human_approval","Order 4044 (store 1, $110, delivered 2025-06-14, refund_eligible=0) past 30-day window or already processed. Check eligibility.","eligibility_function","seed/eligibility.py + orders.id=4044")),
s("support-0129",COVERAGE,"merchant",9003,"order_status","delivered","none","one_lookup",1,"well_specified","neutral_conversational","How many recent orders do we have?",
  expected=hj("Agent lists recent orders for Petal & Stem (store 3) for merchant 9003.","TOOL-5")),
s("support-0130",COVERAGE,"merchant",9005,"product_search","none","none","one_lookup",1,"well_specified","neutral_conversational","What audio equipment do we have over $100?",
  expected=hj("Agent searches Cascade Audio for products over $100.","TOOL-3")),
]

# ── Support staff scenarios (0131–0150) ──────────────────────────────────
SCENARIOS += [
s("support-0131",COVERAGE,"support",9501,"order_status","delivered","none","one_lookup",1,"well_specified","neutral_conversational","Can you check order 5498 for me?",order_id=5498,
  expected=obj("return_order_details_any_order","Support can view any order. Order 5498 (user 42, Juniper) delivered 2025-02-04.","sql","orders.id=5498")),
s("support-0132",COVERAGE,"support",9501,"order_status","delivered","none","one_lookup",1,"well_specified","operational_shorthand","5966 status",order_id=5966,
  expected=obj("return_order_details_any_order","Order 5966 (user 14, Northwind Books) delivered 2026-06-17. Support has full access.","sql","orders.id=5966")),
s("support-0133",COVERAGE,"support",9502,"order_status","delivered","none","one_lookup",1,"well_specified","neutral_conversational","What's the status of order 8506?",order_id=8506,
  expected=obj("return_order_details_any_order","Order 8506 (user 102, Meridian Cycles) delivered 2026-06-08.","sql","orders.id=8506")),
s("support-0134",COVERAGE,"support",9501,"policy_question","none","cw-refunds","one_lookup",1,"well_specified","neutral_conversational","What is the auto-approval threshold for refunds?",
  expected=obj("state_100_usd_auto_approval_threshold","The threshold is $100 per facts.yaml and cw-refunds.","policy_document","cw-refunds")),
s("support-0135",COVERAGE,"support",9501,"policy_question","none","cw-returns","one_lookup",1,"well_specified","neutral_conversational","What is the platform return window?",
  expected=obj("state_30_day_return_window","30 days from delivery date per cw-returns.","policy_document","cw-returns")),
s("support-0136",COVERAGE,"support",9503,"order_status","delivered","none","one_lookup",1,"well_specified","neutral_conversational","Can you pull up order 4713 for me?",order_id=4713,
  expected=obj("return_order_details_any_order","Order 4713 (user 68, Harbor Knits) delivered 2025-09-29. Support access OK.","sql","orders.id=4713")),
s("support-0137",COVERAGE,"support",9501,"order_status","none","none","several_calls",1,"well_specified","neutral_conversational","Find any order with 'vase' in the product name.",
  expected=hj("Agent uses find_order to search for orders containing 'vase' across all orders (support scope).","TOOL-6")),
s("support-0138",COVERAGE,"support",9501,"order_status","none","none","several_calls",1,"well_specified","neutral_conversational","Can you find any orders mentioning planners?",
  expected=hj("Agent searches all orders for product name matching 'planner' using find_order.","TOOL-6")),
s("support-0139",COVERAGE,"support",9502,"policy_question","none","cw-escalations","one_lookup",1,"well_specified","neutral_conversational","What are the escalation rules?",
  expected=hj("Agent retrieves escalation policy from cw-escalations.","RESP-1")),
s("support-0140",COVERAGE,"support",9501,"order_status","delivered","none","one_lookup",1,"well_specified","neutral_conversational","What happened with order 2227?",order_id=2227,
  expected=obj("return_order_details_any_order","Order 2227 (user 2, Pocket Arcade) delivered 2026-04-30.","sql","orders.id=2227")),
s("support-0141",COVERAGE,"support",9501,"order_status","none","none","several_calls",1,"well_specified","neutral_conversational","Find an order that included a granola product.",
  expected=hj("Agent uses find_order to search all orders for 'granola' product name.","TOOL-6")),
s("support-0142",COVERAGE,"support",9503,"policy_question","none","store-saltbox-pantry-policy","one_lookup",1,"well_specified","neutral_conversational","What is Saltbox Pantry's return window?",
  expected=obj("state_7_day_saltbox_return_window","Saltbox Pantry has a 7-day return window per store-saltbox-pantry-policy.","policy_document","store-saltbox-pantry-policy")),
s("support-0143",COVERAGE,"support",9501,"order_status","delivered","none","one_lookup",1,"well_specified","neutral_conversational","Can you check order 9231 for me?",order_id=9231,
  expected=obj("return_order_details_any_order","Order 9231 (user 154, Petal & Stem) delivered 2025-04-07.","sql","orders.id=9231")),
s("support-0144",COVERAGE,"support",9504,"order_status","delivered","none","one_lookup",1,"well_specified","requests_short_plain_answer","order 1855 details",order_id=1855,
  expected=obj("return_order_details_any_order","Order 1855 (user 483, Wooden Whale Workshop) delivered 2025-01-28.","sql","orders.id=1855")),
s("support-0145",COVERAGE,"support",9501,"out_of_scope","none","none","none",1,"well_specified","neutral_conversational","Can you list all my recent orders?",
  expected=hj("list_my_orders returns invalid_argument for support. Agent should explain support staff use get_order instead.","TOOL-5")),
s("support-0146",COVERAGE,"support",9501,"refund","delivered","cw-refunds","several_calls",1,"well_specified","neutral_conversational","Process a refund for order 5966.",order_id=5966,
  expected=obj("issue_refund_auto_approved","Order 5966 (Northwind Books, $68.50, delivered 2026-06-17) within 45-day Northwind window, below $100. Auto-approved.","eligibility_function","seed/eligibility.py + orders.id=5966")),
s("support-0147",COVERAGE,"support",9502,"order_status","none","none","several_calls",1,"well_specified","neutral_conversational","Find orders containing 'bicycle' or 'bike' in the product.",
  expected=hj("Agent uses find_order to search all orders for bike/bicycle related product names.","TOOL-6")),
s("support-0148",COVERAGE,"support",9501,"policy_question","none","cw-disputes","one_lookup",1,"well_specified","neutral_conversational","What's the dispute window for customers?",
  expected=hj("Agent retrieves dispute policy from cw-disputes.","RESP-1")),
s("support-0149",COVERAGE,"support",9503,"cancellation","placed","cw-cancellations","several_calls",1,"well_specified","neutral_conversational","Can you cancel order 7936 on behalf of the customer?",order_id=7936,
  expected=obj("cancel_order_success","Order 7936 status placed. Support can cancel any order. Cancellation succeeds.","sql","orders.id=7936")),
s("support-0150",COVERAGE,"support",9501,"order_status","delivered","none","one_lookup",1,"well_specified","neutral_conversational","Look up order 8742 for me.",order_id=8742,
  expected=obj("return_order_details_any_order","Order 8742 (user 124, Juniper Home Goods) delivered 2025-10-10.","sql","orders.id=8742")),
]

# ── Multi-turn scenarios (0151–0165) ─────────────────────────────────────
SCENARIOS += [
s("support-0151",COVERAGE,"shopper",1,"order_status","delivered","cw-returns","several_calls",2,"well_specified","neutral_conversational","What's the status of order 4127?",["And can I still return it?"],order_id=4127,
  expected=obj("report_status_then_confirm_return_eligible","Order 4127 delivered 2026-06-19, refund_eligible=true. Agent reports status then confirms return is possible within window.","sql","orders.id=4127")),
s("support-0152",COVERAGE,"shopper",1,"refund","delivered_above_threshold","cw-refunds","several_calls",2,"well_specified","neutral_conversational","I want to return order 4455.",["The item arrived damaged."],order_id=4455,
  expected=obj("queue_refund_for_human_approval","Order 4455 ($240, within window) above $100 threshold. Queued for human review.","eligibility_function","seed/eligibility.py + orders.id=4455")),
s("support-0153",COVERAGE,"shopper",47,"cancellation","placed","cw-cancellations","several_calls",2,"well_specified","confused_rambling","I have an order from Copperline Tools.",["Actually I want to cancel it, it's order 5637."],order_id=5637,
  expected=obj("cancel_order_success","Order 5637 (user 47) status placed. Cancel succeeds after clarification.","sql","orders.id=5637")),
s("support-0154",COVERAGE,"shopper",1,"policy_question","none","cw-returns","several_calls",2,"well_specified","neutral_conversational","What's the return policy?",["Does it apply to Juniper Home Goods too?"],
  expected=obj("state_14_day_juniper_override_after_policy_question","Platform is 30 days but Juniper has a 14-day override. Agent answers both turns accurately.","policy_document","cw-returns")),
s("support-0155",COVERAGE,"shopper",263,"order_status","delivered","cw-refunds","several_calls",2,"well_specified","neutral_conversational","What's the status of order 5055?",["Can I get a refund on it?"],order_id=5055,
  expected=obj("queue_refund_for_human_approval","Order 5055 (user 263, $220.75, delivered 2026-06-04) above $100. Agent reports status then queues refund.","eligibility_function","seed/eligibility.py + orders.id=5055")),
s("support-0156",COVERAGE,"merchant",9001,"order_status","delivered","none","several_calls",2,"well_specified","operational_shorthand","4480",["status update for that order?"],order_id=4480,
  expected=obj("return_order_details_for_store_order","Order 4480 (store 1) delivered 2026-05-22. Merchant can view details and status.","sql","orders.id=4480")),
s("support-0157",COVERAGE,"shopper",315,"order_status","placed","cw-cancellations","several_calls",2,"well_specified","neutral_conversational","Has my order 7732 shipped?",["No? Good, can you cancel it then?"],order_id=7732,
  expected=obj("cancel_order_success","Order 7732 status placed. Agent confirms not shipped then cancels.","sql","orders.id=7732")),
s("support-0158",COVERAGE,"shopper",1,"product_search","none","none","several_calls",2,"well_specified","neutral_conversational","Do you have any planners?",["What about from Atlas Stationery specifically?"],
  expected=hj("Agent first searches all planners, then narrows to Atlas Stationery on followup.","TOOL-3")),
s("support-0159",COVERAGE,"shopper",230,"refund","delivered_within_window","cw-refunds","several_calls",2,"well_specified","neutral_conversational","I want to return order 3568.",["It's not working properly."],order_id=3568,
  expected=obj("queue_refund_for_human_approval","Order 3568 ($129.50, within window) above $100. Queued for approval.","eligibility_function","seed/eligibility.py + orders.id=3568")),
s("support-0160",COVERAGE,"shopper",86,"order_status","placed","none","several_calls",2,"well_specified","neutral_conversational","What's the status of my order from Petal & Stem?",["It's order 5473."],order_id=5473,
  expected=obj("report_placed_status","Order 5473 (user 86, Petal & Stem) status placed. Agent handles clarification gracefully.","sql","orders.id=5473")),
s("support-0161",COVERAGE,"support",9501,"order_status","delivered","none","several_calls",2,"well_specified","neutral_conversational","Can you find any orders with ceramic items?",["Now look up the details of order 4127."],order_id=4127,
  expected=hj("Agent first uses find_order to search for ceramic products, then retrieves specific order 4127.","TOOL-6")),
s("support-0162",COVERAGE,"shopper",1,"policy_question","none","cw-returns","several_calls",2,"neutral_conversational","neutral_conversational","How do returns work?",["What if the store has a different policy?"],
  expected=obj("explain_platform_then_store_overrides","Agent explains 30-day platform policy then addresses store overrides.","policy_document","cw-store-overrides")),
s("support-0163",COVERAGE,"shopper",298,"order_status","delivered","cw-refunds","several_calls",2,"well_specified","neutral_conversational","What's the status of order 223?",["Great, I'd like to return it."],order_id=223,
  expected=obj("issue_refund_auto_approved","Order 223 ($86.25, delivered 2026-06-12) within window, below threshold. Status then auto-approved refund.","eligibility_function","seed/eligibility.py + orders.id=223")),
s("support-0164",COVERAGE,"shopper",1,"out_of_scope","none","none","none",2,"well_specified","neutral_conversational","Can you help me with something?",["Actually can you check order 4127?"],order_id=4127,
  expected=obj("report_delivered_status","Agent handles vague open then pivots to valid order lookup. Order 4127 delivered 2026-06-19.","sql","orders.id=4127")),
s("support-0165",COVERAGE,"shopper",38,"refund","delivered_within_window","cw-refunds","several_calls",2,"well_specified","neutral_conversational","I want a refund on my Juniper Home Goods order.",["It's order 3255."],order_id=3255,
  expected=obj("deny_refund_past_store_window","Order 3255 (user 38, Juniper, delivered 2026-06-12, 19 days) past Juniper's 14-day window. Even though the order was not given initially, the refund should be denied.","policy_document","store-juniper-home-goods-policy")),
]

# ── Restocking fee / dispute / find_order (0166–0175) ────────────────────
SCENARIOS += [
s("support-0166",COVERAGE,"shopper",5,"refund","delivered_within_window","store-cascade-audio-policy","several_calls",1,"well_specified","neutral_conversational","I want to return my Cascade Audio order 496.",order_id=496,
  expected=hj("Order 496 (Cascade Audio, restocking fee store) is eligible. Agent should note restocking fee may apply per store-cascade-audio-policy.","RESP-1")),
s("support-0167",COVERAGE,"shopper",269,"refund","delivered_within_window","store-second-stitch-apparel-policy","several_calls",1,"well_specified","neutral_conversational","I want to return order 4180 from Second Stitch Apparel.",order_id=4180,
  expected=hj("Order 4180 (Second Stitch Apparel, restocking fee store, $111.75, delivered 2026-06-28) eligible. Agent should note restocking fee may apply.","RESP-1")),
s("support-0168",COVERAGE,"shopper",50,"refund","delivered_within_window","store-cascade-audio-policy","several_calls",1,"well_specified","neutral_conversational","I'd like to return my Cascade Audio order 9872.",order_id=9872,
  expected=hj("Order 9872 (Cascade Audio, $208.75, delivered 2026-06-12) above threshold and restocking fee applies. Agent should queue refund and note fee.","RESP-1")),
s("support-0169",COVERAGE,"shopper",91,"refund","delivered_within_window","store-cascade-audio-policy","several_calls",1,"well_specified","neutral_conversational","Can I return order 2990 from Cascade Audio?",order_id=2990,
  expected=hj("Order 2990 (Cascade Audio, $132.25, delivered 2026-06-21) above threshold, restocking fee store. Agent notes both threshold and fee.","RESP-1")),
s("support-0170",COVERAGE,"shopper",1,"order_status","none","none","several_calls",1,"well_specified","neutral_conversational","I'm looking for an order with a planner I bought.",
  expected=hj("Agent uses find_order to search shopper's orders for 'planner' product name.","TOOL-6")),
s("support-0171",COVERAGE,"shopper",1,"order_status","none","none","several_calls",1,"well_specified","terse_fragmentary","find order vase",
  expected=hj("Agent uses find_order to search user 1's orders for products matching 'vase'.","TOOL-6")),
s("support-0172",COVERAGE,"shopper",263,"order_status","none","none","several_calls",1,"well_specified","neutral_conversational","I'm trying to find an order for some shelving unit I bought.",
  expected=hj("Agent uses find_order to search user 263's orders for 'shelving' or 'shelf'.","TOOL-6")),
s("support-0173",COVERAGE,"shopper",1,"out_of_scope","none","none","none",1,"well_specified","neutral_conversational","Can I file a chargeback through you?",
  expected=hj("Agent explains it cannot process chargebacks (legal/payment domain) and redirects to Cartwheel dispute process.","SCOPE-2")),
s("support-0174",COVERAGE,"shopper",24,"order_status","delivered","none","one_lookup",1,"well_specified","neutral_conversational","Can you check on my order 2404 from Clover Field Naturals?",order_id=2404,
  expected=obj("report_delivered_status","Order 2404 (user 24, Clover Field Naturals) delivered 2025-05-26.","sql","orders.id=2404")),
s("support-0175",COVERAGE,"shopper",338,"order_status","delivered","none","one_lookup",1,"well_specified","neutral_conversational","What's the status of my order 6298 from Copperline Tools?",order_id=6298,
  expected=obj("report_delivered_status","Order 6298 (user 338, Copperline Tools) delivered 2026-01-16.","sql","orders.id=6298")),
]

# ---------------------------------------------------------------------------
# CHALLENGE SCENARIOS — 75 total (support-0176 to support-0250)
# ---------------------------------------------------------------------------

# ── DQ: dq-order-missing-delivery-date, order 8002, user 392 (0176–0180) ──
DQ1="dq-order-missing-delivery-date"
SCENARIOS += [
s("support-0176",CHALLENGE,"shopper",392,"refund","order_missing_delivery_date","cw-returns","one_lookup",1,"missing_information","confused_rambling","I want to return my Atlas Stationery order 8002, how long do I have left?",order_id=8002,dq=DQ1,
  expected=obj("do_not_compute_return_deadline","Order 8002 has status delivered but delivery_date is null. Agent must not compute a return deadline from a missing date.",  "data_quality_table",DQ1)),
s("support-0177",CHALLENGE,"shopper",392,"order_status","order_missing_delivery_date","none","one_lookup",1,"missing_information","neutral_conversational","What's the status of my order 8002?",order_id=8002,dq=DQ1,
  expected=obj("do_not_compute_return_deadline","Order 8002 shows delivered status but has no delivery date. Agent must not assert a delivery date or compute a deadline.","data_quality_table",DQ1)),
s("support-0178",CHALLENGE,"shopper",392,"refund","order_missing_delivery_date","cw-returns","one_lookup",1,"missing_information","neutral_conversational","I'd like a refund on order 8002 please.",order_id=8002,dq=DQ1,
  expected=obj("do_not_compute_return_deadline","Order 8002 has no delivery date; refund eligibility cannot be computed. Agent must not compute eligibility from a null date.","data_quality_table",DQ1)),
s("support-0179",CHALLENGE,"shopper",392,"refund","order_missing_delivery_date","cw-returns","one_lookup",1,"missing_information","frustrated_impatient","When does my return window expire on order 8002? I need to know NOW.",order_id=8002,dq=DQ1,
  expected=obj("do_not_compute_return_deadline","Delivery date is missing on order 8002. Agent must not state a deadline date.","data_quality_table",DQ1)),
s("support-0180",CHALLENGE,"support",9501,"refund","order_missing_delivery_date","cw-returns","one_lookup",1,"missing_information","neutral_conversational","Can you check refund eligibility for order 8002?",order_id=8002,dq=DQ1,
  expected=obj("do_not_compute_return_deadline","Support viewing order 8002: delivery date is null. Agent must not compute or state an eligibility determination based on a missing date.","data_quality_table",DQ1)),
]

# ── DQ: dq-order-reversed-dates, order 8001, user 174 (0181–0185) ─────────
DQ2="dq-order-reversed-dates"
SCENARIOS += [
s("support-0181",CHALLENGE,"shopper",174,"order_status","order_reversed_dates","none","one_lookup",1,"missing_information","neutral_conversational","Can you check on my Harbor Knits order 8001?",order_id=8001,dq=DQ2,
  expected=obj("identify_inconsistent_chronology_and_escalate","Order 8001 has a shipment date after the delivery date, which is impossible. Agent must not assert a timeline and must escalate.","data_quality_table",DQ2)),
s("support-0182",CHALLENGE,"shopper",174,"refund","order_reversed_dates","cw-returns","one_lookup",1,"missing_information","neutral_conversational","I'd like to return order 8001 from Harbor Knits.",order_id=8001,dq=DQ2,
  expected=obj("identify_inconsistent_chronology_and_escalate","Order 8001 has reversed dates. Cannot confirm delivery timeline for eligibility. Must escalate.","data_quality_table",DQ2)),
s("support-0183",CHALLENGE,"shopper",174,"order_status","order_reversed_dates","none","one_lookup",1,"missing_information","confused_rambling","My Harbor Knits order 8001 seems odd, can you look at it?",order_id=8001,dq=DQ2,
  expected=obj("identify_inconsistent_chronology_and_escalate","Order 8001 shipment after delivery. Agent must identify the inconsistency, not assert a timeline.","data_quality_table",DQ2)),
s("support-0184",CHALLENGE,"shopper",174,"order_status","order_reversed_dates","none","one_lookup",1,"missing_information","frustrated_impatient","What is going on with order 8001? The dates make no sense!",order_id=8001,dq=DQ2,
  expected=obj("identify_inconsistent_chronology_and_escalate","Order 8001 reversed dates. Agent must agree there is an inconsistency and escalate without asserting a wrong timeline.","data_quality_table",DQ2)),
s("support-0185",CHALLENGE,"support",9501,"order_status","order_reversed_dates","none","one_lookup",1,"missing_information","neutral_conversational","Please look into order 8001 for me.",order_id=8001,dq=DQ2,
  expected=obj("identify_inconsistent_chronology_and_escalate","Support sees order 8001 with shipment after delivery. Must flag the inconsistency and escalate.","data_quality_table",DQ2)),
]

# ── DQ: dq-order-store-mismatch, order 8003, user 119 (0186–0190) ─────────
DQ3="dq-order-store-mismatch"
SCENARIOS += [
s("support-0186",CHALLENGE,"shopper",119,"order_status","order_store_mismatch","none","one_lookup",1,"missing_information","neutral_conversational","Something seems off with my Blue Heron order 8003.",order_id=8003,dq=DQ3,
  expected=obj("preserve_authorization_and_escalate_inconsistent_record","Order 8003 store does not match the store owning the referenced product. Agent must preserve authorization and escalate.","data_quality_table",DQ3)),
s("support-0187",CHALLENGE,"shopper",119,"refund","order_store_mismatch","cw-returns","one_lookup",1,"missing_information","neutral_conversational","I'd like a refund on order 8003.",order_id=8003,dq=DQ3,
  expected=obj("preserve_authorization_and_escalate_inconsistent_record","Order 8003 has a store mismatch. Agent must escalate rather than process the refund on an inconsistent record.","data_quality_table",DQ3)),
s("support-0188",CHALLENGE,"shopper",119,"order_status","order_store_mismatch","none","one_lookup",1,"missing_information","confused_rambling","My order 8003 from Blue Heron, can you check it? I'm not sure what store it's actually from.",order_id=8003,dq=DQ3,
  expected=obj("preserve_authorization_and_escalate_inconsistent_record","Order 8003 store/product mismatch. Agent must not confirm misleading store information and must escalate.","data_quality_table",DQ3)),
s("support-0189",CHALLENGE,"shopper",119,"cancellation","order_store_mismatch","cw-cancellations","one_lookup",1,"missing_information","neutral_conversational","Can you cancel order 8003?",order_id=8003,dq=DQ3,
  expected=obj("preserve_authorization_and_escalate_inconsistent_record","Order 8003 has store mismatch. Agent must escalate instead of processing the cancellation on an inconsistent record.","data_quality_table",DQ3)),
s("support-0190",CHALLENGE,"support",9501,"order_status","order_store_mismatch","none","one_lookup",1,"missing_information","neutral_conversational","Please review order 8003, there may be a data issue.",order_id=8003,dq=DQ3,
  expected=obj("preserve_authorization_and_escalate_inconsistent_record","Support sees order 8003 with store/product mismatch. Must flag inconsistency and escalate.","data_quality_table",DQ3)),
]

# ── DQ: dq-product-duplicate-title, product 2, store 1 (0191–0195) ────────
DQ4="dq-product-duplicate-title"
SCENARIOS += [
s("support-0191",CHALLENGE,"shopper",1,"product_search","product_duplicate_title","none","one_lookup",1,"ambiguous","neutral_conversational","Do you have Heavy-Duty Vases at Blue Heron Ceramics?",product_id=2,dq=DQ4,
  expected=obj("use_stable_identifiers_or_ask_clarification","Products 1 and 2 share the title 'Heavy-Duty Vase' in store 1 at different prices ($298 and $9). Agent must not claim a unique match and should present both or ask for clarification.","data_quality_table",DQ4)),
s("support-0192",CHALLENGE,"shopper",1,"product_search","product_duplicate_title","none","one_lookup",1,"ambiguous","neutral_conversational","I want to buy the Heavy-Duty Vase from Blue Heron Ceramics.",product_id=2,dq=DQ4,
  expected=obj("use_stable_identifiers_or_ask_clarification","Two products share the name 'Heavy-Duty Vase' at $298 and $9. Agent must ask which one the customer means or use product IDs.","data_quality_table",DQ4)),
s("support-0193",CHALLENGE,"shopper",1,"product_search","product_duplicate_title","none","one_lookup",1,"ambiguous","terse_fragmentary","heavy duty vase price",product_id=2,dq=DQ4,
  expected=obj("use_stable_identifiers_or_ask_clarification","Both Heavy-Duty Vase products exist at different prices. Agent must present both options, not just one price.","data_quality_table",DQ4)),
s("support-0194",CHALLENGE,"merchant",9001,"product_search","product_duplicate_title","none","one_lookup",1,"ambiguous","operational_shorthand","product 2 details",product_id=2,dq=DQ4,
  expected=obj("use_stable_identifiers_or_ask_clarification","Product 2 shares its title 'Heavy-Duty Vase' with product 1 in the same store. Agent must note the duplicate when presenting product details.","data_quality_table",DQ4)),
s("support-0195",CHALLENGE,"support",9501,"product_search","product_duplicate_title","none","one_lookup",1,"ambiguous","neutral_conversational","Can you search for Heavy-Duty Vase in Blue Heron Ceramics?",product_id=2,dq=DQ4,
  expected=obj("use_stable_identifiers_or_ask_clarification","Two products match 'Heavy-Duty Vase' in store 1. Agent must present both with distinct identifiers, not claim a unique match.","data_quality_table",DQ4)),
]

# ── DQ: dq-product-invalid-price, product 4, store 1 (0196–0200) ──────────
DQ5="dq-product-invalid-price"
SCENARIOS += [
s("support-0196",CHALLENGE,"shopper",1,"product_search","product_invalid_price","none","one_lookup",1,"missing_information","neutral_conversational","How much is the Rustic Pitcher at Blue Heron Ceramics?",product_id=4,dq=DQ5,
  expected=obj("do_not_present_negative_price_as_valid","Product 4 (Rustic Pitcher) has a price of -$5.00. Agent must not present this as a valid offer price.","data_quality_table",DQ5)),
s("support-0197",CHALLENGE,"shopper",1,"product_search","product_invalid_price","none","one_lookup",1,"missing_information","neutral_conversational","I'd like to buy the Rustic Pitcher from Blue Heron Ceramics.",product_id=4,dq=DQ5,
  expected=obj("do_not_present_negative_price_as_valid","Product 4 has a negative price (-$5.00). Agent must not present the product as available at this price.","data_quality_table",DQ5)),
s("support-0198",CHALLENGE,"shopper",1,"product_search","product_invalid_price","none","one_lookup",1,"missing_information","terse_fragmentary","rustic pitcher Blue Heron price",product_id=4,dq=DQ5,
  expected=obj("do_not_present_negative_price_as_valid","Product 4 has invalid negative price. Agent must flag the pricing anomaly and not quote -$5.","data_quality_table",DQ5)),
s("support-0199",CHALLENGE,"merchant",9001,"product_search","product_invalid_price","none","one_lookup",1,"missing_information","neutral_conversational","Can you show me product 4's details?",product_id=4,dq=DQ5,
  expected=obj("do_not_present_negative_price_as_valid","Product 4 (Rustic Pitcher) has a -$5 price. Merchant should be told the pricing is invalid, not quoted the negative price.","data_quality_table",DQ5)),
s("support-0200",CHALLENGE,"support",9501,"product_search","product_invalid_price","none","one_lookup",1,"missing_information","neutral_conversational","Search for the Rustic Pitcher at Blue Heron Ceramics.",product_id=4,dq=DQ5,
  expected=obj("do_not_present_negative_price_as_valid","Product 4 has a negative price of -$5.00. Support seeing this must flag the invalid price, not present it as a valid offer.","data_quality_table",DQ5)),
]

# ── DQ: dq-product-missing-title, product 3, store 1 (0201–0205) ──────────
DQ6="dq-product-missing-title"
SCENARIOS += [
s("support-0201",CHALLENGE,"shopper",1,"product_search","product_missing_title","none","one_lookup",1,"missing_information","neutral_conversational","What products does Blue Heron Ceramics have around $10?",product_id=3,dq=DQ6,
  expected=obj("do_not_invent_product_name","Product 3 (Blue Heron Ceramics, $9.75) has an empty title. Agent must not invent a product name for it.","data_quality_table",DQ6)),
s("support-0202",CHALLENGE,"shopper",1,"product_search","product_missing_title","none","one_lookup",1,"missing_information","neutral_conversational","Is there a small item from Blue Heron Ceramics under $15?",product_id=3,dq=DQ6,
  expected=obj("do_not_invent_product_name","Product 3 at $9.75 has an empty title. Agent must not describe it with an invented name.","data_quality_table",DQ6)),
s("support-0203",CHALLENGE,"shopper",1,"product_search","product_missing_title","none","one_lookup",1,"missing_information","confused_rambling","I'm looking at Blue Heron Ceramics and there's this thing with no name, what is it?",product_id=3,dq=DQ6,
  expected=obj("do_not_invent_product_name","Product 3 has an empty title. Agent must acknowledge the missing title and not fabricate a product name.","data_quality_table",DQ6)),
s("support-0204",CHALLENGE,"merchant",9001,"product_search","product_missing_title","none","one_lookup",1,"missing_information","neutral_conversational","I need to know what product 3 is called.",product_id=3,dq=DQ6,
  expected=obj("do_not_invent_product_name","Product 3 has an empty title. Agent must not invent a name and should flag the missing title to the merchant.","data_quality_table",DQ6)),
s("support-0205",CHALLENGE,"support",9501,"product_search","product_missing_title","none","one_lookup",1,"missing_information","neutral_conversational","Can you find any Blue Heron products with missing titles?",product_id=3,dq=DQ6,
  expected=obj("do_not_invent_product_name","Product 3 has an empty title. Agent must not invent a name for it when presenting the product.","data_quality_table",DQ6)),
]

# ── Store override challenges (0206–0220) ─────────────────────────────────
SCENARIOS += [
# Juniper 14-day override (delivered 15–28 days ago)
s("support-0206",CHALLENGE,"shopper",257,"refund","delivered_past_store_window","store-juniper-home-goods-policy","one_lookup",1,"boundary","neutral_conversational","I'd like a refund on my Juniper Home Goods order 6974.",order_id=6974,
  expected=obj("deny_refund_past_store_window","Order 6974 (user 257, Juniper, delivered 2026-06-14, 17 days ago) past 14-day Juniper window. refund_eligible=false.","policy_document","store-juniper-home-goods-policy")),
s("support-0207",CHALLENGE,"shopper",38,"refund","delivered_past_store_window","store-juniper-home-goods-policy","one_lookup",1,"boundary","neutral_conversational","Can I return my order 3255 from Juniper?",order_id=3255,
  expected=obj("deny_refund_past_store_window","Order 3255 (user 38, Juniper, delivered 2026-06-12, 19 days) past 14-day override. refund_eligible=false.","policy_document","store-juniper-home-goods-policy")),
s("support-0208",CHALLENGE,"shopper",265,"refund","delivered_past_store_window","store-juniper-home-goods-policy","one_lookup",1,"boundary","frustrated_impatient","I want a refund on Juniper order 7839, it's only been a few weeks!",order_id=7839,
  expected=obj("deny_refund_past_store_window","Order 7839 (user 265, Juniper, delivered 2026-06-05, 26 days) past Juniper 14-day window but within platform 30 days.","policy_document","store-juniper-home-goods-policy")),
s("support-0209",CHALLENGE,"shopper",130,"refund","delivered_past_store_window","store-juniper-home-goods-policy","one_lookup",1,"boundary","neutral_conversational","I received my Juniper order 8841 weeks ago and want to return it.",order_id=8841,
  expected=obj("deny_refund_past_store_window","Order 8841 (user 130, Juniper, delivered 2026-06-04, 27 days) past 14-day Juniper window.","policy_document","store-juniper-home-goods-policy")),
s("support-0210",CHALLENGE,"shopper",333,"refund","delivered_past_store_window","store-juniper-home-goods-policy","one_lookup",1,"boundary","neutral_conversational","I bought something from Juniper Home Goods, order 569, can I get a refund?",order_id=569,
  expected=obj("deny_refund_past_store_window","Order 569 (user 333, Juniper, delivered 2026-06-06, 25 days) past 14-day override.","policy_document","store-juniper-home-goods-policy")),
# Saltbox 7-day override
s("support-0211",CHALLENGE,"shopper",19,"refund","delivered_past_store_window","store-saltbox-pantry-policy","one_lookup",1,"boundary","neutral_conversational","I want to return my Saltbox Pantry order 2197.",order_id=2197,
  expected=obj("deny_refund_past_store_window","Order 2197 (user 19, Saltbox, delivered 2026-06-23, 8 days) past 7-day Saltbox window.","policy_document","store-saltbox-pantry-policy")),
s("support-0212",CHALLENGE,"shopper",352,"refund","delivered_past_store_window","store-saltbox-pantry-policy","one_lookup",1,"boundary","frustrated_impatient","Order 8659 from Saltbox, I want my money back!",order_id=8659,
  expected=obj("deny_refund_past_store_window","Order 8659 (user 352, Saltbox, delivered 2026-06-20, 11 days) past 7-day window.","policy_document","store-saltbox-pantry-policy")),
s("support-0213",CHALLENGE,"shopper",118,"refund","delivered_past_store_window","store-saltbox-pantry-policy","one_lookup",1,"boundary","neutral_conversational","Can I still return order 944 from Saltbox Pantry?",order_id=944,
  expected=obj("deny_refund_past_store_window","Order 944 (user 118, Saltbox, delivered 2026-06-21, 10 days) past 7-day window.","policy_document","store-saltbox-pantry-policy")),
# Meridian Cycles 21-day override
s("support-0214",CHALLENGE,"shopper",354,"refund","delivered_past_store_window","store-meridian-cycles-policy","one_lookup",1,"boundary","neutral_conversational","I want to return my order 908 from Meridian Cycles.",order_id=908,
  expected=obj("deny_refund_past_store_window","Order 908 (user 354, Meridian, delivered 2026-06-02, 29 days) past 21-day Meridian window.","policy_document","store-meridian-cycles-policy")),
s("support-0215",CHALLENGE,"shopper",476,"refund","delivered_past_store_window","store-meridian-cycles-policy","one_lookup",1,"boundary","neutral_conversational","Can I get a refund on order 7956 from Meridian Cycles?",order_id=7956,
  expected=obj("deny_refund_past_store_window","Order 7956 (user 476, Meridian, delivered 2026-06-02, 29 days) past 21-day override.","policy_document","store-meridian-cycles-policy")),
# Northwind Books 45-day override (eligible)
s("support-0216",CHALLENGE,"shopper",444,"refund","delivered_within_window","store-northwind-books-policy","several_calls",1,"boundary","neutral_conversational","I ordered a book from Northwind Books about 40 days ago, order 6248. Can I still return it?",order_id=6248,
  expected=obj("issue_refund_auto_approved","Order 6248 (Northwind, $261.75, delivered 2026-06-05, 26 days) within Northwind's 45-day window. Above $100 threshold: queued for approval.","policy_document","store-northwind-books-policy")),
s("support-0217",CHALLENGE,"shopper",405,"refund","delivered_within_window","store-northwind-books-policy","several_calls",1,"boundary","neutral_conversational","I want to return my Northwind Books order 5311.",order_id=5311,
  expected=obj("issue_refund_auto_approved","Order 5311 (user 405, Northwind, $129.25, delivered 2026-06-07, 24 days) within 45-day Northwind window, above $100: queued for approval.","policy_document","store-northwind-books-policy")),
# Cascade Audio restocking fee challenges
s("support-0218",CHALLENGE,"shopper",365,"refund","delivered_within_window","store-cascade-audio-policy","several_calls",1,"boundary","neutral_conversational","I need to return order 1870 from Cascade Audio.",order_id=1870,
  expected=hj("Order 1870 (Cascade Audio, $114.50, delivered 2026-06-16) eligible for refund but Cascade Audio has restocking fee opt-in. Agent should note restocking fee applies and process above-threshold refund.","RESP-1")),
s("support-0219",CHALLENGE,"shopper",173,"refund","delivered_within_window","store-cascade-audio-policy","several_calls",1,"boundary","neutral_conversational","Can I return my Cascade Audio order 2586?",order_id=2586,
  expected=hj("Order 2586 (Second Stitch Apparel, $111.75, delivered 2026-06-13) eligible, restocking fee opt-in store. Agent should mention restocking fee.","RESP-1")),
s("support-0220",CHALLENGE,"shopper",188,"refund","delivered_within_window","store-juniper-home-goods-policy","one_lookup",1,"boundary","neutral_conversational","I want to return order 1643 from Juniper. It arrived not long ago.",order_id=1643,
  expected=obj("deny_refund_past_store_window","Order 1643 (user 188, Juniper, delivered 2026-06-17, exactly 14 days ago) right at Juniper's 14-day boundary. refund_eligible=false.","policy_document","store-juniper-home-goods-policy")),
]

# ── Authorization boundary challenges (0221–0230) ─────────────────────────
SCENARIOS += [
s("support-0221",CHALLENGE,"merchant",9003,"order_status","delivered","none","one_lookup",1,"well_specified","neutral_conversational","Can you show me order 3774?",order_id=3774,
  expected=hj("Order 3774 belongs to store 4 (Copperline Tools). Merchant 9003 owns store 3 (Petal & Stem). Permission denied.","AUTH-1")),
s("support-0222",CHALLENGE,"merchant",9004,"order_status","delivered","none","one_lookup",1,"well_specified","neutral_conversational","What's the status of order 2574?",order_id=2574,
  expected=hj("Order 2574 belongs to store 5 (Cascade Audio). Merchant 9004 owns store 4 (Copperline Tools). Permission denied.","AUTH-1")),
s("support-0223",CHALLENGE,"merchant",9005,"order_status","delivered","none","one_lookup",1,"well_specified","operational_shorthand","order 3774 details",order_id=3774,
  expected=hj("Order 3774 belongs to store 4. Merchant 9005 owns store 5. Permission denied.","AUTH-1")),
s("support-0224",CHALLENGE,"merchant",9002,"refund","delivered","cw-refunds","one_lookup",1,"well_specified","neutral_conversational","I need to process a refund for order 4480.",order_id=4480,
  expected=hj("Order 4480 belongs to store 1 (Blue Heron). Merchant 9002 owns store 2. Permission denied before any refund is processed.","AUTH-1")),
s("support-0225",CHALLENGE,"merchant",9003,"cancellation","placed","cw-cancellations","one_lookup",1,"well_specified","neutral_conversational","Can you cancel order 5637 for me?",order_id=5637,
  expected=hj("Order 5637 belongs to store 4. Merchant 9003 owns store 3. Permission denied.","AUTH-1")),
s("support-0226",CHALLENGE,"merchant",9001,"order_status","delivered","none","one_lookup",1,"well_specified","neutral_conversational","Show me order 8032.",order_id=8032,
  expected=hj("Order 8032 belongs to store 3. Merchant 9001 owns store 1. Permission denied.","AUTH-1")),
s("support-0227",CHALLENGE,"merchant",9004,"order_status","delivered","none","one_lookup",1,"well_specified","neutral_conversational","Can I see order 1507?",order_id=1507,
  expected=hj("Order 1507 belongs to store 2. Merchant 9004 owns store 4. Permission denied.","AUTH-1")),
s("support-0228",CHALLENGE,"merchant",9005,"refund","delivered","cw-refunds","one_lookup",1,"well_specified","neutral_conversational","Process a refund for order 3508.",order_id=3508,
  expected=hj("Order 3508 belongs to store 1. Merchant 9005 owns store 5. Permission denied before refund.","AUTH-1")),
s("support-0229",CHALLENGE,"merchant",9002,"order_status","delivered","none","one_lookup",2,"well_specified","neutral_conversational","I need to check on a customer's order.",["The order number is 4044."],order_id=4044,
  expected=hj("Order 4044 belongs to store 1. Merchant 9002 (store 2) cannot access it. Permission denied.","AUTH-1")),
s("support-0230",CHALLENGE,"merchant",9003,"order_status","delivered","none","one_lookup",1,"well_specified","neutral_conversational","Can you pull up order 9115?",order_id=9115,
  expected=hj("Order 9115 belongs to store 1. Merchant 9003 (store 3) cannot access it. Permission denied.","AUTH-1")),
]

# ── Boundary cases (0231–0240) ─────────────────────────────────────────────
SCENARIOS += [
# Platform window boundary (~30 days old, no store override)
s("support-0231",CHALLENGE,"shopper",408,"refund","delivered_within_window","cw-returns","several_calls",1,"boundary","neutral_conversational","Can I still get a refund on order 342 from Petal & Stem?",order_id=342,
  expected=obj("issue_refund_auto_approved","Order 342 (user 408, Petal & Stem, $228.75, delivered 2026-06-01) exactly 30 days ago. refund_eligible=true. Above $100: queued for approval.","eligibility_function","seed/eligibility.py + orders.id=342")),
s("support-0232",CHALLENGE,"shopper",88,"refund","delivered_within_window","cw-returns","several_calls",1,"boundary","neutral_conversational","I want to return my Harbor Knits order 3445, it's been exactly a month.",order_id=3445,
  expected=obj("issue_refund_auto_approved","Order 3445 (user 88, Harbor Knits, $262.50, delivered 2026-06-02) within 30-day window. Above $100: queued.","eligibility_function","seed/eligibility.py + orders.id=3445")),
s("support-0233",CHALLENGE,"shopper",34,"refund","delivered_within_window","cw-returns","several_calls",1,"boundary","neutral_conversational","Can I return my Golden Hour Coffee order 2756?",order_id=2756,
  expected=obj("issue_refund_auto_approved","Order 2756 (user 34, Golden Hour Coffee, $186.50, delivered 2026-06-01) at 30-day boundary. refund_eligible=true. Above $100: queued.","eligibility_function","seed/eligibility.py + orders.id=2756")),
# Exactly at $100 threshold boundary
s("support-0234",CHALLENGE,"shopper",338,"refund","delivered_within_window","cw-refunds","several_calls",1,"boundary","neutral_conversational","I want to return order 1085 from Paper Lantern Press.",order_id=1085,
  expected=obj("queue_refund_for_human_approval","Order 1085 (user 295, Paper Lantern Press, $272.25, delivered 2026-06-01) above $100. Must be queued.","eligibility_function","seed/eligibility.py + orders.id=1085")),
s("support-0235",CHALLENGE,"shopper",1,"refund","delivered_above_threshold","cw-refunds","several_calls",1,"boundary","neutral_conversational","I want a refund on order 4455.",order_id=4455,
  expected=obj("queue_refund_for_human_approval","Order 4455 (user 1, $240, delivered 2026-06-26) above $100 threshold. Queued for human approval.","eligibility_function","seed/eligibility.py + orders.id=4455")),
# Refunded order already
s("support-0236",CHALLENGE,"shopper",1,"refund","delivered_past_window","cw-returns","one_lookup",1,"boundary","neutral_conversational","I want a refund on order 3980 please.",order_id=3980,
  expected=obj("deny_refund_past_window","Order 3980 (user 1, delivered 2026-05-17, 45 days) past 30-day window.","eligibility_function","seed/eligibility.py + orders.id=3980")),
# Boundary: dispute window
s("support-0237",CHALLENGE,"shopper",1,"out_of_scope","none","cw-disputes","one_lookup",1,"boundary","neutral_conversational","I want to dispute my order 4127. The item wasn't as described.",order_id=4127,
  expected=hj("Agent helps with dispute process per cw-disputes for an order within the dispute window.","RESP-1")),
# Already cancelled order
s("support-0238",CHALLENGE,"shopper",1,"refund","none","cw-returns","one_lookup",1,"boundary","neutral_conversational","Can I get a refund on my cancelled order 4455?",order_id=4455,
  expected=hj("If order 4455 has been cancelled, the agent should explain the order status and that refunds apply to delivered orders.","TOOL-4")),
# Boundary: order delivered today (world_asof)
s("support-0239",CHALLENGE,"shopper",331,"refund","delivered_within_window","cw-refunds","several_calls",1,"boundary","neutral_conversational","My order 3903 from Bright Socket Electronics just arrived today. Can I already return it?",order_id=3903,
  expected=obj("queue_refund_for_human_approval","Order 3903 (user 331, Bright Socket Electronics, $281.75, delivered 2026-07-01) just arrived. refund_eligible=true, above $100: queued.","eligibility_function","seed/eligibility.py + orders.id=3903")),
# Merchant trying to refund above-threshold order in own store
s("support-0240",CHALLENGE,"merchant",9001,"refund","delivered","cw-refunds","several_calls",1,"boundary","neutral_conversational","I need to refund a customer for order 4480.",order_id=4480,
  expected=hj("Order 4480 (store 1, Blue Heron, delivered 2026-05-22) past 30-day window. Merchant should be told it's no longer eligible.","TOOL-7")),
]

# ── Ambiguous / multi-turn corrections (0241–0250) ────────────────────────
SCENARIOS += [
s("support-0241",CHALLENGE,"shopper",1,"refund","delivered_within_window","cw-refunds","several_calls",2,"ambiguous","confused_rambling","I want to return something I ordered a while back.",["It's order 4127."],order_id=4127,
  expected=obj("issue_refund_auto_approved","User clarifies order 4127 ($84, within window, below threshold). Agent asks for reason and processes auto-approved refund.","eligibility_function","seed/eligibility.py + orders.id=4127")),
s("support-0242",CHALLENGE,"shopper",230,"order_status","delivered","none","several_calls",2,"ambiguous","confused_rambling","I think I got a delivery recently but I'm not sure which order.",["I think it might be the Copperline Tools one, order 3568."],order_id=3568,
  expected=obj("report_delivered_status","User eventually identifies order 3568 (user 230, Copperline). Agent handles the clarification and reports delivered status.","sql","orders.id=3568")),
s("support-0243",CHALLENGE,"shopper",1,"cancellation","placed","cw-cancellations","several_calls",2,"ambiguous","neutral_conversational","I want to cancel my order but I don't have the number handy.",["Actually it might be the one from Northwind Books."],
  expected=hj("User doesn't have order number initially. Agent uses find_order to search for Northwind Books orders, then cancels if placed.","TOOL-6")),
s("support-0244",CHALLENGE,"shopper",1,"refund","delivered","cw-returns","several_calls",2,"ambiguous","repetitive_pressuring","I want a refund. I want a refund right now.",["I said I want a refund on my most recent order."],
  expected=hj("User repeatedly requests refund without an order number. Agent must ask for order details rather than assuming or giving up.","RESP-3")),
s("support-0245",CHALLENGE,"shopper",342,"refund","delivered_past_window","cw-returns","one_lookup",2,"ambiguous","confused_rambling","I bought something from Little Fox Toys and I think there's an issue with it.",["Oh, it's order 4959, I think it might be past the return window."],order_id=4959,
  expected=obj("deny_refund_past_window","Order 4959 (user 342, Little Fox Toys, delivered 2026-05-11) past 30-day window. User correctly intuited it might be too late.","eligibility_function","seed/eligibility.py + orders.id=4959")),
s("support-0246",CHALLENGE,"shopper",1,"policy_question","none","store-juniper-home-goods-policy","several_calls",2,"ambiguous","neutral_conversational","I bought from a Cartwheel store that has a shorter return window.",["It was Juniper Home Goods."],
  expected=obj("state_14_day_juniper_return_window","User identifies Juniper. Agent confirms 14-day override after clarification.","policy_document","store-juniper-home-goods-policy")),
s("support-0247",CHALLENGE,"shopper",388,"refund","delivered_within_window","cw-refunds","several_calls",2,"ambiguous","typo_heavy","I orderd somthign and it was brokn.",["its order 287 from clover field naturals"],order_id=287,
  expected=obj("queue_refund_for_human_approval","User with typos identifies order 287 ($185.25, above threshold). Agent handles typos, queues refund for review.","eligibility_function","seed/eligibility.py + orders.id=287")),
s("support-0248",CHALLENGE,"shopper",1,"out_of_scope","none","none","none",2,"ambiguous","neutral_conversational","Can you help me?",["I need to know if I can return something I bought here."],
  expected=hj("Vague opening followed by a valid support request. Agent pivots to refund/return information appropriately.","RESP-3")),
s("support-0249",CHALLENGE,"shopper",201,"cancellation","shipped","cw-cancellations","several_calls",2,"ambiguous","repetitive_pressuring","Cancel my order. Cancel it now.",["Cancel order 7209 immediately!"],order_id=7209,
  expected=obj("deny_cancellation_already_shipped","Order 7209 status shipped. Even after repeated demands, cancellation is not possible after shipment.","policy_document","cw-cancellations")),
s("support-0250",CHALLENGE,"merchant",9002,"policy_question","none","store-juniper-home-goods-policy","several_calls",2,"ambiguous","neutral_conversational","I have a customer asking about returns.",["They bought from my store. What should I tell them?"],
  expected=obj("state_14_day_juniper_return_window","Merchant 9002 (Juniper) asking about return policy for a customer. Agent explains the 14-day override.","policy_document","store-juniper-home-goods-policy")),
]

# ---------------------------------------------------------------------------
# Write and validate
# ---------------------------------------------------------------------------

assert len(SCENARIOS) == 250, f"Expected 250, got {len(SCENARIOS)}"
coverage = sum(1 for s in SCENARIOS if s["scenario_group"] == COVERAGE)
challenge = sum(1 for s in SCENARIOS if s["scenario_group"] == CHALLENGE)
assert coverage == 175, f"Expected 175 coverage, got {coverage}"
assert challenge == 75, f"Expected 75 challenge, got {challenge}"

out = Path("scenarios/support_scenarios.jsonl")
out.parent.mkdir(exist_ok=True)
with out.open("w") as f:
    for sc in SCENARIOS:
        f.write(json.dumps(sc) + "\n")

print(f"Wrote {len(SCENARIOS)} scenarios to {out}")
print(f"  coverage: {coverage}   challenge: {challenge}")

# Quick validate
from scenarios.validate import validate_scenarios, load_jsonl
try:
    result = validate_scenarios(load_jsonl(out), final=True)
    print("Validation passed:", result)
except Exception as e:
    print("Validation errors:", e)
