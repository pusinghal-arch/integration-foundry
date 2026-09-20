# Contributing

This foundry grows from real integration and architecture problems, not from padding a table of contents. Contributions are welcome if they meet that bar.

## Good contributions

- A reference architecture for a scenario not yet covered, written from something you actually built or fixed
- A correction to an existing architecture — a constraint that's missing, a diagram that's wrong, a tradeoff stated too simply
- An addition to the pattern catalog with a real example of where it broke down
- A fix to the dataset generators, or a new table that fills a gap
- A new Architecture Decision Record for a standing question this repository hasn't taken a position on yet — see `docs/decisions/` for the format and existing examples

## What doesn't fit here

- Vendor pitches or product placement dressed up as architecture
- AI-generated filler content with no domain grounding
- Restating public vendor documentation without adding judgment or a tradeoff

## Process

1. Open an issue first for anything larger than a typo fix, so we can agree on scope before you write 2,000 words.
2. Follow the structure of an existing document in the same folder (`docs/architectures`, `docs/decision-guides`, `docs/patterns`) — problem, context, architecture, tradeoffs, when not to use this.
3. Diagrams are Mermaid, inline in the Markdown file, not separate image exports — this keeps them diffable and renders correctly in both light and dark GitHub themes.
4. Submit a pull request. Expect editorial pushback on structure and claims, not just grammar.

## License of contributions

By submitting a pull request, you agree your contribution is licensed under the same terms as the file you're editing — [CC BY 4.0](LICENSE-DOCS.md) for `docs/`, [MIT](LICENSE) for code and data generators.
