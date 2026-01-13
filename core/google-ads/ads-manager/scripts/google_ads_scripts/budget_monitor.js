/**
 * Google Ads Script: Budget Monitor
 *
 * Monitors spend against monthly budget and takes action at thresholds.
 * Runs hourly for more responsive monitoring than daily Python checks.
 *
 * SETUP INSTRUCTIONS:
 * ====================
 * 1. In Google Ads, go to Tools & Settings > Bulk Actions > Scripts
 * 2. Click the + button to create a new script
 * 3. Paste this entire script
 * 4. Update the CONFIG section below with your values
 * 5. Click Preview to test
 * 6. Click Run to execute
 * 7. Set up hourly schedule:
 *    - Click the pencil icon next to the script name
 *    - Under "Frequency", select "Hourly"
 *    - Save
 *
 * NOTE: This script must be added to EACH account individually,
 * or run from an MCC with account iteration enabled.
 *
 * @author PhD Networks & Systems Ltd
 * @version 1.0
 */

// =============================================================================
// CONFIGURATION - UPDATE THESE VALUES
// =============================================================================

var CONFIG = {
  // Monthly budget in GBP
  monthlyBudget: 250.00,

  // Cycle start date (YYYY-MM-DD)
  cycleStart: '2026-01-08',

  // Cycle length in days (set to 0 for one-off budgets)
  cycleDays: 31,

  // Alert thresholds
  warningThreshold: 0.80,   // 80% - log only
  criticalThreshold: 0.95,  // 95% - send email
  pauseThreshold: 1.00,     // 100% - pause campaigns

  // Auto-pause enabled?
  autoPause: true,

  // Email for alerts
  alertEmail: 'daniel.doherty@phdnetworks.co.uk',

  // Account name (for email subject)
  accountName: 'Leeds Rendering'
};

// =============================================================================
// MAIN FUNCTION
// =============================================================================

function main() {
  Logger.log('=== Budget Monitor Started ===');
  Logger.log('Account: ' + CONFIG.accountName);
  Logger.log('Monthly Budget: £' + CONFIG.monthlyBudget.toFixed(2));
  Logger.log('Cycle Start: ' + CONFIG.cycleStart);

  // Calculate date range
  var cycleStart = new Date(CONFIG.cycleStart);
  var today = new Date();

  // Query spend for the period
  var spend = getSpendForPeriod(cycleStart, today);
  var percentUsed = spend / CONFIG.monthlyBudget;
  var remaining = CONFIG.monthlyBudget - spend;

  Logger.log('');
  Logger.log('=== Budget Status ===');
  Logger.log('Spend to date: £' + spend.toFixed(2));
  Logger.log('Budget remaining: £' + remaining.toFixed(2));
  Logger.log('Percent used: ' + (percentUsed * 100).toFixed(1) + '%');

  // Determine status and take action
  var status = 'OK';

  if (percentUsed >= CONFIG.pauseThreshold) {
    status = 'EXHAUSTED';
    Logger.log('');
    Logger.log('🛑 STATUS: BUDGET EXHAUSTED');

    if (CONFIG.autoPause) {
      Logger.log('Auto-pause enabled - pausing all campaigns...');
      var pausedCount = pauseAllCampaigns();
      Logger.log('Paused ' + pausedCount + ' campaign(s)');

      sendAlertEmail(
        '🛑 BUDGET EXHAUSTED - Campaigns Paused',
        'Budget for ' + CONFIG.accountName + ' has been exhausted.\n\n' +
        'Spend: £' + spend.toFixed(2) + ' / £' + CONFIG.monthlyBudget.toFixed(2) + '\n' +
        'Percent used: ' + (percentUsed * 100).toFixed(1) + '%\n\n' +
        pausedCount + ' campaign(s) have been automatically paused.\n\n' +
        'To re-enable, process the client payment and run update_billing_cycle.py'
      );
    } else {
      sendAlertEmail(
        '🛑 BUDGET EXHAUSTED - Action Required',
        'Budget for ' + CONFIG.accountName + ' has been exhausted.\n\n' +
        'Spend: £' + spend.toFixed(2) + ' / £' + CONFIG.monthlyBudget.toFixed(2) + '\n' +
        'Percent used: ' + (percentUsed * 100).toFixed(1) + '%\n\n' +
        'Auto-pause is DISABLED. Please review and take manual action.'
      );
    }

  } else if (percentUsed >= CONFIG.criticalThreshold) {
    status = 'CRITICAL';
    Logger.log('');
    Logger.log('🔶 STATUS: CRITICAL (95%+)');

    sendAlertEmail(
      '🔶 BUDGET CRITICAL - ' + CONFIG.accountName,
      'Budget for ' + CONFIG.accountName + ' is at critical level.\n\n' +
      'Spend: £' + spend.toFixed(2) + ' / £' + CONFIG.monthlyBudget.toFixed(2) + '\n' +
      'Percent used: ' + (percentUsed * 100).toFixed(1) + '%\n' +
      'Remaining: £' + remaining.toFixed(2) + '\n\n' +
      'Campaigns will be auto-paused when budget reaches 100%.'
    );

  } else if (percentUsed >= CONFIG.warningThreshold) {
    status = 'WARNING';
    Logger.log('');
    Logger.log('⚠️ STATUS: WARNING (80%+)');
    // Just log, no email for warnings

  } else {
    Logger.log('');
    Logger.log('✅ STATUS: OK');
  }

  Logger.log('');
  Logger.log('=== Budget Monitor Complete ===');
}

// =============================================================================
// HELPER FUNCTIONS
// =============================================================================

/**
 * Get total spend between two dates
 */
function getSpendForPeriod(startDate, endDate) {
  var dateFormat = 'yyyyMMdd';
  var startStr = Utilities.formatDate(startDate, AdsApp.currentAccount().getTimeZone(), dateFormat);
  var endStr = Utilities.formatDate(endDate, AdsApp.currentAccount().getTimeZone(), dateFormat);

  var report = AdsApp.report(
    'SELECT Cost ' +
    'FROM ACCOUNT_PERFORMANCE_REPORT ' +
    'WHERE Date >= ' + startStr + ' AND Date <= ' + endStr
  );

  var rows = report.rows();
  var totalCost = 0;

  while (rows.hasNext()) {
    var row = rows.next();
    // Cost comes as string with currency symbol, need to parse
    var costStr = row['Cost'].replace(/[^0-9.]/g, '');
    totalCost += parseFloat(costStr) || 0;
  }

  return totalCost;
}

/**
 * Pause all enabled campaigns
 */
function pauseAllCampaigns() {
  var campaigns = AdsApp.campaigns()
    .withCondition('Status = ENABLED')
    .get();

  var count = 0;
  while (campaigns.hasNext()) {
    var campaign = campaigns.next();
    campaign.pause();
    Logger.log('  Paused: ' + campaign.getName());
    count++;
  }

  return count;
}

/**
 * Send alert email
 */
function sendAlertEmail(subject, body) {
  try {
    MailApp.sendEmail({
      to: CONFIG.alertEmail,
      subject: subject,
      body: body + '\n\n---\nGenerated by Google Ads Budget Monitor Script\nPHD Networks & Systems Ltd'
    });
    Logger.log('📧 Alert email sent to ' + CONFIG.alertEmail);
  } catch (e) {
    Logger.log('❌ Failed to send email: ' + e.message);
  }
}
