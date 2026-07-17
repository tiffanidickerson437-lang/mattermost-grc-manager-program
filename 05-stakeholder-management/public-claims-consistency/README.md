# Public claims consistency check

Two public Mattermost pages, reachable from the same documentation nav, describe
the company's federal status in ways that do not line up. A federal buyer doing
diligence can land on either one and come away with the opposite impression. A
third issue sits on top of both pages: they use FedRAMP wording that FedRAMP has
since replaced.

None of this needs any knowledge of Mattermost's internal posture. It is all on
pages they publish, and I checked every quote below against the live page on
17 July 2026. This is claims-consistency work, which is squarely what this role
owns. I am framing it as work to hand over, not as criticism.

## What I checked

| Page | Live link |
|---|---|
| Certifications and compliance overview | https://docs.mattermost.com/product-overview/certifications-and-compliance.html |
| U.S. federal procurement FAQ | https://docs.mattermost.com/product-overview/faq-federal-procurement.html |
| Trust center (ISO certificate) | https://trust.mattermost.com/ |
| FedRAMP notice NTC-0004 (the rename) | https://www.fedramp.gov/notices/0004/ |

## What I found

There are three separate threads here. The source pages blur them together, so I
am keeping them apart.

### 1. The two pages disagree on federal authorization status

The overview page, under the heading "Do you have Fed or Department of Defense
(DOD) Certification?", says:

> "We are in the process of acquiring Authority to Operate (ATO) and Certificate
> of Networthiness (CON) certifications."

The federal procurement FAQ, to the question "Has it been granted a DoD ATO
(Authority to Operate)?", says:

> "Yes. Mattermost has received a Certificate to Field under Platform One's
> Continuous Authority to Operate (CATO)."

One page reads as "not yet"; the other reads as "yes." Both can be technically
true at once, because a Certificate to Field under Platform One's Continuous ATO
is a specific thing, an authorization to run a workload on an already-authorized
DoD platform, and that is not the same as the company holding its own standalone
ATO or CON. But a buyer reading only the overview concludes there is no federal
authorization, and a buyer reading only the FAQ concludes there is full
authorization. The two pages should say the same thing. The exact scope of any
standalone ATO or CON is an owner question, so the fix reconciles the wording
without inventing a status for either page.

### 2. The FAQ uses FedRAMP wording that has been retired

The FAQ answers:

> "Yes. Mattermost is currently FedRAMP High authorized via partner FedHIVE and
> listed on the FedRAMP Marketplace."

FedRAMP notice
[NTC-0004](https://www.fedramp.gov/notices/0004/) (published 25 February 2026)
sets the single official label for a FedRAMP authorization to "Certified," and
replaces the Low, Moderate, and High baselines with Class A through D. Class D is
the current High baseline. So the current wording is "FedRAMP Class D (High)
Certified," not "FedRAMP High authorized." These changes are carried in the
FedRAMP Consolidated Rules for 2026 (CR26); industry write-ups put CR26's
effective date at 4 July 2026 with mandatory enforcement from 1 January 2027,
which is the timeline to plan the wording change against.

The same FAQ page also answers a separate question in DoD Impact Levels:

> "Mattermost has been deployed in IL4, IL5, and IL6 environments, as well as in
> JWICS and other classified IC networks."

IL4, IL5, and IL6 are correct DoD terminology and should stay. But NTC-0004
renamed the FedRAMP baselines for exactly this reason: to stop a reader
conflating a FedRAMP baseline with a DoD Impact Level. Having "FedRAMP High" and
"IL5" a few lines apart on the same page is the collision the rename exists to
prevent. The fix is to label the DoD usage clearly and keep it visibly separate
from the FedRAMP Class statement, not to remove it.

### 3. The overview understates a certification the company holds

The overview page describes ISO 27001 as alignment:

> "ISO 27001 Standards which are met to achieve alignment with international
> security guidelines."

The trust center at https://trust.mattermost.com/ lists a current ISO/IEC
27001:2022 certificate. Describing a held certification as "alignment"
understates it, and understating a real certificate is a claim worth correcting
in the buyer's favor.

## The precision worth protecting

The FAQ's "authorized via partner FedHIVE" wording is careful and correct, and
the fix must keep it. Mattermost, Inc. is not itself a FedRAMP-certified cloud
service provider. It appears inside FedHIVE's authorized boundary as a hosted
workload and inherits that package. That distinction is the whole point in a
federal questionnaire, and it is the thing that tends to get flattened into "we
are FedRAMP High" on a sales call. This deliverable protects the correct claim,
it does not just fix the wrong ones. The corrected wording carries "via partner
FedHIVE" through unchanged.

## Why this is the role's job

Keeping public claims accurate and consistent is what unblocks a security review.
A buyer's reviewer who finds two pages disagreeing, or spots retired vocabulary,
slows the deal down while they resolve it. This maps directly to the role's
success metric 4: customer security questionnaires and trust center content
maintained to unblock deal cycles. Finding and closing exactly these is the work.

## What is in this folder

| File | What it is |
|---|---|
| `README.md` | This summary. |
| `claims-redline.md` | A before/after table for every statement above, with the current public wording quoted and the corrected wording next to it. |
| `check_claims.py` | A runnable checker that scans page text for retired FedRAMP vocabulary and the issues above, and routes each to a person. It never decides. |
| `fixtures/` | The saved public page text the checker runs against offline. |

### Running the checker

```
# offline, against the saved fixtures, no dependencies:
python3 check_claims.py

# a live page (needs: pip install requests):
python3 check_claims.py --url https://docs.mattermost.com/product-overview/faq-federal-procurement.html

# a saved file:
python3 check_claims.py --file path/to/page.txt

# exit non-zero on findings, for CI:
python3 check_claims.py --strict
```

The checker prints each finding with the retired term, the corrected term, the
source line, and a "review required" note. It does not edit any page, and it does
not decide Mattermost's federal status. A person does.

## Sources, checked live 17 July 2026

- Certifications and compliance overview: https://docs.mattermost.com/product-overview/certifications-and-compliance.html
- U.S. federal procurement FAQ: https://docs.mattermost.com/product-overview/faq-federal-procurement.html
- Trust center: https://trust.mattermost.com/
- FedRAMP NTC-0004 (Authorized to Certified, Impact Levels to Class A-D): https://www.fedramp.gov/notices/0004/
