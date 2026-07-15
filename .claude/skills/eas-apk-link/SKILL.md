---
name: eas-apk-link
description: Build Android APKs with Expo EAS, upload for a shareable link, and keep RELEASE_NOTES.md updated automatically. Use when asked to create APK links, publish Android preview builds, or troubleshoot EAS upload/build commands.
---

# EAS APK Link Workflow

Use this workflow for React Native/Expo apps when the user asks for APK generation and a shareable link.

## Preferred one-command publish (auto release-notes update)

Run from project root:

```bash
cd "/Users/joy/Documents/Voice Journal"
npm run release:android:publish
```

This does all of the following:

1. Local Android APK build (`preview` profile)
2. `eas upload` for a shareable Expo build link
3. Auto-update of `RELEASE_NOTES.md` with build metadata

## Manual fallback

### Build local APK

```bash
cd "/Users/joy/Documents/Voice Journal"
mkdir -p ./output
NPM_CONFIG_CACHE=/tmp/npm-cache \
EAS_LOCAL_BUILD_SKIP_CLEANUP=1 \
EAS_LOCAL_BUILD_WORKINGDIR="" \
ANDROID_HOME="$HOME/Library/Android/sdk" \
ANDROID_SDK_ROOT="$HOME/Library/Android/sdk" \
PATH="$HOME/Library/Android/sdk/platform-tools:$HOME/Library/Android/sdk/emulator:$PATH" \
eas build -p android --profile preview --local --output ./output/voice-journal-preview.apk --non-interactive
```

### Upload local APK and get share link

Use `--build-path` (not `--path`).

```bash
cd "/Users/joy/Documents/Voice Journal"
npx --yes eas-cli@latest upload -p android --build-path ./output/voice-journal-preview.apk --non-interactive
```

### Update release notes manually (if needed)

```bash
cd "/Users/joy/Documents/Voice Journal"
BUILD_ID="<build-id>" \
SHARE_URL="https://expo.dev/accounts/joytdh/projects/voice-journal/builds/<build-id>" \
BUILD_PROFILE="preview" \
BUILD_SOURCE="manual" \
COMMIT_HASH="$(git rev-parse HEAD)" \
node scripts/update-release-notes.mjs
```

## Common fixes

### Free-plan remote build limit reached
Use local build + upload flow above.

### Upload argument error
Use:

```bash
npx --yes eas-cli@latest upload -p android --build-path ./output/voice-journal-preview.apk
```

### AI not working outside local Wi-Fi
Set public backend URL and token in EAS env for all envs:

```bash
cd "/Users/joy/Documents/Voice Journal"
BASE_URL="https://<your-public-domain>/ai"
TOKEN="<token>"

for ENV in production preview development; do
  npx --yes eas-cli@latest env:delete "$ENV" --name EXPO_PUBLIC_AI_API_BASE_URL --non-interactive || true
  npx --yes eas-cli@latest env:delete "$ENV" --name EXPO_PUBLIC_AI_API_TOKEN --non-interactive || true

  npx --yes eas-cli@latest env:create "$ENV" --name EXPO_PUBLIC_AI_API_BASE_URL --value "$BASE_URL" --scope project --visibility plaintext --non-interactive
  npx --yes eas-cli@latest env:create "$ENV" --name EXPO_PUBLIC_AI_API_TOKEN --value "$TOKEN" --scope project --visibility sensitive --non-interactive
done
```

Rebuild after env changes.
