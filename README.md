# DSAIT4310 — Modeling and Data Analysis in Complex Networks

We use MovieLens `ml-latest` to study how ratings accumulate over time, how movies relate through content and shared audiences, and whether those relationships help recommend movies.

**Research question:** How do MovieLens users engage with movies over time, and how well do content and shared-audience patterns predict which movies a user will later rate positively?

**Status key**

- **Complete** — implemented in the existing notebooks.
- **Partial / needs update** — implemented in part or needs clearer justification, verification, or presentation.
- **Missing / needs adding** — new work. Optional checks are marked separately.

## 1. Accumulated rating patterns

- **Complete — Growth fits and forecast check.** For the 500 most-rated movies released from 2000 onward, use timestamped ratings to construct cumulative rating curves. Use the existing growth-model fits to describe the different curve shapes and the existing forecast check to show how well the early part of a curve predicts the later part. Interpret the results as patterns of rating activity. A rating timestamp records when a rating was submitted.

## 2. Content and audience movie networks

- **Complete — Graph construction and density sweep.** The Tag Genome and audience cosine graphs are built on the same 500 movies at 5%, 10%, 15%, and 20% density. Audience vectors indicate positive ratings of at least 3.5 stars.
- **Partial / needs update — Justification and comparison.** Explain why cosine normalizes shared-rater counts by audience size, what matching density controls, and why global thresholding can leave movies isolated. Use 15% for the main comparison and keep the other densities as sensitivity checks.
- **Missing / needs adding — Cosine versus dot product.** Build an audience graph using raw shared-rater counts at the same density and compare how the selected edges and degree distributions change.
- **Partial / needs update — Binary edge overlap.** The existing comparison measures whether the same movie pairs are retained. Report the overlap at 15% alongside the density sweep, labeling each result with its density.
- **Missing / needs adding — Degree-preserving null and similarity ranks.** Compare binary overlap with a degree-preserving rewiring baseline. Separately, compare the rankings of content and audience similarities across the same movie pairs before thresholding.
- **Complete — Louvain analysis.** Existing runs compare seeds, densities, and weighted versus unweighted partitions. Cross-network alignment and bridge analysis are also available.
- **Partial / needs update — Community interpretation.** Show cross-network ARI with explicit handling of isolates. Profile representative communities by genre and release era, and use example movies to illustrate where communities connect.
- **Missing / needs adding (optional) — Leiden comparison.** Repeat community detection on the same graphs and compare the partitions with Louvain.

## 3. Evaluate network-based recommendations

- **Complete — Retrospective holdout and baseline comparisons.** The recommendation notebook excludes evaluation users from audience graph and popularity construction. It seeds from positive ratings in each eligible user's first 80% of ratings, excludes all movies rated in that history from the candidates, and scores later positive ratings from the final 20%. It tunes on validation users and compares popularity, one-hop voting, and multi-step spreading on the same test users using NDCG@10 and recall@10.
- **Partial / needs update — Reproduce and present the evaluation.** Rerun the results table and document the eligibility filters, candidate set, and validation and test sizes. Show one test user from seed ratings through the top-10 list to the held-out outcomes. Scope the conclusions to retrospective ranking for active users in the 500-movie catalogue.
- **Missing / needs adding — Three-way recommendation outcomes.** For each method, report the average number of top-10 recommendations that received a later positive rating, received a later rating below 3.5, or had no observed rating in the holdout. Keep NDCG@10 and recall@10 alongside these counts. A missing rating leaves the user's response unknown.
- **Missing / needs adding — Downstream construction check.** Compare cosine and dot-product audience graphs at matched density using the same one-hop ranking method, candidates, and test users.
- **Missing / needs adding (optional) — Common calendar cutoff.** Select the catalogue and build the audience graph and popularity baseline using information available by one cutoff. Evaluate against ratings after that date.
