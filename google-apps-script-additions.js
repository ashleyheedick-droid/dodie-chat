/**
 * ============================================================================
 * GOOGLE APPS SCRIPT ADDITIONS FOR DODIE'S PREMIUM FEATURES
 * ============================================================================
 *
 * INSTRUCTIONS:
 * 1. Open your Google Apps Script project (the one connected to your sheet)
 * 2. Add the functions below to your existing script
 * 3. Make sure you have these NEW tabs/sheets in your Google Sheet:
 *    - "Shoutouts"  (columns: Timestamp, Staff, Reasons, Message, From)
 *    - "Feedback"   (columns: Timestamp, Rating, Text, Categories, From, Email, Sentiment)
 *    - "Specials"   (columns: Day, Icon, Name, Description, Price, OrigPrice, Savings, Type, Availability)
 *    - "ChatLogs"   (columns: Timestamp, Question, Sentiment)
 *    - "VIPs"       (columns: Name, Visits, LastVisit, Favorite, TotalSpent)
 * 4. Re-deploy your Apps Script (Deploy > New Deployment)
 * 5. Copy the new URL to your Control Center if it changed
 *
 * ADD THESE to your existing doGet(e) function's action handlers:
 * ============================================================================
 */

// ── Add these cases inside your existing doGet(e) switch/if block ──────────

// In your doGet function, add these action handlers:

