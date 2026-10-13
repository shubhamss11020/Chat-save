---
conversation_id: 8ee407ad-91bc-4ba1-ac7a-8f41a52187da
platform: claude
username: "harsh"
title: "Chrome extension publisher account type selection"
created_at: "2026-10-13 12:59:49 EDT"
updated_at: "2026-10-13 13:07:32 EDT"
---

# Chrome extension publisher account type selection

## User (2026-10-13 12:59:27 EDT)

i have one question when i will publish a chrome extension in the google developer dashboard after doing payment there is a option for trader and non-trader account to select what to select basically if i select non-trader account can i make publish to other members yes or no?

## Claude (2026-10-13 12:59:49 EDT)

> *Thinking:*
>

I'll start by reading the two skill files.

Yes, a non-trader can still publish to other people. Trader status is an EU consumer-law disclosure and doesn't control who can see or install your extension. As a non-trader you can still choose Public (open to everyone, EU users included), Unlisted, Private for trusted testers or Google Groups, or organization publishing. You can also add team members to your publisher. Google's Chrome Extensions DevRel said in August 2024 that this status has no effect on search ranking or discoverability.

The real difference is what your listing shows:
- **Traders** have to verify a legal name, an address and a phone number that can receive SMS. All three are shown publicly on the listing.
- **Non-traders** skip verification. EU users see a notice on the listing saying consumer rights don't apply to contracts with you.

If yours is a free hobby extension, non-trader is usually right. If it's for a business, or you charge for it in any way, you're probably a trader. Google says you have to make that call yourself, and you can change it later from the dashboard.

The report below covers the EU legal background, a table of visibility options, a guide to choosing, and a few caveats. Some third-party blogs claim non-traders lose EU visibility, but I found no official Google source for that.

<antArtifact identifier="compass_artifact_wf-77f31b40-b763-5b16-aa56-5e535ec94a8b_text/markdown" type="text/markdown" title="Chrome Web Store Trader vs Non-Trader: Can a Non-Trader Still Publish to Other People" version_uuid="01a13637-c89a-7364-8dcd-a62184833486">
# Chrome Web Store "Trader vs Non-Trader": Can a Non-Trader Still Publish to Other People?

**Yes. Choosing "non-trader" does not stop you from publishing your Chrome extension: it can still be public to everyone (including EU users), unlisted, or private for trusted testers and Google Groups. You can also still add team members to your publisher.** The setting is an EU consumer-law disclosure. It is not a permission or visibility switch. Its main effect is a label on your listing telling EU consumers that consumer-protection rights do not apply to contracts with you.

## TL;DR
- **Yes, a non-trader can publish to other people.** Google's distribution settings (Public, Unlisted, Private/trusted testers, Google Groups) don't depend on trader status. Oliver Dunk of Chrome Extensions DevRel wrote in the chromium-extensions Google Group on August 15, 2024 that trader/non-trader status "has no impact on your search rankings or discoverability."
- **The real difference is disclosure.** Traders must verify their legal name, address and an SMS-capable phone number, and these are posted publicly on the listing. Non-traders skip verification, but EU users see a "Non-trader" notice saying consumer rights do not apply.
- **How to pick:** a free hobby extension with no business behind it → non-trader. An extension made for your business, or one you sell or that has paid features → trader. You can switch later from the dashboard. Google says the choice is your own legal determination.

## Key Findings

### 1. What "trader" and "non-trader" mean
- The prompt exists because EU law requires marketplaces to tell consumers who they are dealing with. Google's Trader FAQ says: "The EU Digital Services Act requires that online marketplaces like the Chrome Web Store inform consumers in the EU about the identity of 'traders' on their platforms. On the Chrome Web Store, that would be the publisher of the extension."
- Google's policy page traces it back to the EU's New Deal for Consumers, a provision that took effect on May 28, 2022. The stricter trader *verification* step followed on February 17, 2024, when the EU began requiring marketplaces to identify and verify traders.
- **Everyone has to choose.** "All developers on the Chrome Web Store are required to declare if they are a Trader or Non-Trader."
- Google uses the European Commission's definitions:
  - **Trader:** "Any natural person or any legal person, who is acting for purposes relating to his trade, business, craft or profession in relation to contracts on this marketplace."
  - **Non-trader:** "Any natural person or any legal person, who is acting for purposes which are outside of his trade, business, craft or profession in relation to contracts on this marketplace."
- Google won't decide for you. "Each publisher must make their own determination. We can't provide direct answers for your specific case," and "it is the developer's responsibility to accurately self-declare their trader/non-trader status."

### 2. Can a non-trader publish publicly or to other members? Yes
None of the Developer Dashboard's distribution options are tied to trader status:

| Visibility option | Who can install | Available to non-traders? |
|---|---|---|
| **Public** | "lists your item on the Chrome Web Store for all users to see and install" | Yes |
| **Unlisted** | Not listed, but "allows anyone to install your item if they know its Chrome Web Store URL" | Yes |
| **Private: trusted testers** | Email addresses you add in your account settings | Yes |
| **Private: Google Groups** | "Any members of the specified groups, along with your trusted testers" (groups you own or manage) | Yes |
| **Private: domain / organization publishing** | Your Google Workspace domain, or external organizations whose admin approves you | Yes. Admins see your trader declaration on the approval page |

