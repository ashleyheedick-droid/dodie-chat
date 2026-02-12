/**
 * DODIE'S COMPLETE API — Waitlist + Inventory + Premium Features
 * ============================================================================
 * Paste this ENTIRE file into Google Apps Script (Code.gs) and deploy as:
 *   Execute as: Me
 *   Who has access: Anyone
 *
 * Sheets needed:
 *   "Waitlist"    — your waitlist data
 *   "Live Update" — your seafood inventory (columns: Item, Status, Price, Last Updated)
 *   "Shoutouts"   — staff shoutouts (auto-created if missing)
 *   "Feedback"    — customer feedback (auto-created if missing)
 *   "Specials"    — daily specials (columns: Day, Icon, Name, Description, Price, OrigPrice, Savings, Type, Availability)
 *   "ChatLogs"    — AI chat logs (auto-created if missing)
 *   "VIPs"        — VIP customers (columns: Name, Visits, LastVisit, Favorite, TotalSpent)
 * ============================================================================
 */

const SPREADSHEET_ID = "1klPJoKovTp_lPKUMWWwT26JZw7OmEZ6VVv4rPk20FHs";
const SHEET_WAITLIST  = "Waitlist";
const SHEET_INVENTORY = "Live Update";

const COL = {
  TIME_IN: 1, NAME: 2, PHONE: 3, PARTY: 4, NOTES: 5,
  STATUS: 6, TIME_SAT: 7, WAIT_MIN: 8,
  OPT_IN_SMS: 9, FUTURE_TEXTS: 10, SPICE: 11
};

// ─── HELPERS ────────────────────────────────────────────────────────────────

function ss_() {
  return SpreadsheetApp.openById(SPREADSHEET_ID);
}

function sheet_(name) {
  var s = ss_().getSheetByName(name);
  if (!s) throw new Error('Sheet not found: "' + name + '"');
  return s;
}

function sheetOrCreate_(name, headers) {
  var s = ss_().getSheetByName(name);
  if (!s) {
    s = ss_().insertSheet(name);
    s.appendRow(headers);
  }
  return s;
}

function toDate_(v) {
  if (v instanceof Date && !isNaN(v.getTime())) return v;
  var d = new Date(v);
  return isNaN(d.getTime()) ? null : d;
}

function mins_(a, b) {
  return Math.max(0, Math.round((b.getTime() - a.getTime()) / 60000));
}

function pick_(p, keys, fallback) {
  for (var k = 0; k < keys.length; k++) {
    var v = p[keys[k]];
    if (v !== undefined && v !== null && String(v).trim() !== "") return String(v).trim();
  }
  return fallback;
}

// JSONP-capable output
function out_(e, obj) {
  var cb   = e && e.parameter && e.parameter.callback ? String(e.parameter.callback) : "";
  var json = JSON.stringify(obj);
  if (cb) {
    return ContentService
      .createTextOutput(cb + "(" + json + ");")
      .setMimeType(ContentService.MimeType.JAVASCRIPT);
  }
  return ContentService
    .createTextOutput(json)
    .setMimeType(ContentService.MimeType.JSON);
}

function updateRollingWait_(sheet) {
  var lastRow = sheet.getLastRow();
  if (lastRow < 2) return;
  var now    = new Date();
  var values = sheet.getRange(2, 1, lastRow - 1, COL.SPICE).getValues();
  for (var i = 0; i < values.length; i++) {
    var r      = i + 2;
    var timeIn = toDate_(values[i][COL.TIME_IN - 1]);
    var status = String(values[i][COL.STATUS - 1] || "").toLowerCase();
    var timeSat = toDate_(values[i][COL.TIME_SAT - 1]);
    if (!timeIn) continue;
    if (status === "waiting" || status === "notified") {
      sheet.getRange(r, COL.WAIT_MIN).setValue(mins_(timeIn, now));
    } else if (status === "seated") {
      var sat = timeSat || now;
      if (!timeSat) sheet.getRange(r, COL.TIME_SAT).setValue(sat);
      sheet.getRange(r, COL.WAIT_MIN).setValue(mins_(timeIn, sat));
    }
  }
}

// Helper to read a generic sheet as array of objects (lowercase keys)
function readSheet_(name) {
  var s = ss_().getSheetByName(name);
  if (!s || s.getLastRow() < 2) return [];
  var data = s.getDataRange().getValues();
  var headers = data[0];
  var rows = [];
  for (var i = 1; i < data.length; i++) {
    var obj = {};
    for (var j = 0; j < headers.length; j++) {
      obj[String(headers[j]).toLowerCase()] = data[i][j];
    }
    rows.push(obj);
  }
  return rows;
}

// ─── MAIN ROUTER ────────────────────────────────────────────────────────────

