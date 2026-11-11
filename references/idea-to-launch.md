# From an idea to a maintained product

## Choose the pace

For beginners, ask in everyday language: who is it for, what should they accomplish first, and where will they use it? Infer details from existing context. Explain one consequential decision at a time with a recommended option and costs/tradeoffs. Translate unfamiliar terms when first used. Do not ask a beginner to pick a database or framework without explaining why it matters.

For experienced builders, use their architecture, acceptance criteria and tools. Summarize assumptions and decisions compactly. Both paths use the same verification standard; expertise changes the explanation, not the safeguards.

## Define the first useful version

Write a short brief: audience, problem, core journey, platforms, sensitive data, required features, budget and exclusions. Choose one journey that proves the product helps someone. A portfolio may need no login or database. A marketplace needs identity, ownership and financial workflows. Separate a visual prototype from a working product in every progress report.

Generate planning files with `scripts/launch.py init` or write equivalent documents if Python is unavailable. The generated directory is project documentation; it does not contain a runnable application. Keep it private when filled with internal findings. Select only requested features; native platform checks are always selected for Android/iOS.

## Build a working slice

1. Inspect existing code and conventions. For a new product, choose a maintained stack suited to the target platform and hosting budget; check current official setup instructions. Record why it fits and how the owner can leave the provider. Do not force one stack across native apps and static sites.
2. Define the data model, ownership and authorization before implementing writes. Record a small architecture diagram and the trust boundaries. Create migrations, synthetic fixtures and configuration examples containing names only.
3. Sketch the essential screens and their loading, empty, failure and permission states. Use real accessible controls. Agree routine visual decisions from the user's style; do not stall on every detail.
4. Implement one complete UI-to-server-to-storage journey with real persistence where needed. Use development/sandbox services and distinguish simulated features clearly. Run the app and demonstrate the journey before adding more features.
5. Add selected feature guides and relevant R001-R100 controls as each boundary is built. Do not defer all security until the end. Integrate in small reversible steps and keep the project runnable.
6. Test the successful journey, hostile inputs, denied access, retries and recovery. Record commands, actual results, revision and environment. When a device/provider/tool is unavailable, record the specific blocked check rather than assuming it passed.
7. Prepare export and deployment using the handoff guide. Verify the deployed journey; a build or upload alone is not release evidence.

## Explain progress usefully

Report: what now works, how the owner can try it, what remains, and the next consequential decision. Use a small backlog ordered by user value and risk. Keep a decision log and separate bug reports from future ideas. When a requirement changes, update scope and affected checks before implementing it.

## Release and learn

Use both the numbered assessment and selected launch checks. An accepted exclusion needs a reason; a deferred or failing check is unresolved. A passing declaration gate is only a review aid: inspect the evidence and any omitted features before a release decision. Publish within the user's authorization, identify the operational owner, and leave recovery instructions. After release, collect minimal consent-respecting feedback and fix real failures before expanding scope.
