# Chrome Extension Packaging Guide

## Preparing for Distribution

### 1. Update Manifest

Ensure `manifest.json` has correct version and permissions:

```json
{
  "version": "1.0.0",
  "name": "FlowFacilitator Helper",
  "description": "Blocks distracting websites during flow states"
}
```

### 2. Create Extension Icons

Create icons in the following sizes:
- 16x16 px - Toolbar icon
- 48x48 px - Extension management page
- 128x128 px - Chrome Web Store

Save as PNG in `chrome-extension/icons/` directory.

### 3. Package Extension

#### For Development/Testing

1. Open `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select `chrome-extension/` directory

#### For Distribution (ZIP)

```bash
cd chrome-extension
zip -r ../flowfacilitator-extension-v1.0.0.zip . -x "*.DS_Store" -x "__MACOSX"
```

#### For Chrome Web Store

1. Create a ZIP file (as above)
2. Go to [Chrome Web Store Developer Dashboard](https://chrome.google.com/webstore/devconsole)
3. Click "New Item"
4. Upload ZIP file
5. Fill in store listing:
   - Name: FlowFacilitator Helper
   - Description: (see below)
   - Category: Productivity
   - Language: English
6. Upload screenshots
7. Submit for review

### 4. Store Listing Description

**Short Description** (132 characters max):
```
Block distracting websites during flow states. Stay focused, build resilience, and track your productivity with RPG-style stats.
```

**Detailed Description**:
```
FlowFacilitator Helper is the Chrome extension companion to FlowFacilitator, 
a privacy-first productivity tool that detects and amplifies your flow states.

FEATURES:
• Automatic distraction blocking when you're in flow
• 10-second countdown before unlock (build willpower!)
• Beautiful blocked page with motivational messages
• Resilience tracking for resisting distractions
• Whitelist support for urgent access
• Pause protection temporarily (10 min)
• Block attempt statistics

HOW IT WORKS:
1. Install the FlowFacilitator macOS agent
2. Install this extension
3. Set up native messaging (one-time setup)
4. Start working - the agent detects when you enter flow
5. Extension automatically blocks distracting sites
6. Build your Resilience stat by staying focused!

PRIVACY:
• No data collection
• No tracking
• Works entirely locally
• Open source

REQUIREMENTS:
• FlowFacilitator macOS agent (free, open source)
• macOS 12.0 or later
• Native messaging setup (instructions provided)

Get the agent at: https://github.com/shyamolkonwar/flow-state-ai

PERMISSIONS:
• declarativeNetRequest: To block distracting websites
• storage: To save your settings and statistics
• nativeMessaging: To communicate with the macOS agent

This extension is part of the FlowFacilitator ecosystem. It works best 
when paired with the macOS agent and dashboard for complete flow state 
detection and analytics.
```

### 5. Screenshots

Create screenshots showing:
1. Extension popup with status
2. Blocked page with countdown
3. Settings/whitelist management
4. Statistics display

Recommended size: 1280x800 or 640x400

### 6. Privacy Policy

Link to: `https://github.com/shyamolkonwar/flow-state-ai/blob/main/docs/privacy.md`

### 7. Support & Contact

- **Website**: https://github.com/shyamolkonwar/flow-state-ai
- **Support Email**: (your email)
- **Issues**: https://github.com/shyamolkonwar/flow-state-ai/issues

## Testing Before Submission

### Checklist

- [ ] Extension loads without errors
- [ ] All permissions are necessary and justified
- [ ] Icons display correctly (16px, 48px, 128px)
- [ ] Popup UI works properly
- [ ] Blocked page displays correctly
- [ ] Native messaging connects (with agent running)
- [ ] Blocking rules are created/removed correctly
- [ ] Statistics are tracked accurately
- [ ] No console errors
- [ ] Manifest version is correct
- [ ] Description is accurate
- [ ] Screenshots are clear and representative

### Test Scenarios

1. **Fresh Install**: Install extension on clean Chrome profile
2. **Blocking Test**: Verify sites are blocked when commanded
3. **Whitelist Test**: Add site to whitelist, verify it's not blocked
4. **Pause Test**: Pause protection, verify all sites accessible
5. **Statistics Test**: Verify block counts increment correctly
6. **Native Messaging**: Test connection with agent

## Chrome Web Store Review Process

### Timeline
- Initial review: 1-3 business days
- Updates: Usually faster (hours to 1 day)

### Common Rejection Reasons
1. **Permissions**: Requesting unnecessary permissions
2. **Description**: Misleading or incomplete
3. **Functionality**: Extension doesn't work as described
4. **Privacy**: Not clear about data handling
5. **Icons**: Low quality or missing

### After Approval

1. Extension will be available at: `https://chrome.google.com/webstore/detail/[extension-id]`
2. Users can install with one click
3. Automatic updates will be pushed

## Updating the Extension

### Version Numbering

Follow semantic versioning:
- **Major** (1.0.0): Breaking changes
- **Minor** (1.1.0): New features, backwards compatible
- **Patch** (1.0.1): Bug fixes

### Update Process

1. Update version in `manifest.json`
2. Make changes
3. Test thoroughly
4. Create new ZIP
5. Upload to Chrome Web Store
6. Submit for review

Users will automatically receive updates within a few hours.

## Distribution Outside Chrome Web Store

### Enterprise/Private Distribution

1. Package as CRX file:
```bash
chrome --pack-extension=chrome-extension --pack-extension-key=key.pem
```

2. Host the CRX file
3. Create update manifest XML
4. Configure Chrome policy for auto-install

### Self-Hosted Updates

Create `updates.xml`:
```xml
<?xml version='1.0' encoding='UTF-8'?>
<gupdate xmlns='http://www.google.com/update2/response' protocol='2.0'>
  <app appid='YOUR_EXTENSION_ID'>
    <updatecheck codebase='https://yoursite.com/extension.crx' version='1.0.0' />
  </app>
</gupdate>
```

Add to manifest:
```json
"update_url": "https://yoursite.com/updates.xml"
```

## Analytics (Optional)

If you want to track usage:

1. Add Google Analytics to background script
2. Update privacy policy
3. Add permission to manifest
4. Disclose in store listing

**Note**: FlowFacilitator doesn't include analytics by default for privacy.

## Monetization (Future)

Options for future versions:
- Chrome Web Store payments
- Freemium model (premium features)
- Donations/sponsorships

Current version is 100% free and open source.

---

**Ready to publish?** Follow the checklist above and submit to Chrome Web Store!
