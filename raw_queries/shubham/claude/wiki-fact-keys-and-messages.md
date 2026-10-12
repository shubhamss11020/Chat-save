---
conversation_id: 61dd3291-d49d-4e41-9e2f-c811992a20db
platform: claude
username: "shubham"
title: "Wiki fact keys and messages - Claude"
created_at: "2026-10-12T15:14:33.403824Z"
updated_at: "2026-10-12 14:18:13 EDT"
---

# Wiki fact keys and messages - Claude

## User (2026-10-12 14:18:13 EDT)

What did Stefan send Travis yesterday?

## Claude (2026-10-12 14:18:13 EDT)

Stefan sent Travis nothing yesterday (Sunday, Oct 11 Eastern). Travis's mailbox has no mail from Stefan for that day.

The only message Stefan sent yesterday was to Jameson Brown at Tann Electric, with no copy to Travis. It forwards a question from Greg Owens, CPA, at Keller & Owens about the 2024 tax on the 2B Holdings return. Owens asks whether the federal balance of $25,429 and the Kansas balance of $6,103 were paid, and by whom. He notes no payments appear in the Tann Electric file. The message has no attachments.

If you meant something else, such as messages Stefan sent to Travis on a different day, tell me the date.

Sources: msg 301428 (get_email, Stefan's Sent Items; delivered only to Stefan's mailbox)

## User (2026-10-12 14:18:13 EDT)

What are the most common fact keys across the wiki?

## Claude (2026-10-12 14:18:13 EDT)

I can't give you a reliable ranking. The wiki has about 11,728 indexed facts, and the only tool I have for scanning facts returns at most 200 rows per call, with no aggregation. So I can only count within a sample.

From the 200-row sample, the most frequent keys were:

- **`as_of`**: the most common by a clear margin, about a dozen times. It is page metadata giving the date a page's facts reflect.
- **`accountant`**: 6 times, all on the 2B Holdings LLC pages.
- **`current_status_source`**: 4 times. It is an `erp_owned` marker pointing to the ERP for live figures.
- **`status_raw`**: 3 times, on the .0160 Program page.
- **`supply_option_lead_time_raw`**: 3 times, all from one message.

Most other keys appeared once or twice. The sample is also skewed: it is heavily weighted toward the .0160 Program, 2026 Mid-Year Sales Review and 2B Holdings pages, because the search returns them in page order. Treat these counts as indicative only.

For an exact count, I can query each candidate key on its own (for example `fact_key="accountant"`) and count the rows across the whole wiki. That is a few calls per key and will not give a full ranking of every key.

Sources: page 187, 188, 382, 485, 595 (find_facts, 200-row sample; the count reflects that sample only)

## User (2026-10-12 14:18:13 EDT)

What’s the current status of the largest open purchase order, according to the vault and the ERP?

## Claude (2026-10-12 14:18:13 EDT)

I can't answer this yet. The ERP is not available in this session, and the vault doesn't give me a way to identify the largest open purchase order.

- **ERP:** I searched for the 3GM ERP tools and none loaded, so I could not check any PO's live status or open/closed state.
- **Vault:** The wiki has no list of open POs by size. Searches for "open purchase order" and "PO status" returned only unrelated mail and report pages such as "Mac Metal Sales Open Order Status" (a Steel Dynamics customer-portal snapshot from May 2026, not a current PO list). The Wheeling-Nippon page mentions POs P04525 and P04526, but I haven't verified their size or whether they're still open.

To finish this, either enable the 3GM ERP connector in this chat so I can rank open POs by value, or give me a PO number (for example P04525) and I'll pull its vault history and check its ERP status once the connector is available.

Sources: vault search_wiki (page 615, 616, 628), find_facts (no matching facts), search_raw (65 messages across 33 conversations, none a PO status report)

## User (2026-10-12 14:18:13 EDT)

Which supplier has the longest average lead time, and is it confirmed in both systems?

## Claude (2026-10-12 14:18:13 EDT)

Based on the vault, Wheeling-Nippon Steel has the longest quoted lead time, at 12 weeks. I can't confirm it in the ERP, and I can't give a true average.

The 12-week figure comes from a May 20, 2026 message about the .0160 program, where Wheeling-Nippon was compared with SDI (8 weeks) and BlueScope (4 weeks). Each supplier has only one or two quoted figures in the vault, so these are point quotes, not averages. Many other lead-time entries are dates, such as "week ending 10/31" or "End of June," and can't be converted into weeks without guessing. Wheeling-Nippon also has its own "ready week ending" entries, so its lead time may have changed since May.

The ERP is still unavailable in this session, so I couldn't check whether the 12 weeks matches any lead-time field there, or whether an average can be computed from actual PO receipts. If you enable the 3GM ERP connector, I can compare the two systems, though the ERP may not hold quoted lead times at all.

Sources: page 188 fact lead_time_wn_weeks · msg 63744; page 188 fact lead_times_raw · msg 63574; page 188 fact lead_time_sdi_weeks · msg 63744; page 188 fact lead_time_bsc_weeks · msg 63744; page 176 fact lead_time_weeks · msg 63574; find_facts key_words "lead time" (47 rows)
