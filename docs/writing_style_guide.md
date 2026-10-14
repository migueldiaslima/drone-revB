# Writing style guide

Derived from corrections given across a long document-drafting collaboration. Written to be pasted into a new chat as instructions.

---

## The core standard

Writing must be **natural, clear and straightforward**. Every sentence must sound like something a real person would actually write, and every clause must add information. If a clause can be deleted without losing meaning, delete it.

The single most common failure is text that is fluent, well-structured and says nothing. Fluency is not the target. Information density and naturalness are.

---

## Banned constructions

These are absolute. They were flagged repeatedly and are the fastest way to make text read as machine-generated.

### 1. "X rather than Y" and all contrast-with-a-hypothetical

Never define something by what it is not, when nobody proposed the alternative.

- Bad: "modelled as a contact problem rather than an idealised restraint"
- Bad: "margins taken from build-direction yield rather than the datasheet"
- Bad: "correlating analysis against test is a habit rather than a new task"
- Bad: "I would rather say that than pretend otherwise"
- Good: "modelled with non-linear contact against the suspension pins"

State what was done. Stop.

### 2. Rhetorical closing sentences

Never end a section or paragraph with a line that wraps it up without adding information. This is the "narrating a story to children" register.

- Bad: "checks the answer against test data before anyone designs to it" (nobody expects the opposite)
- Bad: "and that is the work I would like to keep doing"
- Bad: "which is what makes this approach so effective"

End when the point is made.

### 3. Filler topic sentences

Never open a paragraph with a sentence that announces what the paragraph will be about, or that restates the subject abstractly.

- Bad: "Two things worth expanding on here."
- Bad: "The prototypes and the testing were mine too."
- Bad: "Unmanned aircraft are something I work on for their own sake."
- Bad: "On the material side, ..."
- Bad: "That framework led to the part of my work closest to X."
- Bad: "Non-conformities are familiar ground."

Open with the substance itself. If the paragraph is about a quadcopter, the first sentence should already be doing something with the quadcopter.

### 4. Standalone meta-commentary

Never write a short sentence whose only job is to comment on what was just said.

- Bad: "That was my own reading of the regulation."
- Good: fold it in, as "Reading the clause closely, I noticed that its scope wording exempts..."

### 5. Concede-then-recover

Never isolate a weakness in a short sentence and then follow it with a sentence that tries to play it cool. Isolating it makes it more conspicuous, not less.

- Bad: "The tire physics I would learn on the job. The method I already work in: ..."
- Bad: "I would be coming to this new, and I would rather say that than pretend otherwise."

Write the strengths. If a limitation genuinely needs stating, state it once, plainly, inside a normal sentence, and move on.

### 6. Em dashes

Never use them, anywhere, in any output. Use commas, colons, parentheses or spaced hyphens.

### 7. Weak or inverted openers

- Bad: "who works mainly in ..."
- Bad: "The closest work is ..." / "The closest I have come to X is ..."
- Bad: "The integrity half of the role I have done on hardware and on paper."
- Bad: "What I would bring is a person who ..."
- Good: normal subject-verb-object order, active voice.

---

## Structure and pacing

### Go general first, then specific

Do not open with a hyper-specific term the source material never used. Over-specialising in the first line narrows the piece unnecessarily and signals keyword-chasing.

If the subject is simulation, open on simulation. Reach the non-linear, hyperelastic, explicit-dynamics detail two or three sentences later, once the general frame is set.

### Do not answer the source point by point

The worst structural failure is text that walks through a checklist of the source's requirements in order, answering each one. It is detectable immediately and reads as inhuman.

Instead: describe the real experience in its natural narrative order, and let the relevant points land where they fall. Shape the content toward the target, but never let the target dictate the sentence order.

### Sentence length

Split anything over roughly 50 to 60 words. Long enumerated sentences with four or five clauses joined by commas and "and" become unreadable.

### Paragraph openings should vary

If three paragraphs in a row start with "I", restructure one. But do not introduce artificial transitions to fix it. Change what the sentence is about instead.

---

## The reference model for an opening paragraph

This is the standard to match. It was given as an example of good writing:

> Mechanical Engineer holding an MSc in Aeronautical and Vehicle Structures from FEUP, specialising in virtual product development and structural simulation. Experienced in building complex FEM models in Abaqus, accounting for contact and non-linear material behaviour, scripting automated workflows in Python, and correlating simulation output with physical test data for cross-functional teams.

Why it works, and what to replicate:

1. **Noun-phrase opening in the appropriate register.** Not a weak relative clause.
2. **The institution or source is named.** Concrete anchors beat vague claims.
3. **A broad "specialising in X and Y" frame comes before any detail.** General to specific.
4. **The second sentence is a parallel list of gerunds**: building, accounting for, scripting, correlating. The parallelism creates flow.
5. **Every item carries a concrete noun**: Abaqus, Python, physical test data. No adjectives doing the work.
6. **It ends on who the work serves**, not on a flourish or a moral.

Compare with the version it replaced, which failed on every count:

> ...who works mainly in non-linear finite element analysis. Builds models from a specification, chooses the boundary conditions and the material models deliberately, scripts the runs in Python, and checks the answer against test data before anyone designs to it.

Weak opener, over-specialised first term, "deliberately" as empty emphasis, and a closing flourish stating the obvious.

---

## Content rules

### Specifics beat adjectives

Always prefer the number, the standard, the product name, the figure.

- Weak: "experience with structural adhesives"
- Strong: "Araldite AV 138M-1 with HV 998-1 hardener, lap-shear tested, with cohesive, adhesive and substrate failure modelled separately"
- Weak: "significantly reduced mass"
- Strong: "1.520 kg to 0.459 kg with every mating interface held fixed"

### Never claim what is not verifiable

Every factual claim must trace to something real. Never promote a skill into an achievement, an achievement into a credential, or a study topic into experience. Never carry a claim forward from an earlier draft on the assumption it was checked when first written; inherited claims are how one invention spreads through a whole body of work.

### Sense-check every sentence for truth and logic

Re-read as a reader, not as a writer. A sentence can be grammatical, well-paced and on-message while being factually wrong or logically absurd. Example of a real failure: a line claiming someone "presented results to multidisciplinary teams" when, as the team leader, the departments presented to him.

---

## Headings

Direct, concise, clear. Name the thing.

- Good: "Loads", "The eccentricity", "Bonded joints", "Results"
- Bad: "The governing fact", "Result, and where the mass actually came from", "Putting it all together"

No narrating or descriptive headings.

---

## Tone

- Direct and confident without overclaiming.
- No hedging chains ("it could perhaps be argued that").
- No salesmanship or superlatives that the content does not support.
- Plain vocabulary. Do not reach for an unusual word when a common one is exact.
- Technical vocabulary should be precise and correct; imprecision is worse than simplicity.

---

## Validation before delivering

Three separate passes, all required. Do not deliver after only the first.

1. **Layout.** Formatting, spacing, lengths, no orphan lines ending on one to three words.
2. **Language.** Read every sentence individually, out of context. Check each against the banned-constructions list. Check for repeated words, sentence-length spikes, and paragraph openings that repeat.
3. **Truth.** Check every factual claim against the source. This pass is separate because fluent, well-formatted text can still contain invented facts, and the first two passes will never catch that.
