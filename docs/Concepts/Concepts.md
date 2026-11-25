---
type: index
updated: 2026-11-24
---

# Concepts

The things this project is about. Every finding, decision and play links to the concepts it touches, so each concept is a hub in the Obsidian graph. Thin hubs show where work is missing.

## Goal objects: what the play data must locate

| Concept | Status | What it is |
| --- | --- | --- |
| [Player body](player-body.md) | located | Where each player's body is on every frame |
| [Head](head.md) | located | Where each player's head is and which way it faces |
| [Hands](hands.md) | partly located | Where each player's hands are |
| [Feet](feet.md) | partly located | Where each player's feet are |
| [Ball](ball.md) | partly located | Where the ball is on every frame, and who holds it |
| [Referees](referees.md) | not located | Where each official is |

## Pipeline stages: how video becomes play data and a render

| Concept | Status | What it is |
| --- | --- | --- |
| [Cameras](cameras.md) | working | Both cameras' position, orientation and lens on every frame, and the time offset between the two clips |
| [Tracking](tracking.md) | working | Detecting people in each view, following them through time, and pairing a sideline track with the endzone track of the same person |
| [Identity](identity.md) | working | Who each track is |
| [Placement](placement.md) | working | Where each body stands on the field on every frame |
| [Pose](pose.md) | working | Each body's joints |
| [Play events](play-events.md) | partly working | The moments that structure a play |
| [Render and viewer](render-and-viewer.md) | working | Layer 4 |
| [Play data](play-data.md) | not built | Layer 1's single output |

## Measures: how results are judged

| Concept | Status | What it is |
| --- | --- | --- |
| [Census](census.md) | in use | The count of bodies drawn per team against 11, per frame |
| [Reprojection error](reprojection-error.md) | in use | How far a 3D point, projected back into a camera, lands from what that camera saw, in pixels |
| [Plausibility rulers](plausibility-rulers.md) | in use | Checks that the motion is physically possible |
| [Footage review](footage-review.md) | in use | Checking the drawn bodies against the real footage, frame sequence by frame sequence |