/*
  // === SHOUTOUTS ===
  if (action === 'addShoutout') {
    var sheet = ss.getSheetByName('Shoutouts');
    if (!sheet) {
      sheet = ss.insertSheet('Shoutouts');
      sheet.appendRow(['Timestamp', 'Staff', 'Reasons', 'Message', 'From']);
    }
    sheet.appendRow([
      new Date().toISOString(),
      e.parameter.staff || '',
      e.parameter.reasons || '',
      e.parameter.message || '',
      e.parameter.from || 'Anonymous'
    ]);
    return respond({ success: true, message: 'Shoutout saved!' }, callback);
  }

  if (action === 'getShoutouts') {
    var sheet = ss.getSheetByName('Shoutouts');
    if (!sheet) return respond({ success: true, data: [] }, callback);
    var data = sheet.getDataRange().getValues();
    var headers = data[0];
    var rows = data.slice(1).map(function(row) {
      var obj = {};
      headers.forEach(function(h, i) { obj[h.toLowerCase()] = row[i]; });
      return obj;
    });
    return respond({ success: true, data: rows }, callback);
  }

  // === CUSTOMER FEEDBACK ===
  if (action === 'addFeedback') {
    var sheet = ss.getSheetByName('Feedback');
    if (!sheet) {
      sheet = ss.insertSheet('Feedback');
      sheet.appendRow(['Timestamp', 'Rating', 'Text', 'Categories', 'From', 'Email', 'Sentiment']);
    }
    sheet.appendRow([
      new Date().toISOString(),
      e.parameter.rating || '',
      e.parameter.text || '',
      e.parameter.categories || '',
      e.parameter.from || 'Anonymous',
      e.parameter.email || '',
      e.parameter.sentiment || 'neutral'
    ]);
    return respond({ success: true, message: 'Feedback saved!' }, callback);
  }

  if (action === 'getFeedback') {
    var sheet = ss.getSheetByName('Feedback');
    if (!sheet) return respond({ success: true, data: [] }, callback);
    var data = sheet.getDataRange().getValues();
    var headers = data[0];
    var rows = data.slice(1).map(function(row) {
      var obj = {};
      headers.forEach(function(h, i) { obj[h.toLowerCase()] = row[i]; });
      return obj;
    });
    return respond({ success: true, data: rows }, callback);
  }

  // === DAILY SPECIALS ===
  if (action === 'getSpecials') {
    var sheet = ss.getSheetByName('Specials');
    if (!sheet) return respond({ success: true, data: [] }, callback);
    var data = sheet.getDataRange().getValues();
    var headers = data[0];
    var today = new Date().toLocaleDateString('en-US', { weekday: 'long' });
    var rows = data.slice(1)
      .filter(function(row) { return row[0] === today || row[0] === 'Every Day'; })
      .map(function(row) {
        var obj = {};
        headers.forEach(function(h, i) { obj[h.toLowerCase()] = row[i]; });
        return obj;
      });
    return respond({ success: true, data: rows }, callback);
  }

  // === CHAT LOGS (for dashboard analytics) ===
  if (action === 'logChat') {
    var sheet = ss.getSheetByName('ChatLogs');
    if (!sheet) {
      sheet = ss.insertSheet('ChatLogs');
      sheet.appendRow(['Timestamp', 'Question', 'Sentiment']);
    }
    sheet.appendRow([
      new Date().toISOString(),
      e.parameter.question || '',
      e.parameter.sentiment || 'neutral'
    ]);
    return respond({ success: true }, callback);
  }

  if (action === 'getChatLogs') {
    var sheet = ss.getSheetByName('ChatLogs');
    if (!sheet) return respond({ success: true, data: [] }, callback);
    var data = sheet.getDataRange().getValues();
    var headers = data[0];
    var rows = data.slice(1).map(function(row) {
      var obj = {};
      headers.forEach(function(h, i) { obj[h.toLowerCase()] = row[i]; });
      return obj;
    });
    return respond({ success: true, data: rows }, callback);
  }

  // === VIP CUSTOMERS ===
  if (action === 'getVIPs') {
    var sheet = ss.getSheetByName('VIPs');
    if (!sheet) return respond({ success: true, data: [] }, callback);
    var data = sheet.getDataRange().getValues();
    var headers = data[0];
    var rows = data.slice(1).map(function(row) {
      var obj = {};
      headers.forEach(function(h, i) { obj[h.toLowerCase()] = row[i]; });
      return obj;
    });
    // Sort by visits descending
    rows.sort(function(a, b) { return (b.visits || 0) - (a.visits || 0); });
    return respond({ success: true, data: rows }, callback);
  }

  // === DASHBOARD ANALYTICS (aggregated) ===
  if (action === 'getDashboardStats') {
    var stats = {};

    // Chat count
    var chatSheet = ss.getSheetByName('ChatLogs');
    stats.totalChats = chatSheet ? Math.max(chatSheet.getLastRow() - 1, 0) : 0;

    // Shoutout count
    var shoutSheet = ss.getSheetByName('Shoutouts');
    stats.totalShoutouts = shoutSheet ? Math.max(shoutSheet.getLastRow() - 1, 0) : 0;

    // Feedback count & avg rating
    var fbSheet = ss.getSheetByName('Feedback');
    if (fbSheet && fbSheet.getLastRow() > 1) {
      var fbData = fbSheet.getRange(2, 2, fbSheet.getLastRow() - 1, 1).getValues();
      var sum = fbData.reduce(function(a, b) { return a + (Number(b[0]) || 0); }, 0);
      stats.totalFeedback = fbData.length;
      stats.avgRating = (sum / fbData.length).toFixed(1);
    } else {
      stats.totalFeedback = 0;
      stats.avgRating = 0;
    }

    // Waitlist stats
    var wlSheet = ss.getSheetByName('Waitlist');
    if (wlSheet && wlSheet.getLastRow() > 1) {
      var wlData = wlSheet.getDataRange().getValues();
      stats.totalWaitlist = wlData.length - 1;
      stats.seated = wlData.filter(function(r) { return String(r[4] || '').toLowerCase() === 'seated'; }).length;
    } else {
      stats.totalWaitlist = 0;
      stats.seated = 0;
    }

    return respond({ success: true, data: stats }, callback);
  }
*/

/**
 * ============================================================================
 * HELPER: If you don't already have a respond() function, add this:
 * ============================================================================
 */

/*
function respond(data, callback) {
  if (callback) {
    return ContentService
      .createTextOutput(callback + '(' + JSON.stringify(data) + ')')
      .setMimeType(ContentService.MimeType.JAVASCRIPT);
  }
  return ContentService
    .createTextOutput(JSON.stringify(data))
    .setMimeType(ContentService.MimeType.JSON);
}
*/
