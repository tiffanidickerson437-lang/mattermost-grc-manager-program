# Claims redline

Every statement below is quoted from the live page and checked on 17 July 2026.
The "corrected wording" column changes terminology and reconciles the two pages.
It does not assert a federal status that the pages do not already state, and
where the exact scope is an owner question I say so rather than fill it in.

Two references govern the corrections:

- FedRAMP notice [NTC-0004](https://www.fedramp.gov/notices/0004/), published
  25 February 2026: the single official label for a FedRAMP authorization becomes
  "Certified," and the Low, Moderate, and High baselines become Class A through D
  (Class B = Low and Li-SaaS, Class C = Moderate, Class D = High). FedRAMP will
  stop using "levels" or numbers for baseline labels to avoid confusion with the
  DoD Impact Level system. These changes are delivered by the FedRAMP
  Consolidated Rules for 2026 (CR26).
- The trust center at https://trust.mattermost.com/, which lists a current
  ISO/IEC 27001:2022 certificate.

## Summary

| # | Page | From | To |
|---|---|---|---|
| 1 | FAQ | "FedRAMP High authorized" | "FedRAMP Class D (High) Certified" |
| 2 | FAQ | Heading: "FedRAMP authorized (High or Moderate)" | "FedRAMP Certified (Class C (Moderate) or Class D (High))" |
| 3 | FAQ | "IL4, IL5, and IL6 environments" | "DoD IL4, IL5, and IL6 environments" (label as DoD, keep separate from the FedRAMP Class) |
| 4 | Overview | "in the process of acquiring Authority to Operate (ATO) and Certificate of Networthiness (CON)" | Reconcile with the FAQ: inherited Certificate to Field under Platform One's CATO, plus separately pursuing a standalone ATO and CON |
| 5 | Overview | "ISO 27001 Standards which are met to achieve alignment" | "certified to ISO/IEC 27001:2022" |

---

## 1. FAQ, FedRAMP status line

**Source:** https://docs.mattermost.com/product-overview/faq-federal-procurement.html

**Current wording**

> "Yes. Mattermost is currently FedRAMP High authorized via partner FedHIVE and
> listed on the FedRAMP Marketplace."

**Why it needs a change**

"High" and "authorized" are both retired under NTC-0004. The current baseline
name for High is Class D, and the current status word is Certified.

**Corrected wording**

> "Yes. Mattermost is currently FedRAMP Class D (High) Certified via partner
> FedHIVE and listed on the FedRAMP Marketplace."

Keep "via partner FedHIVE." Mattermost inherits FedHIVE's authorized package as a
hosted workload rather than holding its own; that wording is correct and load
bearing. During the transition, keeping "(High)" in parentheses helps buyers who
still search on the old term.

---

## 2. FAQ, the question heading

**Source:** https://docs.mattermost.com/product-overview/faq-federal-procurement.html

**Current wording**

> "Is Mattermost FedRAMP authorized (High or Moderate)?"

**Why it needs a change**

Same rename. "Authorized" becomes "Certified"; High and Moderate become Class D
and Class C.

**Corrected wording**

> "Is Mattermost FedRAMP Certified (Class C (Moderate) or Class D (High))?"

---

## 3. FAQ, DoD Impact Level line

**Source:** https://docs.mattermost.com/product-overview/faq-federal-procurement.html

**Current wording**

> "Mattermost has been deployed in IL4, IL5, and IL6 environments, as well as in
> JWICS and other classified IC networks."

**Why it needs a change**

IL4, IL5, and IL6 are correct DoD terminology and stay. The only issue is
adjacency: this DoD Impact Level answer sits a few lines below the FedRAMP status
line, and NTC-0004 renamed the FedRAMP baselines precisely so a reader would not
read "FedRAMP High" and "IL5" as the same authorization. Label the DoD usage and
keep it visibly separate.

**Corrected wording**

> "Mattermost has been deployed in DoD IL4, IL5, and IL6 environments, as well as
> in JWICS and other classified IC networks. These DoD Impact Levels are distinct
> from the FedRAMP Class stated above."

---

## 4. Overview, DoD certification answer

**Source:** https://docs.mattermost.com/product-overview/certifications-and-compliance.html

**Current wording**

> "We are in the process of acquiring Authority to Operate (ATO) and Certificate
> of Networthiness (CON) certifications."

**Why it needs a change**

This reads as "no DoD authorization yet," while the federal procurement FAQ
answers the same question with "Yes. Mattermost has received a Certificate to
Field under Platform One's Continuous Authority to Operate (CATO)." A federal
buyer landing on this page alone reaches the opposite conclusion from one landing
on the FAQ.

**Corrected wording**

> "Mattermost operates under Platform One's Continuous Authority to Operate
> (CATO) via a Certificate to Field, which authorizes the workload to run on
> Platform One's authorized DoD environment. Mattermost is separately pursuing its
> own Authority to Operate (ATO) and Certificate of Networthiness (CON)."

This combines only what the two pages already state between them, the inherited
Certificate to Field from the FAQ and the standalone ATO and CON pursuit from the
overview. It does not pick a winner. Confirming the exact scope and current
status of any standalone ATO or CON is an owner and day-one question, and should
be verified with the claim owner before publishing.

---

## 5. Overview, ISO 27001 line

**Source:** https://docs.mattermost.com/product-overview/certifications-and-compliance.html

**Current wording**

> "ISO 27001 Standards which are met to achieve alignment with international
> security guidelines."

**Why it needs a change**

The trust center lists a current ISO/IEC 27001:2022 certificate. "Alignment"
understates a certification the company holds.

**Corrected wording**

> "Mattermost is certified to ISO/IEC 27001:2022. The certificate is available on
> the trust center at https://trust.mattermost.com/."

---

## What this redline does not do

- It does not assert whether Mattermost holds a standalone DoD ATO, a CON, or its
  own FedRAMP package. Those are owner questions. The corrections reconcile the
  public wording; they do not resolve the underlying status.
- It does not change the FedHIVE framing. That claim is correct and stays.
- It does not remove DoD Impact Level terms. Those are correct in their own
  context.
