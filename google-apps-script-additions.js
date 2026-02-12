/**
 * ============================================================================
 * GOOGLE APPS SCRIPT — DODIE'S PREMIUM FEATURES
 * ============================================================================
 *
 * HOW TO USE:
 * 1. Open your Google Sheet → Extensions → Apps Script
 * 2. COPY everything below the line of ='s into your Code.gs file
 *    (add it INSIDE your existing doGet function, before the final closing brace)
 * 3. If you don't have a respond() function yet, also copy the helper at the bottom
 * 4. Make sure your Google Sheet has these tabs (the script auto-creates most if missing):
 *    - "Inventory"  (columns: Item, Status, Price, LastUpdated)
 *    - "Waitlist"   (columns: Timestamp, Name, Phone, Party, Status, SpecialNotes, SpiceLevel)
 *    - "Shoutouts"  (columns: Timestamp, Staff, Reasons, Message, From)
 *    - "Feedback"   (columns: Timestamp, Rating, Text, Categories, From, Email, Sentiment)
 *    - "Specials"   (columns: Day, Icon, Name, Description, Price, OrigPrice, Savings, Type, Availability)
 *    - "ChatLogs"   (columns: Timestamp, Question, Sentiment)
 *    - "VIPs"       (columns: Name, Visits, LastVisit, Favorite, TotalSpent)
 * 5. Deploy → New Deployment → Web App → Execute as Me → Anyone can access
 * 6. Copy the URL into Dodie's Control Center page
 * ============================================================================
 */

// ─── PASTE INSIDE YOUR doGet(e) FUNCTION ────────────────────────────────────
// If you don't have a doGet yet, use this complete one:

function doGet(e) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var action = (e.parameter.action || '').trim();
  var callback = e.parameter.callback || '';

  // === INVENTORY (live seafood board) ===
  if (action === 'getInventory') {
    var sheet = ss.getSheetByName('Inventory');
    if (!sheet) return respond({ success: true, data: [] }, callback);
    var data = sheet.getDataRange().getValues();
    var headers = data[0];
    var rows = data.slice(1).map(function(row) {
      var obj = {};
      headers.forEach(function(h, i) { obj[h.trim().replace(/\s+/g, '').replace(/^(.)/, function(m) { return m.toLowerCase(); })] = row[i]; });
      return obj;
    });
    return respond({ success: true, data: rows }, callback);
  }

  // === WAITLIST ===
  if (action === 'getWaitlist') {
    var sheet = ss.getSheetByName('Waitlist');
    if (!sheet) return respond({ success: true, data: [] }, callback);
    var data = sheet.getDataRange().getValues();
    var headers = data[0];
    var rows = data.slice(1).map(function(row, idx) {
      var obj = { row: idx + 2 }; // sheet row number (1-indexed, skip header)
      headers.forEach(function(h, i) {
        var key = h.trim();
        // Map column names to the keys the frontend expects
        if (key === 'Party' || key === 'PartySize') obj.party = row[i];
        else if (key === 'SpecialNotes') obj.specialNotes = row[i];
        else if (key === 'SpiceLevel') obj.spiceLevel = row[i];
        else obj[key.toLowerCase()] = row[i];
      });
      return obj;
    });
    return respond({ success: true, data: rows }, callback);
  }

  if (action === 'addToWaitlist') {
    var sheet = ss.getSheetByName('Waitlist');
    if (!sheet) {
      sheet = ss.insertSheet('Waitlist');
      sheet.appendRow(['Timestamp', 'Name', 'Phone', 'Party', 'Status', 'SpecialNotes', 'SpiceLevel']);
    }
    sheet.appendRow([
      new Date().toISOString(),
      e.parameter.name || '',
      e.parameter.phone || '',
      e.parameter.partySize || '',
      'Waiting',
      e.parameter.specialNotes || '',
      e.parameter.spiceLevel || ''
    ]);
    return respond({ success: true, message: 'Added to waitlist!' }, callback);
  }

  if (action === 'updateWaitlistStatus') {
    var sheet = ss.getSheetByName('Waitlist');
    if (!sheet) return respond({ success: false, error: 'Waitlist sheet not found' }, callback);
    var row = parseInt(e.parameter.row, 10);
    if (!row || row < 2) return respond({ success: false, error: 'Invalid row' }, callback);
    // Status is in column 5 (E)
    var headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
    var statusCol = -1;
    for (var i = 0; i < headers.length; i++) {
      if (headers[i].toString().trim().toLowerCase() === 'status') { statusCol = i + 1; break; }
    }
    if (statusCol === -1) return respond({ success: false, error: 'Status column not found' }, callback);
    sheet.getRange(row, statusCol).setValue(e.parameter.status || '');
    return respond({ success: true, message: 'Status updated!' }, callback);
  }

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
    rows.sort(function(a, b) { return (b.visits || 0) - (a.visits || 0); });
    return respond({ success: true, data: rows }, callback);
  }

  // === DASHBOARD ANALYTICS (aggregated) ===
  if (action === 'getDashboardStats') {
    var stats = {};

    var chatSheet = ss.getSheetByName('ChatLogs');
    stats.totalChats = chatSheet ? Math.max(chatSheet.getLastRow() - 1, 0) : 0;

    var shoutSheet = ss.getSheetByName('Shoutouts');
    stats.totalShoutouts = shoutSheet ? Math.max(shoutSheet.getLastRow() - 1, 0) : 0;

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

  // === FALLBACK: unknown action ===
  return respond({ success: false, error: 'Unknown action: ' + action }, callback);
}

// ─── HELPER: JSONP + JSON response ─────────────────────────────────────────
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
