# Evidence tiers: how you know a step is true

The one rule (document only verified behavior) fails in practice not because anyone ignores it,
but because it is easy to feel verified when you are not. Every step sits in one of three tiers.
Tag each step as you draft it, and never let a lower tier be worded like a higher one.

| Tier | Means | Wording licence |
|---|---|---|
| **DRIVEN** | You performed the action on a live instance and observed the result | Describe the outcome freely: "Saving setup advances the case and records who did it" |
| **OBSERVED** | You looked at the rendered screen (or a screenshot of it) but did not perform the action | Describe only what is visible: controls, labels, columns, states, help text |
| **INFERRED** | You read it in an FRS, a PR body, an API DTO, a Playwright spec or a Jira ticket | Not manual content. Drive it, or mark the step unverified |

## The three ways this goes wrong

**1. Writing from the model instead of the screen.** The most damaging. You have an API DTO or a
spec's field list, you write fluent prose describing the form, and it is wrong in specifics:
columns that don't exist, statuses the UI never shows, and the two columns a user actually looks
at left out. Real example: a QC control-lot page was documented as "scoped to a test and an
instrument" with an "Establishment" status, taken from the REST DTO. The screen has Control
Material and Manufacturer columns, no test or instrument, and only Active and Expired.

> Open and look at every screenshot before writing a word about that screen. Capturing evidence
> and then not reading it is the most common cause of a wrong manual.

**2. Selector-shape blindness.** You list a form with a DOM query and treat the list as complete.
Carbon renders toggles as `button[role="switch"]`, not `input`. Real example: a Basic Info page was
reported as having no Active toggle, and so "no way to retire a test", because the sweep queried
only `input, select, textarea`. Three toggles were invisible to it.

> To check whether a control exists, query
> `input, select, textarea, button, [role="switch"], [role="checkbox"], [role="radio"], [role="combobox"]`
> and cross-check against a screenshot.

**3. Concluding absence from a guessed endpoint.** A 404 on a path you made up is evidence about
your guess, not about the product. Real example: several QA features were listed as "not evidenced
anywhere" on the strength of five invented endpoint names.

> Enumerate real routes from the menu service and read the list to completion. Absence is only
> established by a route list that demonstrably does not contain the feature.

## Practical consequences

- An OBSERVED step says what the screen shows and stops. It does not narrate what pressing the
  button does.
- A step that must stay but could not be verified gets an italic note: *"This step has not yet been
  verified on a live instance. Confirm before publishing."* An honest gap is publishable; confident
  fiction is not.
- The provenance section names which steps were driven, which observed, which unverified, so a
  reviewer can aim their effort.
- Use the screen's vocabulary, not the spec's. The screen says "Control Material"; the DTO says
  `productName`. Readers read the screen.
- A control opening something is function, not persistence. "The Link Reagent button opens a Link
  Reagents dialog" is observed. "You can link a reagent to a test" claims a round trip you did not
  test.
- A run that passes and writes files can still be wrong (an unscoped selector once expanded the
  left-nav menu instead of the component meant). Size and exit code prove nothing about content:
  read the figure.
