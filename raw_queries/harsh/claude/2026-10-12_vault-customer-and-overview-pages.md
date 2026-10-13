---
conversation_id: fdb508b8-ee9e-4bcb-8125-1dac4f1d8a41
platform: claude
username: "harsh"
title: "Vault customer and overview pages"
created_at: "2026-10-12 08:57:42 EDT"
updated_at: "2026-10-13 11:17:01 EDT"
---

# Vault customer and overview pages

## User (2026-10-12 08:55:58 EDT)

What does the vault say about our biggest customer by volume?

## Claude (2026-10-12 08:56:27 EDT)

> *Thinking:*
>

**The vault doesn't say who our biggest customer is by volume.** No page or fact ranks customers by tonnage, and the search for "biggest customer" only returns newsletters plus a February 2026 cash-flow thread that mentions "our biggest customers" without naming any.

The vault does hold per-account volume estimates from territory managers. The largest single-account figure I found is AJ's Steel Buildings at "closer to 5,000mt per year," which Maggie Moore gave in March 2026. All Metal Buildings is at "about 1500mt per year," from the same message. These are estimates, not measured volumes, and I haven't checked all 536 wiki pages, so this isn't a full ranking.

For actual tonnage by customer, the ERP is the authoritative source. I can run that query if you want it.

Sources: page 339 fact account_volume_raw · msg 69640; page 450 fact account_volume_raw · msg 69640; page 37 fact expected_order_volume_raw · msg 68428; search_raw "biggest customer" · msg 70991

## User (2026-10-12 08:57:23 EDT)

What’s in the overview pages, and how do they differ from the entity pages?

## Claude (2026-10-12 08:57:41 EDT)

> *Thinking:*
>

Overview pages are derived summaries that sit on top of the entity and analysis pages. They introduce no new facts: each one links to the page that holds the citation. Entity pages are the source layer, with facts that each carry their own citation. The vault has three overview pages:

- **3GM Group Structure** (page 666): the corporate group as the wiki currently records it, with a section on what isn't established. Its main points are that the legal relationship between 3GM Steel and Mac Metal Sales is unverified, and that the vault's sources contradict the group-entity label on Big Bertha Metals, which the sources describe as an externally owned customer. The overview also notes that Stefan Brown describes his 50% stake in All Boats Service Center in a personal financial statement.
- **Active Matters** (page 670): open or negotiating deals and disputes, sorted oldest first so staleness is visible. It covers only a sample of the analysis pages, so it's a floor, not a full list.
- **Obligations Register** (page 667): contracts, insurance policies, credit facilities and similar instruments with an expiry or renewal date, soonest first. One item needs attention: the Traditional Bank Borrowing Base Line of Credit had a stated maturity of 2026-03-31. The lender raised renewal in February, but no source records a renewal or a lapse, so it's unresolved as of today.

Because they're derived, overviews can lag or miss items. Each one has its own caveats, and the Group Structure and Active Matters pages flag their gaps.

Sources: page 666 (3GM Group Structure) · page 670 (Active Matters) · page 667 (Obligations Register) · page 568 / page 175 (Traditional Bank Borrowing Base Line of Credit, Traditional Bank, Inc.)
