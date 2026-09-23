---
name: deps
description: Add or update a package in Ente safely. Check security advisories and breaking changes, dry-run first, and keep lockfile changes small. Use for any pubspec, Cargo, go.mod or package.json dependency change.
---

# Dependencies

1. **Is it needed?** Say why, and whether existing code or an existing package
   already does it. A new package needs Aman's OK in the plan.
2. **Advisories:**
   - Dart and Flutter: pub.dev advisories and the GitHub Advisory Database
   - Rust: RustSec and crates.io
   - Go: the Go vulnerability database (`govulncheck`)
   - JS: npm, the GitHub Advisory Database and Socket

   Read the changelog between the old and new versions for breaking changes.
3. **Dry run first:** `dart pub upgrade --dry-run <pkg>` or
   `flutter pub upgrade --dry-run <pkg>`, and `cargo update -p <crate>
   --dry-run`. For JS, install with scripts disabled (`--ignore-scripts`).
   Flutter commands may need permission to reach the SDK cache.
4. **Change only what's needed.** Read the lockfile diff for surprise transitive
   bumps.
5. **Build and run** the affected app's tests. Report the versions before and
   after, the advisories you checked, and anything unusual.