- Google states: "All visibility settings have the same policy requirements and will go through the same review process." No visibility option requires trader status.
- **Geography:** you choose "All regions" or specific countries in the Distribution tab. Nothing in Google's documentation hides non-trader items from EU users.
- **Ranking:** Oliver Dunk of Chrome Extensions DevRel wrote on August 15, 2024: "Your trader / non-trader status, as well as the status of any additional verification, has no impact on your search rankings or discoverability. So please do pick whichever option fits your situation."
- **Team members ("group publishing"):** you can invite members to your publisher and give each one of four roles: Viewer, Item Manager, Editor or Admin. Google says this "can be done at no cost, without paying the $5 registration fee." The old split between individual and group publishers is gone: "you can add members to any publisher you are an admin of." An item has only one publisher, and trader status belongs to that publisher account.

### 3. Consequences and restrictions of choosing non-trader
- **EU consumer notice on your listing.** Non-trader listings currently say: "Non-trader — This developer has not identified itself as a trader. For consumers in the European Union, please note that consumer rights do not apply to contracts between you and this developer." Google's policy page confirms that non-traders get this notice. The 2022 wording said rights "may not apply". It now says "do not apply".
- **No public personal contact details beyond what you choose to give.** Non-traders don't go through verification. Traders do: they must give "a legal name, a contact phone number and address", and this information "**will be posted publicly** at the bottom of your extension listing." The phone number must pass SMS verification and "will be displayed on the item listing." Traders also need a Google Payments profile, though verification itself is free. The trader listing reads: "This developer has identified itself as a trader per the definition from the European Union and committed to only offer products or services that comply with EU laws."
- **Group publisher nuance for traders:** "If you only publish extensions under the shared group publisher, and publish nothing on your own account, then the verification information you share is not publicly shown."
- **Monetization:** the Chrome Web Store no longer processes payments at all. Its built-in payments system was deprecated, and from February 1, 2021 "existing items and in-app purchases can no longer charge money with Chrome Web Store payments." Paid features now run through your own processor (Stripe, ExtensionPay, etc.). The Developer Agreement makes the charging developer solely responsible "for all related transactions and authentications, records, and taxes." Any item that offers purchases, additional features or subscriptions must include a physical address in account settings, whatever its trader status.
- **I found no official rule** stopping a non-trader from declaring in-app purchases. In practice some non-trader listings show "Offers in-app purchases." The rule that limits you is legal, not technical: if you are charging money as a business, you probably meet the EU "trader" definition, and declaring non-trader would be an inaccurate self-declaration.

### 4. How to decide, and whether you can change it later

| Your situation | Likely correct choice |
|---|---|
| Free personal or hobby extension, no business, no revenue | **Non-trader** |
| Free open-source tool built in your spare time, voluntary donations only | Usually **non-trader** (legal grey area) |
| Extension published by or for a company, or promoting your business/service | **Trader** |
| Paid extension, subscriptions, premium tier or in-app purchases | **Trader** |
| Freelance work published on behalf of a client's business | Lean **trader**, or have the client publish it |

- **Changing later:** yes. Google's FAQ says you can restart trader verification "at any time by changing from a Trader, to a Non-Trader, and then back to a Trader". It also describes "momentarily changing your trader status to a Non-Trader and then back to a Trader" to update details. Until a new trader finishes verification, the listing "will continue to be labelled as 'non-trader'" (dashboard message quoted by developer Casey Cupp in the chromium-extensions forum, August 14, 2024).

## Recommendations
1. **Free hobby extension:** choose **Non-trader**, then publish with **Public** visibility. EU users can still install it.
2. **Testing with friends or colleagues first:** use **Private** with trusted-tester emails or a Google Group, or **Unlisted** and share the link. Move to Public when you're ready.
3. **Business or monetized extension:** choose **Trader**. Get a phone number that can receive SMS and an address you're comfortable showing publicly. Companies can use the organization path: per Oliver Dunk (August 14, 2024), switching to non-trader and back to trader lets you "mark your account as an organization," which gives "additional verification options outside of personal ID," including a D-U-N-S number if applicable.
4. **Privacy-conscious trader:** consider publishing under a separate publisher, or a business entity and business address, so your home address isn't shown.
5. **If you're unsure:** get legal advice. Google says plainly that this is a determination you must make yourself.

## Caveats
- Some third-party blogs claim non-trader status reduces EU visibility or leads to listings being removed. No official Google source supports this, and it contradicts the DevRel statement above.
- The no-ranking-impact statement comes from Oliver Dunk's August 15, 2024 reply in the official chromium-extensions forum, not from formal policy documentation; his February 15, 2024 PSA likewise said "We do not anticipate any changes for developers marked as a non-trader." Google could change its practices.
- Whether a free extension with donations or a small paid tier makes you a "trader" depends on EU law. Google won't rule on individual cases.
- DSA Article 30 (Regulation (EU) 2022/2065) says that where a trader "fails to correct or complete that information," the marketplace "shall swiftly suspend the provision of its service to that trader… until the request has been fully complied with." Traders already active on February 17, 2024 had 12 months to supply the information or be suspended. This wording comes from a secondary reproduction of the regulation, so check it against the official EUR-Lex text before relying on it. So an inaccurate declaration could carry risk. How Google enforces misdeclarations isn't documented.
</antArtifact>
