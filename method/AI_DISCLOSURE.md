# Generative-AI Rules and Disclosure Statements

> Read this in Phase 1 Track B (checking the venue), in Phase 1.5 (deciding whether the
> venue is compatible with this workflow) and in Phase 6 (writing the AI statement and
> handling AI-generated figures).
>
> The table below was **checked on 2026-10-04**, against each publisher's own page; the
> quoted phrases were read in the original. Several publishers rewrote their policies in
> 2026 (Elsevier 2026-06, ACM 2026-05-14, the IEEE author guidelines 2026-06-25,
> Springer Nature's new framework 2026-09-10), so **treat this table as a signpost
> only**: for every manuscript, re-read the publisher's and the journal's current page
> in Phase 1 Track B and record the link and the date you read it in the venue notes.
> Taiwan's funders are covered in the zh-TW add-on (`setup/addons/zh-tw/README.md`).

## What each venue allows

| Venue | Letting AI draft text | Where the statement goes, what it says | AI-generated figures |
|---|---|---|---|
| Taylor & Francis (incl. Routledge) | **Not allowed**: "does not allow generative AI to create a first draft of a manuscript or sections of a manuscript". Polishing ("spelling, grammar and flow") and translation are allowed; for translation, say which author checked it | In the manuscript: tool name and version, purpose, reason. A statement is required even if no AI was used | Images of research results may not be generated or altered. Data visualizations, conceptual diagrams and flowcharts may be, with tool name and version in the caption; keep every version and prompt |
| Springer Nature (incl. LNCS / CCIS proceedings) | Green (polishing, translation) and yellow (outlining, "drafting sections based on author input") are allowed, both declared. Red: "Writing results or discussion independently", or generating claims | An AI Declaration in the manuscript: system, purpose, extent of the contribution, and confirmation that the authors take responsibility | **Strictest**: "creating content from text prompts or without verifiable source data or material" is red. Figures with a verifiable source (data, the authors' own material, code) are allowed with disclosure in the caption |
| Intellect | Two documents disagree: the ethics page says AI "should only be used to enhance readability and language"; AI policy v1.2 forbids "unverified drafts or sections ... without proper human review" | A separate closing section, "Acknowledgment of the Use of Generative AI and AI-Assisted Technologies"; v1.2 asks for tool, version, provider, date of use and purpose | Evidential images forbidden. Conceptual images and AI images in "creative research" allowed; **the caption must give the tool and the full prompt** ("Image generated using [Tool Name] from the prompt '[Exact Prompt]'"). Because the two documents disagree, ask the editor before submitting |
| Elsevier (2026-06 version) | Allowed; AI must "never be used as a substitute for human critical thinking". Basic grammar and spelling checks need no statement; substantive changes to sentence structure or paragraph organization do | A separate statement with a fixed heading (published with the article); AI used in the research itself goes in Methods | Illustrative figures allowed, with tool, version and use in the caption; data visualizations must be derived directly from the data; original research images forbidden; **graphical abstracts may not use general-purpose image generators** |
| Wiley | Allowed as an aid, not a substitute | Writing, editing and translation: acknowledgements. Research methods: methods section. Figures: caption | Research illustrations allowed with disclosure in the caption; **AI-edited photographs not allowed**; factual and evidential images may not be generated, altered or enhanced |
| SAGE | Assistive use (language, grammar, structure) needs no statement; generated content that affects the methods or conclusions does | Methods section or acknowledgements | Representative illustrations allowed with a statement; presenting generated images as novel research images is misuse |
| ACM (2026-05-14 version) | "ACM no longer requires the disclosure of information regarding the use of AI" (for writing) | AI used in the research (code, data, analysis, AI-dependent figures) **must be described in the methods** | No separate rule; AI-dependent research figures go in the methods |
| IEEE | AI-generated text, figures and code must be disclosed; pure language polishing need not be | Acknowledgements: name of the system, which sections, to what extent | Not forbidden; disclose in the acknowledgements; label AI-simulated data |

Links: Taylor & Francis <https://authorservices.taylorandfrancis.com/editorial-policies/using-ai-in-your-research-and-manuscript-preparations/>;
Springer Nature <https://www.springernature.com/gp/policies/editorial-policies/ai-manuscript-preparation>;
Intellect <https://www.intellectbooks.com/ethical-guidelines> and <https://www.intellectbooks.com/asset/3294/intellect-ai-policy-for-editors-etc-version-1.2.pdf>;
Elsevier <https://www.elsevier.com/about/policies-and-standards/generative-ai-policies-for-journals>;
Wiley <https://www.wiley.com/en-us/publishing/article/ai-guidelines>;
SAGE <https://www.sagepub.com/journals/publication-ethics-policies/artificial-intelligence-policy>;
ACM <https://www.acm.org/publications/policies/new-acm-policy-on-authorship> (blocks plain HTTP clients; read it in a browser);
IEEE <https://journals.ieeeauthorcenter.ieee.org/become-an-ieee-journal-author/publishing-ethics/guidelines-and-policies/submission-and-peer-review-policies/>.
None of them allows an AI to be listed as an author (the IEEE page does not say so in
as many words; it follows from its authorship criteria).

## What this means for the workflow

### Phase 1 Track B: the venue notes always have an "AI policy" section

Record in `venue-notes.md`: the link and the date read; whether AI may draft; where the
statement goes and which fields it needs (version number? date of use?); the rules for
figures; whether the journal has a stricter rule than its publisher (Taylor & Francis
says individual journals may allow language polishing only).

### Phase 1.5: is the venue compatible with this workflow?

By default this workflow has Claude draft the prose (Phase 5). When the venue does not
allow AI drafting (Taylor & Francis; Intellect's ethics page; Springer Nature for
results and discussion), **say so in the direction summary and let the author choose**:
a different venue; a different process (the author writes the first draft, or dictates
it section by section, and AI only translates and polishes); or a question to the
editor first. Phases 2 to 4 (literature, skeleton, method) go ahead as usual; **Phase 5
drafting waits for the author's choice.**

A worked case: a manuscript for a Taylor & Francis journal was written by the author in
their first language and translated and polished with AI; later English additions were
confirmed by the author as their own writing; the statement describes each part as it
happened.

### Phase 6: the statement follows the venue's place and fields, and the facts

- Place and fields come from the table above and the venue notes. ACM no longer asks
  about writing assistance, but AI used in the research always goes in the methods.
- **Say what actually happened.** Describe what this workflow did; do not shrink it to
  "language polishing only". If human coding was done with AI pre-labels visible,
  disclose the procedure in the methods as in `method/RIGOR_PROCESS.md` Stage 11.
- **Re-check the statement whenever the process or the model changes.** If you stop
  back-translating, switch to writing directly in English, or change models, every verb
  in the statement (written / translated / checked / edited) must be backed by a record
  in the project. If you are not sure which words the author wrote, ask.
- Masking, cropping frames, blurring or pixelating can count as image manipulation
  (Taylor & Francis). The statement lists everything done to an image.

### AI-generated figures

| Situation | What to do |
|---|---|
| Research results, observations, photographs of the actual work | **Never generate or alter with AI** (every publisher forbids it). Background removal, retouching and outpainting count as alteration |
| Conceptual diagrams, flowcharts, schematics | Mostly allowed; tool name and version in the caption (Intellect also wants the full prompt). **For Springer Nature, do not generate from a text prompt alone**: start from a base drawing by the authors, or generate the figure with code |
| Graphical abstract | Elsevier forbids general-purpose image generators |
| The artwork itself is AI-generated imagery (common in artistic research) | Intellect v1.2's "creative research" allows it, with tool and prompt in the caption; other publishers' pages say nothing, so ask the editor before submitting |

For any generated image, keep **the engine, model version, seed, full prompt and every
intermediate version** in the project's `figures/ai-generation-log.md`. Write the
caption and the statement from that log, never from memory.
