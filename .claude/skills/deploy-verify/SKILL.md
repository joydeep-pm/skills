# Deploy & Verify Skill

Full deployment pipeline with verification gates for web and mobile.

## Pre-Deployment Checks

1. **TypeScript Compilation**: Run `npx tsc --noEmit` - fix all errors before proceeding
2. **Test Suite**: Run `node --test tests/*.test.js` - all tests must pass
3. **Build Verification**: Build locally first to catch issues early

## Web Deployment (Vercel)

1. **Local Build**: `npx vercel build` to verify build succeeds
2. **Deploy Command**: `npx vercel deploy --prod`
3. **If Deploy Fails**:
   - Do NOT retry blindly
   - Explain the exact error (auth, root directory, env vars)
   - Provide the specific Vercel dashboard URL and settings to change
   - List the manual steps needed
4. **Post-Deploy Verification**:
   - Curl the deployed URL and check for 200 status
   - Verify expected HTML content is present

## Android Deployment

1. **Prebuild**: `npx expo prebuild --platform android`
2. **Gradle Build**: `cd android && ./gradlew assembleRelease`
3. **If Build Fails**: Diagnose from Gradle error output and fix
4. **Installation**: Provide APK path and `adb install` command
5. **Device Setup**: Remind user to run `adb reverse tcp:8081 tcp:8081` for Metro connectivity
6. **Launch Verification**:
   - Check Metro bundler is serving
   - Verify no blank/white screen
   - Check for import errors or navigation issues

## Deployment Report

After completion, write DEPLOY_REPORT.md with:
- Build status (success/failure)
- Deploy URL or APK path
- Any manual steps user needs to take
- Known issues or warnings
- Verification results

Commit this report to the repo.