function doGet(e) {
  try {
    var p      = (e && e.parameter) ? e.parameter : {};
    var action = String(p.action || "").trim();

    // ══════════════════════════════════════════════════════════════════════
    // CORE: WAITLIST + INVENTORY
    // ══════════════════════════════════════════════════════════════════════

    // ── ADD TO WAITLIST ────────────────────────────────────────────────
    if (action === "addToWaitlist") {
      var sheet = sheet_(SHEET_WAITLIST);
      var spice = pick_(p, ["spiceLevel","spice","spice_level","heat","heatLevel"], "No Spice");
      var norm = spice.toLowerCase().replace(/\s+/g, " ").trim();
      if (norm === "turbo hot" || norm === "turbohot") spice = "Turbo Hot";
      else if (norm === "spicy")                        spice = "Spicy";
      else if (norm === "mild")                         spice = "Mild";
      else                                              spice = "No Spice";
      sheet.appendRow([
        new Date(),
        pick_(p, ["name","fullName"], ""),
        pick_(p, ["phone","phoneNumber","tel"], ""),
        pick_(p, ["partySize","party","size"], ""),
        pick_(p, ["specialNotes","notes","note"], ""),
        "Waiting",
        "",
        "",
        pick_(p, ["smsConsent","optIn"], "Yes"),
        pick_(p, ["marketingOptIn","futureTextAlerts"], "No"),
        spice
      ]);
      return out_(e, { success: true });
    }

    // ── UPDATE STATUS ──────────────────────────────────────────────────
    if (action === "updateWaitlistStatus") {
      var rowNum   = Number(p.row);
      var newStatus = String(p.status || "").trim();
      if (!rowNum || rowNum < 2) return out_(e, { success: false, error: "Invalid row" });
      var sheet = sheet_(SHEET_WAITLIST);
      sheet.getRange(rowNum, COL.STATUS).setValue(newStatus);
      if (String(newStatus).toLowerCase() === "seated") {
        var now    = new Date();
        var timeIn = toDate_(sheet.getRange(rowNum, COL.TIME_IN).getValue());
        sheet.getRange(rowNum, COL.TIME_SAT).setValue(now);
        if (timeIn) sheet.getRange(rowNum, COL.WAIT_MIN).setValue(mins_(timeIn, now));
      }
      return out_(e, { success: true });
    }

    // ── GET WAITLIST ───────────────────────────────────────────────────
    if (action === "getWaitlist") {
      var sheet = sheet_(SHEET_WAITLIST);
      updateRollingWait_(sheet);
      var v   = sheet.getDataRange().getValues();
      var rows = [];
      for (var i = 1; i < v.length; i++) {
        if (!v[i][COL.NAME - 1]) continue;
        rows.push({
          row:          i + 1,
          name:         v[i][COL.NAME - 1],
          phone:        v[i][COL.PHONE - 1],
          party:        v[i][COL.PARTY - 1],
          specialNotes: v[i][COL.NOTES - 1],
          status:       v[i][COL.STATUS - 1],
          spiceLevel:   v[i][COL.SPICE - 1] || "",
          waitMin:      v[i][COL.WAIT_MIN - 1] || 0
        });
      }
      return out_(e, { success: true, data: rows });
    }

    // ── GET INVENTORY ─────────────────────────────────────────────────
    if (action === "getInventory") {
      var s = ss_().getSheetByName(SHEET_INVENTORY);
      if (!s || s.getLastRow() < 2) return out_(e, { success: true, data: [] });
      var data  = s.getDataRange().getValues();
      var rows  = [];
      for (var i = 1; i < data.length; i++) {
        if (!data[i][0]) continue;
        rows.push({
          item:        data[i][0],
          status:      data[i][1],
          price:       data[i][2],
          lastUpdated: data[i][3]
        });
      }
      return out_(e, { success: true, data: rows });
    }

    // ══════════════════════════════════════════════════════════════════════
    // PREMIUM: SHOUTOUTS, FEEDBACK, SPECIALS, CHAT, VIPs, DASHBOARD
    // ══════════════════════════════════════════════════════════════════════

    // ── SHOUTOUTS ─────────────────────────────────────────────────────
    if (action === "addShoutout") {
      var sheet = sheetOrCreate_("Shoutouts", ["Timestamp", "Staff", "Reasons", "Message", "From"]);
      sheet.appendRow([
        new Date().toISOString(),
        p.staff || "",
        p.reasons || "",
        p.message || "",
        p.from || "Anonymous"
      ]);
      return out_(e, { success: true, message: "Shoutout saved!" });
    }

    if (action === "getShoutouts") {
      return out_(e, { success: true, data: readSheet_("Shoutouts") });
    }

    // ── CUSTOMER FEEDBACK ─────────────────────────────────────────────
    if (action === "addFeedback") {
      var sheet = sheetOrCreate_("Feedback", ["Timestamp", "Rating", "Text", "Categories", "From", "Email", "Sentiment"]);
      sheet.appendRow([
        new Date().toISOString(),
        p.rating || "",
        p.text || "",
        p.categories || "",
        p.from || "Anonymous",
        p.email || "",
        p.sentiment || "neutral"
      ]);
      return out_(e, { success: true, message: "Feedback saved!" });
    }

    if (action === "getFeedback") {
      return out_(e, { success: true, data: readSheet_("Feedback") });
    }

    // ── DAILY SPECIALS ────────────────────────────────────────────────
    if (action === "getSpecials") {
      var s = ss_().getSheetByName("Specials");
      if (!s || s.getLastRow() < 2) return out_(e, { success: true, data: [] });
      var data = s.getDataRange().getValues();
      var headers = data[0];
      var today = new Date().toLocaleDateString("en-US", { weekday: "long" });
      var rows = [];
      for (var i = 1; i < data.length; i++) {
        var day = String(data[i][0]).trim();
        if (day === today || day === "Every Day") {
          var obj = {};
          for (var j = 0; j < headers.length; j++) {
            obj[String(headers[j]).toLowerCase()] = data[i][j];
          }
          rows.push(obj);
        }
      }
      return out_(e, { success: true, data: rows });
    }

    // ── CHAT LOGS ─────────────────────────────────────────────────────
    if (action === "logChat") {
      var sheet = sheetOrCreate_("ChatLogs", ["Timestamp", "Question", "Sentiment"]);
      sheet.appendRow([
        new Date().toISOString(),
        p.question || "",
        p.sentiment || "neutral"
      ]);
      return out_(e, { success: true });
    }

    if (action === "getChatLogs") {
      return out_(e, { success: true, data: readSheet_("ChatLogs") });
    }

    // ── VIP CUSTOMERS ─────────────────────────────────────────────────
    if (action === "getVIPs") {
      var rows = readSheet_("VIPs");
      rows.sort(function(a, b) { return (Number(b.visits) || 0) - (Number(a.visits) || 0); });
      return out_(e, { success: true, data: rows });
    }

    // ── DASHBOARD STATS ───────────────────────────────────────────────
    if (action === "getDashboardStats") {
      var spreadsheet = ss_();
      var stats = {};

      var chatSheet = spreadsheet.getSheetByName("ChatLogs");
      stats.totalChats = chatSheet ? Math.max(chatSheet.getLastRow() - 1, 0) : 0;

      var shoutSheet = spreadsheet.getSheetByName("Shoutouts");
      stats.totalShoutouts = shoutSheet ? Math.max(shoutSheet.getLastRow() - 1, 0) : 0;

      var fbSheet = spreadsheet.getSheetByName("Feedback");
      if (fbSheet && fbSheet.getLastRow() > 1) {
        var fbData = fbSheet.getRange(2, 2, fbSheet.getLastRow() - 1, 1).getValues();
        var sum = 0;
        for (var i = 0; i < fbData.length; i++) sum += (Number(fbData[i][0]) || 0);
        stats.totalFeedback = fbData.length;
        stats.avgRating = (sum / fbData.length).toFixed(1);
      } else {
        stats.totalFeedback = 0;
        stats.avgRating = 0;
      }

      var wlSheet = spreadsheet.getSheetByName("Waitlist");
      if (wlSheet && wlSheet.getLastRow() > 1) {
        var wlData = wlSheet.getDataRange().getValues();
        stats.totalWaitlist = wlData.length - 1;
        var seated = 0;
        for (var i = 1; i < wlData.length; i++) {
          if (String(wlData[i][COL.STATUS - 1] || "").toLowerCase() === "seated") seated++;
        }
        stats.seated = seated;
      } else {
        stats.totalWaitlist = 0;
        stats.seated = 0;
      }

      return out_(e, { success: true, data: stats });
    }

    // ── RESTAURANT LEAD / SIGNUP ──────────────────────────────────────
    if (action === "addLead") {
      var sheet = sheetOrCreate_("Leads", ["Timestamp", "Contact Name", "Role", "Email", "Phone", "Restaurant", "City", "Cuisine", "Capacity", "Biggest Pain", "Plan"]);
      sheet.appendRow([
        new Date().toISOString(),
        p.contactName || "",
        p.contactRole || "",
        p.email || "",
        p.phone || "",
        p.restaurantName || "",
        p.city || "",
        p.cuisineType || "",
        p.seatingCapacity || "",
        p.biggestPain || "",
        p.plan || "Professional"
      ]);
      return out_(e, { success: true, message: "Lead captured!" });
    }

    if (action === "getLeads") {
      return out_(e, { success: true, data: readSheet_("Leads") });
    }

    // ── FALLBACK ──────────────────────────────────────────────────────
    return out_(e, { success: false, error: "Unknown action: " + action });

  } catch (err) {
    return out_(e, { success: false, error: err.message });
  }
}
