# Example: Local AI That Can Actually Work

## Presentation intent
- **Audience:** technical leadership and engineering peers
- **Goal:** explain why the harness around a local model matters as much as the model itself
- **Desired outcome:** agreement to prototype a bounded local-agent workflow
- **Presenter stance:** raw model benchmarks do not predict whether long-horizon work will converge
- **Format:** paged sections

## Thesis
A capable local model becomes materially more useful when memory, context control, delegation, and validation are treated as one system rather than separate features.

## Narrative arc
Start with the surprising failure mode, show why model quality alone does not fix it, reveal the harness as the missing layer, then end on a concrete prototype rather than a broad AI vision.

## Source ledger
[S1] User brain dump — observed local-agent behavior — internal/user-supplied
[S2] Example benchmark URL — benchmark context — external

## Sections

### 01 — The model is not the product
- **Job:** break the assumption that a better benchmark score guarantees useful agent behavior
- **Audience takeaway:** convergence is a systems property
- **Visible headline:** A smart model can still spend 40 minutes going nowhere.
- **Visible support:**
  - Context drifts
  - Tools fail noisily
  - Recovery consumes the remaining window
- **Visual treatment:** large central sentence surrounded by a subtle expanding trace of failed tool/reasoning loops
- **Interaction:** reveal the failure trace on presenter click
- **Deep-dive drawer:** raw example log and benchmark reference
- **Talking points:** explain why each failure is individually survivable but compounds over long tasks
- **Evidence:** [S1], [S2]
- **Transition:** If intelligence is not sufficient, what layer turns it into reliable work?

### 02 — The harness is the behavior
- **Job:** introduce memory/context/delegation/validation as one operating loop
- **Audience takeaway:** reliability comes from the loop around the model
- **Visible headline:** Memory. Context. Delegation. Proof. One loop.
- **Visible support:** none; labels live inside the visual
- **Visual treatment:** animated system loop with four distinct operating stages and a central model node
- **Interaction:** each stage opens a short right-drawer explanation
- **Talking points:** keep the model interchangeable; preserve the operating contract
- **Evidence:** user-supplied design concept
- **Transition:** turn the architecture into one bounded experiment

## Design direction
- **Concept:** technical field manual meets premium product reveal
- **Mood:** dark, precise, tactile, slightly experimental
- **Palette:** near-black substrate, warm neutral text, one high-energy diagnostic accent
- **Typography:** compact technical labels + strong editorial display headlines using offline-safe stacks
- **Composition:** large spatial diagrams alternating with sparse thesis sections
- **Motion:** traces draw through system diagrams; section changes use restrained depth shift
- **Navigation feel:** left rail resembles a system index, not a slide thumbnail list
- **Imagery / diagrams:** mostly inline SVG and real log excerpts
- **Signature moment:** the initial failure trace collapses into the four-stage harness loop
- **Avoid:** generic AI gradient cards and benchmark-table overload

## Open questions / assumptions
- Which benchmark or production log can be shared with this audience?

## Parking lot
- Full model comparison table
- Raw task transcripts
- Cost calculations
