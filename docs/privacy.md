# Privacy Policy - FlowFacilitator

## Our Commitment to Privacy

FlowFacilitator is designed with privacy as a core principle. Your data belongs to you and stays on your device.

## What We Collect

### Data We DO Collect (Locally Only)

1. **Behavioral Timestamps**
   - Keystroke timestamps (timing only, NOT key content)
   - Mouse movement timestamps
   - Application switch events
   - Idle time measurements

2. **Session Metrics**
   - Flow session start and end times
   - Duration of focus sessions
   - Average typing rate (keystrokes per minute)
   - Application names used during sessions

3. **User Preferences**
   - Flow detection thresholds
   - Blocklist and whitelist domains
   - Dashboard settings

### Data We DO NOT Collect

❌ **Keystroke Content** - We NEVER record what you type
❌ **Screen Content** - We NEVER capture screenshots or screen recordings
❌ **Browsing History** - We NEVER track which websites you visit (except block attempts during flow)
❌ **Personal Information** - No names, emails, or identifying information
❌ **Location Data** - No GPS or location tracking
❌ **Cloud Sync** - No data sent to external servers

## Where Your Data is Stored

### Local Storage Only

All data is stored exclusively on your Mac in:
- **Database**: `~/Library/Application Support/FlowFacilitator/supabase/`
- **Logs**: `~/Library/Application Support/FlowFacilitator/logs/`
- **Config**: `~/Library/Application Support/FlowFacilitator/config.json`

### File Permissions

All data files are:
- Owned by your user account
- Readable/writable only by you (chmod 600)
- Not accessible by other users on your Mac

## How We Use Your Data

Your data is used solely to:
1. Detect when you enter a flow state
2. Protect your focus by blocking distractions
3. Show you analytics about your focus patterns
4. Improve your ability to maintain deep work

## Data Sharing

**We do not share your data with anyone. Period.**

- No third-party analytics
- No telemetry
- No cloud services
- No advertising networks

## Your Rights and Controls

### Complete Control

You have full control over your data:

1. **View All Data** - Access everything through the dashboard
2. **Export Data** - Download your data as CSV anytime
3. **Delete Data** - Permanently delete all data with one click
4. **Adjust Retention** - Configure how long data is kept

### Data Deletion

To delete all your data:
1. Open Dashboard → Settings
2. Click "Delete All Data"
3. Confirm deletion
4. All sessions, events, and logs are permanently removed

### Data Export

To export your data:
1. Open Dashboard → Settings
2. Click "Export Data"
3. Choose date range and format (CSV/JSON)
4. Download file to your chosen location

## Permissions Explained

### Why We Need Accessibility Permission

**Purpose**: To measure typing cadence and detect which app you're using

**What it allows**:
- Counting keystrokes (timing only)
- Detecting app switches
- Measuring idle time

**What we DON'T do**:
- Record key content
- Log passwords or sensitive text
- Monitor specific applications

### Why We Need Notification Permission

**Purpose**: To show helpful reminders and flow state notifications

**What it allows**:
- Display flow state entry/exit notifications
- Show micro-intervention prompts

**What we DON'T do**:
- Send marketing notifications
- Track notification interactions

## Security Measures

### Local Security

1. **Encrypted Storage** - Database files use macOS file encryption
2. **Access Control** - API tokens for dashboard access
3. **Localhost Only** - Dashboard and API bound to 127.0.0.1
4. **No External Network** - No internet connections required

### Code Security

1. **Open Source** - Code available for audit (planned)
2. **Signed App** - macOS code signing and notarization
3. **Regular Updates** - Security patches and improvements

## Data Retention

### Default Retention Policy

- **Raw Events**: 30 days (configurable)
- **Sessions**: 1 year (configurable)
- **Settings**: Indefinite (until you delete)
- **Logs**: 7 days (configurable)

### Automatic Cleanup

The app automatically:
- Deletes events older than retention period
- Compresses old logs
- Maintains database performance

### Manual Cleanup

You can manually:
- Delete individual sessions
- Clear all data before a certain date
- Reset to factory defaults

## Changes to Privacy Policy

If we update this policy:
- You'll be notified in the app
- Changes will be highlighted
- You can review before accepting

## Questions or Concerns

This is a local-only application, so there's no company collecting your data. However, if you have questions about how the app works:

- Review the technical documentation
- Check the open-source code (when available)
- Contact via GitHub issues

## Compliance

### GDPR Compliance

While FlowFacilitator doesn't transmit data, we respect GDPR principles:
- ✅ Data minimization - collect only what's needed
- ✅ Purpose limitation - use data only for stated purpose
- ✅ Storage limitation - configurable retention
- ✅ Right to erasure - complete data deletion
- ✅ Data portability - export in standard formats

### CCPA Compliance

California residents have the right to:
- ✅ Know what data is collected (see above)
- ✅ Delete personal data (Settings → Delete All Data)
- ✅ Opt-out of data sale (we don't sell data)

## Technical Details

### Data Format

All data stored in:
- **PostgreSQL** (via Supabase local)
- **JSON** configuration files
- **Plain text** logs

### No Tracking IDs

We don't use:
- Device fingerprinting
- Unique identifiers
- Tracking cookies
- Analytics SDKs

## Trust but Verify

We encourage technical users to:
- Review the database schema
- Inspect network traffic (should be localhost only)
- Audit file system access
- Examine the source code

---

**Last Updated**: January 2024
**Version**: 1.0.0

**Summary**: Your data never leaves your Mac. We don't collect, share, or sell your information. You have complete control.
