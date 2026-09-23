---
name: perf
description: Fix Ente slowness, jank, memory growth or battery drain against a measured baseline, not a guess. Use for slow screens, dropped frames, OOM or memory, slow startup, slow sync or uploads, or /perf.
---

# Performance

1. **Name the number:** one metric with a unit, and how you measure it. Options
   include frame build and raster times (Flutter DevTools,
   `flutter run --profile`), startup time, memory (Xcode Instruments or
   `adb shell dumpsys meminfo`), sync or upload duration, and API latency.
2. **Baseline** on a profile or release build, never debug, on the same device,
   over a few runs. Record the spread.
3. **Form hypotheses from the trace,** not from reading code. Common causes:
   - work nobody needs: delete it
   - repeated work: cache it, and name what invalidates the cache
   - many small operations: batch them
   - work on the UI isolate: move it to a background isolate or later
   - loading everything up front: load lazily
   - work at the wrong moment: schedule it after the first frame
4. **One change at a time.** Measure after each. Keep it only if the number
   moves; revert what didn't help.
5. **Report** before and after with the unit, device and build mode, plus the
   trace or profile you used.
