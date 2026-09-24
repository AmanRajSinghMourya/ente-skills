---
name: migrate
description: Move Ente mobile screens or packages from ente_ui to ente_components, or do a similar design-system migration, without changing behavior. Use for /migrate or any ente_ui to ente_components task.
---

# Design-system migration

1. **Pin the current look and behavior first:** before-screenshots of the
   screen's states (light and dark, empty, error, loading) on a simulator,
   plus any existing widget tests.
2. **Find the precedent:** a screen in the same app that's already migrated.
   Copy its shape.
3. **Rules:**
   - Use `TextStyles` tokens as they are. No `.copyWith(color: colors.textBase)`,
     `.copyWith(fontWeight: …)` or `.copyWith(height: …)`; pick the closest
     token. Use `copyWith(color:)` only for a genuinely different color. Icons
     keep an explicit `color: colors.textBase`.
   - Keep `showToast`, `createProgressDialog` and `AndroidTextInputAutofocus`
     from `ente_ui` when there's no clean 1:1 component. Don't hand-roll
     replacements.
   - Submit buttons follow the Photos login pattern in
     `mobile/apps/photos/lib/ui/account/login_pwd_verification_page.dart`: a
     `ButtonComponent` that's always present as the `floatingActionButton`, with
     `centerFloat` and no custom animator. Don't restore `DynamicFAB`, and don't
     hide the button when the keyboard opens.
   - In a `BottomSheetComponent`, drop buttons that only dismiss (the sheet
     already has an X). Keep real actions.
   - A shared package imports from `ente_ui`, never from an app's local copy.
4. **Migrate one screen at a time, fully.** Never leave a screen half-migrated.
5. **After-screenshots** of the same states. Every difference is either intended
   by the design or gets fixed.
