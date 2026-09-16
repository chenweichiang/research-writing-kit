# Method Analysis Cards and Decision Index

> **How this document is used**: when choosing a method for a new research question, start with the [Decision Index](#decision-index) and [Condition-Triggered Warnings](#condition-triggered-warnings) below to shortlist candidates, then read the full card(s) that match.
> **Evidence tags**: `[full text]` = checked against the source's full text; `[full text, web]` = checked against a web page or full-text PDF found online; `[abstract only]` = only the bibliographic record or abstract was confirmed — **do not treat this as a settled claim**.
> Quotations marked `[full text]` were checked against the source text when the cards were compiled. Quotations marked `[abstract only]` or `[full text, web]` were not re-checked line by line during this port — check them against the original before you put them in a manuscript.
> Known gaps are listed at the end of this document; methods the cards do not cover (semi-structured interviewing on its own, single-case experimental design, equivalence testing, technical-equivalence verification for reconstructed/restored versions, etc.) need separate research.
> Card numbers: A = quantitative, B = qualitative, C = mixed methods and design research, D = art and design practice research; numbering follows each group's own order.


## Decision index
> Each cell is based only on the cards; the bracketed codes are the cards it draws on. The cards themselves restate content from the author's own analysis playbook where noted, keeping that playbook's original attribution. The index is a starting point — decisions should rest on the full card text. Passages in the cards themselves that lack a citable source are flagged under "no source given"; check the cross-method-issues sections before deciding.
>
> **Card key**
> - Quantitative: A-1 Controlled experiment | A-2 Quasi-experiment | A-3 Cross-sectional survey | A-4 Scale development and validation | A-5 Longitudinal / repeated measures | A-6 Quantitative content analysis and computational text analysis | A-7 Behavioral logs and learning analytics | A-8 Kansei engineering and semantic differential | A-9 Rating / preference experiments
> - Qualitative: B-1 Reflexive thematic analysis | B-2 Grounded theory | B-3 Interpretative phenomenological analysis (IPA) | B-4 Ethnography | B-5 Case study | B-6 Discourse analysis / critical discourse analysis | B-7 Qualitative content analysis | B-8 Focus groups | B-9 Think-aloud and contextual inquiry | B-10 Diary studies and experience sampling | B-11 Visual / artefact analysis | B-12 Open-ended written questionnaires
> - Mixed methods and design research: C-1 Mixed-methods design | C-2 Design-based research (DBR) | C-3 Action research | C-4 Design Research Methodology (DRM) and sampling | C-5 Participatory design / co-design | C-6 Delphi expert-consensus method | C-7 HCI lab, field, and deployment study trade-offs | C-8 Systematic reviews, scoping reviews, and evidence/method maps
> - Art and design practice research: D-1 Research through Design (RtD) | D-2 Practice-based / practice-led research | D-3 Artistic research and performative research | D-4 First-person research and autoethnography | D-5 Speculative design, critical design, and design fiction | D-6 Creativity-support tools and interactive art evaluation | D-7 Documenting work and process | D-8 Digital art conservation and restoration | D-9 Critical and interpretive approaches
> - "A cross-method," "B cross-method," "C cross-method," "D cross-method" refer to the cross-method-issues section at the end of each group's cards (the sub-heading is given in parentheses).

---

How to use this: tag each research question with a "question shape," then look up the matching table for candidates. A single topic often has two or three question shapes at once (e.g., "is there a difference" plus "why"); match each shape separately, then use C-1 for how to integrate them into one paper. "No source given" in a table cell means the card provides a number but no citation for it (see the cross-method-issues sections).

### 1.1 Difference and magnitude (is there a difference between A and B, how large; how much changed before vs. after an intervention)

| Typical situation | Candidate method(s) | Claims it can support | Claims it cannot support | Sample-size justification | Most common reviewer objections |
|---|---|---|---|---|---|
| Comparing two or more system/interface conditions; for a system that does not yet exist, simulate it with a Wizard-of-Oz study [A-1] | Controlled experiment [A-1] | Causal claims about the treatment producing the outcome difference, provided random assignment, manipulation checks, and at least single blinding are genuinely carried out; a factorial design can support claims about which conditions the effect holds under [A-1] | External validity (generalizing a lab effect to real use); constructs sensitive to social desirability (creative support, willingness to use) carry demand characteristics and novelty effects [A-1]; writing a lab effect straight as "how users behave in real life" [C-7] | A priori power analysis at the design stage, plus a Monte Carlo design diagnosis (e.g., with the DeclareDesign R package) that checks bias and coverage together; power alone can look strong even under a biased design [A-1] | Treating a single Likert item as continuous and running a t-test/ANOVA; using the Aligned Rank Transform (ART) on a discrete DV; reporting p-values without effect sizes and confidence intervals; a post-hoc power analysis; treating within-subjects dependent observations as independent [A-1] |
| A course or teaching intervention that cannot randomly assign a whole class, leaving only one group [A-2] | Single-group pre–post design (quasi-experiment) [A-2] | A description of the pre–post change and its size, with the causal claim explicitly downgraded in the write-up [A-2] | "The intervention worked": this design cannot structurally separate the intervention's effect from testing, maturation, and history effects; an example design diagnosis of a single-group pre–post study with N = 40 found that, when a testing effect was present, power was 1.000 but coverage was only 0.218 (this number applies only to that one declared model — rerun the diagnosis for a new topic) [A-2] | Run a design-stage diagnosis first and judge by coverage; power alone can mislead. Adding a control group improves the estimate more than adding participants does [A-2] | Writing a significant difference straight as "the intervention worked" without mentioning testing or maturation effects; no design-stage diagnosis, so the sample size has no stated rationale; mixing the strength of causal language appropriate to quasi-experiments with that of correlational studies [A-2] |
| Several parallel classes or workshop cohorts exist, so the intervention can be delayed or staggered [A-2] | Waitlist control, staggered start, or non-equivalent control group (quasi-experiment) [A-2] | A weak causal claim, if done properly; in the same example diagnosis, switching to a waitlist-control (difference-in-differences) design brought bias to about 0 and coverage to about 0.95 [A-2] | A causal claim when the control group's baseline is not comparable [A-2] | Same as above, plus reporting whether attrition is comparable between the treatment and control groups [A-2] | Using the class next door as a convenience control without establishing whether the baselines are comparable [A-2] |
| Tracking the same group of people across multiple time points [A-5] | Longitudinal / repeated-measures design [A-5] | Within-person patterns of change; individual differences in trajectories [A-5] | Temporal order is not causality; repeated administration of the same scale produces a testing effect that accumulates over waves [A-5] | Estimate at the design stage how attrition affects power, factoring in the intraclass correlation (ICC) and number of waves, e.g. with the `simr` package [A-5] | Treating repeated measures as independent observations; not reporting attrition or running a sensitivity analysis; comparing means across waves without verifying measurement invariance [A-5] |
| Having readers or viewers rate the quality of, or their preference among, works, texts, or generated content [A-9] | Rating / preference experiment [A-9] | A rating panel's relative preference ranking or rating distribution over a stimulus set; when raters are trained and the criteria are explicit, some degree of group consensus [A-9] | Treating a single rater's judgment — often the author's own — as representative of a group; treating results from a convenience-recruited panel as generalizable [A-9] | The number and expertise of independent raters (enough to compute a stable inter-rater reliability), plus the number of stimuli in the set — this is not a sample size in the statistical-power sense [A-9] | The author rating their own work and calling it a rating experiment; recruiting from one's own circle and claiming generality; treating an ordinal rating scale as continuous without an ordinal robustness check; retrospectively cherry-picking the best-performing subset of works before sending them out for rating [A-9] |
| Comparing how well two or more creative tools support the creative process [D-6] | Creativity-support tool evaluation (CSI scale) [D-6] | A comparison of tools' relative performance across the six CSI dimensions [D-6] | A verdict on the aesthetic merit of the resulting work — CSI measures support for the creative process; it does not evaluate the work itself [D-6] | Driven by statistical-power needs (the card states that between-group comparisons typically need several dozen participants or more; no source given) [D-6] | Treating the CSI total score as a single indicator while ignoring that the six dimensions measure different things; treating "the audience found it interesting" as evidence the work succeeded [D-6] |

### 1.2 Relationship and prediction (is there a relationship between X and Y, what predicts what)

| Typical situation | Candidate method(s) | Claims it can support | Claims it cannot support | Sample-size justification | Most common reviewer objections |
|---|---|---|---|---|---|
| A single time point, wanting to know the relationship between variables in some population [A-3] | Cross-sectional survey [A-3] | Description of population characteristics, relationship strength between variables, comparisons between groups [A-3] | Causal direction (cannot rule out reverse causation or a third variable); using cross-sectional data for a mediation analysis and claiming it confirms a causal mechanism [A-3] | A conventional power analysis, with the sampling method (probability or convenience) stated; theory-testing needs a broad sample while exploratory description can be narrow and deep (Cash et al., 2022); the rules of thumb behind SEM sample-size heuristics are themselves contested [A-3] | Writing correlations as causal claims; generalizing from a convenience sample (e.g., one's own class) to a population; ignoring common method variance [A-3] |
| Multi-wave data available, wanting to know what predicts the trajectory of change [A-5] | Longitudinal research and growth models [A-5] | Predictive relationships when temporal order is clear [A-5] | Causation (still requires controlling confounders and handling selective attrition) [A-5] | Same as the longitudinal row in 1.1 [A-5] | Writing a correlational pattern over time as a causal claim [A-5] |
| Which physical attributes of a product or design correspond to which subjective feelings users report [A-8] | Kansei engineering and the semantic differential method [A-8] | A statistical association, usable to guide design decisions, between affective vocabulary and product attributes in a semantic space [A-8] | "Fully capturing the user's feeling": the semantic differential method only captures the part of feeling that can be put into words; there is currently no validated tool on the product-attribute side of the space [A-8] | Keep collecting vocabulary until no new words appear (roughly 50–600 words depending on the domain), then reduce it; participants must represent the target group [A-8] | Reducing the vocabulary before it is exhaustively collected; inconsistent direction of the bipolar adjectives; applying vocabulary collected in one culture/language directly to another; doing only the semantic-space analysis without connecting it back to concrete design parameters [A-8] |

### 1.3 Prevalence and distribution (how common is something, how is it distributed)

| Typical situation | Candidate method(s) | Claims it can support | Claims it cannot support | Sample-size justification | Most common reviewer objections |
|---|---|---|---|---|---|
| The prevalence or distribution of some characteristic in a population [A-3] | Cross-sectional survey [A-3] | Description of population characteristics and their distribution [A-3] | Generalizing from a convenience sample to a population [A-3] | Reporting sampling method (probability or convenience), response rate, and non-response bias [A-3] | Generalizing from convenience sampling to a population; ignoring common method variance [A-3] |
| How often, or in what proportion, some category or theme occurs in a body of text; measuring a latent textual dimension with automated methods [A-6] | Quantitative content analysis and computational text analysis [A-6] | Descriptions of category frequency when there is adequate reliability evidence; automated measures that have been validated against, and can replicate, human coding [A-6] | Treating unvalidated automated output (including LLM output) as ground truth [A-6] | State the corpus's inclusion/exclusion rules (time period, source, language) and the train/test split; the card states that fewer than roughly 30–50 documents is generally unsuited to computational methods (no source given) [A-6] | Reporting a single reliability number without documenting how the codebook evolved; treating unvalidated automated output as equivalent to human coding; conflating reliability with validity; vague sampling rules [A-6] |
| Needing a systematic, auditable categorization of text, and having to justify the process to a quantitatively minded readership [B-7] | Qualitative content analysis (summative, Mayring-style) [B-7] | A systematic description of how categories are distributed; more tolerant than reflexive thematic analysis of statements like "how many items mentioned X," though still not statistical inference [B-7] | Frequency claims unsupported by a codebook and reliability check; deep meaning-making [B-7] | The logic of "covering all known categories" [B-7] | Treating this as interchangeable with thematic analysis; no codebook, or no account of how it was developed; mixing conventional, directed, and summative approaches without saying which one was used [B-7] |
| Collecting written statements from a group under classroom-size or scheduling constraints [B-12] | Open-ended written questionnaire [B-12] | Breadth scanning: how many people expressed which positions or fragments of experience, and in what words [B-12] | The fine texture of deep experience; the process of negotiating meaning; calling this "an interview" [B-12] | The diversity of viewpoints covered is what counts; raw headcount is not the criterion. Report the non-completion rate [B-12] | Writing open-ended responses up as semi-structured interviews (a misleading label); one- or two-sentence responses cannot support the claimed depth of analysis [B-12] |
| Which methods a research field has used, where the evidence is distributed, where the gaps are [C-8] | Scoping reviews, systematic maps, and method maps [C-8] | Breadth and distribution of evidence; which method categories are common or rare; thematic gaps [C-8] | Conclusions about evidence quality (scoping reviews generally do not do risk-of-bias assessment); treating a "systematized" review as equal in rigor to a full systematic review [C-8] | A reproducible search strategy (databases, query strings, dates, exclusion counts at each stage); dual screening with an agreement rate reported [C-8] | Writing a scoping review up as a systematic review; giving only keywords without database and screening flow; no published extraction table; claiming comprehensive coverage from a single database; no agreement rate reported [C-8] |


### 1.4 Experience and meaning (how do people experience or understand something)

| Typical situation | Candidate method(s) | Claims it can support | Claims it cannot support | Sample-size justification | Most common reviewer objections |
|---|---|---|---|---|---|
| Around one research question, what meaningful patterns emerge across participants or texts [B-1] | Reflexive thematic analysis [B-1] | Deep, interpretive description of meaningful patterns; shared meaning structures across cases; exploratory, hypothesis-generating claims [B-1] | Prevalence claims ("most respondents felt..."); generalizing across samples; causation; claiming an "objective" or single correct coding [B-1] | Information power (Malterud et al., 2016); Braun & Clarke recommend avoiding claims of "saturation" [B-1] | Using reflexive-TA language while also reporting multiple coders and Kappa (or the reverse: being pushed by a reviewer to meet coding-reliability standards); mistaking a "topic summary" ("experiences of X," "benefits of X") for a genuine theme; a teacher-researcher's reflexivity statement reduced to one boilerplate sentence [B-1] |
| How one person or a small group personally experiences a particular phenomenon or event [B-3] | Interpretative phenomenological analysis (IPA) [B-3] | Deep, personalized, meaning-level understanding of a specific experience; case-by-case comparison within a small sample [B-3] | Frequency or prevalence; cross-group representativeness; predicting behavior beyond the experience itself [B-3] | Deliberately small and homogeneous, with case depth prioritized over saturation or information power (the card gives 3–6 cases at student level, 10–15 for larger studies; no source given) [B-3] | Labeling something IPA while actually cross-comparing cases for common patterns from the start (which is really TA); a sample size far exceeding convention; unclear criteria for homogeneity [B-3] |
| How a group of people negotiates and jointly constructs a view on some issue through interactive discussion [B-8] | Focus groups [B-8] | The process of collective negotiation, consensus formation, or disagreement; how group norms shape individual statements [B-8] | Deep disclosure of private personal experience; generalizing group opinion distribution from a handful of sessions; treating each speaker's utterance as an independent individual opinion [B-8] | Counted by session (the card gives 6–10 people per session; no source given), with the number of sessions set by topic complexity and whether cross-group comparison is needed; state the rationale for homogeneous vs. heterogeneous groups [B-8] | Breaking a transcript into isolated sentences for thematic analysis without analyzing the interaction itself; not addressing how the moderator handled power imbalances within the group [B-8] |
| How experience, behavior, or emotion changes over time and under what circumstances (e.g., a semester-long learning or creative process) [B-10] | Diary studies and experience sampling [B-10] | Patterns of change over time; the covariation of context and experience; a description closer to the moment than a retrospective interview [B-10] | Causation (unless paired with an experimental manipulation); claiming coverage of all relevant experience when participants self-select when to record [B-10] | Jointly determined by number of recording time points and number of participants; information power or saturation can be invoked, plus stating whether the recording period spans the range of variation in the target experience [B-10] | Low compliance that goes unreported or unaddressed; backfilling several days at once after the fact and presenting it as a diary [B-10] |
| A researcher or designer's own long-term use of a system they designed, or long-term engagement in some practice [D-4] | First-person research and autoethnography [D-4] | Existential claims of the form "this kind of experience is possible and worth noting"; design implications drawn from deep description of one's own experience [D-4] | Inference about other people's experience; "users generally have this kind of experience" [D-4] | N = 1 (or a specific team member), justified by depth and reflexivity — sampling and saturation concepts do not apply [D-4] | "That's just your own experience" (the paper needs to actively justify why N = 1 fits the question); trying something once and packaging it as autoethnography, lacking the required longevity and systematic documentation [D-4] |
| Quickly scanning a group's fragments of experience in writing, as a lead-in to or supplement for deep interviews [B-12] | Open-ended written questionnaire [B-12] | Breadth of experience and positions; screening for who to interview in depth later [B-12] | Depth that only follow-up probing can reach; negotiation of meaning [B-12] | Diversity of viewpoints covered [B-12] | A misleading label; analytical depth that outstrips what the data can support [B-12] |

### 1.5 Process and mechanism (how does X work in this context, why does it happen this way)

| Typical situation | Candidate method(s) | Claims it can support | Claims it cannot support | Sample-size justification | Most common reviewer objections |
|---|---|---|---|---|---|
| Process- or stage-oriented questions such as "how do people do X" or "what is the core process behind this phenomenon" [B-2] | Grounded theory [B-2] | A theory, grounded in the data, that explains a process or action, including a core category and its relationships; middle-range theory [B-2] | Generalizing beyond the sample to a population; cross-case frequency statistics [B-2] | Theoretical sampling continued until theoretical saturation; this saturation is bound to the constant-comparative method and is not the same concept as the "saturation" reflexive TA rejects [B-2] | No theoretical sampling, memo trail, or theoretical integration — the output is just a classification scheme ("grounded theory lite"); citing Charmaz's method label while running Strauss & Corbin's three-stage coding procedure; in HCI/design venues, needing to justify at length the choice of GT over TA [B-2] |
| A single or a few cases where the researcher's control is low and the phenomenon and its context are hard to separate — how and why did this happen [B-5] | Case study [B-5] | Deep explanation of the process/mechanism within a case; analytic generalization to a theoretical proposition, with population-level generalization a separate claim it does not support; under strategic case selection, "this is how this kind of situation may play out" [B-5] | Statistical generalization to a population (unless a multiple-case replication design with a clearly stated logic is used) [B-5] | The logic of case selection (extreme, critical, typical, maximum-variation); the choice between single and multiple cases, with multiple cases using replication logic; state the case boundary [B-5] | "How can you generalize from just one case?"; being unable to say clearly why this case was chosen; using "case study" as a catch-all label when the data is not solid; a single-course case study that does not say whether it follows Stake or Yin [B-5] |
| How practice runs in a field, community, or classroom, and how members make meaning within it [B-4] | Ethnography (including short-term, digital, and classroom ethnography) [B-4] | Thick description of a field's cultural practices; the field's internal logic and system of meaning [B-4] | Generalizing across fields (unless doing a multi-site comparative ethnography with a stated logic); prevalence; causation [B-4] | The field is the sampling unit, with time spent in the field the core justification; short-term ethnography must state the trade-off of sacrificing long immersion [B-4] | Calling it ethnography despite insufficient time in the field; unclear account of the researcher's role (teacher-observer vs. outside observer); missing reflexivity about how the researcher shaped the interaction [B-4] |
| A user's cognition and decisions while performing a task in the moment (think-aloud); how work actually gets done at a real site (contextual inquiry) [B-9] | Think-aloud protocol and contextual inquiry [B-9] | In-the-moment cognitive/operational process during a task; diagnosis of interface or tool problem points; the logic of practice in a real context [B-9] | Users' general attitudes or preferences; assuming without testing that verbalizing has zero effect on task performance; generalizing across contexts [B-9] | Counted by task session, single digits to low teens (the card cites 5–8 people as typically finding most major usability problems, a usability rule of thumb; it is not a statistical inference; no source given); contextual inquiry is driven by site diversity, and headcount is not the criterion [B-9] | Treating retrospective probing after the fact as think-aloud data (a different evidentiary strength); running contextual inquiry as mere shadowing, without collaborative interpretation checks with the user [B-9] |
| Using behavioral traces, without relying on self-report, to see step by step what users or learners actually did, and what the structure of their collaboration looks like [A-7] | Behavioral logs and learning analytics (sequence analysis, social network analysis, ENA) [A-7] | Common paths in a behavioral sequence; structural features of an interaction network (core nodes, subgroups) [A-7] | Motivation or understanding ("did X" does not mean "understood X"); treating centrality metrics as causal influence [A-7] | Counted by the event, since person-level counts are not the relevant unit here — the key is whether event density is enough for stable estimation (the card cites a floor of about 20–30 events; no source given) [A-7] | Equating clicks or dwell time directly with learning engagement; unclear criteria for the number of clusters; arbitrary substitution-cost settings in sequence analysis with no theoretical grounding [A-7] |
| Needing both "is there a difference, how large" and "why, how does it happen" at once [C-1] | Mixed methods (explanatory sequential, convergent, exploratory sequential) [C-1] | An integrated judgment of whether the two strands agree (meta-inference); a mechanistic explanation of a quantitative finding; qualitative evidence given scale by quantitative support [C-1] | Treating the qualitative and quantitative samples as adding up to one larger sample; using one strand's rigor to paper over the other strand's methodological weaknesses [C-1] | Each strand justified on its own terms (qualitative by its own method, quantitative by power analysis) — mixing does not relax the requirements for either strand; in a sequential design, the earlier stage's results determine the later stage's sampling [C-1] | Two studies stapled together: no joint display or narrative integration, independent sampling across strands, a paper that could just as easily be split in two, no meta-inference in the conclusion [C-1] |

### 1.6 Feasibility and design knowledge (can it be built, and what knowledge does building it produce)

| Typical situation | Candidate method(s) | Claims it can support | Claims it cannot support | Sample-size justification | Most common reviewer objections |
|---|---|---|---|---|---|
| Integrating new technology, a new context, or a new form to demonstrate a previously nonexistent possibility; a transferable intermediate concept emerging across a body of work [D-1] | Research through Design (RtD; annotated portfolios, strong concepts) [D-1] | That a design direction is feasible, meaningful, and worth the field's attention; that the work demonstrates a design stance or concept not previously clearly articulated [D-1] | Causal claims; generalized theory across contexts; claims of exact reproducibility [D-1] | Not sample-driven: one work, or a small portfolio; justified by "this case demonstrates something conceptually important"; a strong-concept claim needs both horizontal and vertical grounding [D-1] | A reviewer applying a quantitative frame and asking "where is your sample size"; showing only the design process without addressing relevance (current state vs. a better state), which reads as personal exploration [D-1] |
| The creative work itself is the basis for the knowledge contribution (practice-based), or the study's main output is new understanding of the practice (practice-led) [D-2] | Practice-based / practice-led research [D-2] | The work itself as part of the knowledge claim; new understanding of how a practice works [D-2] | A claim that can be fully verified from the text alone, detached from the work [D-2] | The originality and scope of contribution of this work or set of works — no random-sampling concept applies [D-2] | Conflating practice-based and practice-led; if the claim still holds fully once the work is removed, the necessity of the work itself becomes questionable [D-2] |
| Artistic practice itself as inquiry, revealing knowledge that cannot be reduced to textual propositions [D-3] | Artistic research and performative research [D-3] | Artistic knowledge obtained through cognitive and artistic means; the creative process as a process of data generation [D-3] | Reproducibility; predictive, explanatory theory; an intervention effective across a population [D-3] | Depth of the researcher's own creative-practice case, often a single long-term project at doctoral level [D-3] | "Where is the research here, beyond the creative work itself?"; slapping the label "artistic research" on any creative work without identifying an inquiry question and a knowledge contribution [D-3] |
| How an intervention (course, tool, teaching design) actually functions in a real classroom, while also producing transferable design principles [C-2] | Design-based research (DBR) [C-2] | How the design functioned in a specific setting and through which iterative revisions; mediating mechanisms in the learning process; contextualized design principles [C-2] | Cross-context effect sizes or efficacy comparisons; claiming "proven effective" without describing the history of iterative revisions [C-2] | One to a few classes, chosen for being "theoretically relevant cases"; probability sampling is not used here [C-2] | Treating many rounds of revision as proof of effectiveness while not reporting failed iterations; no transferable design principles; using DBR as an easy stand-in for action research; unaddressed power relations between teacher and students [C-2] |
| The researcher's own teaching setting has a problem; after adjustment, did it improve, and how [C-3] | Action research (including the common form used in teaching-practice research grants) [C-3] | The researcher's observed change and reflection after this round of intervention, in a specific class [C-3] | Cross-class, cross-teacher causal inference or effect-size comparison; "this teaching method generally works" [C-3] | The class or workshop the researcher actually teaches, justified by contextual representativeness; statistical representativeness is not required here [C-3] | "The teacher felt students responded better" presented as a research finding; calling one round of change "action research"; grades not decoupled from research data; running inferential statistics on data from single-digit to low-teens sample sizes [C-3] |
| Whether some design-support tool or method actually helps design practice, and how [C-4] | Design Research Methodology (DRM) [C-4] | Empirical description of the current state (DS-I); theory-building and preliminary validation of a support tool (PS); effect evaluation in an applied context (DS-II) [C-4] | Skipping the descriptive stage and claiming the tool "improved design"; treating a single-stage output as a complete DRM study [C-4] | The eight sampling considerations and dual-loop sampling process from Cash et al. (2022) [C-4] | Conflating descriptive and prescriptive research goals; sampling decisions left unexplained; treating small-scale PS-stage prototype testing as DS-II-level evidence [C-4] |
| Users or stakeholders co-constructing a design direction that is meaningful to them [C-5] | Participatory design / co-design workshops [C-5] | Design ideas co-produced by participants; a collective interpretation of situated needs; tacit knowledge surfaced through co-creation [C-5] | "Users' general needs" (workshop participants are a convenience sample) [C-5] | The representativeness and role mix of relevant stakeholders (the card cites 5–15 people per session, possibly multiple sessions; no source given) [C-5] | Generalizing a single session's output directly to "user needs"; conflating this with usability testing; prompts and materials that systematically steer participants toward a predetermined direction without disclosing it; participation used to rubber-stamp a system ("participation-washing") [C-5] |
| Lacking empirical data but needing expert judgment on a threshold, indicator weights, priorities, or future trends [C-6] | Delphi expert-consensus method [C-6] | The degree of consensus reached by a specific expert panel after a specific number of rounds, and how that consensus converged or diverged [C-6] | Equating consensus with truth; representing all stakeholders' views [C-6] | Professional representativeness and diversity, with recruitment criteria stated (the card cites 10–30 people as common; no source given) [C-6] | An overly homogeneous expert panel; vague or after-the-fact consensus criteria; calling a single round "Delphi"; unreported or unanalyzed dropout [C-6] |
| Placing a system into users' daily lives or work for a period of time [C-7] | Deployment study ("in the wild"), as opposed to lab and short-term field studies [C-7] | Real-world adoption patterns and unexpected appropriations over the long term [C-7] | Strict causation (confounders usually cannot be ruled out); treating a single deployment case as generalizable causal evidence [C-7] | Usually a smaller sample, trading it for a longer observation period [C-7] | Overstating a small, short-term field trial as "in the wild"; not reporting attrition and technical failures during deployment [C-7] |

### 1.7 Interpretation and critique (how can this work, system, or text be read; what assumptions does it reveal)

| Typical situation | Candidate method(s) | Claims it can support | Claims it cannot support | Sample-size justification | Most common reviewer objections |
|---|---|---|---|---|---|
| Under what theoretical framing a work or system can be meaningfully interpreted; what cultural, political, or aesthetic assumptions its formal choices reveal [D-9] | Critical and interpretive approaches (interaction/design criticism, humanistic HCI, media archaeology) [D-9] | A defensible, theoretically grounded reading, whose force comes from the persuasiveness of the argument and its theoretical grounding [D-9] | Empirical claims such as "most viewers read it this way" [D-9] | The representativeness or typicality of the object chosen for deep analysis (why this one) [D-9] | Over-extended interpretation, where switching theoretical frames could support the opposite story; theoretical terminology used as decoration; reflexive positioning reduced to one sentence [D-9] |
| What version of reality or power relation policy documents, teaching discourse, or AI discourse is constructing [B-6] | Discourse analysis / critical discourse analysis [B-6] | How text or talk constructs a particular version of reality, identity, or relationship; critical exposure of the ideological assumptions behind language choices [B-6] | Speakers' actual internal psychological state; frequency or prevalence; generalizing beyond the textual context [B-6] | By text fragment, with no fixed threshold, set by the discursive diversity of the corpus and the depth of analysis [B-6] | Doing "content analysis with theoretical jargon added"; selectively citing passages that support a predetermined position while not addressing counter-examples [B-6] |
| Systematic analysis of student portfolios, images of the creative process, or exhibited works [B-11] | Visual / artefact analysis (researcher-led qualitative interpretation) [B-11] | Systematic, auditable description of a work's or portfolio's form and meaning; turning a teacher's taste judgment into an accountable analytical framework [B-11] | An "objective" aesthetic-quality ranking detached from the interpretive framework; generalizing from a single work to "how this kind of creation generally is" [B-11] | Counted by number of works, set by portfolio completeness and analytic purpose; cross-form generalization needs more works and consideration of information power or saturation [B-11] | The researcher being both the grading teacher and the analyst without addressing that dual role; an analytical framework with no stated source, looking chosen after the fact to fit the conclusion; a handful of selected works standing in for the whole class [B-11] |
| What things might look like under different technological or social conditions, opening contested assumptions to discussion [D-5] | Speculative design, critical design, design fiction, adversarial design [D-5] | Critical exposure of a specific technological or social assumption; opening a space for public discussion [D-5] | User acceptance, market viability; "the future the public really wants" [D-5] | Usually no user sample; the data is the proposed artifact itself and the discourse it provokes after public display [D-5] | A concept render dressed up as research, with no credible bridge (perceptual bridge) between the proposal and the audience's actual experience; "whose preferred future does this represent" [D-5] |

### 1.8 Preservation and reconstruction (is it still the same work; how to preserve or reconstruct it)

| Typical situation | Candidate method(s) | Claims it can support | Claims it cannot support | Sample-size justification | Most common reviewer objections |
|---|---|---|---|---|---|
| A partially degraded or technologically obsolete media artwork: which attributes are defining properties, and which strategy (preserve as-is, emulate, migrate, reinterpret) maintains the work's identity [D-8] | Digital art conservation and restoration research [D-8] | A reasoned determination — through artist/technician interviews and comparison with historical documentation — of the work's defining properties, and on that basis a claim that a given strategy preserved the work's identity; two different installations can both be authentic if both stay faithful to the defining properties [D-8] | That the restored version is materially identical to the original [D-8] | Mostly a single case; sources include artist, technician, and curator interviews, historical documents, and technical examination of the object itself [D-8] | "Are the defining properties your own interpretation?"; using "does it still run" as the sole success criterion while ignoring that the physical medium may itself be a defining property; failing to name the unavoidable losses [D-8] |
| How a work or system evolved to its current state, which decisions were made when and why (creative journals, version records, image documentation, code archaeology) [D-7] | Documenting work and process [D-7] | A descriptive reconstruction of the sequence of decisions and the evolutionary path; evidence base for other knowledge claims [D-7] | That the documentation itself constitutes the research contribution [D-7] | A single work or single creator's complete process; state why these particular fragments were chosen as representative evidence [D-7] | Selectively presenting successes while hiding failed attempts; handing over raw journals or version logs with no analytical interpretation [D-7] |
| This work is itself worth understanding in depth (Stake's intrinsic case) [B-5] | Case study [B-5] | Deep explanation of process and mechanism within the case [B-5] | Statistical generalization to a population [B-5] | State the case-selection logic and case boundary [B-5] | Being unable to say clearly why this case was chosen [B-5] |
| Treating a technical artifact (a line of code, a technical spec) as an object of archaeology, tracing its technical and cultural history [D-9, D-7] | Media archaeology (a branch of critical/interpretive approaches) [D-9] | An interpretive argument entangling a technical object with its cultural context [D-9] | Empirical claims of the form "what most people think" [D-9] | The representativeness or typicality of the object chosen for analysis [D-9] | Switching frames tells a different story; jargon piled on for effect [D-9] |

### Appendix table: measurement instruments (not a question shape — a prerequisite for 1.1, 1.2, and 1.3)

| Typical situation | Candidate method(s) | Claims it can support | Claims it cannot support | Sample-size justification | Most common reviewer objections |
|---|---|---|---|---|---|
| A construct must first be measured reliably and validly: a scale as a dependent variable, or a scale itself as the paper's contribution [A-4] | Scale development and validation (CTT, CFA, IRT) [A-4] | Internal consistency and partial construct validity of scale scores as indicators of a construct; when the scale itself is the contribution, IRT is necessary; treating it as optional is a mistake [A-4] | That a high alpha equals a valid scale; that a high alpha implies a single dimension [A-4] | EFA rules of thumb are themselves contested (the card cites 5–10 people per item, or a total of 200–300; no source given); CFA and IRT need larger samples still; the validation sample must be able to test both convergent and discriminant validity [A-4] | Running EFA and CFA on the same dataset; treating alpha as validity evidence; forcing a sum score onto a multidimensional construct; comparing means across a translated scale without first testing measurement invariance; a self-made Likert scale with no validation at all [A-4] |

---


## Condition-triggered warnings


How to read this: each sub-heading is a condition X; each bullet says "watch for Y, see this card." A single topic usually triggers several conditions at once — check them all.

### 2.1 If the researcher is also the instructor or grader
- Students invited before grades are finalized find it hard to freely decline or answer honestly → invite formally only after grades are settled, make clear that declining does not affect grades already given, or have a third party collect consent or raw data → see B cross-method (reflexivity and the teacher-researcher), B-11, C-3
- Students will systematically give answers more positive, or more aligned with what the teacher expects, than their actual views — this is produced by the situation's structure; it is not a matter of honesty → the reflexivity statement must spell out specifically what was done to recognize and reduce this (anonymized codes, a third party collecting and de-identifying data, telling students the teacher cannot see responses linked to an individual) → see B cross-method (reflexivity and the teacher-researcher)
- This power-relation disclosure applies whenever data comes from one's own class. It covers thematic analysis, focus groups, diaries, artefact analysis, and open-ended questionnaires, in addition to methods labeled "interview" → see B cross-method (reflexivity and the teacher-researcher), B-1, B-8, B-10, B-11, B-12
- A reflexivity statement that is just one boilerplate sentence ("as the instructor, the author may have influenced the data") will be read as a box-ticking exercise → see B-1
- A grader who also analyzes the work they graded will be suspected of packaging their grading rationale as analysis after the fact → state how the dual role was handled → see B-11, B cross-method (reflexivity and the teacher-researcher, point 3)
- Experiments and quasi-experiments recruiting one's own students should decouple grades from research participation and use anonymized codes → see A-1, A-2, A-3 (the consent form should state that non-participation does not affect grades)
- Cross-semester tracking sustains the teacher-student relationship longer, so the power relation needs even more attention → see A-5
- Grading authority and data-collection authority sitting with the same person is a core ethical issue for action research, and one that DBR and participatory-design reviewers also probe → see C-3, C-2, C-5
- When the researcher runs their own workshop and students are the participants, workshop outputs will be presumed to be led by the researcher's preset agenda → disclose the prompts and materials used → see C-5

### 2.2 If there is only one class or one cohort
- A single-group pre–post design cannot support "the intervention worked"; an example design diagnosis shows that, for this design, doubling the number of people actually makes coverage worse → whenever a control can be found (waitlist, staggered start, another cohort), use it; simply recruiting more into the treatment group does not fix the design → see A-2, A cross-method (power analysis and sample-size justification)
- When no control can be found, explicitly downgrade the claim to non-causal in the write-up, and use the design-diagnosis numbers to state exactly what the design can support → see A-2
- A "longitudinal study" with only two time points and no control is, in substance, a single-group pre–post design → see A-5
- When multiple parallel classes or cohorts are available, do not fall back to a single-group pre–post design → see A-2 (when not to use)
- Framed as action research or DBR, the sampling logic is contextual relevance or theoretically relevant case selection — it cannot claim a cross-class, cross-context effect → see C-3, C-2
- Framed as a case study, state the case-selection logic clearly, and whether it is Stake-style (understanding this case) or Yin-style (theoretical generalization) → see B-5
- A narrow sample collected under theory-building logic should not be written in the register of theory-testing → see A cross-method (small-sample and convenience-sample claim limits), A-3

### 2.3 If the sample is small
- A small sample is not itself a flaw; the problem is a mismatch between the claim's scope and the sample's logic → see A cross-method (small-sample and convenience-sample claim limits)
- Lakens (2022) lists "resource constraints" and "explicitly acknowledging the absence of a justification" as legitimate, if weaker, sample-size justifications; what reviewers want is an honest account of the rationale → see A cross-method (power analysis and sample-size justification)
- Do not force a multi-factor design onto a sample that cannot support an interaction test → see A-1
- Do not force a full psychometric validation (CFA or IRT) onto a sample too small to give stable estimates → see A-4
- Do not use computational text analysis on too little text; use qualitative analysis instead → see A-6
- Do not attempt sequence or network analysis when there are too few events → see A-7
- Qualitative research should not reason about sample size in statistical terms; choose the justification that matches the method: information power for reflexive TA, theoretical saturation for grounded theory, case-selection logic for case studies, case depth for IPA → see B cross-method (sample-size justification), B-1, B-2, B-3, B-5, C-1
- Running a t-test or ANOVA on single-digit to low-teens data is a commonly flagged misuse → see C-3 (in tension with A-2 and A cross-method's position — see 3.1)
- Too few Delphi experts, or too few rounds, cannot be called robust; if there is not enough time for multiple rounds, rename it a single-round expert review or a focus group → see C-6
- A rating experiment with only the author or one or two non-independent raters should be relabeled a creator's statement / self-assessment → see A-9

### 2.4 If the data was already collected before the analysis was decided
- Deciding the analysis after seeing the data manufactures false findings even without any bad intent (the garden of forking paths); deciding to collect more data after seeing it is the same problem → see A cross-method (preregistration; the problem of retrospective analysis)
- A post-hoc power analysis is meaningless → see A-1, A cross-method (preregistration)
- The minimum defense is a time-stamped analysis plan written before analysis begins, including exclusion rules, primary outcome variables, and the choice of test → see A cross-method (the problem of retrospective analysis)
- Retrospectively cherry-picking the best-performing subset of works before sending them out for rating is a selection bias → see A-9
- If the system was not built to log behavior from the start, reconstructing a behavioral sequence from memory afterward has doubtful validity; it should be positioned as self-report data → see A-7
- Calling two datasets that had no planned upstream/downstream relationship a "sequential mixed-methods" study after the fact will read as two studies stapled together → see C-1
- If data was collected in writing without follow-up probing, it cannot be relabeled "interview" data at the write-up stage; downgrade the claimed depth of analysis → see B-12
- After the fact, when picking material from journals or version records, state the selection rationale to avoid a hindsight-biased narrative → see D-7
- Whether member checking or a reflexivity statement is still possible once data collection is complete should be written up honestly → see B cross-method (reflexivity and the teacher-researcher)

### 2.5 If the research object is the researcher's own work
- RtD needs to actively address relevance (current state vs. a better state), or it will read as a personal exploration log → see D-1
- First-person research needs to actively explain why N = 1 fits this question; trying something once does not count as autoethnography → see D-4
- "Where is the research here, beyond the creative work itself?": name the inquiry question and the knowledge contribution; "art is special" does not exempt the work from methodological scrutiny → see D-3, D cross-method (the scope of knowledge claims)
- State clearly whether this is practice-based (the work is the contribution) or practice-led (new understanding of the practice) → see D-2
- Documentation material tends to selectively show success and hide failure → see D-7
- Rating one's own work does not count as a rating experiment → see A-9
- When interpreting your own work, the reflexive position must actually enter the argument, and address "would a different frame yield the opposite reading" → see D-9, D-4
- Actively name the limitations, losses, and possible alternative readings → see D cross-method (how artistic research should respond to a quantitatively minded reviewer), D-8
- When journals mention family, colleagues, or students as third parties, privacy and consent still need to be addressed → see D-4, D-7

### 2.6 If human subjects are involved but ethics approval has not yet been obtained
- The cards list situations that need ethics review: experiments involving manipulation or deception (A-1), questionnaires (A-3), general qualitative research (B-1), interviews involving deep self-disclosure (B-3), long-term fieldwork that may need continuing review (B-4), group confidentiality in focus groups (B-8), the burden of diary studies on daily life (B-10), student work used in research and public display (B-11), minors or vulnerable groups in workshops (C-5), privacy and withdrawal mechanisms in long-term deployment (C-7), recording at exhibitions (D-5, D-6), interviews with living artists and technicians (D-8) → see "Resources and ethics" in each card
- The cards disagree, with no source given for either claim, about whether educational interventions need review (A-2 says expedited review or partial exemption is often available; C-3 says most teaching-practice grants do not require external IRB review) → do not use the cards to decide this is exempt; see 3.1, 3.3
- Consent should not be sought before grades are finalized → see B-11, B cross-method (reflexivity and the teacher-researcher)
- Ethics belongs at the front of sampling and method choice; bolting it on afterward is too late → see C cross-method (framework 3), C-4 (Cash et al.'s first consideration)
- The two strands of a mixed-methods study may have different review requirements (e.g., a survey vs. interviews); estimate the timeline for each separately → see C-1
- Long interventions and cross-semester tracking take longer; build approval time into the data-collection schedule → see C-2, A-5

### 2.7 If the data is cross-language
- Document the quote-translation procedure: who translated it, whether it was one-way or back-translated and checked, whether the original text appears in the manuscript, and whether the translation leans literal or free → see B cross-method (translating cross-language quotations)
- The Chinese back-translation used for author sign-off and the translation procedure for a participant's quotations are two different things and cannot substitute for each other → see B cross-method (translating cross-language quotations)
- No dedicated reporting standard for cross-language quotations could be found in the design/HCI literature; at minimum, address it in a paragraph in the methods section → see B cross-method (translating cross-language quotations)
- A translated scale needs translation and back-translation, and measurement invariance must be tested before comparing means across languages → see A-4
- Applying affective vocabulary across cultures without adaptation causes errors — the semantic differential method itself rests on a particular language's semantic structure → see A-8
- State the language inclusion/exclusion rules clearly for text analysis and literature reviews → see A-6, C-8

### 2.8 If an LLM is used to help code or rate
- Unvalidated automated output cannot be treated as ground truth; a supervised method must demonstrate it can replicate human coding (Grimmer & Stewart, 2013) → see A-6
- A checklist of reviewer expectations (human review, inter-rater reliability, an auditable trail, an explicit codebook-rewriting step, an accept/reject-with-reason ledger, line-level evidence binding, reproducible prompt settings) reflects emerging practice; there is no single citable source for it → see A-6, B cross-method (LLM-assisted qualitative coding)
- Using an LLM to generate initial codes for the researcher to confirm is, in practice, closer to a codebook or coding-reliability approach; it cannot simultaneously claim reflexive TA's exemption from reliability checks → see B cross-method (LLM-assisted qualitative coding), B-1
- The methods section must state the model, version, and prompt-design logic — this is checked separately from the AI-use disclosure required at submission → see B cross-method (LLM-assisted qualitative coding)
- Review norms are still shifting; re-check the target venue's policy from the last year before every submission → see B cross-method (LLM-assisted qualitative coding)
- The claim that "LLMs outperform expert coders" is only confirmed at the headline level in the cards, and cannot be used to skip validation → see A-6
- Using an LLM as a rater of works or text is not directly addressed in the cards; only two adjacent rules apply — automated output must be validated, and multiple independent raters' agreement must be reported → see A-6, A-9, and see 3.4

### 2.9 If this is a proposal (data not yet collected)
- This is the only point where the design can still be changed: run a design-stage diagnosis, judge by coverage, and fix the design (add a control) before talking about sample size → see A-2, A-1, A cross-method (power analysis and sample-size justification)
- Power analysis and the smallest effect size of interest should be declared at the design stage; the best time to preregister is right after the design diagnosis is run → see A cross-method (preregistration)
- Qualitative research should decide sample size at the design stage using information power; rationalizing "we reached saturation" after the fact does not substitute for this → see B cross-method (sample-size justification)
- Behavioral logging needs to be built into the system at the design stage → see A-7
- Diary studies need incentives and reminders planned in advance; longitudinal studies need attrition estimated in advance → see B-10, A-5
- A claim of "improved teaching quality" needs evidence from actual classroom implementation; a proposal can only describe how that evidence will be obtained → see C-3
- DRM's four stages typically span multiple years; state in the proposal which stages are covered → see C-4
- Sequential mixed-methods designs cannot run in parallel, so the timeline is longer → see C-1
- Power-relation safeguards need to be written in at the method-selection stage; adding them later is too late → see C cross-method (framework 3)
- Some reporting-guideline fields cannot be filled in retroactively (e.g., the pre-existing relationship between researcher and participants); check against them at the proposal stage

### 2.10 If the field is arts-based and the reviewer may have a quantitative background
- A three-layer response strategy: lead with relevance as the evaluative criterion, since validity is the wrong frame for this kind of work, and offer alternative criteria; cite Borgdorff's position that research on art and research in art are equal, without claiming methodological privilege; actively name the limitations → see D cross-method (how artistic research should respond to a quantitatively minded reviewer)
- Saying only "your standard doesn't apply," without offering an alternative standard (process, invention, relevance, extensibility, or contestable, defensible, substantive), is easily dismissed → see D cross-method, D-1
- Invoking "this is art, so it doesn't need validation" without first laying out a methodological position is easily dismissed → see D-3
- Practice-based work presumes the reviewer will engage with the work itself; a text-only review process may stall — consider an annotated-portfolio format → see D-2
- Some long-paper tracks in arts venues expect a layer of validating evidence → add an evaluation design → see D-1, D cross-method, A-9; call-for-papers requirements change year to year, so re-check them close to the deadline
- N = 1 needs an active justification of why it fits → see D-4
- "How can you generalize from just one case?" → respond with the distinction between theoretical and statistical generalization → see B-5
- With a positivist-minded reviewer, Lincoln & Guba's four trustworthiness criteria are usually easier to communicate with → see B cross-method (trustworthiness criteria)
- A reviewer treating RtD's "where is your sample size" as a real question is itself a case of a mismatched evaluation frame, but the paper still needs to explain its own sampling logic → see D-1, D cross-method

### 2.11 If data collection is spread across multiple sessions, or submitted by participants after class on their own
- Self-submitted data means the researcher was not present and could not probe further, so it cannot be called an interview → see B-12
- Report the non-completion rate; open-ended items usually have higher attrition than closed items → see B-12
- Distributing before grades are settled and collecting after class raises questions about how free participation really was → see B-12, B cross-method (reflexivity and the teacher-researcher)
- Diary-type data needs a compliance rate reported; backfilling several days at once has already degraded into retrospective data → see B-10
- Attrition across multiple time points needs to be judged as random or non-random missingness, with the handling explained and a sensitivity analysis run → see A-5
- Compare attrition rates between the treatment and control groups → see A-2
- Multi-round Delphi studies need each round's response rate and the characteristics of dropouts reported → see C-6
- Deployment studies need to report how attrition and technical failures affected data completeness → see C-7
- Consistency and difference across multiple workshops or focus groups should be reported as they actually occurred, with each session's composition stated → see C-5, B-8
- If log data was added in stages, coverage periods may differ across participants → see A-7
- Multi-stage data needs to state how the earlier stage fed the later stage's sampling or instrument → see C-1
- Also check, for every activity: confirm the data was actually received and is usable — attendance records are not the same as data

---


### 2.12 If the researcher is the only judge
- Rating one's own work, analyzing one's own students' work or reflections, being both the author and the grader, being the sole coder — "narrowing the claim" only solves half the problem; plan for at least one independent check besides the author: a second coder (independently coding a subset of the data), a blind rater (unaware of condition or authorship), external expert review, or a third party collecting and de-identifying the data → see A-9, B-1, B-11, D-4, D-6, B cross-method (reflexivity and the teacher-researcher)
- Not having collaborators is not a reason to skip this: a colleague, graduate student, or peer in the field can do a small-scale independent read, reported honestly with its scale and limits stated → see A-9, D-6
- Basis: in the author's internal blind test of method decisions, this was the most frequently missed issue, and it was the single most common reviewer criticism in cases where the paper relied on the author's own judgment alone.

## Group A: Quantitative methods

> Verification approach: check your own local literature library (if you have one) first, and only search the web if a source is not found there. Every literature-based claim gives author, year, DOI or a stable link, a verbatim quotation (≤40 words) with page number, and one of the evidence tags above. Technical statistical details (how to choose GLMM vs. ART vs. clmm, how to correct for multiple comparisons) are covered in your own analysis playbook and are not repeated here — this card only cites their conclusions where relevant to a decision.

---

### A-1 Controlled experiment (within-subjects / between-subjects / factorial design; system-comparison experiments, Wizard of Oz)

**Question shapes it answers**: "How large is the difference in outcome Y caused by treatment A versus treatment B (or versus no treatment)" — a causal-comparison question. It can also answer "under which conditions does the effect hold or disappear" (interactions in a factorial design). The Wizard-of-Oz variant answers "if this system — which does not yet exist or is not yet mature — worked as users expect, how would they respond."

**Epistemic stance and claim scope**:
- **Can support**: A causal claim about the treatment producing the outcome difference (provided random assignment, manipulation checks, and double- or at least single-blinding are genuinely carried out). Blair et al. (2019) formalize the core components of this kind of design as the MIDA framework — Model (how the world works, including the confounders you worry about), Inquiry (the estimand), Data strategy (how you collect and assign), Answer strategy (how you estimate): "declaration of these features in code provides sufficient information for researchers and readers to use Monte Carlo techniques to diagnose properties such as power, bias, accuracy of qualitative causal inferences, and other 'diagnosands'" (Blair, Cooper, Coppock & Humphreys 2019, *American Political Science Review* 113(3):838, DOI 10.1017/S0003055419000194) [full text]. With this kind of declaration, the legitimacy of a causal inference can be formally checked; it does not need to rest on the slogan "we randomized."
- **Cannot support**: External validity (whether a lab or controlled-setting effect transfers to real use) needs a separate argument and does not follow automatically from internal validity; participants who know they are being observed and are performing a researcher-designed task are subject to demand characteristics and novelty effects, especially for constructs sensitive to social desirability such as "creative support" or "willingness to use."

**Data and sample**: Sample-size justification means an a priori power analysis, but the Blair et al. framework is stricter than a conventional power analysis: high power does not mean a good design — the diagnosis should also check bias (whether the estimate is biased) and coverage (whether the confidence interval covers the true value at close to its nominal rate, ideally about 0.95), because "a biased design only gets worse coverage as you add participants" (this is a quantitative result from running a Monte Carlo design diagnosis, using the DeclareDesign R package, on an example single-group pre–post study with N = 40 — it is a demonstration of the method. It is not a finding from the Blair et al. paper itself; the two are kept honestly distinct here). Typical sample size depends on the expected effect size and design efficiency (within-subjects designs are usually more sample-efficient than between-subjects designs but must address carryover effects).

**Analysis procedure notes**: The technical details (continuous DV plus repeated measures → afex/lmer → emmeans; ordinal/Likert → clmm; ARTool is not used here — a modeling study by Tsandilas (*Journal of Visualization and Interaction*, 2024) is reported to show that using ART on discrete/ordinal/binomial DVs systematically inflates the Type I error rate. **This citation is secondhand**: this port could not locate the full text of Tsandilas (2024) in either a local library or via Crossref [abstract only — relayed secondhand from an internal analysis playbook; the original was not checked in this pass]) are outside the scope of this card. At the design stage, run a Monte Carlo diagnosis (e.g., DeclareDesign's `diagnose_design()`) at the design stage, before data collection begins.

**Quality criteria**: Whether the manipulation check was effective; whether random assignment was genuinely random (not systematically alternated); within-subjects designs must report counterbalancing of order; Wizard-of-Oz studies must report the consistency of the operator's script and whether participants were later asked "did you think this was a real person or a system."

**Reporting standard**: With random assignment → **CONSORT** (the CONSORT-SPI extension for social/psychological interventions where applicable).

**Common reviewer critiques and misuses**: (1) treating a single Likert item as continuous and running a t-test/ANOVA; (2) using ARTool on a discrete DV (the Tsandilas warning above, secondhand and unverified); (3) reporting p-values without effect sizes and confidence intervals; (4) a power analysis added after the fact (post-hoc power is meaningless); (5) treating within-subjects dependent observations as independent (violating the statistical assumption).

**Acceptance and conventions in this kind of venue**: This is the home turf for this kind of design in HCI/IUI-style venues, which typically expect a controlled experiment with standard scales and system metrics, with the contribution typically centered on the system itself, since a human-factors finding alone is often not treated as sufficient; some venues are comparatively lenient and will accept a complete experiment report on its own.

**Resources and ethics**: Needs IRB/ethics review, especially for designs that manipulate cognitive or emotional state, or use deception. If the researcher is also an instructor, recruiting their own students into a controlled experiment raises the same power-relation problem as the quasi-experiment card below and needs the same procedural safeguards (anonymization, decoupling from grades).

**Common combinations**: Data profiling and diagnostic plots → statistical test → emmeans post-hoc comparisons; mixed-methods designs often pair task-behavior logs with a short interview to explain "why."

**When not to use**: (1) the question centers on "is this tool usable, how do users understand it" — for this kind of question a qualitative method fits better than a head-to-head "how much better is A than B" comparison; (2) the sample ceiling clearly cannot support the interaction test of a multi-factor design, yet a multi-factor design is used anyway; (3) the phenomenon itself cannot be induced in a controlled setting (e.g., long-term motivational change in a real classroom) — use a quasi-experimental or longitudinal design instead.

**Key sources**:
- Blair, G., Cooper, J., Coppock, A., & Humphreys, M. (2019). Declaring and Diagnosing Research Designs. *American Political Science Review*, 113(3), 838–859. DOI: 10.1017/S0003055419000194. [full text]
- Tsandilas, T. (2024). The Illusory Promise of the Aligned Rank Transform. *Journal of Visualization and Interaction*. https://www.journalovi.org/2024-tsandilas-ranktransforms/ (page and title confirmed to exist; the original card mistakenly named this *Journal of Vision*). [page confirmed only, full text not read]

---

### A-2 Quasi-experiment (single-group pre–post, non-equivalent control group, waitlist control, staggered start)

**Question shapes it answers**: "Did the outcome change from before to after the intervention, and by how much" — most common in educational settings such as "did this course or teaching method work," where a whole class cannot be randomly assigned.

**Epistemic stance and claim scope**:
- **Cannot support**: A single-group pre–post design **cannot structurally separate "the intervention's effect" from testing effects, maturation effects, and history effects** — this is a quantitative result from running a Monte Carlo design diagnosis (using the DeclareDesign package) on an example single-group pre–post study with N = 40: under a "testing effect of 0.20" scenario, bias = 0.196, power = 1.000, but **coverage = 0.218**; under a "true effect is zero, entirely due to the testing effect" scenario, power is still 1.000 but coverage = 0.000. **High power does not mean the estimate is correct — this design guarantees a significant result regardless of whether the intervention worked.** This is the port's own reproducible analysis result; it is not a finding reported by an external publication (the analysis method and framework come from Blair et al.'s 2019 DeclareDesign work, but this specific set of numbers is the port's own diagnostic output; the two are kept honestly distinct here).
- **Can support (the version with a control group)**: A waitlist control or a staggered/stepped-wedge start, done properly, can support a weak causal claim. In the same diagnosis, converting the single-group pre–post design into a waitlist-control (difference-in-differences) design brought bias to about 0 and coverage to about 0.95, and reached 98% power at N = 80 (40/40) — better than simply doubling the single-group N to 120 (whose coverage went from 0.228 to 0.000, i.e. worse with more people). In that one declared model, adding a control beat adding participants; this is not a general rule — a new topic needs its own MIDA declaration and its own diagnosis to know whether adding a control or adding participants pays off better.
- Shadish, Cook & Campbell's classic textbook (*Experimental and Quasi-Experimental Designs for Generalized Causal Inference*, Boston: Houghton Mifflin, 2002) is the standard source for the taxonomy of internal-validity threats used here (history, maturation, testing, instrumentation, regression to the mean, selection, attrition, diffusion of treatment). This port could not find the full text in a local library; Crossref returned only book-review records (DOI 10.1086/345281, 10.1002/pam.10129); the book itself was not found there. [abstract only — cited per the textbook-citation convention, original not read]

**Data and sample**: Sample-size justification should not rest on a conventional power analysis alone — **run a design-stage diagnosis (e.g., DeclareDesign) first and judge by coverage; power alone is not the criterion**. Adding a control group contributes more to estimate quality than adding participants (see above). If a single-group design truly cannot add a control, the causal claim must be explicitly downgraded in the write-up, with the diagnosis numbers used to state exactly what the design can support.

**Analysis procedure notes**: Pre–post differences use `lmer` or a paired test; staggered/stepped-wedge designs follow the design logic and analytic cautions set out in Hemming et al. (2015), *The stepped wedge cluster randomised trial* (BMJ) [full text] — a stepped-wedge design with randomization is an intermediate form that has effectively upgraded from quasi-experimental toward near-randomized. Single-case experimental designs (common in education and rehabilitation research) follow the Tate et al. (2016) SCRIBE guideline.

**Quality criteria**: Whether internal-validity threats are addressed one by one (especially the testing effect — repeated administration of the same scale can itself raise scores); whether a non-equivalent control group exists as a comparison baseline; whether attrition is comparable between treatment and control groups.

**Reporting standard**: **TREND** (Transparent Reporting of Evaluations with Nonrandomized Designs) is the mainstay reporting standard for this design; single-case designs follow **SCRIBE** (Tate et al. 2016): "Many such guidelines exist and the CONSORT Extension to Nonpharmacologic[al Trials]..." (Tate, Perdices, Rosenkoetter et al. 2016, p.1) [full text] — SCRIBE is itself a 26-item reporting checklist modeled on the spirit of CONSORT for single-case designs.

**Common reviewer critiques and misuses**: (1) writing a significant pre–post difference straight as "the intervention worked" without mentioning the two competing explanations of testing and maturation effects; (2) having a control group that is a "convenience control" (e.g., the class next door) without establishing baseline comparability; (3) no design-stage power or diagnosis, so the sample size has no stated rationale; (4) conflating the strength of causal language appropriate to a quasi-experiment with that of a correlational study.

**Acceptance and conventions in this kind of venue**: Single-group pre–post designs are broadly accepted in education journals and teaching-practice grants, though review has grown stricter in recent years and reviewers increasingly expect either a discussion of threats to validity or a staggered design. HCI venues (DIS/CHI) accept this design less readily and tend to expect at least a non-equivalent control group.

**Resources and ethics**: Quasi-experiments on educational interventions frequently involve an "instructor as researcher" — the instructor's grading authority and consent-seeking authority over their own students create a clear power imbalance, and grades must be decoupled from research participation with anonymized codes, the same caution that applies throughout the qualitative cards below. Ethics review for educational interventions can often be expedited or partly exempted, but anything touching grades or personal data still needs an application.

**Common combinations**: A design-stage diagnosis first → pre-post or multi-wave growth models with `lmer` → process logs (e.g., sequence analysis) to add "how it changed"; when a scale is the outcome variable, validate it (see A-4) first.

**When not to use**: (1) when random assignment is available (multiple parallel classes, multiple cohorts), a controlled experiment or at least a staggered-start design should be preferred over falling back to a single-group pre–post design; (2) the research question is itself the intervention's mechanism, beyond simply whether it worked — a qualitative or mixed-methods approach fits better.

**Key sources**:
- Blair, G., Cooper, J., Coppock, A., & Humphreys, M. (2019). Declaring and Diagnosing Research Designs. *APSR* 113(3):838–859. DOI 10.1017/S0003055419000194. [full text] (the methodological framework; the specific numbers above are this port's own analysis output; they are not content from this paper)
- Shadish, W. R., Cook, T. D., & Campbell, D. T. (2002). *Experimental and Quasi-Experimental Designs for Generalized Causal Inference*. Boston: Houghton Mifflin. [abstract only]
- Tate, R. L., Perdices, M., Rosenkoetter, U., et al. (2016). The Single-Case Reporting guideline In BEhavioural interventions (SCRIBE) 2016 statement. [full text]
- Hemming, K., Haines, T. P., Chilton, P. J., Girling, A. J., & Lilford, R. J. (2015). The stepped wedge cluster randomised trial: rationale, design, analysis, and reporting. *BMJ*, 351:h391. [full text]

---

### A-3 Cross-sectional survey

**Question shapes it answers**: "In this population, what is the relationship, prevalence, or distribution of X and Y" — a descriptive/correlational question at a single point in time.

**Epistemic stance and claim scope**:
- **Can support**: Description of population characteristics, correlational strength between variables, comparisons between groups.
- **Cannot support**: Causal direction — a cross-sectional design cannot rule out reverse causation or a third variable, and cannot support a claim of the form "this intervention caused this outcome" (that is the territory of cards A-1 and A-2).
- **A common fatal flaw is common method bias**: when all variables come from the same source, the same time point, and the same self-report instrument, correlations can be inflated by shared method variance. The canonical source is Podsakoff, MacKenzie, Lee & Podsakoff (2003), *Common Method Biases in Behavioral Research: A Critical Review of the Literature and Recommended Remedies*, *Journal of Applied Psychology* 88(5):879, DOI 10.1037/0021-9010.88.5.879 — not in a local library, confirmed to exist and to be the most-cited methodological source in this area via Crossref, but **not read in full**, so [abstract only]. Common procedural remedies (anonymizing the questionnaire, randomizing item order, staggering collection across time points) are illustrated in an applied example: "several procedural remedies were implemented during data collection to minimize potential common method bias. These included ensuring respondent anonymity, using…" [full text — cited as an applied illustration; it is not the methodological source itself].

**Data and sample**: State the sampling method (probability vs. convenience) clearly. Sample-size justification runs through conventional power analysis; structural equation modeling has its own rules of thumb (e.g., 10 observations per parameter) that are themselves contested — see Lakens (2022) on the "using heuristics" path. Cash et al. (2022) propose eight key sampling considerations for design research; their distinction between theory-building and theory-testing directly determines the sampling logic: "Typically, more focused on understanding a phenomenon in a specific group and context, via rich, deep data" (theory-building) vs. "Typically, more focused on understanding scope of a theory across groups and contexts via selected, wide data" (theory-testing) (Cash, Isaksson, Maier & Summers 2022, Table 1, p.7–8, DOI 10.1016/j.destud.2021.101077) [full text] — a survey doing theory-testing (checking whether an established model holds in a new sample) needs a broad sample; one doing exploratory description can be narrow and deep.

**Analysis procedure notes**: The technical details of regression, SEM, and correction for multiple comparisons are outside the scope of this card. How to treat Likert items (a single ordinal item vs. a multi-item summed scale) should follow your own decision rules.

**Quality criteria**: Response rate and non-response bias; a check for common method bias (e.g., Harman's single-factor test, of limited power but still commonly asked for by reviewers); scale reliability and validity (if using an existing scale, see A-4).

**Reporting standard**: **STROBE** (Strengthening the Reporting of Observational Studies in Epidemiology) — the standard for observational/cross-sectional, survey-type studies.

**Common reviewer critiques and misuses**: (1) writing a cross-sectional correlation as causal language ("A raised B" should be "A correlates with B"); (2) generalizing from a convenience sample (e.g., one's own class) to a population; (3) ignoring common method bias; (4) running a mediation analysis on cross-sectional data and claiming it validates a causal mechanism.

**Acceptance and conventions in this kind of venue**: Design and HCI education journals broadly accept cross-sectional surveys as pilot or descriptive evidence, but top-tier venues (CHI/DIS) increasingly expect a survey to be paired with another method; a survey standing alone as the main contribution is increasingly less accepted.

**Resources and ethics**: Needs IRB or at least an ethics-exemption statement; if participants are one's own students, the consent form must state clearly that non-participation does not affect grades.

**Common combinations**: Survey + interviews (mixed-methods explanation of quantitative findings); survey as the data-collection stage of scale validation (see A-4).

**When not to use**: (1) the question is fundamentally causal ("did this intervention work") — use A-1 or A-2 instead; (2) only a small, non-random convenience sample is reachable but a population-level claim is wanted — use a case study or a qualitative method instead, and honestly narrow the claim.

**Key sources**:
- Podsakoff, P. M., MacKenzie, S. B., Lee, J.-Y., & Podsakoff, N. P. (2003). Common Method Biases in Behavioral Research. *Journal of Applied Psychology*, 88(5), 879. DOI 10.1037/0021-9010.88.5.879. [abstract only, confirmed via Crossref]
- Cash, P., Isaksson, O., Maier, A., & Summers, J. (2022). Sampling in design research: Eight key considerations. *Design Studies*, 78, 101077. DOI 10.1016/j.destud.2021.101077. [full text]

---

### A-4 Scale development and validation (CTT reliability/validity, CFA, IRT; when the scale itself is a contribution)

**Question shapes it answers**: "Can this construct (e.g., 'AI literacy,' 'aesthetic preference') be measured reliably and validly" — a measurement-infrastructure question. On its own, it does not usually count as a substantive research question.

**Epistemic stance and claim scope**:
- **Can support**: A claim that scale scores have internal consistency and (partial) construct validity as an operationalization of the construct.
- **Cannot support**: A high Cronbach's alpha alone cannot support "the scale is valid" — this is the most commonly misunderstood point in the scale-development literature. Messick's (1995) unified view of validity argues that validity is not divisible into three separate, substitutable types (content, criterion, construct): "The traditional conception of validity divides it into three separate and substitutable types—namely, content, criterion, and construct validities. This view is fragmented and incomplete" (Messick 1995, p.1) [full text]. He proposes six facets — content, substantive, structural, generalizability, external, and consequential (same page) [full text] — and the **consequential facet** is the one quantitative researchers most often overlook: what decisions scale scores are used for, and what social consequences follow, is also part of the validity evidence.
- Clark & Watson (2019) restate that the core principles of scale development have not changed: "the primary goal of scale development is to create valid measures of underlying constructs," and list six essentials — (a) clearly define the target construct, (b) start with an overinclusive item pool, (c) word items carefully, (d) test discriminant power against closely related constructs, (e) choose validation samples thoughtfully, (f) **value unidimensionality over internal consistency** (Clark & Watson 2019, Abstract) [full text]. Point (f) is a common trap: a high Cronbach's alpha does not guarantee unidimensionality — a multidimensional scale summed into one score can still have a high alpha.

**Data and sample**: The sample-size rules of thumb for the EFA stage (5–10 people per item, or a total of ≥200–300) are themselves contested; CFA and IRT need larger samples still (IRT is especially sensitive to sample size and needs multi-category response data for models such as the PCM). Sample choice involves more than size — Clark & Watson (2019) stress "choosing validation samples thoughtfully": the validation sample must be able to test both convergent and discriminant validity; convenience alone does not qualify it.

**Analysis procedure notes**: For an existing scale: reliability analysis → CFA (with a measurement-invariance test if comparing across groups). For a new scale: item pool → EFA/reliability → CFA → IRT (polytomous Likert data uses TAM/PCM, dichotomous data uses eRm/CML, multidimensional data uses mirt) — technical detail is outside the scope of this card. **The decision rule for when the scale itself counts as a contribution**: when the scale is only a dependent variable, reliability plus CFA is enough; when the scale itself is the paper's contribution, IRT is necessary; treating it as optional overlooks that only IRT can report how much information and discrimination items carry at different levels of the trait, a question CTT's alpha and CFA loadings cannot answer.

**Quality criteria**: Internal consistency (alpha/omega); construct validity (convergent and discriminant); measurement invariance (configural/metric/scalar) when comparing across groups (language, gender); the item information function and reliability curve for IRT.

**Reporting standard**: No single dedicated guideline, but journal-specific psychometric reporting norms commonly require the factor-loading table, model fit indices (CFI/RMSEA/SRMR), and reliability coefficients with confidence intervals.

**Common reviewer critiques and misuses**: (1) running EFA and then treating the same dataset as if it were a CFA (circular reasoning); (2) treating alpha as validity evidence, when it only reflects internal consistency; (3) forcing a sum score onto a multidimensional construct; (4) comparing means on a translated scale across cultures without testing measurement invariance; (5) using a self-made Likert scale with no validation procedure at all and claiming it measures the construct — a standard, validated scale is close to the default expectation in this kind of venue, and a custom Likert scale will usually be asked to be replaced or supplemented with validation evidence.

**Acceptance and conventions in this kind of venue**: Design education and HCI venues have high psychometric expectations — reliability/validity evidence, and IRT when the scale itself is the contribution; using standardized scales (SUS, TLX, CSI, etc.) is close to the default, especially in creativity-support-tool evaluation venues.

**Resources and ethics**: Scale development is a time-consuming, multi-stage undertaking (item generation → pilot → revision → formal validation, often needing several independent samples), and its cost is often underestimated. If the construct touches a sensitive topic (mental health, low self-efficacy), the questionnaire itself may cause discomfort and should be addressed in ethics review.

**Common combinations**: Scale development is often paired with qualitative methods (interviews/focus groups to generate items); cross-cultural scales need translation and back-translation.

**When not to use**: (1) a well-validated standard scale already covers the construct, yet a new scale is built anyway (wasteful, and hard to justify to reviewers); (2) the sample is clearly too small to support stable CFA or IRT estimation, yet a full psychometric validation is attempted anyway.

**Key sources**:
- Messick, S. (1995). Validity of Psychological Assessment. *American Psychologist*. [full text]
- Clark, L. A., & Watson, D. (1995). Constructing Validity: Basic Issues in Objective Scale Development. *Psychological Assessment*, 7(3), 309-319. [full text, matched search snippet]
- Clark, L. A., & Watson, D. (2019). Constructing Validity: New Developments in Creating Objective Measuring Instruments. [full text]

---

### A-5 Longitudinal / repeated-measures research (multi-wave, growth models)

**Question shapes it answers**: "How does this outcome change over time, does the rate of change vary between people, what predicts the trajectory of change" — this differs from A-2's quasi-experiment in that a longitudinal study need not involve an "intervention"; it can track naturally occurring change (e.g., multi-wave observation of a learning process).

**Epistemic stance and claim scope**:
- **Can support**: Within-person patterns of change, individual differences in trajectories, predictive relationships over time (if temporal order is clear).
- **Cannot support**: Temporal order alone is not causation (confounders still need to be controlled and selective attrition addressed); repeated administration of the same scale can itself produce a practice/testing effect (the same warning as A-2, amplified across more waves in a longitudinal design).

**Data and sample**: Attrition needs to be estimated at the design stage for its effect on power — this is the core sample-size issue for longitudinal research, and differs from the cross-sectional power-analysis logic: a multi-wave design must consider the combined effect of the intraclass correlation (ICC) and the number of waves on statistical power. It's recommended to estimate sample size with a package such as `simr` at the design stage, before running a growth model on the pre-post/multi-wave data. Multi-level (mixed-effects) models are the analytic tool of choice, but Gries (2015) notes they carry their own data requirements and risk of misuse, calling multilevel models "the most under-used statistical method" in corpus linguistics [full text — cited as methodological context; it is not a source specific to longitudinal design].

**Analysis procedure notes**: Pre-post/multi-wave data → growth-curve modeling with `lmer` plus ICC; process logs → sequence analysis (e.g., TraMineR, with seqHMM for clustering); collaborative interaction → social network analysis (e.g., igraph); technical detail is outside the scope of this card.

**Quality criteria**: Whether attrition is missing at random (MAR) or missing not at random (MNAR, more serious); whether the missing-data handling is documented (missingness over 5% commonly calls for multiple imputation, with the MAR assumption stated); whether measurement invariance holds across waves (whether the same scale is measuring the same construct at each time point).

**Reporting standard**: No single dedicated guideline; a randomized multi-wave intervention still follows CONSORT/TREND depending on whether it was randomized (see A-1, A-2).

**Common reviewer critiques and misuses**: (1) treating repeated-measures data as independent observations (violates the statistical assumption, underestimates standard error); (2) not reporting or not running a sensitivity analysis on longitudinal attrition; (3) comparing mean change across waves on a multi-wave scale without validating measurement invariance; (4) writing a correlational temporal pattern as causal language.

**Acceptance and conventions in this kind of venue**: Design-education research venues treat social network analysis / epistemic network analysis as near-standard for collaboration research (a convention common in the CSCL field); the learning-analytics community (LAK/ICQE) broadly accepts sequence and network analysis as method, though a paper submitted outside that community should explain the methodological choice.

**Resources and ethics**: Multi-wave tracking needs a longer research cycle and higher-cost attrition management; if the research subjects are one's own students tracked across semesters, the teacher-researcher power relation (same as A-2) needs even more attention because the relationship is sustained longer.

**Common combinations**: Heavily overlaps with behavioral logging/learning analytics (A-7) and is often used together with it; a scale used as an outcome variable should be validated first (A-4).

**When not to use**: (1) only two time points with no control group — this effectively degrades to A-2's single-group pre–post design, and should be honestly treated within that framework's causal limits; (2) attrition during the tracking period is too high (e.g., over 40–50%) with no sensitivity analysis of the missing data.

**Key sources**:
- Gries, S. Th. (2015). The Most Under-Used Statistical Method in Corpus Linguistics: Multi-level (and Mixed-Effects) Models. [full text, cited as methodological context]
- (A dedicated textbook on longitudinal-design methodology, such as Singer & Willett's *Applied Longitudinal Data Analysis*, was not found in a local library and was not otherwise checked — flagged honestly as not found)

---


### A-6 Quantitative content analysis and computational text analysis (coding schemes, inter-rater reliability, text as data)

**Question shapes it answers**: "In this body of text, how often, or in what proportion, does a given category or theme appear" / "can a latent textual dimension (stance, sentiment, style) be measured automatically or semi-automatically" — turning unstructured text into a structured, analyzable variable.

**Epistemic stance and claim scope**:
- **Can support**: Descriptive claims about category frequency (with adequate reliability evidence); claims of agreement between a validated automated measure and human coding.
- **Cannot support**: **Treating any unvalidated automated method's output as ground truth.** Grimmer & Stewart (2013) offer four principles for quantitative text analysis, the fourth being the paper's central admonition: "(1) All quantitative models of language are wrong—but some are useful. (2) Quantitative methods for text amplify resources and augment humans. (3) There is no globally best method for automated text analysis. (4) Validate, Validate, Validate." (Grimmer & Stewart 2013, Table 1, p.269, DOI 10.1093/pan/mps028) [full text]. The specific requirement behind principle 4: "it is incumbent upon the researcher to validate their use of automated text analysis…When categories are known in a calculation problem, scholars must demonstrate that the supervised methods are able to reliably replicate human coding" (same source, Principle 4 section) [full text] — in other words, supervised methods must demonstrate they can replicate human coding, and unsupervised methods must combine experimental, substantive, and statistical evidence to argue for conceptual validity. **Automated text-analysis output with no validation step cannot stand as a conclusion on its own.**

**Data and sample**: State the corpus's inclusion/exclusion rules clearly (time period, source, language); if machine learning assists classification, state the train/test split and ratio. LLM-assisted coding is a fast-growing area — Törnberg (2024) reports "Large language models outperform expert coders and supervised classifiers at annotating political social media messages" (the title itself is the finding) — but this does not mean validation can be skipped; if anything it raises the bar reviewers set for the validation procedure (see the LLM coding checklist below).

**Analysis procedure notes**: This card focuses on "text as data" quantitative approaches — word frequency, topic models, sentiment analysis, stance detection — implemented with tools such as quanteda or epistemic-network-analysis packages for coded co-occurrence structure; technical detail is outside the scope of this card.

**Quality criteria**: Choosing a reliability metric is itself a methodological decision; it is not an arbitrary pick. Hayes & Krippendorff (2007) systematically compare existing reliability coefficients (percent agreement, Bennett's S, Scott's π, Cohen's κ, Fleiss's K, Cronbach's α) and conclude that Krippendorff's alpha is best suited as a standard: "It is general in that it can be used regardless of the number of observers, levels of measurement, sample sizes, and presence or absence of missing data" (Hayes & Krippendorff 2007, Abstract, p.77, DOI 10.1080/19312450709336664) [full text]. The paper flags a commonly overlooked flaw in Cohen's kappa: "Kappa, by accepting the two observers' proclivity to use available categories idiosyncratically as baseline…has the effect of punishing observers for agreeing on the frequency distribution of categories" (same source, p.7) [full text] — **if two raters both happen to favor a given category, kappa can be pulled down**, which is a common source of confusion when choosing kappa over Krippendorff's alpha. Practical rule of thumb: 2 raters, categorical → Cohen's kappa; 3+ raters, categorical → Fleiss's kappa; continuous → ICC; Krippendorff's alpha works across all of these.

**Reporting standard**: The qualitative-coding portion follows COREQ/SRQR; a systematic-review-style content analysis follows PRISMA 2020.

**Common reviewer critiques and misuses**: (1) reporting a single inter-rater reliability number without documenting how the codebook evolved; (2) treating automated (including LLM) output as equivalent to human coding without validating it; (3) conflating "reliability" (two coders' results agree) with "validity" (the coding actually measures the intended construct); (4) vague sampling rules (e.g., "we randomly selected N posts" with no account of how the randomization was done).

**LLM-assisted coding — recent reviewer expectations (reflects emerging practice; there is no single citable source for it)**: (1) human review; (2) inter-rater reliability (kappa ≥ .61 as a starting bar); (3) an auditable coding trail; (4) an explicit, iterative "codebook rewrite" step; (5) an accept/reject ledger with reasons; (6) line-level evidence binding; (7) saved prompts/settings for reproducibility.

**Acceptance and conventions in this kind of venue**: Political science and communication research (Grimmer & Stewart's home field) hold automated text analysis to a very high validation standard; acceptance in HCI/design-education venues depends on the question — analyzing open-ended survey responses usually still requires an inter-rater reliability report.

**Resources and ethics**: Large-scale corpus analysis involving social media or personal publications should consider the research-ethics boundary for public data (even publicly posted content carries re-identification risk when quoted verbatim).

**Common combinations**: Content analysis is often paired with social network analysis (who is interacting with whom) and sequence analysis (how the discussion evolves) — see A-7.

**When not to use**: (1) the corpus is too small (e.g., fewer than roughly 30–50 documents) to support stable computational estimation — traditional qualitative thematic analysis (Braun & Clarke) is more honest; (2) the research question needs a deep interpretation of a single text's meaning — for that kind of question a qualitative method fits better than finding patterns across a large corpus.

**Key sources**:
- Grimmer, J., & Stewart, B. M. (2013). Text as Data: The Promise and Pitfalls of Automatic Content Analysis Methods for Political Texts. *Political Analysis*, 21, 267–297. DOI 10.1093/pan/mps028. [full text]
- Hayes, A. F., & Krippendorff, K. (2007). Answering the Call for a Standard Reliability Measure for Coding Data. *Communication Methods and Measures*, 1(1), 77-89. DOI 10.1080/19312450709336664. [full text]
- Törnberg, P. (2024). Large language models outperform expert coders and supervised classifiers at annotating political social media messages. [full text at title/abstract level; not cited in depth]

---

### A-7 Behavioral logs and learning analytics (logs, sequence analysis, social network analysis)

**Question shapes it answers**: "What did the user or learner actually do, step by step (not what they self-report doing)" / "what does the structure of an interaction or collaboration look like" — using behavioral traces, without relying on self-report, to address "what was done" — a different question from "how it felt."

**Epistemic stance and claim scope**:
- **Can support**: Descriptions of patterns in a behavioral sequence (who did what first, common paths); structural features of an interaction network (core nodes, subgroup structure).
- **Cannot support**: Log data alone does not reveal motivation or understanding — "did action X" does not mean "understood concept X," a common over-inference trap in educational data mining. Fan et al. (2024), discussing AI-assisted learning-process analysis, mention using "epistemic network analysis to gain a deeper understanding of the SRL [self-regulated learning] process" [full text] as a method example — but this kind of method reveals the co-occurrence structure between behavioral/cognitive categories, and still needs a coding-validity argument (does the codebook actually measure the intended cognitive process) before it can support a claim about "understanding the process."

**Data and sample**: The unit of log data is usually the "event," not the "person," so sample-size logic differs from surveys or experiments — the key is whether event density is high enough to support stable sequence- or network-analysis estimates (e.g., a too-sparse interaction network cannot yield meaningful centrality metrics).

**Analysis procedure notes**: Process logs → sequence analysis (e.g., TraMineR, with seqHMM for clustering); collaborative interaction → social network analysis (e.g., igraph, near-standard in the CSCL field); discourse/coded data → epistemic network analysis (a mainstream method in the learning-analytics community, though a paper submitted outside that community should explain the choice). This port could not find the foundational papers for epistemic network analysis or for TraMineR/social-network-analysis methodology in a local library; Crossref confirmed related literature exists (e.g., epistemic-network-analysis conference papers, DOI 10.1007/978-3-030-93859-8_9), but the originals were not read — [abstract only].

**Quality criteria**: If sequence analysis rests on human-coded event categories, the codebook's reliability still needs an inter-rater check (see A-6); network-analysis edge definitions must be explicit (what counts as an "interaction"); the similarity metric in sequence analysis (the substitution-cost setting in optimal matching) should be theoretically grounded; an arbitrary setting is not defensible.

**Reporting standard**: No single dedicated guideline; if human coding is used as a preprocessing step, it still follows COREQ/SRQR's transparency requirements for coding.

**Common reviewer critiques and misuses**: (1) treating "engagement" metrics from logs (clicks, dwell time) as directly equivalent to "learning engagement" or "understanding" with no validity argument; (2) not stating the criteria used to choose the number of clusters in a sequence-analysis clustering; (3) over-interpreting social-network centrality metrics as causal influence.

**Acceptance and conventions in this kind of venue**: The CSCL (computer-supported collaborative learning) and learning-analytics communities (LAK/ICQE) accept social network/epistemic network analysis as near-standard method; general HCI or design-education journals accept it at a moderate level and expect more methodological groundwork.

**Resources and ethics**: Log collection generally needs to be built into the system at the design stage (retrofitting instrumentation afterward is costly and produces inconsistent coverage periods); logs that can identify individual behavioral patterns (e.g., keystroke-level logging) need stricter ethics review and de-identification.

**Common combinations**: Heavily overlaps with longitudinal research (A-5); sequence/network structure is often paired with a small number of qualitative interviews to explain "why the interaction looks like this."

**When not to use**: (1) the system was not built with behavioral logging and a behavioral sequence is reconstructed from memory afterward — this has doubtful validity; a retrospective interview, honestly positioned as self-report data, is more defensible; (2) too few interaction events (e.g., fewer than 20–30) to support stable sequence or network pattern detection.

**Key sources**:
- Fan, Y., et al. (2024). Beware of metacognitive laziness: Effects of generative artificial intelligence on learning motivation, processes, and performance. [full text, cited as a method example]
- Epistemic-network-analysis conference papers (e.g., Tan, Hinojosa & Marquart 2022, "Epistemic Network Analysis Visualization," DOI 10.1007/978-3-030-93859-8_9; **not** Shaffer's foundational work, which was not found locally): **not read**, [abstract only]
- TraMineR / sequence analysis and social-network-analysis foundational methodology papers: not found in a local library — flagged honestly as not found; speculative citation is avoided

---

### A-8 Kansei engineering and the semantic differential method (quantitative procedures for Kansei engineering)

**Question shapes it answers**: "Which physical attributes of a product or design correspond to which subjective feelings users report" — translating hard-to-articulate affective impressions (Kansei) into operable design parameters, the core method of the Kansei-engineering field.

**Epistemic stance and claim scope**:
- **Can support**: A statistical association in a semantic space between affective vocabulary and product attributes, usable to guide design decisions.
- **Cannot support**: Kansei is an internal sensation, and every currently available measurement method is external — Schütte et al. (2004) state this limit plainly: "Since the Kansei is an internal sensation the question arising is how the Kansei can be grasped and measured. Unfortunately all the presently available measuring methods are external methods interpreting different body expressions" (Schütte, Eklund, Axelsson & Nagamachi 2004, p.9) [full text]. Describing Kansei with words has a further structural limit: "those parts of the Kansei, which cannot explicitly be expressed in words, are latent or in worst case excluded" (same source, same page) [full text] — the semantic differential method only ever measures the part of feeling that language can capture, a ceiling that must be honestly acknowledged; it should not be described as *fully capturing the user's feeling*.

**Data and sample**: Vocabulary collection should continue until saturated — Schütte et al. cite Nagamachi's rule of thumb that "the word collection is continued until no new words occur," with the number of Kansei words "generally vary[ing] between 50 and 600 words" depending on the domain (same source, p.11) [full text], before factor or cluster analysis reduces this to a workable set of items. The participant sample must represent the target group; López et al.'s (2021) systematic review (1995–2020, *Sensors* 21:6532, DOI 10.3390/s21196532) [full text] is the most complete methodological survey of Kansei-engineering practice available for reference, useful for checking convention and method-choice trends in a specific product domain (its quality-assessment table systematically scores each reviewed paper's sampling and statistical method, see its Table 3).

**Analysis procedure notes**: Osgood's original semantic differential method separates the object from the sign, using a set of bipolar adjective scales for participants to rate, from which three stable factors typically emerge: "Evaluation (E)…good-bad, kind-cruel…Potency (P)…large-small, strong-weak…Activity (A)…active-passive, fast-slow" (Osgood et al. 1957, as quoted in Schütte et al. 2004, p.7) [full text, secondhand from Schütte's summary of Osgood's original three-factor structure; Osgood's original book also has a corresponding passage]. Kansei engineering then maps the semantic space onto the product-attribute space to build predictive models, using tools including linear regression, GLM, quantification theory type I, neural networks, genetic algorithms, and rough-set analysis (Schütte et al. 2004, p.16–17) [full text]. Current trends and scoring detail are outside the scope of this card.

**Quality criteria**: Stability of the semantic space's dimensionality (whether the three-factor structure reappears in the domain in question); model validation — a predictive model built at the synthesis stage should be tested against a new sample, what Schütte et al. call a "test of validity," and they note that currently **only the semantic-space side has a validation tool; the product-attribute space still lacks one**: "no tool is available to do the same with the Space of Product Properties" (same source, p.19) [full text] — this is an unresolved gap in the method itself, and can be honestly acknowledged in a paper.

**Reporting standard**: No dedicated reporting standard; a systematic review follows PRISMA 2020.

**Common reviewer critiques and misuses**: (1) reducing the Kansei vocabulary before it is exhaustively collected, missing important affective dimensions; (2) inconsistent direction of bipolar adjectives (positive terms sometimes placed left, sometimes right), confusing participants; (3) applying vocabulary collected across cultures or languages directly to another culture, without considering that the semantic differential method itself rests on a particular language's and culture's semantic structure; (4) doing only the semantic-space analysis without the "synthesis" step that connects affective vocabulary back to concrete design parameters — measuring feeling without answering the design question.

**Acceptance and conventions in this kind of venue**: Kansei engineering, developed in Japanese industry, is a mature and well-conventioned method in design-engineering journals (e.g., *International Journal of Industrial Ergonomics*) and dedicated Kansei-engineering journals (*International Journal of Affective Engineering*); general HCI venues accept the semantic differential method without objection when it is positioned as a standard affective-measurement tool.

**Resources and ethics**: Kansei-vocabulary collection needs a relatively large, time-consuming participant effort (multiple rounds of collection, reduction, and validation); if the research touches a specific cultural group's affective vocabulary, translation and cultural equivalence need attention (the same limit noted above, since the method rests on a particular language's context).

**Common combinations**: Heavily overlaps with scale development (A-4) — the semantic differential scale itself needs reliability/validity work; often paired with rating/preference experiments (A-9), using participant ratings of product samples to build the synthesis model.

**When not to use**: (1) the goal is validating an already-known aesthetic theory, and exploring a new affective dimension is not the aim — using an existing, validated scale (e.g., AttrakDiff) is more efficient; (2) the target group is too heterogeneous (affective judgment is highly dependent on individual experience and cultural background) but all participants' data is analyzed together, ignoring group differences.

**Key sources**:
- Schütte, S. T. W., Eklund, J., Axelsson, J. R. C., & Nagamachi, M. (2004). Concepts, Methods and Tools in Kansei Engineering. [full text]
- Osgood, C. E., Suci, G. J., & Tannenbaum, P. H. (1957). *The Measurement of Meaning*. [full text]
- López, Ó., Murillo, C., & González, A. (2021). Systematic Literature Reviews in Kansei Engineering for Product Design—A Comparative Study from 1995 to 2020. *Sensors*, 21, 6532. DOI 10.3390/s21196532. [full text]
- Nagamachi, M. (1995). Kansei Engineering: A new ergonomic consumer-oriented technology. [full text, matched search snippet, no detailed quotation]

---

### A-9 Rating / preference experiments (having readers or viewers rate works or texts; psychophysical rating, paired comparison)

**Question shapes it answers**: "What is the preference or quality judgment of a group of raters toward these works or texts, and how much do the judgments agree" — common in creative evaluation, aesthetic judgment, and generated-content quality assessment.

**Epistemic stance and claim scope**:
- **Can support**: A rating panel's relative preference ranking or rating distribution over a specific stimulus set; when raters are well trained and the rating criteria are explicit, a degree of group consensus on "quality."
- **Cannot support**: "There is no single correct answer in aesthetic judgment" is not itself a flaw — it is an inherent feature of aesthetic-judgment tasks — but it also means **a single coder's or rater's judgment cannot claim to represent group consensus**; multiple raters and a reported agreement statistic are required (the same logic extends from the reliability discussion in A-6). The classic paired-comparison framework (the method of paired comparisons, canonically H. A. David's monograph) was not found in full text in a local library; Crossref confirmed only corresponding book-review records (e.g., DOI 10.2307/1270014), **not read**, [abstract only] — its technical detail is not fabricated here; it is simply noted as the standard psychophysical framework for pairwise "which stimulus wins" comparisons. A common practical alternative is direct Likert-style rating (e.g., a single Likert item as a paired comparison, analyzed with a Wilcoxon test plus an ordinal robustness check).
- Amabile's Consensual Assessment Technique (CAT) is another classic framework for creativity/aesthetic rating experiments; its core claim is that a construct like "creativity" is best rated independently by domain experts and then assessed for agreement; an external "objective" metric does not measure it directly [full text, excerpt].

**Data and sample**: The number and expertise of raters is the core sample-size justification — this means "enough independent raters to compute a stable inter-rater reliability," a different concept from a statistical-power sample size; the stimulus set (the number of works or texts being rated) must also be large enough to support statistical comparison — practical caps on image-based tools elsewhere in a project's pipeline (e.g., style/embedding tools with per-run limits in the hundreds to low thousands) are a useful practical reference point for how large a stimulus set to plan for.

**Analysis procedure notes**: A single-item Likert paired comparison uses a Wilcoxon test plus an ordinal robustness check; creativity-support-tool evaluation is often paired with a standardized scale such as the Creativity Support Index (CSI, 15 weighted paired items) — Cherry & Latulipe (2014) is the original source for this scale, held in a local library [full text, title- and abstract-level citation]. Psychophysical ranking/rating tasks that need to be converted into a comparable scale (e.g., Thurstone scaling) are an advanced technique; this port found no reliable source, local or online, for its technical detail, and flags this honestly as not found; the formula is not invented to fill the gap.

**Quality criteria**: Inter-rater reliability (Krippendorff's alpha or ICC, depending on data type — the same reliability framework as A-6 applies); whether the rating criteria were clearly defined and raters trained (untrained crowdsourced raters and trained domain experts have different quality standards and should be reported separately).

**Reporting standard**: No single dedicated guideline; a mixed-methods design follows GRAMMS.

**Common reviewer critiques and misuses**: (1) a single rater — often the author — rating and claiming to represent group taste; (2) recruiting raters through convenience sampling (e.g., friends in the same social circle) while claiming general results; (3) treating an ordinal rating scale as continuous and running parametric statistics without an ordinal robustness check; (4) retrospectively selecting a "best-performing" subset of works before sending them to raters, a form of selection bias (see the cross-method-issues discussion of retrospective analysis).

**Acceptance and conventions in this kind of venue**: In generative-art / computational-aesthetics venues (e.g., ISEA, SIGGRAPH), long-paper tracks in some sub-communities explicitly favor validated protocols with human-impact evaluation, and a rating experiment has gone from a bonus to a near-requirement in parts of that field; general HCI venues' acceptance of creative-tool rating experiments depends on whether it is paired with a standardized scale.

**Resources and ethics**: The time and cost of recruiting enough independent raters — especially trained domain experts — is often underestimated; if the rated material could cause discomfort, participants should be told during recruitment.

**Common combinations**: Highly complementary with Kansei engineering / the semantic differential method (A-8) — rating experiments are often the data-collection step of an SD study; shares a reliability/validity framework with scale development (A-4).

**When not to use**: (1) only the author, or one or two non-independent raters, actually rate the work — in this case it is more honest to relabel it a "creator's statement / self-assessment" than a "rating experiment"; (2) the rating construct is defined so vaguely that different raters understand it completely differently, with no calibration beforehand.

**Key sources**:
- Cherry, E., & Latulipe, C. (2014). Quantifying the Creativity Support of Digital Tools through the Creativity Support Index. [full text, title/abstract level]
- Amabile, T. M. Social Psychology of Creativity: A Consensual Assessment Technique. [full text, excerpt]
- David, H. A. *The Method of Paired Comparisons*. Confirmed via Crossref book-review records (e.g., DOI 10.2307/1270014), [abstract only]

---

## Group A cross-method issues

### Power analysis and sample-size justification

Lakens (2022) systematically lays out six paths to justifying a sample size in quantitative empirical research: "1) collecting data from (almost) the entire population, 2) choosing a sample size based on resource constraints, 3) performing an a-priori power analysis, 4) planning for a desired accuracy, 5) using heuristics, or 6) explicitly acknowledging the absence of a justification" (Lakens 2022, Abstract, *Collabra: Psychology* 8(1):33267, DOI 10.1525/collabra.33267) [full text]. **The value of this list is that even "resource constraints" and "explicitly acknowledging the absence of a justification" count as legitimate, if weaker, paths to a sample-size justification** — meaning reviewers do not require a perfect power analysis every time; they want an **honest account of the decision rationale**, even if that rationale is simply "this is everyone we could recruit."

But a power analysis alone is not enough to judge design quality. Blair et al.'s (2019) DeclareDesign framework points to a more fundamental issue: **high power does not mean a good design**. In a real example — a single-group pre–post study with N = 40 — a Monte Carlo diagnosis found that, with a testing effect present, power was still 1.000 but coverage (the proportion of confidence intervals that cover the true value) was only 0.218, and when "the true effect is zero, entirely due to the testing effect," coverage was 0.000 (a result from this port's own analysis; it is not a finding reported in the cited paper itself). **The criterion should be coverage. A biased design only gets worse coverage as more participants are added, so high power alone is not a safeguard** — "just find more people" does not work under a biased design; run a design-stage diagnosis first to find the source of bias, then decide whether to fix the design or add participants (the numbers above apply only to that one declared model).

### Preregistration

Preregistration addresses the core problem of "researcher degrees of freedom" — researchers, even without any bad intent, still face many defensible branch points during data analysis. Gelman & Loken (2014) coin the "garden of forking paths" to describe how this problem does not require deliberate "fishing": "researchers can perform a reasonable analysis given their assumptions and their data, but had the data turned out differently, they could have done other analyses that were just as reasonable in those circumstances" (Gelman & Loken 2014, p.1–2) [full text]. This concept goes further than Simmons, Nelson & Simonsohn's (2011) "researcher degrees of freedom": even when each individual analytic choice is defensible on its own and no explicit multiple-comparison fishing occurred, the analytic path taken is still a function of the data, creating a hidden multiple-comparisons problem.

Empirically, the scale of this problem can be measured with "many analysts, one dataset" designs: Silberzahn et al. (2018) and Coretta et al. (2023) both had multiple independent teams analyze the same dataset to answer the same research question and compared how much the conclusions varied. Coretta et al. had 46 research teams analyze the same speech dataset to answer the same research question, finding "substantial variability in reported effect sizes and their interpretation," with "little to no evidence that the observed variability can be explained by analysts' prior beliefs, expertise, or the perceived quality of their analyses" (Coretta et al. 2023, Abstract, DOI 10.1177/25152459231162567) [full text] — **the variability in conclusions is not because some analysts did a worse job; the space of defensible analytic choices is itself large enough to produce substantively different conclusions**. This is the underlying reason preregistration and multiverse analysis (Steegen et al. 2016) exist at all.

The practical rule: a power analysis and the smallest effect size of interest (SESOI) must both be declared at the **design stage** — a post-hoc power analysis is meaningless. Preregistration is optional in HCI venues today, though the **best time to register is right after a design diagnosis is run** (the MIDA declaration is effectively a draft of the hypothesis and analysis plan) — folding preregistration into the design-diagnosis workflow avoids filing a separate formal document after the fact.

### The claim limits of small samples and convenience samples

Small and convenience samples are not themselves a sin; what matters is whether the claim's scope matches the sampling logic. Cash et al.'s (2022) theory-building vs. theory-testing distinction (see A-3) provides an honest framework: if the goal is to explore "what is happening in a context, is it interesting," a narrow, deep sample (a convenience sample, a case study) is methodologically **appropriate**; it is not a compromise. If the goal is theory-testing — "do proposed relationships hold true in empirical data" — it needs "wide data" to support cross-group, cross-context claims (Cash et al. 2022, Table 1) [full text]. **The single most common reviewer complaint is a sample collected under theory-building logic being written up in the register of a theory-testing claim** (e.g., a convenience-sample interview study with N = 15 stated as "showing that X phenomenon is prevalent"). Conversely, honestly framing a small or convenience sample as theory-building, hypothesis-generating, or case-level deep description is a completely defensible methodological position, and does not need to be dressed up in overstated claim language.

### The problem of retrospective analysis (deciding the analysis after seeing the data)

The core risk of retrospective analysis is the same coin as the problem preregistration solves: Gelman & Loken's (2014) "forking paths" concept is essentially describing how deciding an analytic path after seeing the data can manufacture false findings without any bad intent. Simmons, Nelson & Simonsohn's (2011) "false-positive psychology" study further uses simulation and empirical demonstration to show that even when every analytic decision follows normal practice and is reported honestly, several "reasonable" analytic degrees of freedom combined can push the false-positive rate far above the nominal .05.

This connects tightly to two other points in this cross-method section: (1) **power analysis must be finished at the design stage**, because deciding to collect more data after seeing it is itself a form of retrospective analysis (optional stopping); (2) **preregistration works precisely because** it locks the analytic decisions in before the data is seen, so the later analytic path cannot adjust based on how the data turned out. The most directly actionable defense: **write the analysis plan — including exclusion rules, primary outcome variables, and the choice of statistical test — before analysis begins, once data collection is complete**, even without a formal OSF preregistration; at minimum, keep a time-stamped internal analysis-plan document. Any pre-submission checklist should treat "the rule and number of excluded cases" as a mandatory item, precisely because of this risk.

---

Sources: see the key-sources list in each card.


## Group B: Qualitative methods

> Evidence tags: `[full text]` = read from the original text in your own local literature library; `[full text, web]` = an actual web page or full-text PDF was read (including a methodological statement on an author's own website); `[abstract only]` = only an abstract or authoritative bibliographic record was read; the full text was not read.

---

### B-1 Reflexive Thematic Analysis

**Question shapes it answers**: "Around a research question, what meaningful patterns (themes) emerge in the participants' data or texts" / "what does this phenomenon look like in the data, what facets does it have" — essentially a meaning-making question. It is not a "which is more common" counting question.

**Epistemic stance and claim scope**:
- **Can support**: Deep, interpretive description of "meaningful patterns" in a dataset; shared meaning structures across cases; exploratory, hypothesis-generating statements.
- **Cannot support**: Prevalence/frequency claims ("most respondents felt..."), generalization across samples, causal claims, claims of an "objective" or single "correct" coding. Braun & Clarke state plainly: "the 'keyness' of a theme is not necessarily dependent on quantifiable measures – but rather on whether it captures something important in relation to the overall research question," and give an example of a theme that "appeared in between two and 22 of the 26 talk shows" yet is still "key" — because the analysis is driven by the research question; frequency of occurrence is not the criterion [full text, Braun & Clarke 2006, *Qualitative Research in Psychology*, 3(2), 77-101, journal page 82].
- The method itself is **epistemically neutral and can be used across paradigms**: the original text states that "thematic analysis is actually firmly in the second camp, and is compatible with both essentialist and constructionist paradigms within psychology" [full text, same source, journal page 78]. This means the **same dataset analyzed under different epistemic stances yields claims of a different character** — a paper must state up front which stance it takes (a realist report of experience itself, or a constructionist examination of how meaning is constructed).

**Data and sample**:
- Braun & Clarke explicitly **do not recommend "saturation" as the sample-size justification for reflexive TA**: "we recommend avoiding claims of 'saturation' (Braun & Clarke, 2021); you might instead refer to the concept of 'information power' (Malterud et al., 2016) as a guide" [full text, web, from their official methodology page]. The corresponding paper is Braun, V., & Clarke, V. (2019/2021), *To saturate or not to saturate? Questioning data saturation as a useful concept for thematic analysis and sample-size rationales*, *Qualitative Research in Sport, Exercise and Health*, 13(2), 201-216 (online 2019, print 2021, DOI: 10.1080/2159676X.2019.1704846).
- The sample-size justification instead relies on: the dataset's "information richness" (depth over quantity), the scope of the research question, and the complexity of data items. From the official page: "there's no simple answer to dataset size... no simple way to factor in elements such as data depth, richness, complexity, to arrive at a 'correct' dataset size" [full text, web, same source].
- Data can be a small number of "information-rich" deep items, or a larger number of "thinner" items — depth and breadth are an explicit trade-off [full text, web, same source].

**Analysis procedure notes**: Six phases (1. familiarizing with the data; 2. generating initial codes; 3. searching for themes; 4. reviewing themes; 5. defining and naming themes; 6. producing the report). The process is recursive; it is not linear — the original text states: "[a]nalysis involves a constant moving back and forward between the entire data set, the coded extracts of data that you are analysing, and the analysis of the data that you are producing." Writing is not something that begins after analysis ends: "writing should begin in phase one, with the jotting down of ideas and potential coding schemes, and continue right through the entire coding/analysis process" [full text, Braun & Clarke 2006, journal page 86]. **A theme is the "output" of analysis; it is not analysis's "input"** — this is the most fundamental difference from the other two schools of thematic analysis below; a theme is not assumed to pre-exist in the data waiting to be "found" [full text, web, from their FAQ page].

**Quality criteria**:
- Reflexive TA **explicitly rejects inter-coder reliability / multiple independent coders**. The official position: "using a coding frame [is] precisely so that you can calculate inter-rater reliability scores... we don't advocate the use of a coding frame, or the calculation of reliability scores"; the reasoning is that their stance holds there is "no single, 'accurate' reading of data, and meaning is not treated as fixed and singular," so the realist/positivist assumptions behind inter-coder reliability do not hold — a reliability score "demonstrates not that two researchers code data 'accurately,' but that they have been trained to code data in the same way" (citing Yardley 2008) [full text, web, from their FAQ page]. They also quote Morse's (1997) verdict: "maintaining a simplified coding frame for the purpose of testing inter-rater reliability...to define categories...reduces the research to the point that even the richness the insight offers can be lost" [full text, web, secondhand quotation, Morse, J. (1997). "Perfectly healthy, but dead": The myth of inter-rater reliability. *Qualitative Health Research*, 7(4), 445-447].
- Alternative quality criteria: conceptual coherence / "fit" (Braun & Clarke, 2013), Levitt et al.'s (2017) "methodological integrity," the depth and transparency of reflexive writing.
- The spectrum of three kinds of thematic analysis (**a key distinction for review and write-up decisions**):
  1. **Coding reliability**: Boyatzis (1998), Guest et al. (2012), Joffe (2011) — uses a structured codebook, multiple independent coders, and a statistical reliability figure (Cohen's Kappa, commonly with a threshold above .80); themes are often treated as analytic "input" (equivalent to a "topic summary").
  2. **Codebook**: template analysis (King & Brooks, 2017), framework analysis (Ritchie & Spencer, 1994), matrix analysis (Miles & Huberman, 1994) — uses a codebook but does not compute reliability statistics; sits between the other two, common in team collaboration, commissioned policy research, and time-pressured applied settings.
  3. **Reflexive**: the Braun & Clarke line — a single researcher or a small team, organically evolving coding, themes as an analytic output.
  Calling these three "the same method at different levels of rigor" is a mistake: they are **different methods with different epistemic commitments**, and mixing them produces methodological inconsistency (e.g., using reflexive TA's language while reporting a reliability coefficient) [full text, web, same source].

**Reporting standard**: **There is no formal COREQ/SRQR-style checklist for this method**, and Braun & Clarke themselves are critical of existing checklists — they published a critique of COREQ (Braun & Clarke, 2024, *Methods in Psychology*, DOI: 10.1016/j.metip.2024.100155) and developed two tools of their own: **RTARG** (Reflexive Thematic Analysis Reporting Guidelines, *Qualitative Research in Psychology*, DOI: 10.1177/02692163241234800) and **BQQRG** (Big Q Qualitative Reporting Guidelines, DOI: 10.1080/14780887.2024.2382244) — the latter designed as "a tool for researchers to reflect with, rather than a checklist to be ticked off item by item" [abstract only for all three — only the official website's summary of their stance and function was read; the full papers were not read]. If the target venue (e.g., nursing or medical-education journals) **requires COREQ**, this tension needs addressing beforehand: COREQ's assumptions (structured coding, multi-coder reliability) are **incompatible** with reflexive TA's epistemic stance, and forcing it will produce a methodologically contradictory manuscript.

**Common reviewer critiques and misuses**:
- The most common misuse is conflating the three kinds of TA — using reflexive-TA language ("themes emerged") while actually running a coding-reliability analysis (multiple coders plus Kappa), or the reverse: writing a genuinely reflexive analysis but being checked by a reviewer against coding-reliability expectations (asked to report Kappa, asked "how was saturation ensured").
- Common reviewer questions: whether the sample size is adequate (if "saturation" language is used, per the stance above this counts as a weakness; it does not count as a strength); whether the themes are genuine "patterns with a central organizing concept" or merely "topic summaries" (the FAQ page specifically addresses this confusion: names like "Experiences of Y" or "Benefits of X" are typical symptoms of a topic summary disguised as a theme) [full text, web, same source].
- In a teacher-researcher scenario: a reflexivity statement reduced to a single boilerplate sentence ("as the instructor, the author may have influenced the data") without specifics on how it was handled will be seen as a box-ticking exercise.

**Acceptance and conventions in this kind of venue**: DIS/CHI hold qualitative rigor to a high standard and near-default expect a reflexivity/positionality statement; design-education journals accept it commonly but also show frequent terminology confusion. SIGGRAPH/ISEA art tracks generally do not require it. **Not found**: an explicit convention in design-focused Chinese-language journals distinguishing the three kinds of TA — check whether a paper using reflexive TA has been accepted recently in the target venue before submitting.

**Resources and ethics**: Moderate time cost (no need to coordinate multiple coders, but reflexive writing itself is time-consuming); general qualitative-research ethics review is needed if students/participants are involved; the teacher-researcher power relation is covered in the cross-method-issues section.

**Common combinations**: Often paired with open-ended questionnaires, semi-structured interviews, and diary studies as data sources; can be combined with quantitative scales in a mixed-methods design (reported with GRAMMS); often used alongside visual/artefact analysis in design-education research.

**When not to use**: Not for prevalence or quantitative-comparison claims (use content analysis or survey statistics instead); if the review venue explicitly requires inter-coder reliability (as some medical-education journals do) and the editor cannot be persuaded to accept a reflexive stance, a codebook or coding-reliability approach avoids the epistemic contradiction; not suitable with only one or two data items too thin to support the analysis.

**Key sources**:
- Braun, V., & Clarke, V. (2006). Using thematic analysis in psychology. *Qualitative Research in Psychology*, 3(2), 77-101. [full text]
- Braun, V., & Clarke, V. (2019/2021). To saturate or not to saturate? *Qualitative Research in Sport, Exercise and Health*, 13(2), 201-216. DOI: 10.1080/2159676X.2019.1704846 [full text, web, from the authors' official website; not read directly in full]
- Braun, V., & Clarke, V. (2021). One size fits all? What counts as quality practice in (reflexive) thematic analysis? *Qualitative Research in Psychology*, 18(3), 328-352. DOI: 10.1080/14780887.2020.1769238 (Crossref confirmed) [abstract only; the substance of their position was read via the official site's summary, tagged full text, web]
- thematicanalysis.net (Braun & Clarke's official website): /faqs/, /quality-in-ta/, /designing-for-reflexive-ta/ [full text, web]
- Morse, J. (1997). "Perfectly healthy, but dead": The myth of inter-rater reliability. *Qualitative Health Research*, 7(4), 445-447. [full text, web, secondhand quotation]
- Malterud, K., Siersma, V. D., & Guassora, A. D. (2016). Sample size in qualitative interview studies: Guided by information power. *Qualitative Health Research*, 26(13), 1753-1760. DOI: 10.1177/1049732315617444 [abstract only, confirmed via Crossref]

---

### B-2 Grounded Theory (Glaser & Strauss / Strauss & Corbin / Charmaz's constructivist version)

**Question shapes it answers**: "How does this social process/action work" — grounded theory's output is a **theory** ("grounded" meaning it grows out of the data) that explains a process or action; it is not a descriptive theme. Fits process- or stage-oriented questions such as "how do people do X" or "what is the core process behind this phenomenon."

**Epistemic stance and claim scope**:
- The three schools take different epistemic stances, and **picking the wrong one makes the whole methodology self-contradictory**:
  - **Classic / Glaser school**: leans objectivist; theory is seen as "emerging" from the data, with the researcher trying not to impose an existing theoretical framework.
  - **Strauss & Corbin school**: a more structured procedure (open coding → axial coding → selective coding, a three-stage system), allowing the researcher's analytic framework to actively engage the data.
  - **Constructivist / Charmaz school**: explicitly abandons the assumption that theory "objectively emerges," arguing instead that theory is **co-constructed** by researcher and participants — the researcher's position, interactions, and reflexivity are part of theory-building; they are not a contamination to be eliminated.
  The three schools diverge on "three key points of divergence: opposing coding procedures, opposing philosophical stances, and conflicting ways of using the literature" [abstract only, Kenny, M., & Fourie, R. (2015). Contrasting Classic, Straussian, and Constructivist Grounded Theory. *The Qualitative Report*, 20(8). DOI: 10.46743/2160-3715/2015.2251 — only the abstract and author information were read; the full PDF was blocked at 403].
- **Can support**: A grounded-theory explanation of a process/action, including a core category and its relationships; construction of a middle-range theory.
- **Cannot support**: Generalizing beyond the sample to a population (unless a further theoretical-generalization argument is made after reaching theoretical saturation); cross-case frequency statistics.
- Braun & Clarke note that their own coding approach "shares some similarities with the initial coding stage of grounded theory" (citing Charmaz, 2006), showing that TA and GT overlap at the early open-coding stage, though GT's goal is a **theory**; a pattern-style theme is not the target [full text, web, from their FAQ page].

**Data and sample**: Sampling stops at **theoretical saturation**. No sample size is fixed in advance; the researcher continues "theoretical sampling" (deciding who to interview or what data to examine next based on emerging categories) until new data no longer produces new properties or relationships for existing categories. **This "saturation" is not the same "saturation" that reflexive TA explicitly rejects** — GT's theoretical saturation is bound to the full methodological framework of the constant-comparative method and theoretical sampling; B&C's objection is to stripping "saturation" of that context and using it as a generic sample-size justification for any qualitative study (see the cross-method-issues section, Braun & Clarke 2021).

**Analysis procedure notes**: The constant-comparative method runs throughout; memo-writing is a continuous vehicle for analytic thinking throughout the process; theoretical sampling; (common in the Strauss & Corbin / general practice tradition) open coding → axial coding (finding relationships between categories) → selective coding (integrating a core category).

**Quality criteria**: Glaser & Strauss's original criteria — fit, workability, relevance, modifiability. Constructivist GT adds reflexive transparency (how the researcher co-constructed meaning with participants).

**Reporting standard**: No dedicated checklist; commonly reported using general qualitative reporting standards (COREQ/SRQR) plus GT-specific requirements — the logic of theoretical sampling, how memos were used, how the core category was developed from the data, and a specific description of the saturation criterion.

**Common reviewer critiques and misuses**: The most common misuse is "claiming grounded theory while actually only doing thematic or content analysis, with no real theoretical sampling, constant comparison, or theoretical integration into a core category" ("grounded theory lite"). Reviewers typically ask three things: did the study use theoretical sampling and not simply one-time convenience sampling; is there a memo trail; and is the final output really a "theory" and not merely a classification scheme. Mixing schools (citing Charmaz's method label while running Strauss & Corbin's linear three-stage coding) is also a common contradiction.

**Acceptance and conventions in this kind of venue**: Common with mature conventions in education research and nursing/medical-education journals; relatively rare in HCI/design research, and typically needs extra space to justify GT over TA. **Not found**: explicit data on how design-focused Chinese-language journals treat the three GT schools.

**Resources and ethics**: High time cost (the constant-comparative method requires repeated returns to the field/data, and theoretical sampling may need multiple rounds of data collection); full ethics review is needed, especially for repeated contact with interviewees.

**Common combinations**: Often paired with interviews (the most common data source), diary studies, and ethnographic observation; rarely mixed with quantitative methods (the epistemic assumptions clash more strongly, so any mixing needs an explicit paradigm statement).

**When not to use**: If only a "pattern-style" description is wanted, and theory-building is not the goal, TA is lighter-weight; if there is no capacity for multiple rounds of theoretical sampling (e.g., interviewees are only available once, with no possibility of returning), GT's core methodological steps cannot be completed and TA or content analysis is more honest; in cross-disciplinary collaborations where collaborators are unfamiliar with the differences between the three GT schools, methodological patchwork is an easy trap.

**Key sources**:
- Glaser, B. G., & Strauss, A. L. (1967). *The Discovery of Grounded Theory: Strategies for Qualitative Research*. Aldine. [abstract only, Crossref confirms the bibliographic record: DOI 10.4324/9780203793206-1 (a 2017 reprint chapter)]
- Strauss, A., & Corbin, J. (1998/2008). *Basics of Qualitative Research: Techniques and Procedures for Developing Grounded Theory* (3rd ed.). Sage. DOI: 10.4135/9781452230153 [abstract only]
- Charmaz, K. (2006/2014). *Constructing Grounded Theory: A Practical Guide Through Qualitative Analysis*. Sage. [abstract only; bibliographic record confirmed via thematicanalysis.net's official reference list and a citation in the same domain's literature]
- Kenny, M., & Fourie, R. (2015). Contrasting Classic, Straussian, and Constructivist Grounded Theory. *The Qualitative Report*, 20(8), 1270-1289. DOI: 10.46743/2160-3715/2015.2251 [abstract only]
- Mills, J., Bonner, A., & Francis, K. (2006). The Development of Constructivist Grounded Theory. *International Journal of Qualitative Methods*, 5(1), 25-35. DOI: 10.1177/160940690600500103 [abstract only]

---

### B-3 Interpretative Phenomenological Analysis (IPA) and the phenomenological approach

**Question shapes it answers**: "How does this person (or small group) personally experience a particular phenomenon or event" — focused on an individual's meaning-making about a specific experience: a **personal, deeply descriptive** question; it is not a search for a common pattern across cases (that is TA's territory).

**Epistemic stance and claim scope**:
- Braun & Clarke contrast IPA and TA's epistemic difference directly: "IPA is attached to a phenomenological epistemology..., which gives experience primacy..., and is about understanding people's everyday experience of reality, in great detail, in order to gain an understanding of the phenomenon in question," noting that IPA and grounded theory both "look for patterns in the data, but within a theoretically bounded way," in contrast to TA's theoretical freedom [full text, Braun & Clarke 2006, journal page 80].
- **Can support**: A deep, personalized, meaning-level understanding of a specific experience; idiographic case-by-case comparison: going deep into a single case first, then comparing across cases; a search for commonality is not the starting point.
- **Cannot support**: Frequency or prevalence claims; cross-group representativeness; behavioral prediction beyond the experience itself. IPA explicitly acknowledges the "double hermeneutic" — the researcher is interpreting the participant's interpretation of their own experience — and this double layer of mediation itself limits any claim to have "captured the objective experience itself."

**Data and sample**: **Deliberately small, homogeneous sampling** — this is IPA's biggest operational difference from other methods; the sample-size justification is neither saturation nor information power but **case depth first**: 3–6 cases is common at student level, up to 10–15 in larger studies, with the sample deliberately homogeneous (a similar type of experience, similar background) to support cross-case interpretive power. An overly large sample is, in the IPA tradition, seen as a failure to go deep enough into each case; it does not count as added rigor.

**Analysis procedure notes**: Case-by-case analysis (fully analyzing the first case's transcript before moving to the second, to avoid premature cross-case comparison contaminating the fine detail within a case) → within-case themes → cross-case comparison and integration into superordinate themes. The unit of analysis is usually a semi-structured, in-depth interview transcript.

**Quality criteria**: Awareness and articulation of the "double hermeneutic"; the richness (thick description) of the case depiction; reflexive bracketing — the researcher's attempt to become aware of and set aside their own preconceptions, though the phenomenological tradition generally accepts that full bracketing is impossible; the point is to **document the attempt**; claiming success is not the goal.

**Reporting standard**: No dedicated checklist; commonly borrows COREQ/SRQR or a journal's own IPA reporting guidance; the core items to state are the criteria for sample homogeneity, the order of case-by-case analysis, and a statement acknowledging the double hermeneutic.

**Common reviewer critiques and misuses**: The most common misuse is labeling a study IPA while actually doing thematic analysis (cross-comparing cases for common patterns from the start, without first going deep into one case); a sample size clearly outside IPA convention (e.g., 30+ cases labeled IPA) will be questioned for lack of depth; vague criteria for homogeneous sampling ("why are these participants considered homogeneous") is also a common follow-up question.

**Acceptance and conventions in this kind of venue**: IPA is a mainstay in psychology, health psychology, and counseling research; it is **uncommon** in HCI/design-education journals, and typically needs extra space to justify choosing IPA over the more common TA. **Not found**: a specific precedent for IPA in the venues the author usually submits to (design journals, IJDesign, DIS, etc.).

**Resources and ethics**: Interviews need to be relatively long and deep (often 1-2 hours), requiring participants willing to disclose deeply — ethics review requirements are higher, especially for emotional, traumatic, or intimate experience topics.

**Common combinations**: Almost exclusively paired with deep semi-structured interviews; rarely mixed with other methods, because the case depth and phenomenological stance it emphasizes do not mix easily with other paradigms.

**When not to use**: Not suited to finding a cross-case common pattern; personal, deep experience is IPA's focus instead. At a sample size above roughly 15, this is no longer IPA's strength methodologically; when the research question is "how does phenomenon X operate in this setting," and not "how does this person experience X" — TA or ethnography fits better.

**Key sources**:
- Smith, J. A., & Osborn, M. (2003/2008). Interpretative phenomenological analysis. In J. A. Smith (Ed.), *Qualitative Psychology: A Practical Guide to Research Methods*. Sage. DOI: 10.4135/9781036232764.n3 (2024 record) [abstract only, confirmed via Crossref]
- Braun, V., & Clarke, V. (2006). Using thematic analysis in psychology (the passage contrasting IPA and TA). [full text]

---

### B-4 Ethnography (including short-term, digital, and classroom ethnography)

**Question shapes it answers**: "How does this field/community/cultural practice work, how do members live within it and make meaning" — emphasizing long-term immersion and contextual wholeness, suited to holistic questions such as "what happened in this setting and why." A single variable or single event is not this method's focus.

**Epistemic stance and claim scope**:
- **Can support**: Thick description of a field's cultural practices; understanding of the field's internal logic and system of meaning; reflexive exposure of "taken for granted" practices.
- **Cannot support**: Generalization across fields (unless a multi-site comparative ethnography with a clearly stated comparative logic is done); quantitative prevalence; causal claims.
- Short-term or focused/rapid ethnography sacrifices the long immersion traditional ethnography emphasizes, trading it for time feasibility — this trade-off itself needs to be stated explicitly in the methods section, or the study will be questioned as "not really ethnography, just extended participant observation."
- Digital ethnography extends the field into online communities and platforms, and needs to address extra questions such as "where are the field's boundaries" and "what does participant observation mean in an algorithmically mediated environment."
- Classroom ethnography is common in education research, where the observer's role (teacher-as-observer vs. outside observer) directly affects the nature and credibility of the data.

**Data and sample**: The sampling unit is the "field," and headcount is not the relevant measure; length of time is the core justification (traditional ethnography often needs months to years; short-term ethnography compresses this to weeks but must state the trade-off); data sources are typically diverse (field notes, interviews, documents, audiovisual material, artifacts).

**Analysis procedure notes**: Field-note writing runs throughout (descriptive notes plus analytic memos); constant movement back and forth between the field and analysis; often paired with thematic analysis or grounded-theory coding of field data; triangulation (corroborating multiple data sources) is common practice.

**Quality criteria**: Richness of the thick description; reflexivity (how the researcher's position in the field shaped observation and interpretation); whether the length of engagement is enough to support the claimed depth.

**Reporting standard**: No dedicated formal checklist; commonly follows general qualitative reporting standards, plus reporting the length of time in the field, the researcher's role (participant/non-participant, insider/outsider), and how access to the field was gained and left.

**Common reviewer critiques and misuses**: The most common critique is calling something "ethnography" with insufficient time invested ("ethnography-lite," in substance a few observations plus interviews); an unclear account of the researcher's role (especially in a teacher-researcher scenario — see the cross-method-issues section); missing reflexivity about how the researcher was perceived in, and influenced interaction within, the field.

**Acceptance and conventions in this kind of venue**: CSCW/CHI accept digital ethnography readily; design-education journals have some convention around classroom ethnography / teaching-setting research, but the boundary with "teaching observation" or "action research" can be blurry and reviewers may ask for the distinction to be clarified. **Not found**: an explicit consensus in *Design Studies*/IJDesign on a minimum time threshold for short-term ethnography.

**Resources and ethics**: One of the most time-costly qualitative methods; the power-relation issue is sharpest when a teacher-researcher does classroom ethnography (see the cross-method-issues section); long-term engagement in a field may need continuing ethics review; a one-time approval is not always enough.

**Common combinations**: Often paired with interviews, focus groups, document analysis, and visual analysis for triangulation; the analysis stage commonly follows with thematic analysis or grounded theory.

**When not to use**: When time resources clearly cannot support the claim of "immersive understanding" (in this case, honestly calling it participant observation or a case study is safer); when the research question only concerns a specific intervention's effect, and not the field's overall cultural logic, other methods are leaner and more effective.

**Key sources**:
- Hammersley, M., & Atkinson, P. (2019). *Ethnography: Principles in Practice* (4th ed.). Routledge. DOI: 10.4324/9781315146027 [abstract only, Crossref confirms the bibliographic record]
- Pink, S., Horst, H., Postill, J., Hjorth, L., Lewis, T., & Tacchi, J. (2016). *Digital Ethnography: Principles and Practice*. Sage. [abstract only; bibliographic record confirmed via a book review, DOI 10.14267/cjssp.2017.01.08]

---


### B-5 Case Study (Yin / Stake / Flyvbjerg's case-selection logic and generalization)

**Question shapes it answers**: "How and why does a phenomenon happen and operate within this (single or small number of) case(s)" — especially suited to "how" and "why" questions, and to situations where the researcher has low control over events and the phenomenon and its context are hard to separate (Yin's classic criteria).

**Epistemic stance and claim scope**:
- The three scholars' approaches and claim scope differ, and **choosing the wrong case-selection logic undermines the generalization claim**:
  - **Yin**: leans post-positivist, emphasizing rigor in case-study design (propositions, units of analysis, the data-proposition link, the explanatory logic); supports **analytic generalization** (generalizing case findings to a theoretical proposition; population-level generalization is not supported); a multiple-case design can use "replication logic" (verifying the same proposition case by case) to strengthen the argument.
  - **Stake**: distinguishes an **intrinsic case study** (studying this case is itself the goal, because the case is inherently worth understanding) from an **instrumental case study** (this case is a tool for understanding a larger issue). Stake's approach is more qualitative and interpretive, valuing the case's uniqueness, and pursuing "generalizability" is not the core concern of this approach.
  - **Flyvbjerg**: directly rebuts the common misunderstanding that "you cannot generalize from a single case, so single-case research cannot contribute to scientific development" — he names this as one of five common misunderstandings and argues that "a scientific discipline without a large number of thoroughly executed case studies is a discipline without systematic production of exemplars" [abstract only, from the abstract's concluding sentence, Flyvbjerg, B. (2006). Five Misunderstandings About Case-Study Research. *Qualitative Inquiry*, 12(2), 219-245. DOI: 10.1177/1077800405284363]. Flyvbjerg argues that **strategic case selection** (extreme cases, critical cases, maximum-variation cases, typical cases) can produce more transferable knowledge than random sampling — this is a sampling logic specific to case-study research: strategic selection deliberately targets atypical or extreme cases, the opposite orientation from random sampling's aim of representativeness.
- **Can support**: A deep explanation of the process/mechanism within the case; analytic generalization (generalizing findings to a theoretical proposition); under strategic case selection, a speculative claim about "how this kind of situation may operate."
- **Cannot support**: Statistical generalization to a population (unless a multiple-case replication design with a clearly stated logic is used).

**Data and sample**: Case-selection logic is itself a core methodological decision and must be stated explicitly in the manuscript — which type (extreme/critical/typical/maximum-variation) and why; the choice between a single case and multiple cases — multiple cases trade some depth for stronger analytic-generalization power via replication logic. Data sources are usually triangulated from multiple types (documents, interviews, observation, artifacts).

**Analysis procedure notes**: Yin emphasizes building an analytic framework (propositions) before data collection, then doing pattern matching, explanation building, and time-series analysis during analysis; Stake's approach leans more narrative and interpretive in its case description and meaning-making.

**Quality criteria**: Yin proposes construct validity (triangulation across multiple evidence sources), internal validity (the logic of pattern matching), external validity (whether the logic of analytic generalization holds), and reliability (the reproducibility of the case-study protocol) — this set of criteria borrows positivist vocabulary, and using it should be checked against whether it matches the study's own epistemic stance.

**Reporting standard**: No dedicated independent checklist; commonly expected to state the case-selection criteria and rationale, the unit of analysis, how data sources were triangulated, and how the case boundary was drawn.

**Common reviewer critiques and misuses**: The most common critique is "there's only one case here, how can you generalize?" — this is precisely the misunderstanding Flyvbjerg rebuts directly, and can be answered by citing his distinction between analytic and statistical generalization; unclear case-selection logic ("why this case") is another common complaint; using "case study" as a lazy catch-all label when the data is not solid.

**Acceptance and conventions in this kind of venue**: Deep case studies of a system or tool (deployment studies) are common in design research and HCI; single-course or single-class case studies are common in education research but are often asked to clarify whether they follow Stake's approach (understanding meaning) or Yin's (theoretical verification).

**Resources and ethics**: Resource needs vary widely with the number of cases and data sources; when a teacher does a case study of their own course, the same power-relation issue applies (see the cross-method-issues section).

**Common combinations**: Often paired with interviews, document analysis, and observation for triangulation; paired with grounded theory or thematic analysis for within-case data analysis.

**When not to use**: When the research question is fundamentally comparative ("does situation A differ from situation B") and needs statistical generalization, a case study is not the right tool; if the case-selection logic is not stated clearly and it is really just "whatever case happened to be at hand," it should at least be honestly labeled a convenience sample; calling it a strategic selection would not be accurate.

**Key sources**:
- Yin, R. K. (2018). *Case Study Research and Applications: Design and Methods* (6th ed.). Sage. [abstract only; this book has no stable DOI, but its bibliographic record is confirmed via multiple citing works]
- Stake, R. E. (1995). *The Art of Case Study Research*. Sage. DOI: 10.2307/329758 (book-review record) [abstract only]
- Flyvbjerg, B. (2006). Five Misunderstandings About Case-Study Research. *Qualitative Inquiry*, 12(2), 219-245. DOI: 10.1177/1077800405284363 [abstract only, confirmed via Crossref]

---

### B-6 Discourse Analysis / Critical Discourse Analysis

**Question shapes it answers**: "What does language/text do here, what social reality or power relation does it construct" — concerned with the constructive function of language; the "real" psychological state or objective fact behind it is not the focus. Critical discourse analysis (CDA) further asks "how does this discourse maintain or challenge power/ideological relations."

**Epistemic stance and claim scope**:
- Braun & Clarke place discourse analysis in the "theoretical thematic analysis" camp: they write that a method like IPA has "(as yet) relatively limited variability in how the method is applied, within that framework. In essence, one recipe guides analysis," whereas "grounded theory..., discourse analysis... or narrative analysis... there are different manifestations of the method, from within the broad theoretical framework" [full text, Braun & Clarke 2006, journal page 78]. Discourse analysis itself spans a spectrum of theoretical commitments; no single method defines it: the Foucauldian version concerns "how the world, society, events, and the psyche are produced in the use of language and discourse" [full text, quoted passage from Candy 2006], while van Dijk's critical discourse analysis centers on "how power abuse, dominance, and inequality are enacted, reproduced, and resisted by discourse in the social and political context" [abstract only, van Dijk, T. A. (1993). Principles of Critical Discourse Analysis. *Discourse & Society*, 4(2), 249-283. DOI: 10.1177/0957926593004002006].
- **Can support**: How a text/talk constructs a particular version of reality, identity, or relationship; a critical exposure of the ideological assumptions behind language choices and their social consequences.
- **Cannot support**: The speaker's "true" internal psychological state or belief (DA takes a constructionist stance toward language; talk is not treated as a transparent reflection of internal psychological states); prevalence/frequency claims; generalization detached from the textual context.

**Data and sample**: The unit of analysis is a text/talk fragment, and a "headcount" is not the relevant measure; the sample-size justification depends on the discursive diversity of the corpus and the depth of analysis, with no fixed threshold; sources can be interview transcripts, policy documents, media reports, social-media posts, and similar.

**Analysis procedure notes**: Close, sentence-by-sentence or segment-by-segment reading, attending to word choice, rhetorical strategy, presupposition, and how actors are referred to, and to the tensions and contradictions in the discourse; CDA typically combines this with a social-context analysis, reading the power structures in which the text is produced and circulated in addition to the text itself.

**Quality criteria**: The analysis's persuasiveness comes from a tight connection to textual detail and consistent use of the theoretical framework; reflexivity about how the researcher's own position shapes their critical reading of the discourse.

**Reporting standard**: No dedicated formal checklist; core items to state are the criteria for text selection, the theoretical source of the analytic framework, and how counter-examples were handled.

**Common reviewer critiques and misuses**: The most common misuse is doing "content analysis with theoretical jargon added" — merely categorizing topics and labeling them "discourse" without actually doing a language-level constructive analysis; CDA is often accused of "drawing the target around the arrow" (the researcher brings a predetermined power-critique framework to the text and selectively cites supporting passages) — the way to respond is to demonstrate the systematicity of the analysis and how counter-examples/contradictory evidence were handled.

**Acceptance and conventions in this kind of venue**: Bardzell & Bardzell's (2015) *Humanistic HCI* lists critical discourse analysis as one of the shared inquiry practices in HCI's humanistic-research community [full text]. Critical analysis of policy texts, teaching discourse, and AI discourse is growing in design research, but it is still not the common method in mainly quantitative venues (IUI/HCII).

**Resources and ethics**: Moderate-to-high time cost (close reading is time-consuming); text involving identifiable individuals (e.g., social-media posts) needs to address de-identification and informed consent.

**Common combinations**: Often paired with ethnography and interview data (analyzing the discursive level of an interview transcript, beyond topic coding alone); complementary with content analysis (content analysis finds patterns, DA digs into the constructive mechanism behind them).

**When not to use**: When the research question only concerns "what was said" (content/topic), and not "how it was said, what social effect it produced," content or thematic analysis is more direct; without enough training in linguistics/discourse theory to support close reading, a forced application of DA easily degrades into "sticking on labels."

**Key sources**:
- Fairclough, N. (1995). *Critical Discourse Analysis: The Critical Study of Language*. Longman. [abstract only; bibliographic record confirmed via a book review, DOI 10.2307/329335]
- van Dijk, T. A. (1993). Principles of Critical Discourse Analysis. *Discourse & Society*, 4(2), 249-283. DOI: 10.1177/0957926593004002006 [abstract only]
- Bardzell, J., & Bardzell, S. (2015). Humanistic HCI. *Synthesis Lectures on Human-Centered Informatics*. [full text]
- Candy, L. (2006). *Practice Based Research: A Guide*. [full text, discourse-analysis definition passage]

---

### B-7 Qualitative Content Analysis (Mayring; Hsieh & Shannon's three types)

**Question shapes it answers**: "What does the pattern and distribution of pre-set or emergent categories in this text data look like" — sitting between qualitative depth and quantitative counting, suited to text categorization that needs to be reasonably systematic and auditable, and common where the researcher needs to explain the process transparently to a quantitatively minded reader or commissioning body.

**Epistemic stance and claim scope**:
- Hsieh & Shannon (2005) state that content analysis "is not a single method" and that current applications fall into three distinct approaches — conventional, directed, and summative — "the main differences among the approaches are coding schemes, origins of codes, and threats to trustworthiness" [abstract only, Hsieh, H.-F., & Shannon, S. E. (2005). Three Approaches to Qualitative Content Analysis. *Qualitative Health Research*, 15(9), 1277-1288. DOI: 10.1177/1049732305276687]:
  - **Conventional**: codes are derived inductively straight from the data, with no preset coding frame (closest to inductive thematic analysis).
  - **Directed**: starts from existing theory/literature, with preset categories against which the data is coded (verifying or extending an existing theoretical framework).
  - **Summative**: first counts the frequency of keywords/content, then interprets their contextual meaning (combining quantitative counting with qualitative interpretation).
- Mayring's approach emphasizes **deductive category application** and a systematically built codebook/coding rules, and argues that qualitative content analysis can retain some "quantitative" element (frequency, counts of relationships between categories) without losing its grip on contextual meaning [abstract only, Mayring, P. (2022). *Qualitative Content Analysis*. Sage. DOI: 10.4135/9781036231798].
- **Can support**: A systematic distribution description of categories/themes in text; to some degree, frequency/magnitude claims (especially in the summative or Mayring approach, which is more tolerant than reflexive TA of statements like "how many data items mentioned X," though still not statistical inference); theory-driven category verification (directed approach).
- **Cannot support**: A frequency claim unsupported by a codebook or reliability check; deep meaning-making (if the goal is deep interpretation, and not systematic categorization, TA or IPA fits better).

**Data and sample**: The unit is the text corpus; because this method often involves a codebook and possibly a multi-coder reliability check, the sample-size justification can partly rely on the logic of "covering all known categories"; information power or saturation alone is not the only basis.

**Analysis procedure notes**: Build a codebook (category definitions, coding rules, examples) → (common in directed/summative approaches) pilot coding with multiple coders → compute inter-coder reliability → formal coding → analyze category distribution and relationships. **A key difference from reflexive TA**: content analysis (especially the directed and summative approaches) tolerates or even encourages inter-coder reliability checks, which is the opposite of B&C's stance — choosing content analysis over reflexive TA means choosing a different epistemic stance and quality criterion at the same time, and the write-up must be internally consistent; it cannot have it both ways.

**Quality criteria**: Transparency and reproducibility of the codebook; (if used) an inter-coder reliability coefficient (Cohen's kappa for 2 coders, Fleiss's kappa for 3+, or Krippendorff's alpha as a general-purpose choice — see A-6's decision rule); exhaustiveness and mutual exclusivity of categories.

**Reporting standard**: Commonly follows the general qualitative reporting standards COREQ/SRQR; core items to add are the codebook's development process, (if applicable) the inter-coder reliability figures and how they were computed, and whether categories came from theory or from the data.

**Common reviewer critiques and misuses**: The most common misuse is treating "qualitative content analysis" and "thematic analysis" as interchangeable names, when the two have different epistemic assumptions about reliability and frequency claims; a codebook that is not attached or whose development is not described; mixing the three approaches (conventional/directed/summative) without saying which one was used, leaving readers unable to judge the legitimacy of any frequency statements.

**Acceptance and conventions in this kind of venue**: Common with mature convention in education research and nursing/health-communication fields; in HCI/design research, open-ended questionnaires or user-study responses are often given a lightweight content analysis (especially the summative type: counting plus interpretation) as an alternative or supplement to thematic analysis.

**Resources and ethics**: A multi-coder design needs coordinating coder training and a reliability-checking workflow, raising time cost; ethics review requirements are similar to general qualitative research.

**Common combinations**: Often paired with open-ended questionnaires and document analysis (see B-12); frequently used alongside quantitative frequency counts (a natural extension of the summative approach).

**When not to use**: When the goal is deep meaning-making, and not systematic categorization and distribution, use reflexive TA or IPA instead; without the resources to build a codebook or (if that approach was chosen) run a reliability check, yet claiming a rigorous directed or summative content analysis, the claimed method and the actual execution will not match.

**Key sources**:
- Hsieh, H.-F., & Shannon, S. E. (2005). Three Approaches to Qualitative Content Analysis. *Qualitative Health Research*, 15(9), 1277-1288. DOI: 10.1177/1049732305276687 [abstract only]
- Mayring, P. (2022). *Qualitative Content Analysis*. Sage. DOI: 10.4135/9781036231798 [abstract only]

---

### B-8 Focus Groups

**Question shapes it answers**: "How does this group of people jointly construct and negotiate a view on some issue through interactive discussion" — **the core selling point is the group interaction itself**; a focus group is not simply an efficient version of individual interviews with several people at once.

**Epistemic stance and claim scope**:
- Kitzinger (1994) identifies interaction between research participants as "one of the most fundamental" features distinguishing focus groups from one-on-one interviews or questionnaires — a core methodological claim, beyond mere efficiency [abstract only, Kitzinger, J. (1994). The methodology of Focus Groups: the importance of interaction between research participants. *Sociology of Health & Illness*, 16(1), 103-121. DOI: 10.1111/1467-9566.ep11347023].
- **Can support**: Understanding of how an issue is collectively negotiated, and how consensus forms or diverges; insight into how group norms shape how individuals present their views; treating how an individual adjusts their stated view under group pressure as data itself; it is not noise to be filtered out.
- **Cannot support**: Deep disclosure of private personal experience (the group setting itself can suppress certain disclosures — an individual interview fits better for depth); generalizing group opinion distribution from a handful of focus-group sessions; treating each participant's statement as an independent, identically distributed individual opinion (ignoring group-interaction effects is a misuse of the data).

**Data and sample**: The "session," not raw headcount, is the sampling unit; a typical session size is 6–10 people, with the number of sessions set by topic complexity and whether cross-group comparison is needed (e.g., one session per background group); sampling should weigh the trade-off between group homogeneity and heterogeneity (homogeneous groups more easily create a safe atmosphere for discussion, heterogeneous groups more easily spark clashing viewpoints — the two serve different research goals).

**Analysis procedure notes**: Transcripts need to mark speaker identity and interaction features (who interrupted whom, who agreed with whom, silences and turns); the unit of analysis can be an individual utterance or the interaction sequence itself; commonly followed by thematic or content-analysis coding, but the coding should preserve interaction context; breaking the transcript into isolated sentences loses this.

**Quality criteria**: An account of the moderator's skill and role (how discussion was guided without being dominated, how a dominant speaker was managed); whether the effect of group dynamics on the data was explicitly analyzed, and not simply ignored.

**Reporting standard**: COREQ explicitly covers focus groups (its 32-item checklist is titled "for interviews and focus groups").

**Common reviewer critiques and misuses**: The most common misuse is treating a focus-group transcript as a pile of independent individual opinions for thematic analysis, without analyzing the interaction at all — using the form of a focus group without using its core methodological advantage; reviewers commonly ask how the moderator handled power imbalances within the group (e.g., top-down suppression of a view), whether the number of sessions is justified, and whether the group composition (homogeneous/heterogeneous) and its rationale were reported.

**Acceptance and conventions in this kind of venue**: Common in user research and design education (e.g., using classroom small-group discussion as data); when a teacher uses their own class's small-group discussion as focus-group data, the power-relation issue is similar to classroom ethnography (see the cross-method-issues section).

**Resources and ethics**: Needs an experienced moderator's skill — the resource demand centers on personnel more than duration; ethics review needs to address group confidentiality, since it cannot guarantee, the way an individual interview can, that other group members will not disclose information outside the session.

**Common combinations**: Often complementary with individual interviews (a focus group sees collective negotiation, an individual interview adds personal depth); paired with content analysis or thematic analysis for coding.

**When not to use**: When the topic involves highly private or stigmatized experience (e.g., trauma, sexual-minority experience in a non-safe space), the group setting may suppress genuine disclosure — use individual interviews instead; if the only goal is to save time by "interviewing several people at once" with no intent to analyze the interaction itself, this is in substance a misuse of the method.

**Key sources**:
- Kitzinger, J. (1994). The methodology of Focus Groups. *Sociology of Health & Illness*, 16(1), 103-121. DOI: 10.1111/1467-9566.ep11347023 [abstract only]
- Krueger, R. A., & Casey, M. A. (2015). *Focus Groups: A Practical Guide for Applied Research* (5th ed.). Sage. [abstract only; bibliographic record confirmed via multiple citations]

---


### B-9 Think-Aloud Protocol and Contextual Inquiry

**Question shapes it answers**: "What does a user's cognitive process/decision-making look like while performing a task in the moment" (think-aloud); "how does a user actually do this in a real work/life context, and how does the surrounding environment shape their approach" (contextual inquiry) — both are **task-oriented, context-embedded** questions; retrospective attitude/opinion questions are a different category.

**Epistemic stance and claim scope**:
- Think-aloud's methodological foundation is Ericsson & Simon's protocol-analysis theory of verbal reporting: "Giving a verbal protocol should not affect the cognitive processes involved in task performance as there is not an indication that concurrent verbalization changes either the sequence or the content of the participants' thoughts" (Atman et al. 2008, p.7, citing Ericsson & Simon 1993) [full text, secondhand quotation, citing Ericsson & Simon 1993's position] — this assumption is itself a contested methodological premise that needs to be stated; it is not a self-evident fact; van Someren, Barnard & Sandberg (cited in Dorst & Cross 2001) provide a further practical operating guide [full text].
- Contextual inquiry (part of Beyer & Holtzblatt's Contextual Design) emphasizes observing **at the user's actual work site** — a lab setting is not used — combining observation and interviewing, with the inquirer taking an "apprentice" role, asking the user to teach how the work is actually done.
- **Can support**: A description of the cognitive/operational process during task execution; diagnosis of interface/tool problem points; the logic of practice in a real usage context (contextual inquiry).
- **Cannot support**: Users' general attitudes or preferences (think-aloud focuses on the current task; it is not an attitude survey); assuming concurrent verbalization has "zero effect" on task performance without testing it is itself a methodological simplification; generalizing across contexts (contextual-inquiry data is deeply embedded in a specific site).

**Data and sample**: The "task session" is the unit; typical scale is single digits to the low teens (reflecting the diminishing-returns effect for finding usability problems — 5–8 people typically find most major problems; this is a usability-testing rule of thumb, not a strict statistical inference); contextual inquiry usually needs deep inquiry at a small number (3–10) of real work sites, with the sample-size justification resting on site diversity; headcount is not the basis.

**Analysis procedure notes**: Think-aloud — verbatim transcription of the verbal report, segmented to match task steps, coded into cognitive/operational categories (hesitation, error correction, strategy switching); contextual inquiry — field notes plus a joint review with the user afterward to confirm the researcher's understanding ("interpretation checking" is a built-in step, similar to member checking).

**Quality criteria**: Whether verbalization genuinely did not interfere with task performance (this risk needs to be addressed — for example, by comparing task-completion time with and without verbalization); whether contextual inquiry's interpretation-checking step was actually carried out and documented.

**Reporting standard**: No dedicated checklist; commonly expected to report task design, the verbalization instructions given, and the transcription and coding method.

**Common reviewer critiques and misuses**: A common critique is using think-aloud as a substitute for a general interview (retrospective probing after the fact, and not concurrent verbalization — methodologically this is no longer think-aloud but retrospective verbal report, with a different evidentiary strength); contextual inquiry done as mere "shadowing observation" with no collaborative process of meaning confirmation with the user.

**Acceptance and conventions in this kind of venue**: Common in IUI/HCII/DIS system-evaluation settings, often paired with creative-tool evaluation; also fits when studying students' design-process cognition in design education.

**Resources and ethics**: Moderate time cost (needs to be done one-on-one); contextual inquiry at a user's workplace needs to address workplace privacy and employer consent.

**Common combinations**: Often paired with usability scales (SUS, TLX); contextual inquiry is often a lead-in study for a later design intervention.

**When not to use**: When a task is too complex or demands high concentration such that verbalization clearly interferes with performance, use a retrospective think-aloud instead (e.g., paired with video playback); when the goal is to understand attitude, and not operational process, neither method fits.

**Key sources**:
- Ericsson, K. A., & Simon, H. A. (1993). *Protocol Analysis: Verbal Reports as Data*. MIT Press. [full text, secondhand quotation]
- Beyer, H., & Holtzblatt, K. (1998). *Contextual Design: Defining Customer-Centered Systems*. Morgan Kaufmann. [abstract only; the authors and topic are confirmed via a CHI'99 course record, DOI 10.1145/632780.632801, which is not the book itself]

---

### B-10 Diary Studies and Experience Sampling Method

**Question shapes it answers**: "How does this experience/behavior/emotion change over time, and under what circumstances does it occur" — solving the memory-distortion problem of retrospective interviews/questionnaires, capturing "life as it is being lived" — a reconstructed narrative after the fact is not the aim [abstract only, the title itself states this stance, Bolger, N., Davis, A., & Rafaeli, E. (2003). Diary Methods: Capturing Life as it is Lived. *Annual Review of Psychology*, 54, 579-616. DOI: 10.1146/annurev.psych.54.101601.145030].

**Epistemic stance and claim scope**:
- **Can support**: Patterns of change in experience/behavior over time; the covariation of situational triggers and experience (with signal-contingent experience sampling, even some degree of time-lagged association analysis); a description closer to the moment than a retrospective interview.
- **Cannot support**: Causal claims (unless paired with an experimental manipulation); if participants choose when to record (this is event-contingent sampling; signal-contingent sampling is not used), there is a selective-reporting bias, and the data cannot claim to cover all relevant experience.
- There is precedent in Chinese-language design-education literature: a 2025 study on designers collaborating with generative AI used a diary-study method, describing its strength as being able "to closely examine the research subject's behavior, emotion, and thought process in daily or specific contexts," citing Janssens et al. (2018) as its methodological basis [full text, cited as a Chinese-language precedent for design journals] — useful as a precedent when submitting to a Chinese-language design journal.

**Data and sample**: Jointly determined by "number of recording time points" and "number of participants"; the experience sampling method (ESM) commonly triggers several times a day (e.g., 5–8 signals), over 1-2 weeks; diary studies might instead be a longer, once-daily reflective record over weeks to months. Sample-size justification can still invoke information power or saturation logic, with the added requirement of stating whether the recording period is long enough to capture the target experience's range of variation (e.g., a study of a semester-long learning experience should cover at least a full semester's key points).

**Analysis procedure notes**: Start with a descriptive summary of the time series/situational distribution, then move to qualitative coding (thematic or content analysis); if the data structure allows, a multilevel growth model can follow (a quantitative path — structured, scored diary data can connect to this).

**Quality criteria**: Compliance rate (the proportion of records participants actually completed — too low undermines representativeness); whether the recording method genuinely stays close to "the moment" (delayed recording degrades into retrospective data, losing the method's main advantage).

**Reporting standard**: No dedicated formal checklist; core items to state are the recording frequency and time window, the compliance-rate figure, and the trigger method (signal-, event-, or fixed-interval-based).

**Common reviewer critiques and misuses**: The most common critique is a low compliance rate that goes unreported or unaddressed (heavy missing records systematically bias toward the kind of experience people remember to report); treating delayed, backfilled multi-day entries as a "diary," which has in substance degraded into retrospective data.

**Acceptance and conventions in this kind of venue**: Growing use in design education and learning-process research for tracking long-term learning/creative processes (see the Chinese-language precedent above); ESM is common in HCI for context-sensitive research on emotion/usage behavior.

**Resources and ethics**: High demand for sustained participant cooperation, with attrition a common risk — incentives and reminder mechanisms need planning at the design stage; ongoing disruption to participants' daily lives needs specific attention in ethics review regarding burden management.

**Common combinations**: Often paired with a follow-up retrospective interview (using diary content as a prompt for further questions, combining in-the-moment capture with reflective meaning-making); connects to thematic or content analysis for coding.

**When not to use**: When the research question only concerns a static description of experience at a single point in time, the longitudinal design of a diary method is unnecessary; when participant compliance is expected to be very low (e.g., high-burden occupations, low-motivation participants) with no way to provide adequate incentive, the attrition risk is too high and a retrospective interview is more practical.

**Key sources**:
- Bolger, N., Davis, A., & Rafaeli, E. (2003). Diary Methods: Capturing Life as it is Lived. *Annual Review of Psychology*, 54, 579-616. DOI: 10.1146/annurev.psych.54.101601.145030 [abstract only]
- Hektner, J. M., Schmidt, J. A., & Csikszentmihalyi, M. (2007). *Experience Sampling Method: Measuring the Quality of Everyday Life*. Sage. DOI: 10.4135/9781412984201 [abstract only]
- A 2025 Chinese-language design-journal study on designer–generative-AI collaboration [full text, cited for its diary-study methodology section]

---

### B-11 Visual / Artefact Analysis (systematic analysis of student work, images, and exhibited works)

**Question shapes it answers**: "What does this visual work/image convey at the level of form, content, and context, and how can it be systematically described and compared" — suited to analyzing student portfolios, images of the creative process, and exhibited work in design education. This differs from the computational-aesthetics tools used elsewhere in a research pipeline (e.g., image-distance or embedding-based metrics): **this method is the researcher's own qualitative interpretation; it is not a computational distance metric**.

**Epistemic stance and claim scope**:
- Rose's *Visual Methodologies* argues that image analysis should address meaning at three levels at once: the site of production (how the work was made), the image itself (composition, form), and the site of audiencing/circulation (how the work is viewed and interpreted) — missing any of the three unbalances the analysis [abstract only, Rose, G. (2016). *Visual Methodologies: An Introduction to Researching with Visual Materials*. Sage; bibliographic record confirmed via a book review, DOI 10.29173/cjs18626].
- **Can support**: Systematic, auditable qualitative description of a work's or portfolio's form and meaning; systematizing design education's judgment of student creative process and quality (e.g., turning a teacher's "taste judgment" into an accountable analytical framework).
- **Cannot support**: An "objective" aesthetic-quality ranking detached from the interpretive framework (for that kind of claim, use computational quality/distance-metric tools instead; the two methods work as complementary evidence, and neither substitutes for the other); generalizing from a single work's analysis to "how this kind of creation generally is."

**Data and sample**: The unit is the "number of works"; sample-size justification depends on the portfolio's completeness and the analytic purpose (a descriptive single-case analysis can use a handful of works; a cross-form generalization needs more works and should consider saturation/information power).

**Analysis procedure notes**: An analytical framework needs to be established first (form, content, and context as three levels, or dimensions custom-defined by the research question); it's recommended to triangulate with the creator's own stated intent (a creative statement, or a verbal account given in the teaching setting) so the researcher's interpretation does not entirely replace the creator's intent; can be paired with thematic or content analysis for systematic coding.

**Quality criteria**: Whether the analytical framework's theoretical basis is stated clearly; whether the researcher's interpretive position (whether they are the instructor grading the work) is disclosed — this is a core reflexivity issue when a teacher-researcher analyzes their own students' work (see the cross-method-issues section).

**Reporting standard**: No dedicated formal checklist; recommend stating at minimum the source of the analytical framework, the criteria for selecting works, and the relationship between the researcher and the analyzed work/creator.

**Common reviewer critiques and misuses**: The most common critique is a researcher who is both the grading instructor and the analyst without addressing how this dual role was handled (raising suspicion that the analysis is just a repackaging of the grading rationale); an analytical framework with no stated source, looking chosen after the fact to fit a predetermined conclusion; a small selection of works treated as representative of an entire class or term's student output.

**Acceptance and conventions in this kind of venue**: Art and design education journals have some convention for artefact analysis, but the boundary with a teacher's own teaching reflection or action research can be blurry, and reviewers may ask for a clearer methodological framework, and not a teaching-reflection-style description.

**Resources and ethics**: Needs students' informed consent for their work to be used in research and potentially displayed publicly; under a teacher's dual role, the consent procedure needs attention to the power imbalance (consent should not be sought before grades are finalized — see the cross-method-issues section).

**Common combinations**: Often paired with open-ended questionnaires/interviews (comparing the creator's stated intent against the analysis of the work itself); complementary with computational image-metric tools; it does not replace them.

**When not to use**: When the research question is fundamentally "is there a statistically systematic difference between this batch of generated/created images and another batch," a computational metric should be the primary evidence, with qualitative artefact analysis as a supporting explanation; it should not be the main evidence. Writing impressionistic descriptions like "this work presents..." with no analytical framework established first risks being read as a teaching anecdote; it does not read as method.

**Key sources**:
- Rose, G. (2016). *Visual Methodologies: An Introduction to Researching with Visual Materials* (4th ed.). Sage. [abstract only]

---

### B-12 Open-Ended Written Questionnaires (often mislabeled "interviews")

**Question shapes it answers**: "What did a group of people, each in writing, state about some issue" — this is the **most commonly mislabeled method** in this set of cards: many manuscripts write open-ended questionnaire responses up as "interview data," but the two differ systematically in what kind of data they produce and what claims they can support.

**Epistemic stance and claim scope (what it can and cannot support)**:
- Braun, Clarke, Boulton, Davey & McEvoy (2021) argue that online open-ended questionnaires can be a rigorous qualitative research tool, but **explicitly not a substitute for interviews** — the two produce data of a different character: questionnaire responses are typically shorter, lack the depth and detail an interviewer's probing brings out, have no non-verbal cues, and lack the real-time negotiation of meaning that happens in an interview; but a questionnaire's advantage is reaching geographically dispersed or reluctant-to-be-interviewed participants at large scale and low cost, and it removes the social-desirability pressure created by an interviewer's presence [abstract only, Braun, V., Clarke, V., Boulton, E., Davey, L., & McEvoy, C. (2021). The online survey as a qualitative research tool. *International Journal of Social Research Methodology*, 24(6), 641-654. DOI: 10.1080/13645579.2020.1805550].
- **Can support**: A breadth scan of an issue (how many people, in what kind of wording, expressed which positions/fragments of experience); suited to content analysis or lightweight thematic analysis; can serve as a lead-in or supplement to deeper interviews (using the questionnaire to screen who to interview further).
- **Cannot support**: The fine texture of deep personal experience (there is no depth without follow-up probing — this is a structural limit; it is not a matter of poor execution); data on the process of negotiating meaning (meaning in an interview is generated interactively between researcher and participant; a questionnaire response is a one-way, one-time written product); calling this "an interview" when participants in fact never interacted with the researcher — **this is the single most common methodological dishonesty reviewers catch**, and the label must accurately reflect how the data was collected.

**Data and sample**: Can reach a large scale (relative to the labor intensity of interviewing, a questionnaire can cheaply scale up the sample), but **response depth and sample size are often inversely related** — individual responses in a large-scale open-ended questionnaire tend to be very short, so the sample-size justification should shift toward "the diversity of viewpoints covered," and not raw headcount; report the attrition/non-completion rate (open items usually have higher attrition than closed items).

**Analysis procedure notes**: Because responses are typically short and lack context, a lightweight content analysis (conventional or summative) or thematic analysis fits; stay modest about the "depth" of any theme — it is not appropriate to claim the fine-grained interpretive detail of a deep interview transcript from one or two sentences of written response.

**Quality criteria**: Similar to other qualitative methods, but with the extra need to state whether the wording was leading, the distribution of response length (whether and how very short responses were handled), and the logic of pairing open items with other item types (e.g., closed-form scales).

**Reporting standard**: Can borrow general qualitative reporting standards (COREQ was originally designed for interviews and focus groups; if forced onto questionnaire data, some items will not apply, such as "was the interview audio-recorded" — state that the item does not apply, and do not force an answer).

**Common reviewer critiques and misuses**:
- **The single most central misuse is a mislabeled method**: writing open-ended questionnaire responses up directly as "semi-structured interviews" — this is a methodological-integrity problem, beyond a mere wording slip; once a reviewer notices that the data-collection method (no researcher present, no follow-up probing) does not match the claimed method (interview), they will typically demand major revision or directly question the study's overall integrity.
- Common questions: whether the response depth can support the claimed analytic fine-grainedness (e.g., claiming a full six-phase reflexive-TA coding on data that is 1-2 sentences per item); the rationale for choosing a questionnaire over an interview (pure convenience vs. a methodological reason such as reaching a dispersed population or reducing social-desirability pressure).

**Acceptance and conventions in this kind of venue**: Common in education research and large-scale user surveys; given class size and time constraints, design-education research commonly relies on open-ended questionnaires; individual interviews are less feasible at that scale. This is entirely defensible methodologically, **provided it is honestly named a questionnaire, and not an interview, and the claimed analytic depth matches the nature of the data**.

**Resources and ethics**: Far lower resource demand than interviews (no scheduling or transcription needed); still needs informed consent and de-identification in ethics review; when a teacher distributes a questionnaire to their own students, the power-relation issue is the same as in interviews (see the cross-method-issues section) — especially if the questionnaire is distributed mid-semester or before grades are finalized, participation's freedom will be questioned.

**Common combinations**: Often paired with closed-form scale items (a mixed design where the scale gives descriptive statistics and the open item gives a lightweight qualitative "why"); can serve as a lead-in screening tool for deep interviews or focus groups.

**When not to use**: When the research question needs the fine texture of deep personal experience, the process of negotiating meaning, or a complex process that only follow-up probing can clarify, an open-ended questionnaire structurally cannot deliver this — use interviews instead; if questionnaire data has already been collected but there is a temptation to package it at interview-level depth, the honest move is to downgrade the claimed level; blurring how the data was actually collected when reporting the method is not acceptable.

**Key sources**:
- Braun, V., Clarke, V., Boulton, E., Davey, L., & McEvoy, C. (2021). The online survey as a qualitative research tool. *International Journal of Social Research Methodology*, 24(6), 641-654. DOI: 10.1080/13645579.2020.1805550 [abstract only, DOI and authors confirmed via Crossref]

---


## Group B cross-method issues

### Sample-size justification: the paradigm shift from "saturation" to "information power"

- **Saturation** is traditionally the most common sample-size rationale in qualitative research, but its operational definition has long been inconsistent. Guest, Bunce & Johnson (2006) tested this concept empirically against 60 in-depth interviews from a West African HIV-prevention study, finding that "saturation occurred within the first twelve interviews," and that "after twelve interviews, we had created 92% ... of the total [codebook]" [abstract only — read via a search-engine-indexed excerpt of the original text; the full paper was not read, Guest, G., Bunce, A., & Johnson, L. (2006). How Many Interviews Are Enough? *Field Methods*, 18(1), 59-82. DOI: 10.1177/1525822X05279903] — but they stress that this specific number **cannot simply be applied to other studies**: the saturation point depends heavily on sample homogeneity and how narrowly the study's goal is defined, and the paper's own title points to the core problem: the concept of saturation is useful conceptually, but offers little practical guidance for **estimating** the necessary sample size **before** data collection (from the abstract).
- Malterud, Siersma & Guassora (2016) go further and propose **information power** to replace saturation: their abstract states plainly that "the more information the sample holds, relevant for the actual study, the lower amount of participants is needed," with information power determined by five dimensions: (a) the aim of the study, (b) sample specificity, (c) use of established theory, (d) quality of dialogue, and (e) analysis strategy [abstract only, full abstract read, Malterud et al. 2016, DOI: 10.1177/1049732315617444]. The advantage of this framework is that it moves the sample-size decision **forward to the design stage** (a qualitative parallel to the quantitative point that "power analysis only happens at the design stage" elsewhere in this document); it does not rationalize an arbitrary stopping point after the fact with "we reached saturation."
- Hennink & Kaiser (2022) conducted a systematic review of 23 empirical studies that tested saturation, and their abstract gives a clear convergent finding: "Studies using empirical data reached saturation within a narrow range of interviews [9-17] or focus group discussions [4-8], particularly those with relatively homogenous study populations and narrowly defined objectives," and they conclude that "studies converged on a relatively consistent sample size for saturation for commonly used qualitative research methods," while cautioning that "these findings only apply to specific types of studies (e.g. those with a homogenous study population)" — cross-national studies, meta-themes, or "meaning saturation" of codes (as opposed to simple "code saturation") need larger samples [abstract only, full abstract read (this is an open-access paper, confirmed CC-BY-NC-ND), Hennink, M., & Kaiser, B. N. (2022). Sample sizes for saturation in qualitative research: A systematic review of empirical tests. *Social Science & Medicine*, 292, 114523. DOI: 10.1016/j.socscimed.2021.114523]. **A concrete reference point**: for an interview study with a homogeneous sample (e.g., students in the same course/cohort) and a clearly defined goal, 9–17 people is an empirically grounded reference range, though the manuscript should state this is a reference point; it is not a mechanical rule.
- Braun & Clarke (2019/2021, see B-1) critique the concept of saturation itself from a **methodological-consistency** angle: for a method like reflexive TA, which holds that "meaning is not fixed in the data and is actively constructed by the researcher," the saturation logic of "no new information is being produced" presupposes an external, finite pool of information waiting to be "used up" — a presupposition that contradicts reflexive TA's epistemic stance. **⇒ Decision rule**: for reflexive TA, use information power or a design-based argument; saturation language is not used here. For grounded theory, saturation is a built-in stopping criterion of theoretical sampling and belongs to a different context; it should not be confused with the above (see B-2); for content analysis / coding-reliability approaches, using saturation to justify sample size is a defensible, traditional practice.

### Trustworthiness criteria: Lincoln & Guba's four criteria vs. Tracy's "big-tent" eight criteria

- **Lincoln & Guba (1985)** propose four trustworthiness criteria for qualitative research, as a qualitative counterpart to quantitative validity/reliability concepts: credibility (parallel to internal validity), transferability (parallel to external validity/generalization), dependability (parallel to reliability), and confirmability (parallel to objectivity). This framework remains the most widely cited starting point for qualitative quality, though it is often criticized as too closely mimicking quantitative vocabulary and not fitting well with some qualitative paradigms (constructionist, critical). **The original text was not located for this port**; this paragraph reflects broad scholarly consensus, [abstract only] — check the exact wording directly in Lincoln, Y. S., & Guba, E. G. (1985). *Naturalistic Inquiry*. Sage, when needed.
- **Tracy (2010)** proposes eight "big-tent" criteria, designed specifically to be **shared across different qualitative paradigms** without binding to a single epistemic stance: worthy topic, rich rigor, sincerity, credibility, resonance, significant contribution, ethics, and meaningful coherence [abstract only, full abstract read, Tracy, S. J. (2010). Qualitative Quality: Eight "Big-Tent" Criteria for Excellent Qualitative Research. *Qualitative Inquiry*, 16(10), 837-851. DOI: 10.1177/1077800410383121]. This framework is more flexible for a manuscript spanning different paradigms (reflexive TA, grounded theory, case study, and so on), and works well as a **high-level self-check before submission** — but it cannot replace the specific quality criteria required by the method itself (e.g., reflexive TA still needs to address coding transparency; Tracy's eight items are a higher-level overall assessment; they do not function as an item-by-item checklist).
- **Decision rule**: if the venue or reviewer explicitly uses positivist vocabulary (reliability, validity) to evaluate qualitative work, Lincoln & Guba's corresponding terms communicate more easily; if the venue is more receptive to paradigm plurality in qualitative research (such as DIS or humanistic HCI), Tracy's eight-item framework fits contemporary qualitative research's self-understanding better and does not force an ill-fitting epistemic stance.

**Inter-coder/inter-rater reliability — there are two sides, and B&C's position is not the only one**: the B-1 card already covers Braun & Clarke's explicit rejection of coder reliability, but this **is not the only position in the qualitative research community**, and a manuscript citing the opposing view to justify skipping reliability checks should honestly acknowledge this is taking a contested side; it is not the single "correct" practice. O'Connor & Joffe (2020) argue directly for the value of inter-coder reliability (ICR): their abstract states that "ICR is a somewhat controversial topic in the qualitative research community, with some arguing that it is an inappropriate or unnecessary step within the goals of qualitative analysis," but they argue that "ICR assessment can yield numerous benefits ..., which include improving the systematicity, communicability, and transparency of the coding process; promoting reflexivity and dialogue within research teams; and helping convince diverse audiences of the trustworthiness of the analysis" [abstract only, full abstract read (open access, confirmed gold OA), O'Connor, C., & Joffe, H. (2020). Intercoder Reliability in Qualitative Research: Debates and Practical Guidelines. *International Journal of Qualitative Methods*, 19. DOI: 10.1177/1609406919899220]. **⇒ Additional decision rule**: choosing whether to run an inter-coder reliability check is essentially **picking a side between two epistemically supported positions**; it is not a matter of "more rigorous" versus "sloppier." When using a multi-person team, needing to communicate with quantitatively minded collaborators or reviewers, or needing coder training to be auditable, O'Connor & Joffe's practical argument fits better; when doing reflexive TA with a single researcher, where meaning-making is the emphasis and "finding the correct code" is not the goal, B&C's position is more internally consistent. Whichever is chosen, **the methods section should state why that side was chosen**; leaving it ambiguous is not acceptable.

### Reflexivity and the teacher-researcher power relation

- Levitt et al.'s (2018) JARS-Qual reporting standard explicitly lists disclosing the researcher's own stance as a mechanism that enhances trustworthiness: "by recognizing their own standpoint and positionality in relation to the topic of the research and the population under study ..., researchers enhance the credibility of their claims by simultaneously pointing out their contextual embeddedness (or lack thereof) and its role in the interpretative process" [full text, Levitt et al. 2018, from the "An Ethic of Transparency" section; the local copy is an author's masked manuscript, using internal page numbering; it does not carry the published journal's pagination — the manuscript's page is cited by section name, and no fabricated journal page number is used].
- Being **both the instructor and the researcher** — studying one's own course or one's own students (interviews, questionnaires, artefact analysis, and diary studies can all be affected) — carries a structural dual-role problem:
  1. **Freedom of consent**: students invited while grades are not yet finalized, still subject to the instructor's grading authority, find it hard to freely decline or answer honestly; common remedies include issuing formal invitations only after grades are settled, ensuring that declining does not affect grades already given, and having a third party (not the instructor) collect data or at least collect informed consent.
  2. **Systematic bias in responses**: students may present a more positive or more teacher-pleasing version of their views in interviews/questionnaires/diaries because they hope to appear favorable to the instructor — this is a structural effect of the social situation, not simply a matter of honesty, and the reflexivity statement needs to specify concretely how this was recognized and reduced (e.g., anonymized codes with no names attached, a teaching assistant or third party collecting raw data before it reaches the researcher de-identified, and telling students explicitly that the instructor cannot see responses linked to a specific person).
  3. **The dual role in artefact analysis** (especially relevant to B-11): if the teacher is both the grader of student work and the research analyst, the boundary between the analysis and the grading rationale needs to be stated explicitly, or reviewers will suspect the analysis is just a repackaging of the grading logic after the fact.
- This power-relation disclosure applies **not only to methods labeled "interview"** — whenever data comes from one's own class, methods B-1, B-8, B-10, B-11, and B-12 (thematic analysis, focus groups, diaries, artefact analysis, open-ended questionnaires) all need the same disclosure; it is not something to address only when the word "interview" appears.

### Translating cross-language quotations

- When participants speak Chinese and a paper is published in English, the manuscript **must** state: who translated it, whether it was one-way or back-translated and checked, and whether the original Chinese text appears in the manuscript.
- Common practice: present the English translation in the main text, with the Chinese original in an appendix or footnote, and briefly state in the methods section the translator's identity (the researcher, a professional translator, or bilingual cross-checking) and the translation approach (favoring literal translation to preserve semantic detail, or favoring free translation to ensure the English reader's comprehension — each is a trade-off that needs to be stated).
- **⚠️ This is a separate matter from the Chinese back-translation used elsewhere for the author's own sign-off on an English manuscript, and the two cannot substitute for each other**: that kind of back-translation is a quality-control step for the author's own approval of the full English text; the quotation-translation procedure discussed here is part of the qualitative-methods reporting itself, answering "how can a reader trust that this English quotation faithfully reflects what the participant actually said." If a manuscript only does one of these but leaves the reader thinking it also covers the other (or vice versa), reviewers will flag the methods section as unclear.
- **No dedicated reporting standard** for cross-language quotation translation could be found specific to the design/HCI field (as distinct from the back-translation norms of translation-studies research); it's recommended to at minimum meet COREQ/SRQR's general transparency requirements and address this explicitly in a paragraph of the methods section; leaving it for a reviewer to ask about is not sufficient.

### LLM-assisted qualitative coding: current state and reviewer expectations

- A full pipeline and reviewer-expectations checklist for this (transcription → an initial thematic scan with a language model → a hierarchical codebook tool → LLM-assisted coding → dual-rater reliability) is not repeated here in detail; the seven items an emerging CHI-style human-AI hybrid coding protocol asks for are: (1) human review, (2) inter-rater reliability (kappa ≥ .61 as a starting bar), (3) an auditable coding trail, (4) an explicit, iterative "codebook rewrite" step, (5) an accept/reject ledger with reasons, (6) line-level evidence binding (preventing the LLM from generating excerpts/codes not present in the original text), and (7) reproducible saved prompts/settings. This card only adds **methodological positioning and a read of the current state**.
- Current state: LLM-assisted qualitative coding is still a **fast-moving field whose review standards have not stabilized**. Recent methodological-discussion literature (e.g., a preprint updating "The Future of Coding" for generative-LLM qualitative coding, DOI: 10.31235/osf.io/wg82k) and governance/validity-oriented discussion (e.g., a paper on "Large Language Models in Qualitative Research: Governance, Validity, and the Limits of Computational Assistance," DOI: 10.2139/ssrn.6577019) show the field is still debating LLM coding's validity basis and governance framework, with no single agreed standard yet [abstract only, both papers read only at the Crossref bibliographic/title level, full argumentative content **not found**].
- **Practical reminders**:
  1. Whenever an LLM (including a Claude-family model) is used to assist an initial thematic scan or coding, the methods section must explicitly disclose the model, version, and prompt-design logic — this overlaps with, but cannot substitute for, the generative-AI-use disclosure required at submission; the AI-disclosure statement is a formalized declaration, while the methods-section account is substantive methodological transparency, and reviewers check the two separately.
  2. **The epistemic tension between reflexive TA and LLM coding**: reflexive TA holds that meaning is actively constructed by the researcher and rejects the assumption of a single "correct" coding; using an LLM to generate an initial coding for the researcher to "confirm" needs to honestly acknowledge that this is, in practice, closer to a coding-reliability or codebook approach (an externally generated coding proposal exists beforehand); it is not a purely organic reflexive coding evolution — when mixing the two, the methodological position needs to be stated clearly; claiming both the efficiency of LLM assistance and reflexive TA's epistemic exemption from reliability checks at once is not defensible.
  3. Review expectations are still moving quickly; **re-check the target journal's LLM-assisted qualitative research policy from the last year before every submission** (some journals now require a reproducible prompt record for every AI-assisted step, others say nothing and leave it to reviewer discretion) — do not assume the previous submission's standard still holds.

---

Sources: see the key-sources list in each card.


## Group C: Mixed methods, design research, and educational research design

> Scope: mixed methods designs, design-based research (DBR), action research, Design Research Methodology (DRM) and sampling in design research, participatory design / co-design workshops, the Delphi method, HCI user-research venue choices (lab/field/in-the-wild), and systematic and scoping reviews plus method mapping. Also includes a "Cross-method issue: choosing a method for a topic" section.

---

### C-1 Mixed Methods Designs

**Name**: Mixed Methods Research. Core designs: Convergent Design, Explanatory Sequential Design, Exploratory Sequential Design; advanced frameworks include embedded/intervention, multistage, case-study, and participatory designs. Category: cross-epistemology research-design methodology.

**What questions it can answer**: questions that need to know both "is there a difference, and how large" and "why, how, and how it is experienced by the people involved"; or that need to explore constructs/item pools before validating them at scale; or that need quantitative and qualitative findings to explain and cross-check each other.

**Epistemological stance and scope of claims**: mixed methods is a pragmatist methodological choice. The decision to mix is driven by the research question itself; it does not require a prior philosophical commitment. It **can support**: an integrated judgment (meta-inference) that qualitative and quantitative results "agree" or "disagree"; mechanistic explanation of quantitative findings; scaled corroboration of qualitative findings. It **cannot support**: simply adding a small qualitative sample to a large quantitative sample to get one bigger sample; nor can the reliability/validity evidence for one strand paper override the other strand's methodological weaknesses. Fetters, Curry, and Creswell (2013) define integration explicitly at three levels (design, methods, and interpretation/reporting) — a structured concept, distinct from simply stapling "two reports" together:
> "This article describes integration principles and practices at three levels in mixed methods research and provides illustrative examples. Integration at the study design level occurs through three basic mixed method designs—exploratory sequential, explanatory sequential, and convergent—and through four advanced frameworks—multistage, intervention, case study, and participatory."
(Fetters, Curry, & Creswell, 2013, *Health Services Research* 48(6pt2), doi:10.1111/1475-6773.12117, p.1 (abstract) [full text, web])

**Data and sample**: the qualitative and quantitative strands each justify their own sample logic independently (qualitative = saturation/case-selection logic, quantitative = power analysis); mixing does not lower either strand's sampling requirements. In sequential designs, results from the earlier phase commonly drive sampling in the later phase (e.g., an exploratory sequential design uses qualitative work first to build survey items, then validates them with a quantitative sample).

**Analytic procedure**:
- Convergent: qualitative and quantitative data are collected in parallel, analyzed separately, then compared/contrasted at the interpretation stage.
- Explanatory sequential: quantitative results come first, and qualitative work explains outliers, extreme groups, or unexpected findings afterward.
- Exploratory sequential: qualitative work first explores constructs, which are then used to build an instrument (survey, intervention), followed by quantitative validation.
- Integration techniques (Fetters et al., 2013): at the methods level, *connecting* (one strand's data links to the other through sampling), *building* (one strand's results shape the other strand's data collection), *merging* (the two strands are combined and compared during analysis), and *embedding* (linking strands across multiple time points); at the interpretation/reporting level, narrative integration, data transformation (e.g., quantitizing qualitative themes), and **joint displays**.
Levitt et al. (2018), the APA JARS mixed-methods reporting module, define the joint display as the central tool for presenting integration:
> "Authors: In mixed methods research, the findings section... mixed methods analysis through 'joint display' tables or graphs that array in qualitative results (e.g., themes) against the quantitative results (e.g., categorical or continuous data). This enables researchers to directly compare results or to see how results from the quantitative and qualitative strands."
(Levitt et al., 2018, *American Psychologist*, 73(1), 26–46; local library [full text])

**Quality criteria**: O'Cathain, Murphy, and Nicholl (2008) proposed GRAMMS (Good Reporting of A Mixed Methods Study). Their own study of published mixed-methods work found that most did not actually integrate:
> "Researchers mainly ignored the mixed methods design and described only the separate components of a study. There was a lack of justification for, and transparency of, the mixed methods design... Judgements about integration could rarely be made due to the absence of an attempt at integration of data and findings from different components within a study."
(O'Cathain, Murphy, & Nicholl, 2008, *Journal of Health Services Research & Policy* 13(2), 92–98, doi:10.1258/jhsrp.2007.007074, abstract [full text, web, abstract via Crossref API])
GRAMMS's six reporting points, per the equator-network entry ([abstract only] — the full six-item list was not verified verbatim against the original; only the entry's existence and title were confirmed): whether the rationale for using mixed methods is stated, the design's name and rationale, how each strand was conducted, how the samples were integrated, how each strand's limitations affected inference, and the degree of integration achieved. The core criterion is whether integration actually happened; the quality of each separate report does not settle that question.

**Reporting standards**: GRAMMS (O'Cathain et al., 2008); the APA JARS-Mixed Methods module (Levitt et al., 2018); MMARS (the Mixed Methods Article Reporting Standards table in the same source).

**Common reviewer objections and misuses**: "this is just two separate studies stapled together" (see the criteria below); applying quantitative sample-size logic to qualitative samples ("too small"); overgeneralizing from a qualitative case despite a significant quantitative result; no joint display or any integrative analysis, with the two strands simply discussed separately; a sequential design that never explains how the later phase's sampling or instrument actually derived from the earlier phase's results.

**🔴 When mixed methods is only "two studies stapled together" (criteria)**:
1. No integrative analysis — no joint display, no narrative integration, no data transformation; the two strands are reported and discussed separately.
2. Independent sampling — in a sequential design, the later phase's sample is not actually derived from the earlier phase's findings.
3. Independent research questions — the quantitative and qualitative questions could be split into two unrelated papers; the "mixed methods" label exists only to look methodologically diverse.
4. No meta-inference — the conclusion never addresses whether the two strands agree, or what disagreement means.
O'Cathain et al.'s (2008) empirical finding is itself the source of this criterion: most of the "mixed methods studies" they reviewed fell into exactly this trap (see the quote above).

**Acceptance and conventions in the venues above**: mixed methods is common at DIS and IUI (quantitative system metrics plus qualitative interviews explaining "why"; the author's statistics playbook, a separate document outside this kit). Education and health journals often require a GRAMMS or MMARS checklist directly. Design research venues (Design Studies) use looser terminology for design-level mixed-methods choices; Cash et al. (2022) note that the design-research literature is highly inconsistent even in its sampling and method vocabulary (see card 4).

**Resources and ethics**: the two strands may have different ethics requirements (e.g., a quantitative survey may be exempt while qualitative interviews need IRB review); time and staffing costs run higher than a single-method study, especially for sequential designs, which cannot run in parallel.

**Common combinations**: P-C (creative-tool evaluation) = standard scales (CSI/SUS) plus qualitative interviews; combining P-D (qualitative) and P-A (quantitative experiment) should follow GRAMMS; education-intervention research commonly uses an embedded design of "quantitative pre/post plus qualitative process interviews."

**When not to use it**: when the research question is fully answerable with a single kind of data; when there is no time or staff to actually integrate the two strands (better to run one method honestly than to half-run two); when epistemological commitments conflict so sharply that they cannot be reconciled in one paper.

**Key sources**:
- Fetters, M. D., Curry, L. A., & Creswell, J. W. (2013). Achieving Integration in Mixed Methods Designs—Principles and Practices. *Health Services Research*, 48(6pt2), 2134–2156. doi:10.1111/1475-6773.12117 [full text, web]
- Levitt, H. M., Bamberg, M., Creswell, J. W., Frost, D. M., Josselson, R., & Suárez-Orozco, C. (2018). Journal Article Reporting Standards for Qualitative Primary, Qualitative Meta-Analytic, and Mixed Methods Research in Psychology. *American Psychologist*, 73(1), 26–46. Local library [full text]
- O'Cathain, A., Murphy, E., & Nicholl, J. (2008). The quality of mixed methods studies in health services research. *Journal of Health Services Research & Policy*, 13(2), 92–98. doi:10.1258/jhsrp.2007.007074 [full text, web, abstract via Crossref]
- Creswell, J. W., & Plano Clark, V. L. (2011). *Designing and Conducting Mixed Methods Research* (2nd ed.). Sage. [abstract only — title and edition confirmed via repeated citation in Fetters et al. 2013 and Jackson et al. 2022; full text not read]

---

### C-2 Design-Based Research (DBR)

**Name**: Design-Based Research (DBR) / design experiments. Category: educational and learning-sciences research method.

**What questions it can answer**: "how does this intervention (curriculum, tool, instructional design) actually work in a real classroom setting, and why does it work or not?"; "can we design iteratively while also generating transferable learning theory?" At its core it asks whether the design can be built at all, and whether building it can contribute both to practical intervention and to theory at the same time.

**Epistemological stance and scope of claims**: DBR's stance is that the researcher actively intervenes, systematically reshaping the environment in naturalistic settings through repeated iteration, in place of manipulating variables in a laboratory. Barab and Squire (2004) state its position relative to traditional empiricist paradigms directly:
> "If one believes that context matters in terms of learning and cognition, research paradigms that simply examine these processes as isolated variables within laboratory or other impoverished contexts of participation will necessarily lead to an incomplete understanding of their relevance in more naturalistic settings... Design-based research is not so much an approach as it is a series of approaches, with the intent of producing new theories, artifacts, and practices that account for and potentially impact learning and teaching in naturalistic settings."
(Barab & Squire, 2004, *The Journal of the Learning Sciences*, 13(1), 1–14, doi:10.1207/s15327809jls1301_1, p.1–2 [full text, web])
It **can support**: claims about how a design works within a specific context, what iterative revisions it went through, and what mediating mechanisms shaped the learning process; and contributions to context-dependent "design principles." It **cannot support**: cross-context causal effect sizes or efficacy comparisons (DBR typically has no control group, and its validity is ecological and consequential — Messick's 1995 consequential validity, see card A-4 — not internal); nor can it claim an intervention is "proven effective" without describing its history of iterative revision, since the intervention itself keeps changing during the study and is never held fixed as a treatment.

**Data and sample**: case counts are typically small (one to a handful of classrooms or teaching settings), emphasizing rich contextual description over statistical representativeness; the sample logic follows "theoretically relevant cases" — a purposive, non-probability approach. Anderson and Shattuck (2012), reviewing a decade of highly cited DBR papers, found the methodology still lacks a unified, rigorous operational standard:
> "Design-based research (DBR) evolved near the beginning of the 21st century and was heralded as a practical research methodology that could effectively bridge the chasm between research and practice in formal education... They conclude that interest in DBR is increasing and that results provide limited evidence for guarded optimism that the methodology is meeting its promised benefits."
(Anderson & Shattuck, 2012, *Educational Researcher*, 41(1), 16–25, doi:10.3102/0013189x11428813, abstract [full text, web, Crossref abstract])

**Analytic procedure**: the typical cycle is problem analysis (defined jointly with practitioners) → developing an intervention prototype (with a theoretical rationale) → repeated cycles of design, implementation, analysis, and redesign (what Barab & Squire, 2004, call "iterative") → production of contextualized design principles. McKenney and Reeves's *Conducting Educational Design Research* proposes a general phase model — analysis/exploration → design/construction → evaluation/reflection — a cyclical, non-linear process (doi:10.4324/9781315105642; [abstract only] — title, DOI, and chapter structure were cross-checked via Crossref and multiple citing works; the specific phase names follow widely cited secondary sources, and the original text was not read verbatim).

**Quality criteria**: ecological validity (whether the work truly happened in a natural setting, without artificial control); consequential validity (whether the intervention's real educational consequences are credible and traceable); transferability of the design principles (are the conditions of applicability and non-applicability stated clearly); transparency of the iterations (are the reasons for each round of revision honestly documented, with the full history shown alongside the final version).

**Reporting standards**: there is no single mandatory checklist for educational design research. A common approach is to use conjecture mapping (Sandoval, 2014; local library, [hit in local library but not read verbatim for this card, marked abstract only]) as a framework for reporting the relationship between an intervention's theoretical conjectures and its observed indicators; the qualitative component can additionally be checked against COREQ/SRQR.

**Common reviewer objections and misuses**: treating "many rounds of revision" as automatically meaning "it worked," without reporting failed iterations; lacking clear, generalizable design principles and leaving only a one-off anecdotal description; treating DBR as a cheap substitute for action research and skipping the theoretical contribution; not addressing the power relationship between the teacher-researcher and the students being studied.

**Acceptance and conventions in the venues above**: education-technology and learning-sciences journals (e.g., *Journal of the Learning Sciences*) are DBR's home turf and accept it readily; general HCI/design journals vary by reviewer background and usually require an extra methodological justification (per the note in the author's statistics playbook, a separate document outside this kit). Multi-year educational intervention studies under Taiwan's Ministry of Education Teaching Practice Research Program (a Taiwan-specific example of a publicly funded teaching-improvement scheme) often present as DBR or a hybrid with action research, but the program's official review criteria do not publicly enumerate DBR-specific standards (verified: the official site, tpr.moe.edu.tw, publishes only a program overview and Q&A page, with no item-by-item review-criteria text found — flagged as "could not find," not guessed, and discussed further in card 3).

**Resources and ethics**: long-term involvement in the teaching setting means the power relationship between the teacher-as-researcher and the students needs to be handled directly (especially when studying one's own class); it requires cooperation and resource commitment at the school or course level (not a one-off intervention); multiple iterations typically mean the study spans at least a semester, sometimes years.

**Common combinations**: DBR's boundary with action research is often blurry (see the distinction in card 3); embedded mixed methods combining a quantitative pre/post test with qualitative process interviews (see card 1); conjecture mapping paired with TraMineR sequence analysis for process data (the author's statistics playbook, a separate document outside this kit).

**When not to use it**: when only a single fixed intervention version needs validating (no iterative design involved) — a quasi-experimental design is more honest and more acceptable to quantitatively oriented reviewers; when there is no capacity or resource for multi-round, cross-time iteration in the field, in which case DBR degenerates into a single-round action-research study dressed up as multi-round design research; when cross-context effect-size comparisons are needed (DBR is inherently disadvantaged here).

**Key sources**:
- Barab, S., & Squire, K. (2004). Design-Based Research: Putting a Stake in the Ground. *The Journal of the Learning Sciences*, 13(1), 1–14. doi:10.1207/s15327809jls1301_1 [full text, web]
- Anderson, T., & Shattuck, J. (2012). Design-Based Research: A Decade of Progress in Education Research? *Educational Researcher*, 41(1), 16–25. doi:10.3102/0013189x11428813 [full text, web, Crossref abstract; full text not read]
- McKenney, S., & Reeves, T. C. (2018). *Conducting Educational Design Research* (2nd ed.). Routledge. doi:10.4324/9781315105642 [abstract only]
- Sandoval, W. (2014). Conjecture Mapping: An Approach to Systematic Educational Design Research. Local library [hit in local library; not read verbatim, marked abstract only]

---

### C-3 Action Research (including teacher action research / Taiwan's Ministry of Education Teaching Practice Research Program)

**Name**: Action Research; Teacher Action Research; Taiwan's Ministry of Education "Teaching Practice Research Program" (TPR) commonly uses this design or a variant of it (a Taiwan-specific example, included here to illustrate one country's institutional variant). Category: cyclical, practice-oriented research method.

**What questions it can answer**: "I have a problem in my own teaching/practice — after making this adjustment, did things improve, and how?" It focuses on the practitioner-researcher's intervention in, and reflection on, their own setting; producing cross-context theory is a separate goal it does not pursue.

**Epistemological stance and scope of claims**: it **can support** claims about what the researcher (usually also the practitioner) observed and reflected on after one cycle of intervention in a specific classroom or setting. It **cannot support** cross-classroom, cross-teacher causal inference or effect-size comparison (the sample is usually the researcher's own class; there is no random sampling), nor can it claim a teaching method is "proven generally effective." The tradition emphasizes a spiral cycle of plan–act–observe–reflect (the Lewinian lineage, developed further by Kemmis and McTaggart; this genealogical claim is broadly accepted in the methodology literature, though the Kemmis & McTaggart original was not read directly for this card — searxng returned no usable results for this query, so the local library's bibliographic trail was used instead: local library "[Candy 2006] Practice based research" lists Stringer's 2003 *Action Research in Education* in its bibliography, confirming this lineage exists within the design-research methodology literature; Stringer's own text was not read, so only the citation's existence is confirmed here — its argument remains unverified [full text]).

**Data and sample**: the sample is the researcher's own class or workshop participants; its justification rests on contextual representativeness, a logic distinct from statistical representativeness; scale is typically single digits to a few dozen (one or a few classes).

**Analytic procedure**: a spiral of plan (identify problem) → act (implement intervention) → observe (collect data: teaching logs, student work, surveys, interviews) → reflect (revise), possibly iterated over multiple rounds; analysis is usually qualitative (teacher reflection notes, student feedback) paired with simple descriptive quantitative summaries (grades, survey means), with inferential statistics rare given the small, non-random samples.

**Quality criteria**: researcher reflexivity (especially given the dual role of teacher studying their own students); triangulation (teaching logs + student feedback + peer observation); a traceable cycle record (what each round's revision was based on, and why); claims of "improved teaching quality" need evidence from actual classroom implementation; planning-document-level inference alone does not meet that bar. Taiwan's Ministry of Education Teaching Practice Research Program's official site explicitly centers the requirement on formal classroom implementation of a complete lesson plan:
> "透過不同任務之同步推展，積極鼓勵大專校院投入資源，協助大學教師增進教學能力，經由完整且優良之教案在課堂上的正式實施，提升教學品質，幫助學生增進知識學習的相關成效。" [By advancing several tasks in parallel, the program actively encourages universities to commit resources to help faculty build their teaching capacity, so that formal classroom implementation of complete, well-designed lesson plans improves teaching quality and helps students learn more effectively.]
(Taiwan Ministry of Education Teaching Practice Research Program official site, "Program Overview" page, tpr.moe.edu.tw/plan/intro [full text, web])

**Reporting standards**: there is no single mandatory checklist for action research in education; if a quantitative pre/post component is involved, TREND applies (non-randomized intervention, see the reporting-guideline table in `method/METHOD_DECISION.md` §8); the qualitative component can be checked against COREQ/SRQR. Taiwan's Teaching Practice Research Program itself requires an official report format (motivation and purpose, literature review, research questions, design and methods, teaching and research outcomes, recommendations and reflection) — a structure confirmed against an actual outcome report PDF (table-of-contents structure [full text, web]); a different report states, "本計畫採用行動研究方法在計畫、執行與事實發現三個螺旋歷程中，逐步調整教學方法和策略" [This project uses action research, adjusting teaching methods and strategies through a spiral of planning, implementation, and fact-finding], a sentence drawn from an outcome report's abstract fragment via a search-result snippet [abstract only — this sentence came from a search-result fragment; the PDF itself was not opened to verify the exact location of the passage].

**Common reviewer objections and misuses**: treating "the teacher felt the students responded better" as a finding without concrete supporting data; calling a single round of intervention "action research" without the spiral iteration the term implies; failing to address the fact that the teacher-researcher's dual role links grading power to data collection; using inferential statistics (t-tests, ANOVA) on samples of a handful to a dozen or so participants.

**Acceptance and conventions in the venues above**: Taiwan's Ministry of Education Teaching Practice Research Program is the main institutionalized channel for this kind of research in Taiwan; its official site confirms the program's purpose is to "build an ongoing peer-review and mentoring model" (tpr.moe.edu.tw/plan/intro). The public pages do **not** list a complete, itemized review-criteria text — the specific scoring rubric appears to be internal reviewer material, and this port **could not find** a publicly available verbatim version. Design-education conferences and educational-technology journals generally accept action research well, provided reflexivity and cycle records are clearly documented.

**Resources and ethics**: the dual power relationship of the teacher-researcher toward their own students is the central ethical issue — grading authority and data-collection authority sit with the same person, and concrete mitigations are needed (e.g., a statement decoupling grades from research participation, analyzing data only after the semester ends, de-identification); most Teaching Practice Research Program projects, being routine classroom improvement, do not require external IRB review. An increasing number of journals nonetheless require an ethics statement when the work is published as a paper (see the submission statements in `skills/co-author/SKILL.md`, Phase 6).

**Common combinations**: the boundary with DBR is blurry — action research usually emphasizes "solving a problem in one's own setting" with more modest theoretical ambitions, while DBR explicitly aims to produce transferable "design principles" or theory. Teaching Practice Research Program projects commonly combine action research with a simplified quantitative pre/post test and student surveys.

**When not to use it**: when cross-teacher, cross-classroom generalizable conclusions are needed; when the venue explicitly expects causal inference or effect-size comparison; when the researcher lacks the reflexive documentation capacity, or cannot manage the conflict of interest between grading authority and research data.

**Key sources**:
- Taiwan Ministry of Education Teaching Practice Research Program, "Program Overview," https://tpr.moe.edu.tw/plan/intro [full text, web]
- Taiwan Ministry of Education Teaching Practice Research Program, "FAQ," https://tpr.moe.edu.tw/plan/qa [full text, web; page structure only, no itemized review criteria — could not find]
- A Teaching Practice Research Program outcome report, report.kmu.edu.tw [full text, web; table-of-contents structure confirmed]
- [Candy 2006] Practice based research, local library (bibliography section lists the Action Research tradition; content not read verbatim) [full text, bibliography confirmed only]

---

### C-4 Design Research Methodology (DRM, Blessing & Chakrabarti 2009) and sampling in design research (Cash et al. 2022)

**Name**: DRM, a Design Research Methodology; the eight sampling considerations for design research (Cash, Isaksson, Maier, & Summers, 2022). Category: an integrative methodological framework for engineering/product-design research.

**What questions it can answer**: "does this design-support tool or method actually help design practice, and how?" DRM splits the whole design-research process into four linked stages of inquiry, chaining together "first describe the current situation, then develop support, then validate whether the support helps" into one testable sequence.

**Epistemological stance and scope of claims**: DRM itself is a **methodological framework** spanning descriptive and prescriptive research; it is broader than any single method. It **can support**: an empirical description of the current state of design practice (Descriptive Study I); theoretical construction and preliminary validation of a design-support tool (Prescriptive Study); and empirical evaluation of that tool's effect in an applied setting (Descriptive Study II). It **cannot support**: skipping Descriptive Study I and claiming directly that a tool "improved design," since there is no baseline for comparison; nor can a single stage's output be treated as a complete DRM study. The original definition of DRM's four stages:
> "DRM consists of four stages: Research Clarification, DS I, Prescriptive Study (PS) and Descriptive Study II (Blessing et al. 1992; Blessing et al. 1995)... In the Research Clarification (RC) stage the researchers try to find some evidence..."
(Blessing & Chakrabarti, 2009, *DRM, a Design Research Methodology*, Springer, doi:10.1007/978-1-84882-587-1, local library [full text])

**Data and sample**: Cash et al. (2022) address the long-neglected, terminologically confused problem of sampling in design research, proposing eight considerations as a checklist for sampling decisions (headings verified verbatim against the local library):
1. Scientific good conduct: what ethical concerns are relevant?
2. Design framing: what type of impact on practice do you hope for?
3. Theoretical framing: where in the theory-building/theory-testing cycle?
4. Scope: how general and abstract is the intended contribution?
5. Generalisation approach: what type of generalisability?
6. Sample schema: what schema fits your theoretical framing?
7. Sample size: what size fits with your generalisation approach?
8. Sampling strategy: (when using multiple studies) what strategy fits?
(Cash, Isaksson, Maier, & Summers, 2022, *Design Studies* 78, 101077, doi:10.1016/j.destud.2021.101077, local library [full text])
They also point out that sampling in design research has long been reported opaquely:
> "there has been little specific discussion of sampling terminology or considerations in the design research literature. Hence, the reporting of sampling decisions is often implicit and can appear to be something of a methodological 'black box'."
(ibid., p.2 [full text])

**Analytic procedure**: DS-I (describing the current state) commonly uses observation, interviews, literature analysis, or secondary analysis of existing data; PS (developing prescriptive support) combines theory-building with prototype design; DS-II (evaluating impact) uses experimental or quasi-experimental evaluation of the support tool's effect in real or simulated settings. Sampling strategy converges through what Cash et al. call a "double-loop sampling process" (a definition loop determining the sampling schema, and a refinement loop determining the sample strategy and size).

**Quality criteria**: DRM itself offers no single reliability/validity formula; instead it requires that the logical link across the four stages be transparent. Cash et al.'s eight sampling considerations are fundamentally a transparency-and-justification checklist — reviewers can use them to check whether sampling decisions were stated and justified, replacing a bare after-the-fact objection that "the sample is too small."

**Reporting standards**: no dedicated checklist exists; engineering-design-research journals (*Design Studies*, *Journal of Engineering Design*) commonly expect authors to state explicitly which DRM stage the study occupies and which sampling considerations were followed.

**Common reviewer objections and misuses**: conflating descriptive and prescriptive research goals; failing to state or justify sampling decisions (the "black box" problem Cash et al. identify); mistaking a small-scale prototype test (PS stage) for large-scale efficacy validation (DS-II stage).

**Acceptance and conventions in the venues above**: DRM is a highly cited integrative framework within engineering design research (the Design Society / *Design Studies* community); design-education and HCI journals adopt the DRM terminology less often, but its "describe the current state, then develop, then validate" logic resonates with the cyclical spirit of DBR and action research and is often cited across boundaries as a way to position a study.

**Resources and ethics**: running the full four stages typically spans years (doctoral-level work); most single papers cover only one or two stages; they should honestly state that limited scope. Claiming a complete DRM study on that basis overreaches.

**Common combinations**: DS-I often pairs with qualitative methods (interviews, observation); DS-II often pairs with quasi-experimental designs or user studies; the eight sampling considerations can be applied as a cross-cutting checklist at any method-selection stage of design research.

**When not to use it**: when the study is explicitly a single, small-scale exploratory piece with no intention of building the full current-state–support–validation chain; when the eight sampling considerations are applied to a purely quantitative, large-sample statistical study, in which case a standard power-analysis report is a better fit.

**Key sources**:
- Blessing, L. T. M., & Chakrabarti, A. (2009). *DRM, a Design Research Methodology*. Springer. doi:10.1007/978-1-84882-587-1. Local library [full text]
- Cash, P., Isaksson, O., Maier, A., & Summers, J. (2022). Sampling in design research: Eight key considerations. *Design Studies*, 78, 101077. doi:10.1016/j.destud.2021.101077. Local library [full text]

---

### C-5 Participatory Design / Co-Design as a research method

**Name**: Participatory Design (PD); Co-Design; Co-Creation. Category: design research methods that involve users/stakeholders as active participants.

**What questions it can answer**: "how do users/stakeholders jointly construct a design direction that is meaningful to them?"; "what insights or artefacts emerge once part of the design decision authority is handed to participants?" These are generative, exploratory questions; validating an existing design against a benchmark is a separate task.

**Epistemological stance and scope of claims**: Sanders and Stappers (2008) frame this as an epistemological shift from "user as research subject" to "user as design partner":
> "The user-centred design approach (i.e. 'user as subject') has been primarily a US-driven phenomenon. Increasingly, since the 1970s, people have been given more influence and room for initiative in roles where they provide expertise and participate in the informing, ideating, and conceptualising activities in the early design phases. The participatory approach (i.e. 'user as partner') has been led by Northern Europeans."
(Sanders & Stappers, 2008, *CoDesign*, 4(1), 5–18, doi:10.1080/15710880701875068, p.5 [full text, web])
It **can support**: the design ideas participants jointly produce, a collective interpretation of a situated need, and the tacit knowledge revealed by the co-creation process itself. It **cannot support**: treating a participatory workshop's output as equivalent to "general user needs" — workshop participants are a convenience sample, and their ideas reflect a specific small group's collective creativity under specific facilitation; the result falls well short of a population-representative survey. A more recent methodological warning: Sloane et al. (2022) argue that "participation" can itself be co-opted as a "design fix" for machine-learning systems: the gesture substitutes for a genuine redistribution of power — a critical caution against over-optimistic claims for participatory methods (local library [hit at the title/abstract level; content not read verbatim, marked abstract only]).

**Data and sample**: the sample is usually a recruited small group of stakeholders (design workshops commonly run 5–15 people per session, possibly across multiple sessions); the sampling logic rests on "representativeness of contextually relevant stakeholders," a different standard from statistical representativeness; diversity of roles in the room matters more than a large sample of a single role.

**Analytic procedure**: workshop outputs (sketches, models, card sorts, storyboards) are themselves data; analysis commonly combines thematic analysis of discussion transcripts with artefact analysis. Generative toolkits (make-tools, cards, collage materials) are used to elicit hard-to-articulate tacit experience.

**Quality criteria**: transparency of facilitation technique and workshop design (are the workshop script and prompt cards made available); whether participants' voices are represented without being overtaken by the researcher's interpretive frame (reflexivity); whether consistency and difference across multiple sessions or groups are honestly presented in full, without cherry-picking only the outputs that support the researcher's hypothesis.

**Reporting standards**: no dedicated checklist; the qualitative component can be checked against COREQ/SRQR; the design-research community commonly expects a detailed account of the workshop flow (warm-up, divergence, convergence phases) and the rationale for material design.

**Common reviewer objections and misuses**: extrapolating a single workshop's output directly to "user needs" without noting sample limitations; conflating "participatory design" with plain usability testing (where users remain "subjects" without ever becoming "design partners"); a workshop's prompts and materials systematically steering participants toward the researcher's preferred direction without disclosing this in the methods section; the "participation-washing" risk Sloane et al. (2022) warn about deserves particular vigilance in AI-related design research.

**Acceptance and conventions in the venues above**: DIS, CHI, and design-education conferences broadly accept and expect this kind of method as part of a valid contribution, especially in human-centered design and civic-tech work; in purely technical systems papers (IUI's system-contribution bias), it usually plays only a supporting role.

**Resources and ethics**: recruitment and venue costs run higher (in-person or synchronous online time is needed); working with minors or vulnerable groups raises ethics-review requirements; when a teacher facilitates a workshop with their own students as participants, the same power-relationship issue noted in card 3 applies.

**Common combinations**: commonly paired with P-C (creative-tool evaluation) and P-D (qualitative interviews), with workshop-generated ideas feeding into prototyping and subsequent user testing; also a common concrete stage inside a DBR or action-research cycle.

**When not to use it**: when the research question needs a validating, statistically representative conclusion; when there is not enough time for proper warm-up, facilitation, and convergence design; when the political stakes of a design decision are high but only a convenience sample of like-minded participants was recruited, while claiming "user voices have been incorporated."

**Key sources**:
- Sanders, E. B.-N., & Stappers, P. J. (2008). Co-creation and the new landscapes of design. *CoDesign*, 4(1), 5–18. doi:10.1080/15710880701875068 [full text, web]
- Sloane, M., Moss, E., Awomolo, O., & Forlano, L. (2022). Participation is not a Design Fix for Machine Learning. Local library [title and hit fragment level; full text not read verbatim]

---

### C-6 The Delphi Method / Expert Consensus

**Name**: Delphi Survey Technique. Category: multi-round, anonymous expert-consensus method.

**What questions it can answer**: "can a group of experts converge on a collective consensus about an issue that has no settled answer yet?" It suits problems that lack sufficient empirical data and must rely on expert judgment.

**Epistemological stance and scope of claims**: Hasson, Keeney, and McKenna (2000) define it as a structured process for turning opinion into consensus:
> "Consensus methods such as the Delphi survey technique are being employed to help enhance effective decision‐making in health and social care. The Delphi survey is a group facilitation technique, which is an iterative multistage process, designed to transform opinion into group consensus."
(Hasson, Keeney, & McKenna, 2000, *Journal of Advanced Nursing*, 32(4), 1008–1015, doi:10.1046/j.1365-2648.2000.t01-1-01567.x, abstract [full text, web, abstract via Crossref API])
It **can support** claims about the degree of consensus a specific panel of experts reached after specific rounds, and a documented record of how that consensus converged or diverged across rounds. It **cannot support** the claim that "consensus equals truth," nor can it claim to represent all stakeholders' views.

**Data and sample**: expert panels commonly run 10–30 people; the sampling logic follows "professional representativeness and heterogeneity," a criterion apart from random sampling; recruitment criteria need to be stated and justified explicitly in the methods section.

**Analytic procedure**: the first round is usually an open-ended question-gathering exercise, then compiled into a structured questionnaire sent back to the same panel for further rounds of ratings; between rounds, "controlled feedback" is provided (usually group central-tendency statistics without revealing individual identities); this repeats until a preset consensus standard or round limit is reached (typically 2–4 rounds). Its core design features are **anonymity**, **iteration**, **controlled feedback**, and **statisticized group response**.

**Quality criteria**: transparency of the consensus definition; justification and disclosure of the heterogeneity of expert selection criteria; reporting of attrition and per-round response rates; avoiding hidden bias from the facilitator screening items after the fact.

**Reporting standards**: there is no single mandatory checklist, though Hasson et al. (2000) is itself widely cited as methodological guidance for reporting, covering: clarity of problem definition, expert-selection criteria, round design, feedback mechanism, and consensus criteria.

**Common reviewer objections and misuses**: too homogeneous an expert panel while still claiming "expert consensus"; vague or post hoc consensus criteria; misusing "Delphi" to label a single-round survey; high attrition that goes unreported or unanalyzed.

**Acceptance and conventions in the venues above**: highly accepted and well established in health and social-science fields; less common in design and HCI, where it is mostly used for building indicators, evaluation frameworks, or priority rankings.

**Resources and ethics**: multiple rounds mean a longer timeline; anonymity must be maintained to protect experts from peer pressure; ethics review usually focuses on recruitment method and data-confidentiality procedures.

**Common combinations**: commonly paired with scale development (IRT/CFA; the author's statistics playbook, a separate document outside this kit); can also pair with a scoping review (card 8).

**When not to use it**: when sufficient empirical data already exists for direct analysis; when a sufficiently heterogeneous, representative expert group cannot be found (a panel smaller than roughly 10 people is usually too small to be called a robust Delphi); when time pressure does not allow multiple rounds.

**Key sources**:
- Hasson, F., Keeney, S., & McKenna, H. (2000). Research guidelines for the Delphi survey technique. *Journal of Advanced Nursing*, 32(4), 1008–1015. doi:10.1046/j.1365-2648.2000.t01-1-01567.x [full text, web, Crossref abstract; full text blocked by a Wiley 403]

---

### C-7 HCI user-research venue choices: field studies, deployment studies (in-the-wild), and lab studies

**Name**: Laboratory Study; Field Study; In-the-Wild / Deployment Study. Category: methodology for choosing the setting of an HCI user study.

**What questions it can answer**: a lab study answers "under controlled conditions, what difference does a specific variable in the interface/system make?"; a field study answers "in a real but still researcher-mediated, short-term setting, how does the system get used?"; an in-the-wild/deployment study answers "once the system is genuinely placed into people's everyday lives or work for a period of time, what adoption patterns, unexpected uses, and long-term effects emerge?"

**Epistemological stance and scope of claims**: the central tension across the three is the trade-off between internal validity and ecological validity. Rogers and Marshall (2017) position in-the-wild research against traditional controlled research, emphasizing observation of the co-evolution of systems and human behavior in real settings (doi:10.1007/978-3-031-02220-3; [abstract only] — the bibliographic entry and chapter structure were confirmed via Crossref, but the argument text was not read for this port). Lazar, Feng, and Hochheiser's textbook *Research Methods in Human-Computer Interaction* devotes a chapter to comparing field studies and laboratory studies ([abstract only] — only the book title, authors, and chapter topic were confirmed; the content itself remains unread). It **can support**: lab studies can support causal comparisons of controlled variables (paired with the author's statistics playbook, a separate document outside this kit); in-the-wild studies can support descriptions of real-world, long-term adoption patterns and unexpected appropriation, though they usually cannot rule out confounds. It **cannot support**: extrapolating a lab effect directly to real-world use; generalizing a single in-the-wild deployment case as universal causal evidence.

**Data and sample**: lab-study sample size follows a power analysis; in-the-wild sample sizes are usually smaller but observed over a longer period, with the sample logic favoring depth over breadth; field studies fall in between.

**Analytic procedure**: lab studies use random assignment, controlled variables, and statistical testing; in-the-wild studies commonly combine behavioral logs, experience sampling, and post-deployment interviews, mixing quantitative usage patterns with qualitative thematic analysis.

**Quality criteria**: lab studies are judged on internal validity and statistical power; in-the-wild studies are judged on reporting transparency; the choice of setting itself should match the research question.

**Reporting standards**: lab studies with random assignment can use CONSORT; in-the-wild/deployment studies have no single mandatory checklist, but the community expects clear reporting of deployment length, sample attrition, and how technical problems affected data completeness.

**Common reviewer objections and misuses**: exaggerating a short-term "field trial" as an "in-the-wild deployment"; writing lab-study effects directly into conclusions about real-world behavior; high attrition in a deployment study that goes unreported.

**Acceptance and conventions in the venues above**: CHI/DIS place high value on justifying the choice of setting; IUI favors controlled experiments with system metrics; HCII is relatively friendly to all three settings but expects the methods to be fully justified.

**Resources and ethics**: in-the-wild research requires accepting a loss of control; long-term deployment involves continuous data collection from participants' daily lives or work, so ethics review is usually more demanding than for a single lab session.

**Common combinations**: the three can form a progressive research plan; in-the-wild work is commonly paired with qualitative process analysis (the author's statistics playbook, a separate document outside this kit).

**When not to use it**: labeling a short deployment "in-the-wild" when resources cannot actually support a genuine long-term deployment; when the research question needs rigorous causal comparison and does not need to trade control away for ecological validity.

**Key sources**:
- Rogers, Y., & Marshall, P. (2017). *Research in the Wild*. Synthesis Lectures on Human-Centered Informatics. Springer. doi:10.1007/978-3-031-02220-3 [abstract only]
- Lazar, J., Feng, J. H., & Hochheiser, H. *Research Methods in Human-Computer Interaction* (2nd ed.). Morgan Kaufmann / Wiley. [abstract only — only the chapter topic was confirmed to exist in the table of contents]

---

### C-8 Systematic reviews, scoping reviews, and method mapping

**Name**: Systematic Review; Scoping Review (Arksey & O'Malley, 2005); PRISMA-ScR (Tricco et al., 2018); Systematic Mapping Study (Petersen et al.); method mapping (the core task of this card). Category: methods for synthesizing literature evidence.

**What questions it can answer**: a systematic review answers "for a well-defined question, what is the overall direction or size of the existing empirical evidence?"; a scoping review answers "what concepts, methods, and evidence types does this research area currently cover, and where are the gaps?" — its goal is to **map** the field, without settling on a single pooled effect. Arksey and O'Malley (2005) draw this distinction explicitly:
> "First, a systematic review might typically focus on a well defined question where appropriate study [designs can be identified]... The 'scoping' study comprises a further type of literature review, yet until recently much less emphasis has been placed on the scoping study as a technique to 'map' relevant literature in the field of interest."
(Arksey & O'Malley, 2005, *International Journal of Social Research Methodology*, 8(1), 19–32, doi:10.1080/1364557032000119616, p.3 [full text, web])

**Epistemological stance and scope of claims**: it **can support**: a scoping review can support a description of what the current distribution of methods looks like in a field, and where the evidence gaps are; a systematic review (including meta-analysis) can support conclusions about the direction and magnitude of a pooled effect. It **cannot support**: a scoping review generally does not include a formal risk-of-bias assessment, so it cannot conclude anything about "evidence quality"; a systematic mapping study or "systematized review" (a middle ground; see Jackson et al., 2022, on this distinction [full text]) also cannot claim the rigor of a complete systematic review.

**🔴 How to systematically extract method fields from a batch of comparable studies** (this card's core task):

Drawn from three worked examples (all read in full from the local library):

1. **Define the scope and question** (Arksey & O'Malley's Stage 1).
2. **Systematic search** (Stage 2): at least two databases, an explicit Boolean query string, a date range, and language limits. Hussain et al.'s (2023) approach is a workable template:
   > "We searched two academic databases (Scopus and Web of Science) for papers using the query 'threshold concept* AND research*' in the abstract, title, and keyword fields. The search resulted in 441 unique papers."
   (Hussain, Moalagh, & Farshchian, 2023, *Koli Calling '23*, doi:10.1145/3631802.3631827, local library [full text])
3. **Screening**: apply predefined inclusion/exclusion criteria article by article, reporting the count removed at each layer (Jackson et al., 2022: "77 non-English articles removed... 162 articles removed that were not from peer-reviewed sources... 319 articles removed" [full text]); dual independent screening with a reported agreement rate is a common quality practice (Jackson et al., 2022, report a second-author check of 30 articles, 7.5%, 100% agreement [full text]).
4. **Data extraction (the core of method mapping)**: design an extraction sheet with standardized fields, ideally testing it on a small set of "seed articles" first (Jackson et al., 2022, use two representative articles first to define keywords and themes [full text]).
5. **Mapping and synthesis**: cross-tabulate the extracted fields to describe the distribution; a pooled effect size is not the goal here.
6. **Report against PRISMA-ScR**: Tricco et al. (2018) provide a 20-core-item plus 2-optional checklist covering title, abstract, rationale and objectives, methods, results, and discussion and funding (doi:10.7326/M18-0850; [abstract only] — the outlet and identity of the paper were confirmed via a PubMed entry; the item structure is broadly cross-confirmed via secondary sources, but the original was not opened to check every item's exact wording).

**Suggested extraction-sheet fields** (synthesized from Jackson et al., 2022; Lopez et al., 2021; and Hussain et al., 2023):
- Identification: title, authors, year, publication type
- Context/setting: discipline, educational stage or research setting, sample's institution or cultural context
- Research design: qualitative/quantitative/mixed, specific design name; Creswell's QUAN/qual notation can mark the primary/secondary strand and sequencing (Jackson et al., 2022 [full text])
- Sample: sample size, sampling method, participant role
- Data sources and collection tools
- Analysis method
- Theoretical framework
- Key findings
- Quality assessment/risk of bias, if performed (Lopez et al., 2021, use five quality-assessment questions, QAQ1–QAQ5, each rated Y/P/N [full text])
- Limitations and critiques
- Notes/links

**Quality criteria**: reproducibility of the search strategy (mapping to the literature-search-strategy documentation item on a pre-submission checklist); dual-screening and dual-extraction agreement rates; a scoping review does not require formal risk-of-bias assessment; it should still state clearly whether or why one was performed (Jackson et al., 2022, state candidly, "we conducted a narrower search than might be done with additional resources and have not included a formal validity assessment of the included studies" [full text] — this honest disclosure is precisely what earns the work the label "systematized review" — a step short of a full "systematic review").

**Reporting standards**: PRISMA-ScR (the first choice for scoping reviews, Tricco et al., 2018); PRISMA 2020 (systematic review/meta-analysis, see the reporting-guideline table in `method/METHOD_DECISION.md` §8); systematic mapping studies commonly cite the five-step process from the software-engineering literature by Petersen et al. (which Hussain et al., 2023, cite and follow [full text], though Petersen's original text itself was not read directly, marked [abstract only]).

**Common reviewer objections and misuses**: writing a "scoping review" as a "systematic review" without a risk-of-bias assessment; giving only keywords for the search strategy; an undisclosed or unexplained data-extraction sheet; claiming a "comprehensive review" from a single database; unreported dual-screening agreement rates.

**Acceptance and conventions in the venues above**: education, health, and computing-education journals accept PRISMA-ScR/PRISMA readily; design-research journals commonly use "systematic literature review" (SLR) without necessarily following PRISMA-ScR item by item, focusing on transparent search strategy and a self-designed quality-assessment tool.

**Resources and ethics**: search and screening are time-consuming; human-subjects ethics review is usually not required. Summarizing and critiquing other researchers' methods still requires faithfully representing the original context.

**⚠️ A criterion for the process that follows this card**: before choosing a method for a new topic, one should: (1) run a small method map on comparable published studies using the six steps above; (2) list each article's design, sample, analysis, quality criteria, and critiques; and (3) identify what this sub-field currently favors and what weaknesses reviewers or subsequent literature have criticized, using that as the empirical input to the "Cross-method issue: choosing a method for a topic" section below.

**Key sources**:
- Arksey, H., & O'Malley, L. (2005). Scoping studies: towards a methodological framework. *International Journal of Social Research Methodology*, 8(1), 19–32. doi:10.1080/1364557032000119616 [full text, web]
- Tricco, A. C., et al. (2018). PRISMA Extension for Scoping Reviews (PRISMA-ScR): Checklist and Explanation. *Annals of Internal Medicine*, 169(7), 467–473. doi:10.7326/M18-0850 [abstract only]
- Jackson, A., et al. (2022). Learning from failure: A systematized review. *International Journal of Technology and Design Education*. doi:10.1007/s10798-021-09661-x. Local library [full text]
- López, Ó., Murillo, C., & González, A. (2021). Systematic Literature Reviews in Kansei Engineering for Product Design—A Comparative Study from 1995 to 2020. *Sensors*, 21(19), 6532. doi:10.3390/s21196532. Local library [full text]
- Hussain, S. S., Moalagh, M., & Farshchian, B. A. (2023). Which Threshold Concepts Do Computing Students Encounter while Learning Empirical Research Methods? *Koli Calling '23*. doi:10.1145/3631802.3631827. Local library [full text]

---

## Group C cross-method issue: choosing a method for a topic

The following gathers **evidence-based frameworks for method choice**, arranged by decision criterion. Each framework is sourced and its verification level noted; the goal is to give citable decision criteria — no single "correct answer" is on offer.

### Framework 1: question–method fit

**The shape of the question's verb** determines the method family:
- "Is there a difference, how big, is there a causal relationship" → quantitative experiment/quasi-experiment (the author's statistics playbook, a separate document outside this kit)
- "Why, how does it happen, how do people experience it" → qualitative research (P-D)
- "Can it be built, and what design knowledge does building it produce" → RtD (D-1) / DBR (C-2) / DRM (C-4)
- "What does the existing evidence look like, where are the gaps" → systematic/scoping review (card 8)
- Fetters, Curry, and Creswell (2013) apply exactly this logic when judging whether to mix methods: "Health services researchers use quantitative methodologies to address research questions about causality, generalizability, or magnitude of effects. Qualitative methodologies are applied to research questions to explore why or how a phenomenon occurs, to develop a theory, or to describe the nature of an individual's experience." (same quote as in card 1, [full text, web]) — this sentence is itself the direct source for the "question type determines method" criterion.

### Framework 2: epistemological stance

- Post-positivist stances lean toward controlled quantitative methods.
- Constructivist/interpretivist stances lean toward qualitative research, participatory design, and action research — emphasizing meaning as co-constructed by researcher and participant.
- Pragmatism is the epistemological stance most often invoked for mixed methods research; both Fetters et al. (2013) and Creswell & Plano Clark's framework rest on the idea that method should serve the question; it should not be locked to a single philosophical stance (see card 1).
- The design-research community (Cash et al., 2022) additionally emphasizes a "theory-building vs. theory-testing cycle" position as a criterion mapped directly onto sampling-strategy choice (see card 4).

### Framework 3: feasibility and ethics

- Cash et al.'s (2022) first consideration is "Scientific good conduct: what ethical concerns are relevant?" — ethics comes first, ahead of sampling and method choice (see card 4).
- The power relationship of teacher-researchers (cards 3 and 5) is the feasibility/ethics constraint most directly relevant to university-based practitioner-researchers, and is best addressed at the method-selection stage; patching it in afterward is a far weaker fix.
- DBR and long-term deployment (in-the-wild) research (cards 2 and 7) make the highest demands on time and resources; when time or staffing falls short, honestly downgrading to a smaller-scope method is better than falsely claiming a full-scale version.

### Framework 4: venue expectations

- The author's own venue notes, kept in a separate document, compare quantitative and qualitative/RtD expectations for DIS, IUI, HCII, ISEA, SIGGRAPH Art, and design-education conferences; check each venue's current call and review form yourself.
- Reporting standards themselves are a concrete embodiment of venue expectations: COREQ/SRQR, CONSORT/CONSORT-SPI, TREND, STROBE, PRISMA/PRISMA-ScR, GRAMMS — the reporting-guideline table in `method/METHOD_DECISION.md` §8 notes clearly that a checklist is a completeness check for reporting; it does not guarantee method quality. It should be consulted once a journal is chosen, well before submission.
- Taiwan's Teaching Practice Research Program, as a specific venue, states its expectations explicitly around formal classroom implementation plus empirical evidence of improved teaching quality (see the card 3 quote) — a venue-expectation criterion that takes priority over abstract methodological theory.

### Framework 5: method mapping as an empirical calibration of venue expectations

The four frameworks above are all abstract, and taken alone risk being "theoretically correct, but blind to what this sub-field is actually doing." A fifth, operationally final, criterion is therefore proposed: run card 8's method-mapping process on comparable published studies first, then use the first four frameworks to explain why a sub-field clusters around certain methods and why some methods keep drawing reviewer criticism, before settling on a method for the new topic. This ordering — empirical stocktaking first, theoretical criteria second — echoes Cash et al.'s (2022) diagnosis of the "black box" problem in design-research sampling: transparently showing how comparable studies were compared and how the decision was made is itself part of what makes a method choice legitimate — it is not a literature review tacked on after the method is already picked.

---

Sources: see the key-sources list in each card.

## Group D: Art and design practice research

Scope: SIGGRAPH Asia (Art Papers, Educator's Forum), Leonardo, Technoetic Arts, ISEA, DIS (the RtD track, Pictorials), NIME, EvoMUSART, Studies in Conservation, IJDMD.

---

### D-1 Research through Design (RtD) and intermediate knowledge

**Name**: Research through Design (RtD) / forms of intermediate knowledge: annotated portfolios, strong concepts.

**What questions it can answer**:
- "Can this thing be built? And once built, what previously nonexistent possibility does it demonstrate?"
- "What design space does this new integration open up?"
- "What transferable intermediate-level concept emerges across this series of related works?"
It does not answer "how much better is A than B" or "what is the user-satisfaction score."

**Epistemological stance and scope of claims**:
- **Can support**: claims that a design direction is feasible, meaningful, and worth the community's attention; claims that a piece demonstrates a design stance not previously clearly articulated.
- **Cannot support**: causal claims, cross-context generalizable theory, or claims of reproducibility with identical results. Zimmerman et al. argue the benchmark should shift from *validity* to *relevance*: "Instead of validity, the benchmark for interaction design research should be relevance. This constitutes a shift from what is true — the focus of behavioral scientists, to what is real — the focus of anthropologists." (p.8–9 [full text])
- Gaver further argues that RtD's theory is inherently **provisional, contingent, and aspirational**, and that the community should "moderate expectations of creating extensible and verifiable theory" [full text].

**Data and sample**: not sample-oriented. The typical scale is **one or a few deeply documented works or prototypes**, or a related set forming a "portfolio." There is no power analysis, no notion of saturation; the justification logic is what conceptually important thing a case demonstrates.

**Analytic procedure**: an iterative design–build–evaluate cycle; the output is "annotated" (text plus images) to point out the conceptual dimensions it demonstrates. Claiming intermediate-level knowledge (a strong concept) requires what Höök and Löwgren call **bidirectional grounding**: horizontal grounding (mapping to other examples at the same level) and vertical grounding (explaining down to concrete instances, and up to supporting theory).

**Quality criteria**:
- Zimmerman et al. (2007) propose four evaluative lenses: **process, invention, relevance,** and **extensibility** (p.8 [full text]).
- Höök and Löwgren's criteria for strong concepts: **contestable, defensible, substantive** — "is generative and carries a core design idea, cutting across particular use situations… resides on an abstraction level above particular instances" (abstract [full text]).

**Reporting standards**: no formal checklist exists; in practice, follow venue convention (DIS's RtD track, Pictorials format requirements).

**Common reviewer objections and misuses**:
- "Where's the sample size / how does this generalize" — applying a quantitative evaluation framework to an RtD submission is itself a misreading.
- Zimmerman et al.'s own noted misuse: many self-described RtD submissions document only the design process without addressing relevance, making the work "appears to be self-indulgent, and personal exploration that informs the researcher but makes no promise to impact the world" (p.9 [full text]).
- Gaver notes that internal community disagreement over whether the field should converge on a unified standard can be misread as evidence the method is immature. He argues instead that diversity is simply natural for a generative field [full text].

**Acceptance and conventions in the venues above**: DIS has a formal RtD track and Pictorials (12 pages, visually driven narrative, roughly 25% acceptance, verified 2026-06-05); ISEA's art track does not require statistics; **SIGGRAPH Art Papers long-form submissions are an exception** — the call explicitly favors validated protocols and human-impact evaluation, in which case the design should shift toward P-A or P-C; an annotated portfolio alone will not carry the submission.

**Resources and ethics**: time is spent mainly on design and making; if the work involves evaluating human users, whether ethics review is needed depends on the form of evaluation. If the work involves students, the teacher-researcher power relationship (see "cross-method issues") needs separate handling.

**Common combinations**: commonly paired with autoethnography/first-person methods (card 4); when a human-impact claim is needed, quantitative or semi-structured evaluation from P-A/P-C should be added.

**When not to use it**: when the research question is inherently comparative or causal, or when the review community explicitly expects a reproducible experimental design.

**Key sources**:
1. Zimmerman, J., Forlizzi, J., & Evenson, S. (2007). Research through design as a method for interaction design research in HCI. *CHI 2007*. DOI: 10.1145/1240624.1240704. Local library [full text]
2. Zimmerman, J., & Forlizzi, J. (2014). Research Through Design in HCI. In *Ways of Knowing in HCI*. DOI: 10.1007/978-1-4939-0378-8_8. **Not found in the local library; bibliographic entry confirmed only via Crossref** [bibliographic entry only]
3. Gaver, W. (2012). What should we expect from research through design? *CHI 2012*. Local library [full text]
4. Gaver, W., & Bowers, J. (2012). Annotated Portfolios. *interactions* 19(4). Local library [full text]. **⚠️ Filename warning**: the local library also holds a file with the same filename label whose actual content is Hoggenmueller et al. (2021, DIS), *Eliciting New Perspectives in RtD Studies through Annotated Portfolios* — filename and content do not match. This card uses only the correctly matched copy.
5. Höök, K., & Löwgren, J. (2012). Strong Concepts: Intermediate-Level Knowledge in Interaction Design Research. *TOCHI* 19(3). Local library [full text]

---

### D-2 Practice-based / Practice-led Research

**Name**: Practice-based Research and Practice-led Research.

**What questions it can answer**:
- Practice-based: "can this creative artefact itself constitute an original contribution to knowledge?"
- Practice-led: "what is the nature of this practice, and what does doing it teach us that is new about how to do this kind of practice?"

**Epistemological stance and scope of claims**: Candy's (2006) definition: "If a creative artefact is the basis of the contribution to knowledge, the research is practice-based. If the research leads primarily to new understandings about practice, it is practice-led." "Practice-based Research is an original investigation undertaken in order to gain new knowledge partly by means of practice and the outcomes of that practice… a full understanding can only be obtained with direct reference to the outcomes." (p.1 [full text])
- **Can support**: using the creative artefact itself as part of a knowledge claim, or a new understanding of how a practice works.
- **Cannot support**: claims fully verifiable from text alone, detached from the work's own context — a reviewer or examiner must engage with the work itself.

**Data and sample**: usually a single doctoral-level creative project, or a small number of related works; the justification logic is the originality and scope of contribution. Vear (2022) cites Candy & Edmonds's critique of "individuality" — the method is inherently person-specific and hard to standardize (secondhand citation via local library [full text]).

**Analytic procedure**: practice is itself part of the method ("method as doing"); research design and the practice process are interwoven, with no linear sequence separating them.

**Quality criteria**: Candy (2006) notes that one criterion for judging the research component of a practice-based doctoral thesis is "whether general scholarly requirements are met" [full text].

**Reporting standards**: no formal rubric; Candy & Edmonds's (2018, *Leonardo*) "Practice-Based Research in the Creative Arts" is confirmed by Crossref (DOI: 10.1162/leon_a_01471), but full text was not read for this port [bibliographic entry only].

**Common reviewer objections and misuses**: conflating practice-led and practice-based; questioning whether the written account can stand independently of the work.

**Acceptance and conventions in the venues above**: high acceptance at Leonardo and ISEA; short-form SIGGRAPH Art Papers also commonly take this form.

**Resources and ethics**: time is invested mainly in creative practice; when a teacher is simultaneously a creator and a supervisor, boundaries need attention.

**Common combinations**: often paired with card 3 (artistic/performative research) and card 7 (documentation methods).

**When not to use it**: when the venue expects a knowledge claim verifiable from text alone, independent of the work; consider card 1 (RtD) instead.

**Key sources**:
1. Candy, L. (2006). *Practice Based Research: A Guide*. CCS Report 2006-V1.0. Local library [full text]
2. Candy, L., & Edmonds, E. (2018). Practice-Based Research in the Creative Arts: Foundations and Futures from the Front Line. *Leonardo* 51(1), 63-69. DOI: 10.1162/leon_a_01471 [bibliographic entry only, confirmed via Crossref]
3. Vear, C. (Ed.) (2022). *The Routledge International Handbook of Practice-Based Research* (preview excerpt). Local library [full text, preview excerpt only]

---

### D-3 Artistic Research and Performative Research

**Name**: Artistic Research; Performative Research (Haseman); Practice as Research (Barrett & Bolt).

**What questions it can answer**: "can this artistic practice itself constitute an epistemic act?"; "what knowledge does this creative process reveal that cannot be reduced to a written proposition?"

**Epistemological stance and scope of claims**:
- Borgdorff argues **research in the arts** should be treated as **equal in standing** to **research on the arts**: "Research in the arts is of equal value to research on the arts, and should therefore be treated equally at the institutional level." (ch.1 [full text]) He also argues the unique nature of art knowledge does **not** justify a uniquely privileged methodology: "the unique nature of knowledge in art… does not justify any unique methodology of research. 'Art knowledge'… is accessed by artistic research through both cognitive and artistic means." [full text]
- Haseman argues performative research constitutes a **third paradigm**, whose symbolic data operate "performatively" and which **rejects translating practice into words or numbers**: "they have little interest in trying to translate the findings and understandings of practice into the numbers (quantitative) and words (qualitative) preferred by traditional research paradigms" (p.4 [full text]).
- Hubner (2024) cites Candy & Edmonds's observation about method "individuality" and argues artistic research needs a **flexible research design**, rejecting "necessary 'ticking-the-method-box'" thinking (introduction [full text]), while also citing an AEC/Polifonia working group's statement that artistic research "cannot be dissolved into or identified completely with any combination of its component disciplines" but "should be able to make use of any research tool, method, or knowledge base" [full text].
- Barrett (in the introduction to Barrett & Bolt, 2007) grounds creative-arts research in **tacit knowledge**: "artistic researchers who recognise that the opposition between explicit and tacit knowledge is a false one (Bolt 2004)" [full text; corrected against the original during this port's review — the source card had mis-worded "opposition" as "distinction" and had spliced in text not present in the original].

**Cannot support**: reproducibility, or claims of producing "predictable, explicable theory"; it cannot support claims like "this intervention works for the population."

**Data and sample**: the artist/researcher's own creative practice is the core data source; the sample logic is case depth — population representativeness plays no role here.

**Analytic procedure**: the creative process itself generates data, supplemented by written reflection (an exegesis). Barrett notes: "artist's own critical commentary in writing of the creative arts exegesis is crucial" [full text].

**Quality criteria**: no single standardized criterion; Höök and Löwgren's contestable/defensible/substantive criteria (card 1) are often borrowed. Borgdorff stresses distinguishing "research in the arts" from "art itself."

**Reporting standards**: no formal rubric; journals commonly require a submitted link to the work, video, or performance record.

**Common reviewer objections and misuses**:
- "What makes you say this is research, and where does the creative work end?" — Borgdorff's "equal but not privileged" stance is the common defense.
- Labeling any creative activity "artistic research" without a clearly identifiable inquiry question or knowledge contribution.

**Acceptance and conventions in the venues above**: highly accepted at Leonardo, Technoetic Arts, and ISEA's art track; institutional recognition of creative work as equivalent to a thesis varies.

**Resources and ethics**: long-term creative commitment; co-creation with others may need ethics review; a teacher-artist needs to separate personal creative work from teaching duties.

**Common combinations**: heavily overlaps with card 2; often paired with card 4 (first-person methods).

**When not to use it**: when the venue expects a propositional knowledge claim verifiable independently of the work, without first laying out a methodological position such as Borgdorff's or Haseman's.

**Key sources**:
1. Borgdorff, H. (2012). *The Conflict of the Faculties: Perspectives on Artistic Research and Academia*. Leiden University Press. Local library (⚠️ the file contains a stray non-printing character and must be read with `grep -a`) [full text]
2. Hubner, K. (2024). *Method, Methodology and Research Design in Artistic Research: Between Solid Routes and Emergent Pathways*. Local library [full text]
3. Haseman, B. (2006). A Manifesto for Performative Research. *Media International Australia* (118), 98-106. Local library [full text]
4. Barrett, E., & Bolt, B. (Eds.) (2007). *Practice as Research: Approaches to Creative Arts Enquiry*. I.B.Tauris. Local library [full text, introduction chapter only]
5. Nelson, R. (2013). *Practice as Research in the Arts: Principles, Protocols, Pedagogies, Resistances*. Palgrave Macmillan. Local library (full text on file; this card checked only the title page and table of contents — the body text was not verified in detail) [full text, partially checked]

---

### D-4 First-Person Research / Autoethnography

**Name**: First-Person Methods; Autoethnography; Autobiographical Design.

**What questions it can answer**: "what does the researcher/designer experience by being the primary participant, using their own designed system over an extended period?"; "how does that personal, embodied experience translate into design knowledge?"

**Epistemological stance and scope of claims**:
- Biggs et al.'s (2021) *Watching Myself Watching Birds* centers autoethnography as its core method, framed as a **performative practice of autoethnographic birdwatching** that challenges human-centered design [full text]. Its definition of autoethnography (quoting reference [22]): "Autoethnography is 'the creation of an ethnography focused on the self; the author is both informant and investigator'"; it separately cites Ellis: "arts-based (autoethnographic) inquiry experiments with alternative ways to transform what is in our consciousness into…" (corrected against the original during this port's review — the source card had spliced these two sentences into one and misattributed the definition to Ellis).
- Höök et al.'s (2016) *Somaesthetic Appreciation Design* shows first-person bodily experience as design material: researchers needed **direct participation** ("simply imagining what they would be like was not enough to qualify the experience") to gain a credible design understanding [full text].
- **Can support**: existential claims that a kind of experience is possible and worth attending to; design implications drawn from a thick description of the designer's own experience.
- **Cannot support**: inferences about other people's experience; claiming "users generally have this experience" — the sample is inherently N=1, a built-in limitation, and it **cannot** substitute for user research.

**Data and sample**: N=1 (the researcher) or a specific team member; data forms include diaries, field notes, video records, and written descriptions of bodily sensation. Saturation and sampling logic do not apply.

**Analytic procedure**: long-term, sustained first-person engagement (Lucero, Desjardins, and Neustaedter's "A Sample of One," DOI: 10.1145/3301019.3319996 — **only the bibliographic entry was confirmed for this port**); combining diary writing, arts-based writing forms, and design-making.

**Quality criteria**: reflexivity is the core criterion. Desjardins and Ball's (2018) "Revealing Tensions in Autobiographical Design in HCI" (DIS 2018, DOI: 10.1145/3196709.3196781) points, by its title, to a built-in tension in the method; **not read in full for this port** [bibliographic entry and title only]. Neustaedter and Sengers (2012), "Autobiographical design in HCI research" (DIS, DOI: 10.1145/2317956.2318034), is likewise **only bibliographically confirmed** [bibliographic entry only].

**Reporting standards**: no formal checklist; DIS/CHI convention expects clear disclosure of the relationship between researcher and the object of design.

**Common reviewer objections and misuses**:
- "This is just your own experience — how do we know it generalizes?" — the paper still needs to actively explain why N=1 is appropriate for this research question.
- Packaging "I tried my own system once" as "autoethnography" without the long-term engagement, reflexive analysis, or systematic data collection the label implies.

**Acceptance and conventions in the venues above**: autoethnography/first-person methods are "institutionalized" at DIS/CHI (verified 2026-06-05); the soma design lineage (Höök) is the primary home base within interaction design.

**Resources and ethics**: requires long-term commitment from the researcher's own life/practice; if the diary content involves third parties, their privacy and consent still need consideration.

**Common combinations**: often paired with card 1 (RtD) and card 3 (artistic research); also common in card 9 as an opening methodological move.

**When not to use it**: when the research question needs to understand other people's experience — the researcher's own experience will not answer that.

**Key sources**:
1. Biggs, H. R., et al. (2021). Watching Myself Watching Birds: Abjection, Ecological Thinking, and Posthuman Design. *DIS 2021*. Local library [full text]
2. Höök, K., et al. (2016). Somaesthetic Appreciation Design. *CHI 2016*. Local library [full text]
3. Desjardins, A., & Ball, A. (2018). Revealing Tensions in Autobiographical Design in HCI. *DIS 2018*. DOI: 10.1145/3196709.3196781 [bibliographic entry only, confirmed via Crossref]
4. Lucero, A., Desjardins, A., & Neustaedter, C. (2019). A Sample of One: First-Person Research Methods in HCI. *DIS 2019 Companion*. DOI: 10.1145/3301019.3319996 [bibliographic entry only, confirmed via Crossref]
5. Neustaedter, C., & Sengers, P. (2012). Autobiographical design in HCI research. *DIS 2012*. DOI: 10.1145/2317956.2318034 [bibliographic entry only, confirmed via Crossref]

---

### D-5 Speculative design, critical design, and design fiction as research methods

**Name**: Speculative Design; Critical Design; Design Fiction; Adversarial Design.

**What questions it can answer**: "if technological/social conditions were different, what might things look like?"; "how can this proposal make a contested assumption discussable?" It asks whether a proposal can spark meaningful public discussion or critical reflection — a different question from "will users use this product."

**Epistemological stance and scope of claims**:
- Dunne and Raby position their goal as **provoking debate**: "Not in trying to predict the future but in using design to open up all sorts of possibilities that can be discussed, debated, and used to collectively define a preferable future for a given group of people" (ch.1 [full text]), proposing a "cone of futures" — probable/plausible/preferable/fantasy — and stressing that "preferable" requires asking "for whom, and who decides" [full text].
- Auger splits the method into two types and stresses that **credibility management (a perceptual bridge)** is decisive: "if it strays too far into the future to present implausible concepts or alien technological habitats, the audience will not relate to the proposal resulting in a lack of engagement" [full text].
- DiSalvo's *Adversarial Design* reframes critical design as a **political, agonistic act**.
- **Can support**: critical exposure of specific technological/social assumptions; opening a space for public discussion. **Cannot support**: claims about user acceptance or market viability, nor that a proposal represents what the public truly wants.

**Data and sample**: usually no user sample; the data are the proposal object itself and any public discourse it provokes.

**Analytic procedure**: extrapolating from existing technological systems, or swapping the ideological frame while keeping contemporary technology; often followed by public exhibition to gather discussion.

**Quality criteria**: no standardized criterion; the core is narrative credibility and internal consistency, usually judged subjectively. Bardzell and Bardzell's (2013) "What is 'critical' about critical design?" examines exactly how "critical" should be evaluated; **not read in full for this port** [bibliographic entry only, confirmed via Crossref].

**Reporting standards**: no formal checklist; Blythe's (2014) "Research through design fiction" discusses design fiction's positioning as a research method; **not read in full for this port** [bibliographic entry only, confirmed via Crossref].

**Common reviewer objections and misuses**:
- Packaging a plain concept render as "speculative design research" without a perceptual bridge leaves the work reading as sci-fi illustration; it does not yet function as a research argument.
- "Whose preferable future does this proposal represent?" — reviewers may press on the designer's standpoint and representativeness.
- Bardzell and Bardzell's (2013) title points to inconsistent use of "critical" within this community (**a reasonable inference from the bibliography and title alone — this card did not read the original to confirm it**).

**Acceptance and conventions in the venues above**: highly accepted at ISEA, SIGGRAPH Art, and Leonardo; DIS also has a well-established track; HCII/IUI accept it less readily.

**Resources and ethics**: time cost of making the proposal object; public exhibition to gather audience reactions needs informed-consent consideration.

**Common combinations**: often paired with card 6 (audience research); also often defended using card 1's relevance lens.

**When not to use it**: when the research goal is to validate a specific product's usability or market acceptance.

**Key sources**:
1. Dunne, A., & Raby, F. (2013). *Speculative Everything: Design, Fiction, and Social Dreaming*. MIT Press. Local library [full text]
2. Auger, J. (2013). Speculative design: crafting the speculation. *Digital Creativity* 24(1). Local library [full text]
3. Bardzell, J., & Bardzell, S. (2013). What is "critical" about critical design? *CHI 2013*. DOI: 10.1145/2470654.2466451 [bibliographic entry only, confirmed via Crossref]
4. Blythe, M. (2014). Research through design fiction: narrative in real and imaginary abstracts. *CHI 2014*. DOI: 10.1145/2556288.2557098 [bibliographic entry only, confirmed via Crossref]
5. DiSalvo, C. (2012). *Adversarial Design*. MIT Press. Local library [full text, table of contents and preface only]

---

### D-6 Evaluating creative-support tools and interactive art

**Name**: Creativity Support Tools Evaluation; Interactive Art Evaluation.

**What questions it can answer**: "in what ways does this creative tool support or hinder the creative process?"; "how does an audience/user experience this piece of interactive art?"

**Epistemological stance and scope of claims**:
- Cherry and Latulipe's **Creativity Support Index (CSI)** measures six dimensions: "Exploration, Expressiveness, Immersion, Enjoyment, Results Worth Effort, and Collaboration" (abstract [full text]), developed through "the iterative, rigorous development and validation process" modeled on NASA-TLX [full text].
- **Can support**: quantitative comparative claims about a tool's relative performance on these dimensions. **Cannot support**: an aesthetic judgment about an artwork's goodness.
- Remy et al. (2020), "Evaluating Creativity Support Tools in HCI Research," systematically examines evaluation methods in this area; **not read in full for this port** [bibliographic entry only].
- Vear (2022) cites frameworks such as Bilda, Edmonds, and Candy's (2008) model for evaluating interactive art experience [secondhand citation, original not read] — indicating a distinct lineage of interactive-art evaluation frameworks exists, though only its existence and citation context are confirmed here.

**Data and sample**: CSI is a questionnaire scale, so sample size follows statistical power requirements; audience research for interactive art commonly uses smaller convenience samples.

**Analytic procedure**: after CSI scoring, general linear models can compare tools (the author's statistics playbook, a separate document outside this kit); interactive-art evaluation commonly mixes observation, short interviews, and questionnaires.

**Quality criteria**: CSI has documented reliability/validity evidence; the reliability/validity of interactive-art evaluation frameworks **was not verified for this port**.

**Reporting standards**: CSI use should report subscale reliability (e.g., Cronbach's α); between-group comparisons should follow scenario P-A/P-C conventions (effect size plus CI).

**Common reviewer objections and misuses**:
- Treating the CSI total score as a single indicator, ignoring that the six dimensions are conceptually heterogeneous.
- **A definitional dispute within the NIME community about what "evaluation" means**: a commonly cited paper on this, Barbosa et al. (2015), "What does 'evaluation' mean for the NIME community?" **could not be located** — absent from the local library, and a Crossref search for this exact title did not return a matching DOI record (NIME 2015 proceedings did not universally register DOIs at the time). This card records only that the dispute is well known within the NIME community, without making any specific claim about its content.
- Treating "the audience found it interesting" directly as evidence of aesthetic success, without distinguishing willingness to engage from aesthetic/conceptual contribution.

**Acceptance and conventions in the venues above**: the creative-tools sub-community at DIS/CHI commonly uses CSI/NASA-TLX-style questionnaires; the NIME community still has internal debate about what evaluation should look like (based on general field awareness; **this port could not verify the specifics**).

**Resources and ethics**: questionnaire distribution needs standard behavioral-research ethics review; audience research involving video/audio recording needs informed consent.

**Common combinations**: CSI pairs with S2 and S6; interactive-art evaluation pairs with card 7 (process documentation).

**When not to use it**: when the research goal is to judge a work's artistic/conceptual contribution itself — use card 9 (critical/interpretive approaches) instead.

**Key sources**:
1. Cherry, E., & Latulipe, C. (2014). Quantifying the Creativity Support of Digital Tools through the Creativity Support Index. *ACM TOCHI* 21(4). Local library [full text]
2. Remy, C., MacDonald Vermeulen, L., Frich, J., et al. (2020). Evaluating Creativity Support Tools in HCI Research. *DIS 2020*. DOI: 10.1145/3357236.3395474 [bibliographic entry only, confirmed via Crossref]
3. Bilda, Z., Edmonds, E., & Candy, L. (2008). An Attribute and Predisposition Model for Evaluating Interactive Art Experience. *CoDesign* 4(4), 225-238 (secondhand citation via Vear 2022; original not read) [secondhand citation only]
4. Barbosa, J., et al. (2015). What does "evaluation" mean for the NIME community? *NIME 2015*. **Could not be located** — absent from the local library, and no reliable Crossref match found

---

### D-7 Documenting works and process

**Name**: Design/Creative Journals; Version History; Visual/Video Documentation; Code Archaeology.

**What questions it can answer**: "how did this work/system evolve to its current state?"; "which design decisions were made at which point, and why?" This kind of method usually functions as **a form of evidence supporting other methods** (RtD, practice-based, conservation) — it seldom stands as an independent research method on its own.

**Epistemological stance and scope of claims**:
- Annotated portfolios (card 1) are themselves a systematic documentation method: Gaver and Bowers argue that annotation preserves the particularity of individual cases while clearly articulating the concepts that link and distinguish different cases, without abstracting into cross-case generalizations (paraphrased from [full text]).
- Montfort et al.'s (2012) *10 PRINT CHR$(205.5+RND(1)); : GOTO 10* treats a single line of BASIC code as a research object, demonstrating that code itself can be primary source material for humanistic archaeology (local library [full text on file; this card checked only the title and existence — the specific wording of its argument remains unchecked]).
- **Can support**: descriptive reconstruction of decision sequences and evolutionary paths, and the evidentiary basis for other knowledge claims. **Cannot support**: documentation alone does not constitute a research contribution.

**Data and sample**: usually the complete process of a single work or a single creator; data types include version-control history, time-series images of sketches/prototypes, development notes, and decision memos.

**Analytic procedure**: reconstructing a timeline; annotating decision points; sometimes paired with interviews to supplement what cannot be seen at the object level alone.

**Quality criteria**: no formal reliability/validity concept; the core criteria are **traceability** and **transparency of the rationale for selecting material** (avoiding hindsight bias).

**Reporting standards**: no formal checklist; conservation contexts (card 8) commonly expect provenance, version numbers, and modification dates.

**Common reviewer objections and misuses**: "how were these documents selected — is there a risk of cherry-picking successes and hiding failed attempts?"; submitting raw excerpts of version history without analytical interpretation.

**Acceptance and conventions in the venues above**: used as supporting evidence in nearly all RtD/practice-based/conservation papers, rarely forming the sole core method of a paper.

**Resources and ethics**: mainly the time cost of organizing and preserving documents; a collaborator's private notes need their consent to quote publicly.

**Common combinations**: almost always paired with cards 1, 2, and 3; in a conservation context it is a core data source for card 8.

**When not to use it**: when the research question requires independent validation; descriptive reconstruction alone will not satisfy that need.

**Key sources**:
1. Gaver, W., & Bowers, J. (2012). Annotated Portfolios (see card 1, source 4, used here as a documentation-method example).
2. Montfort, N., et al. (2012). *10 PRINT CHR$(205.5+RND(1)); : GOTO 10*. MIT Press. Local library [full text on file; existence and title checked only]
3. Löwgren, J. (2013). Annotated portfolios and other forms of intermediate-level knowledge. *interactions* 20(1). Local library (a duplicate copy also exists under a different file entry) [full text on file; quotations not individually verified for this card]

---

### D-8 Research methods for digital art conservation and restoration

**Name**: Media Art Conservation; Variable Media Paradigm; Time-Based Media Conservation.

**What questions it can answer**: "for this partially degraded or obsolete media artwork, which attributes are the 'work-defining properties' that must be preserved?"; "when the original medium is unavailable, what reconstruction/emulation/migration strategy still preserves the work's 'identity' — the persisting logic that outlasts any single 'state'?" This is precisely the kind of question a restoration case study submitted to a journal such as *Studies in Conservation* is expected to answer.

**Epistemological stance and scope of claims**:
- Laurenson (2006) argues media-art conservation needs a conceptual framework **different from traditional fine-art conservation**: traditional conservation treats authenticity as physical integrity, but time-based media installations are closer to works created in two stages (like a musical score and its performance), so "the reference 'state' of an object has been replaced with the concept of the 'identity' of the work" (conclusion [full text, web]).
- This means it **can support** claims that interviewing the artist/technicians and comparing historical documentation makes it possible to reasonably determine a work's defining properties, and therefore that a restoration strategy preserves the work's identity. It **cannot support** a claim that a restored version is materially identical to the original — Laurenson argues this does not hold in time-based media, since two different installations/performances that both remain faithful to a work's defining properties can "both be authentic" [full text, web].
- The Variable Media Network's core methodological claim: define a work by its **medium-independent behaviors**, deliberately decoupled from any specific technology, proposing four strategies for technological obsolescence — **Storage, Emulation, Migration, and Reinterpretation** — each with trade-offs: "Possible disadvantages of emulation include prohibitive expensive [sic] and inconsistency with the artist's intent"; "Migration… the original appearance of the work will probably change"; "Reinterpretation is a dangerous technique when not warranted by the artist" [full text, web].

**Data and sample**: primarily single case studies; data sources include **interviews with artists, conservators/technicians, historical documentation, and technical examination of the physical and digital objects themselves**. Balagopal and Chin (2026, *Studies in Conservation*), on Jenny Holzer's *Survival: UNEX Sign*, is a direct example of this methodology, with data sources explicitly listing "Interviews with conservators, curators, and technicians" (p.1 [full text]), for a single-work case. This methodology aligns closely with restoration case studies of other software-based or media-installation works submitted to the same journal.

**Analytic procedure**:
1. Collect and compare historical documentation against the surviving object.
2. Interview the artist (if living) or technicians/curators familiar with the work's installation history to identify work-defining attributes.
3. Evaluate feasible preservation paths against the Variable Media four strategies.
4. Document the decision process itself.

**Quality criteria**: no psychometric criterion; the core criteria are the **completeness of the evidentiary chain** and **transparency of the decision process**. Laurenson states, "it may be that we cannot prevent the loss of some properties of a work but these should be named as losses" [full text].

**Reporting standards**: *Studies in Conservation* has no mandatory reporting checklist of its own, but convention includes technical specifications, a restoration timeline, a brief methods account, and the rationale for decisions.

**Common reviewer objections and misuses**: "how do you know your judgment of the work-defining properties is correct, and where does your own interpretation end?"; treating "does it still run" as the sole success criterion, ignoring that the physical medium itself may be part of a work's defining properties.

**Acceptance and conventions in the venues above**: *Studies in Conservation* explicitly welcomes case-study submissions, showing the journal treats a restoration/treatment account itself as a publishable research form.

**Resources and ethics**: requires cooperation and permission from the holding institution and the artist (or estate); interviews with living artists usually require research-ethics consent; irreversible interventions require particular caution.

**Common combinations**: inseparable from card 7 (documentation methods); often paired with card 9 when dealing with artist intent and meaning.

**When not to use it**: when the research object is a fully functioning work with no urgent risk of obsolescence, straightforward technical documentation is sufficient.

**Key sources**:
1. Laurenson, P. (2006). Authenticity, Change and Loss in the Conservation of Time-Based Media Installations. *Tate Papers* (6). Full text: https://www.tate.org.uk/research/tate-papers/06/authenticity-change-and-loss-conservation-of-time-based-media-installations [full text, web]
2. Laurenson, P. (2016). Old Media, New Media? Significant Difference and the Conservation of Software-Based Art. In B. Graham (Ed.), *New Collecting*. Routledge. DOI: 10.4324/9781315597898-4. **Not read in full for this port** [bibliographic entry only]
3. Variable Media Network. *Variable Media Network — welcome*. https://www.variablemedia.net/e/welcome.html [full text, web]
4. Rinehart, R., & Ippolito, J. (2003). *Permanence Through Change: The Variable Media Approach*. Guggenheim Museum Publications. **Bibliographic entry only** [bibliographic entry only]
5. Balagopal, L., & Chin, Z. (2026). "In a Dream You Saw a Way to Survive": Obsolescence as Ensemble in Jenny Holzer's *Survival: UNEX Sign*. *Studies in Conservation* 71(sup1), 1-7. DOI: 10.1080/00393630.2025.2610019. Local library [full text]

---

### D-9 Critical and interpretive approaches (work analysis, theoretical interpretation, media archaeology)

**Name**: Interaction/Design Criticism; Humanistic HCI; Media Archaeology.

**What questions it can answer**: "in what theoretical context can this work/system be meaningfully interpreted?"; "what cultural, political, or aesthetic assumptions does this work's formal choices reveal?"

**Epistemological stance and scope of claims**:
- Bardzell and Bardzell (2015), *Humanistic HCI*, position **interaction criticism** as a rigorous interpretive method: "We understand design criticism as referring to rigorous interpretive…" (the sentence is cut off at this point in the local file; the remainder was **not found**) (around p.567 [full text, sentence cut off in the source]). It places this method alongside "interpretation, hermeneutic analysis" and a "hermeneutics of suspicion" [full text].
- **Can support**: interpretive arguments about a work's meaning, cultural context, or theoretical positioning, whose force depends on argument and theoretical grounding; statistical significance plays no role here. **Cannot support**: empirical claims such as "most viewers interpret the work this way."
- Reflexive positioning is itself treated as part of the argument, following Bardzell's view that disclosing "who is speaking" at the outset folds the author's positionality into the argument itself.
- An earlier foundational text, Bardzell and Bardzell's "Towards a Feminist HCI Methodology," argues social-science and feminist theory can contribute to how HCI handles social-change questions (local library [full text, abstract and introduction only]).

**Data and sample**: the object of analysis is the work itself; no human subjects are involved. There is no sampling logic — the justification is the representativeness or typicality of the chosen object.

**Analytic procedure**: close reading of the artefact; situating the work within a specific theoretical frame; media archaeology treats a technical object itself as an archaeological object (as in card 7's Montfort et al., 2012).

**Quality criteria**: no psychometric criterion; the core criteria follow the humanities tradition — rigor of argument, appropriateness of theoretical grounding, and fidelity of interpretation to the details of the work.

**Reporting standards**: no formal reporting standard; journal convention expects a clear account of why a theoretical frame and object were chosen.

**Common reviewer objections and misuses**: "has this interpretation overreached — could a different theoretical frame tell an opposite story?"; using theoretical terms as decoration without advancing understanding; a reflexive disclosure that is merely a formal gesture.

**Acceptance and conventions in the venues above**: high acceptance for interpretive/theoretical work at Leonardo and Technoetic Arts; the Humanistic HCI lineage has gradually built its own methodological legitimacy at DIS; IUI/CHI's empirical track accepts this less readily.

**Resources and ethics**: mainly reading and writing time; human-subjects ethics review is usually not needed; critical assessment of a living artist's work needs care for scholarly fairness and citation accuracy.

**Common combinations**: often paired with card 3 and card 8; often uses card 4 as an opening methodological move.

**When not to use it**: when the research question needs empirical evidence to support a claim about what most people think.

**Key sources**:
1. Bardzell, J., & Bardzell, S. (2015). Humanistic HCI. *interactions* 22(3). Local library [full text]
2. Bardzell, S., & Bardzell, J. (2011). Towards a Feminist HCI Methodology: Social Science, Feminism, and HCI. *CHI 2011*. Local library [full text, abstract and opening only]
3. Montfort, N., et al. (2012). *10 PRINT CHR$(205.5+RND(1)); : GOTO 10* (see card 7, source 2).

---

## Group D cross-method issues

**1. The scope of a knowledge claim: the tension between relevance and validity**

Running through cards 1, 3, and 5 is a core methodological stance — the framework shift Zimmerman et al. (2007) proposed and that has since been widely borrowed across art and design practice research: moving the evaluative benchmark from *validity* to *relevance* ([full text], see card 1). Borgdorff (card 3) expresses a similar stance by arguing "research in the arts" should be equal to "research on the arts," while **explicitly rejecting** the idea that "art knowledge is special" exempts it from methodological scrutiny. The distinction to hold onto most carefully when submitting practice-research papers: **claiming relevance does not mean abandoning rigor** — it means adopting a different set of rigor criteria (traceability of process, adequacy of theoretical grounding, transparency of reflexivity), which still need to be stated explicitly; simply waving them away with "this is art, so it doesn't need explaining" will not do.

**2. How to get accepted at SIGGRAPH Art Papers / Leonardo / DIS Pictorials / ISEA**

According to the author's venue notes (checked 2026-06-05; calls change every year, so verify against the current call):
- **ISEA's art track does not require statistics**, accepting a portfolio, proposal, and video documentation.
- **DIS** has a formal RtD track and Pictorials (12 pages, visually driven, roughly 25% acceptance), but still expects strong qualitative rigor; LLM-assisted coding carries a "three-requirement" note (the companion guide already covers this in more detail; it is not repeated here).
- **SIGGRAPH Art Papers long-form submissions are the exception to the exception**: the call explicitly favors validated protocols plus human-impact evaluation, meaning an annotated portfolio in the style of card 1 is not sufficient on its own — it must be supplemented with card 6 or P-A-style evidence. This matters, for example, when choosing an argumentative strategy for a series of related artworks submitted to a venue: confirm first whether the format is short-form (more lenient) or long-form (requiring a validating evidence layer).
- **Leonardo** accepts theoretical-interpretive work (card 9) and practice-based work (card 2) readily, and is where several of this card's "bibliographic entry only" sources (e.g., Candy & Edmonds, 2018) were actually published.

**3. How to respond when quantitatively oriented reviewers question artistic research**

Three commonly used response strategies:
- **Reframe the benchmark**: invoke Zimmerman et al.'s relevance/validity distinction while proactively stating what criteria the work's own methodology uses (process, invention, relevance, extensibility; or Höök & Löwgren's contestable/defensible/substantive) — it is not enough to say "your standard doesn't apply" without offering a replacement.
- **Equal but not privileged**: invoke Borgdorff's position, avoiding "this is art" as a blanket excuse to dodge methodological scrutiny.
- **Honestly state limitations**: invoke Laurenson's (card 8) spirit — proactively stating sample logic, plausible alternative readings, and built-in limitations is more persuasive than avoidance or over-defense.

**⚠️ This card's weakest points (disclosed honestly)**:
1. Card 6's NIME evaluation dispute (Barbosa et al., 2015) **could not be located at all** — its existence is recorded from general field awareness only, with no claim made about its content.
2. Several key sources in cards 4 and 5 are **confirmed only bibliographically, with no full text read** — anyone using this should fetch full texts before citing these works' specific arguments directly.
3. The local library was found to contain at least one **filename that does not match its content**; a systematic filename/content audit of the whole library is recommended.
4. Card 3's Nelson (2013) and card 7's Löwgren (2013) / Montfort et al. (2012) were checked only for title/table of contents/existence — **sentence-by-sentence verification is still outstanding**.

---

Sources: see the key-sources list in each card.

## Known issues found during integration review

Several of these were fixed in the author's own statistics playbook; the cards below still carry the original wording where noted.

### Contradictions between cards

| # | Issue | Card numbers and original wording | Effect on decisions |
|---|---|---|---|
| 1 | Whether to justify qualitative sample size by "saturation" | C-1: "qualitative and quantitative data each justify their sample logic independently (qualitative = saturation/case-selection logic, quantitative = power analysis)"<br>B-1: "Braun & Clarke explicitly recommend against using 'saturation' to justify sample size in reflexive TA"<br>B cross-method: "for reflexive TA, replace saturation language with information power or a design rationale; for grounded theory, saturation is a built-in theoretical-sampling stopping rule" | C-1 treats "qualitative" as one sampling logic, too broadly. Per B's decision rule, route by analysis method: reflexive TA uses information power, grounded theory uses theoretical saturation, case study uses case-selection logic |
| 2 | Sample-size stopping rule for content analysis (within Group B) | B cross-method: "for content analysis/reliability-coding methods, saturation is a defensible traditional stopping rule"<br>B-7: "sample-size justification can partly borrow the logic of covering all known categories, not just information power or saturation" | Not strictly incompatible, but pick one framing consistently in a methods section rather than mixing both |
| 3 | Coding-agreement threshold | B-1: "use a structured codebook, multiple independent coders, and a statistical reliability coefficient (Cohen's Kappa, commonly >.80)"<br>A-6 (citing the companion guide): "inter-rater reliability, κ ≥ .61 as a starting point" | The two thresholds differ substantially and neither is sourced. Find independent support before adopting either |
| 4 | Which agreement coefficient to use (within Group A) | A-6, citing Hayes & Krippendorff (2007): "the conclusion is that Krippendorff's alpha is best suited as the standard," noting κ "has the effect of punishing observers for agreeing on the frequency distribution of categories"<br>A-6 (citing the guide's §3): "2 raters, categorical = Cohen's κ; 3+ raters = Fleiss' κ; continuous = ICC; Krippendorff's α works across all cases" | The same card argues for α while reproducing a κ-default quick-reference. The side with an actual sourced quote favors α |
| 5 | Can COREQ be applied to text or content analysis | A-6: "qualitative coding follows COREQ/SRQR"; A-7: same for human coding preprocessing<br>B-8: "COREQ explicitly covers focus groups"<br>B-12: "COREQ was designed for interviews and focus groups; forcing it onto survey data leaves items inapplicable" | Applying COREQ to text, logs, or survey coding leaves items inapplicable; A-6/A-7 should read "SRQR, or the applicable COREQ items with a note on inapplicable ones" |
| 6 | How many requirements for LLM-assisted coding | D cross-method: "three requirements"; B cross-method and A-6: "seven requirements" | Source is the companion guide's own internal inconsistency (see below); use seven, and note it is an internal compilation |
| 7 | Primary analysis for a single-item Likert scale | A-1: "use clmm, not ARTool"; A-9: "Wilcoxon plus an ordinal robustness check" | Primary-analysis and robustness-check roles are swapped; source is an inconsistency in the companion guide itself (see below) |
| 8 | Whether small classes should run inferential statistics | C-3: "using inferential statistics on samples of a handful to a dozen"; A-2: "pre/post differences via lmer or a paired test"; A cross-method: "even limited resources and an explicit lack of rationale are legitimate, if weaker, paths for sample-size justification" | A's position is "you can run it, but state the rationale and downgrade the claim"; C-3 has no source and leans toward "shouldn't." Favor A's sourced version, while anticipating C-3's objection from education-venue reviewers |
| 9 | Does an educational intervention need ethics review | A-2: "IRB review can often qualify for expedited review or partial exemption, but grades or personal data still need an application"; C-3: "most Teaching Practice Research Program projects do not require external IRB" | Neither statement is sourced; neither should be used as grounds for skipping review |
| 10 | Should artistic research claim a unique methodology (two sources within D-3) | D-3 citing Borgdorff: art knowledge's uniqueness "does not justify any unique methodology"<br>D-3 citing Haseman: performative research is a "third paradigm" that rejects translating practice into numbers/words | The D cross-method section picks Borgdorff as the defensive framing; citing both in the same paper is a genuine conflict — pick one |
| 11 | Source of consequential validity | C-2: "Messick's 1992 consequential validity" (no source entry)<br>A-4: Messick (1995), read in full, proposes six validity facets including the consequential facet | Cite the 1995 source per A-4 |
| 12 | Internal cross-reference errors | Group C framework 1 points RtD/DBR/DRM to "cards 2 and 4" (RtD is actually D-1); C-8 refers to a "section 9" that does not exist in Group C; B-11 misdescribes B-7; A-9 misattributes a quote to the wrong section of the companion guide | Does not affect the method judgments, but needs correcting on merge or cross-references will point the wrong way |

### Contradictions between cards and the method decision guide

| # | Issue | Guide's original wording | Card's original wording | Recommendation |
|---|---|---|---|---|
| 1 | Always justify qualitative sample size by saturation | Guide: "sample-size legitimacy = saturation, not statistical power... no new codes for 2–3 consecutive interviews" | B-1, B cross-method: reflexive TA should avoid claiming saturation, use information power instead | The guide needs to route by analysis method; the "2–3 consecutive interviews" figure also has no source |
| 2 | Always requiring dual-coder reliability for qualitative work | Guide pipeline: "...→ dual-rater IRR" | B-1 (citing thematicanalysis.net): "we do not advocate using a coding frame, nor do we advocate calculating inter-coder reliability scores" | The guide applies a coding-reliability default to all qualitative work; for reflexive TA this should be replaced with a reflexivity/consistency account |
| 3 | Which kind of thematic analysis the pipeline maps to is unstated | Guide: "LLM initial thematic scan → ... → Claude-assisted coding" | B cross-method: an LLM-then-researcher-confirms workflow is actually closer to a coding-reliability or codebook approach, not organic reflexive coding | The guide should note which approach this pipeline belongs to; it should not simply be applied to reflexive TA |
| 4 | Scope of COREQ's applicability | §2.5: "education journals often specify COREQ" | B-1: COREQ's defaults are incompatible with reflexive TA's stance; B-12: survey data leaves COREQ items inapplicable | §2.5 should flag this tension before submitting reflexive TA to a COREQ-requiring journal |
| 5 | Number of LLM-coding requirements (internal to the guide) | §2 table: "three requirements"; P-D: seven total | A-6 and B cross-method list seven; D cross-method still uses three | Change the §2 table to seven, or point it to the fuller section |
| 6 | Single-item Likert (internal to the guide) | P-A: clmm as primary; P-G: Wilcoxon as primary | A-1 follows P-A; A-9 follows P-G | Unify which is primary and which is the robustness check |
| 7 | Source of the ART warning | Guide: Tsandilas, *JoVI* 2024, verified 2026-06-07 | A-1: gives the journal as *Journal of Vision*, and could not locate the full text | Do not copy A-1's bibliographic entry into a manuscript; obtain the original before citing the ART rule |
| 8 | Content of Remy et al. (2020) | Guide P-C: creative tools don't necessarily need statistical evaluation, but the evaluative logic must be stated | D-6: not read in full, bibliographic entry only | The guide's summary currently has no verified original-text support; read the original before citing |
| 9 | Which reporting standard applies to a wait-list control | §2.5: non-randomized intervention (wait-list) → TREND | A-1: random assignment → CONSORT; A-2: a randomized stepped-wedge design is an intermediate form | If the wait-list is actually randomized, use CONSORT (CONSORT-SPI for social/psychological interventions); §2.5 should add this condition |
| 10 | Reviews only list PRISMA 2020 | §2.5: systematic review/meta-analysis → PRISMA 2020 | C-8: PRISMA-ScR is the first choice for scoping reviews | §2.5 should add a PRISMA-ScR row |
| 11 | S0 diagnostic numbers written up as a general rule | Guide §0: a diagnostic is only as good as the declared data-generating process; it shows "how the design behaves under this model," not "how the world is" | A-2 and A cross-method state specific numbers ("40 matched controls beats 80 more treatment participants") as a general conclusion | The cards overreach beyond the guide's own stated limit. A new topic should rerun its own declared model rather than reuse these numbers |

> **Status as of this integration review**: rows 1–6 and 8–11 above have already been fixed in the author's own statistics playbook (routing qualitative sample size and agreement coefficients by analysis method, unifying LLM-coding requirements to the seven-item version, fixing the single-item Likert primary/robustness relationship, flagging the Remy summary as unverified, switching to CONSORT for a randomized wait-list, adding PRISMA-ScR, and noting the S0 numbers apply only to that declared model). Row 7's journal-name mismatch has been corrected and the page confirmed to exist (full text still unread). The cross-reference errors above have been fixed, and the overreaching general-rule language has been rewritten. The remaining rows are open issues — keep them in mind when making decisions.

### Passages with clearly insufficient evidence — do not rely on these for decisions

| Card | Passage | Why it can't be relied on |
|---|---|---|
| A-1 | Claim that ART inflates Type I error for discrete DVs | Admittedly a secondhand citation with no original text found; journal name conflicts with the guide |
| A-2 | Claims about education-journal and HCI-venue acceptance of single-group pre/post designs | No source given |
| A-2, A cross-method | Specific power/coverage numbers and the "40 vs. 80" conclusion | Drawn from a single design under a single declared model, not an empirical literature result; should not be treated as a general rule |
| A-3 | "Top venues have in recent years rarely accepted pure survey studies" | No source; the common-method-variance citation is confirmed to exist but not read |
| A-4 | The 5–10-per-item, 200–300-total rule of thumb for EFA | No source (the card itself notes this rule of thumb is contested) |
| A-5 | The "over 40–50%" attrition threshold; the basis for multilevel models | No source for the threshold; the cited corpus-linguistics text is not longitudinal-design literature |
| A-6 | The "fewer than 30–50 texts" threshold; a citation checked only at the title level; the seven LLM-coding requirements | No source for the threshold; the seven items are an internal compilation |
| A-7 | The whole card, especially the "fewer than 20–30 events" threshold and the ENA/sequence-analysis/SNA claims | The card itself admits this is its weakest evidentiary basis |
| A-8 | The venue-acceptance passage | No source |
| A-9 | The "no single right answer" argument; paired comparison; a creativity-assessment technique; CSI | The first has an internal-note basis, not literature; the rest are checked only at the fragment/abstract level |
| B-1 | A bibliographic entry with an inconsistent DOI prefix; three critique papers | The bibliography is internally inconsistent; none of the three were read in full |
| B-1 | The claim that art tracks "typically do not require" a reflexivity statement | No source |
| B-2 | Procedural and epistemic differences among grounded-theory schools | Read only at the abstract level; none of the original grounded-theory texts were read |
| B-3 | The whole card, including a case-count range | Apart from one comparison passage, no original text was read; the range has no source |
| B-4 | The whole card | Both sources are bibliographic-only |
| B-5 | Differences among case-study approaches | None of the three original texts were read |
| B-7 | Content-analysis approaches | Both cited sources are abstract-only |
| B-8 | The core claim and a participant-count figure | Abstract-only; the count has no source |
| B-9 | A "5–8 people" rule of thumb; contextual inquiry | The rule of thumb has no source; the method reference was found only as course notes |
| B-10 | A methodological position attributed to a 2003 paper | Based on a literal reading of the title only |
| B-11 | A three-level framework of meaning | Confirmed only via a book review |
| B-12 | The core claim of the whole card | The sole source was read only at the abstract level; this card is cited widely and should be prioritized for full-text follow-up |
| Group B cross-method | Several sourced claims about qualitative rigor criteria | Some figures could not be located; some are paraphrased from disciplinary consensus; two citations are bibliographic only. Search tools were unreachable during part of this card's verification |
| C-1 | The six GRAMMS items | Not verified verbatim against the original |
| C-2 | The three-phase model; conjecture mapping | Phase names follow secondary sources; one source is on file but unread |
| C-3 | Claims about IRB exemption; a quoted sentence; the official review criteria | The first has no source; the second is a search-result fragment; the criteria could not be located |
| C-5 | A participant-count figure; venue-acceptance claims | Both without a source |
| C-6 | The 10–30-expert range | The sole source was read only at the abstract level |
| C-7 | The lab/field/deployment trade-off argument | Confirmed only bibliographically and by chapter title |
| C-8 | The PRISMA-ScR 20+2 items; a five-step process | Not verified against the original; cited only secondhand |
| D-1, A-9, D cross-method | Claims about SIGGRAPH Art Papers' and DIS Pictorials' review preferences | Both come only from the companion guide's internal verification dated 2026-06-05; CFPs change yearly — re-verify before submitting |
| D-1 | A 2014 bibliographic entry | Bibliographic entry only |
| D-2 | Two cited works | One is bibliographic only; the other was read only as a preview excerpt |
| D-3 | A quotation and a book reference | The quotation was corrected during this port's review; the book was checked only against its table of contents |
| D-4 | Three cited works and a quotation | The three are bibliographic entries only; the quotation was cut off in the source |
| D-5 | Two cited works' arguments; a third source | The first two are bibliographic-only, and the card itself calls its description "a reasonable inference"; the third was read only at the table-of-contents/preface level |
| D-6 | Several cited sources and figures | One is bibliographic only; one is a secondhand bibliographic citation; one could not be located; a participant-count figure has no source; reliability/validity was not verified |
| D-7 | Two cited works | Checked only for existence, not verified sentence by sentence |
| D-8 | Two web-captured sources; two bibliographic-only sources; a journal-acceptance claim | The web captures exist outside the shared local library and could become orphaned if moved; the acceptance claim is inferred from a single article — single-article evidence |
| D-9 | A definitional sentence; a claim from an internal writing-method document; a 2011 paper | The definitional sentence is cut off in the local file; the second item is not from the original source; the 2011 paper was read only at the abstract level |
| All cards | Local-library filenames | At least one file was found with a filename that does not match its content; a filename alone cannot serve as evidence |

### Methods the four card sets don't cover, but that the index needs

| Missing method | Where the index needs it | Current state in the cards |
|---|---|---|
| Semi-structured/in-depth interviewing (the data-collection method itself) | Needed in several places in the decision index | Group B's cards are all analysis methods; no card covers interviewing itself |
| Narrative inquiry/narrative analysis | Needed in the index | Mentioned only in passing |
| Single-case experimental design | Needed where an effect is claimed from just one person or one class | Only a reporting-standard mention, no design/analysis content |
| Equivalence/non-inferiority testing, Bayesian analysis | Needed when a study wants to claim "no difference" | Only in the companion guide, no card |
| Computational image metrics (distributional distance and aesthetic-quality indicators) | Needed for claims about differences in image-based work | Deferred to the companion guide, no card on what claims it can and cannot support |
| Secondary analysis of existing data | Needed in the index | Only the risks of retrospective analysis are discussed, no card on the method itself |
| Pilot/feasibility studies | Needed in the index | No card exists |
| Usability testing and heuristic evaluation | Needed for tool/system work | Covers only think-aloud protocols; other tools appear only in the companion guide |
| Audience research and exhibition observation | Needed for audience response in art venues | Pointed to but not actually covered |
| Archival and historical research, oral history | Needed in the index | Historical documents and interviews are listed as data sources, but no method card exists |
| Technical equivalence verification for a reconstructed or migrated work | Needed when claiming a reconstruction preserves a work's identity | Only the trade-offs among four preservation strategies are listed, no verification method |
| Validation of an LLM or model acting as a rater | Needed in the index | Neither the coding card nor the human-rater card directly addresses this |
| A single round of expert review | Needed when there isn't time for a full Delphi | Listed only as an alternative, with no content |
| Meta-analysis | Needed for pooling effects across studies | Only mentioned in passing; the tool itself is in the companion guide |
