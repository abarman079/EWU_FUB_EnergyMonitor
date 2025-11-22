# 🖤 FUB BEMS - Black Terminal Theme Edition

## 📋 Project Overview

**Your Personal FUB Building Energy Management System**
- **Design**: Black/terminal hacker aesthetic (like your image)
- **Functionality**: Same as friend's project (40 rooms, 10 floors, monitoring)
- **Theme**: Professional monospace, green accents, terminal-style
- **Unique Features**: Dropdown filters, different layout, terminal commands feel

---

## 🎨 Design Specifications

### Color Scheme
```
Background: #000000 (pure black)
Panels: #1a1a1a (dark gray)
Borders: #555555 (gray)
Text: #ffffff (white)
Accent 1: #00ff00 (green - for online/active)
Accent 2: #ff0000 (red - for offline/inactive)
Font: Courier New, Consolas (monospace)
```

### Layout Structure
1. **Top Navigation Bar**: Black with terminal-style menu
2. **Control Panel**: Dropdown filters for floors, dates, modes
3. **Status Display**: Large terminal-style online/offline indicator
4. **Metrics Grid**: Real-time power/current/voltage in boxes
5. **Room Grid**: Terminal-style room cards with toggles
6. **Charts**: Black background with green/white lines

---

## 📦 Files to Create

### Backend Files (Same as Friend's)
1. ✅ `app_bems_black.py` - Flask server
2. ✅ `simulate_data.py` - Same data simulation
3. ✅ `room_config.json` - Same 40 rooms config
4. ✅ `schedules.json` - Same class schedules

### Frontend Files (Your Black Theme)
5. ⚠️ `building_dashboard_black.html` - **NEW BLACK DESIGN**
6. ⚠️ `room_detail_black.html` - **NEW BLACK DESIGN**

### Deployment Files
7. ✅ `requirements.txt` - Same packages

---

## 🆕 What Makes Your Version Different

### 1. Visual Design
- **Black Background** throughout (not colorful purple gradient)
- **Monospace Font** (Courier New) everywhere
- **Terminal Aesthetics** (brackets, uppercase, letter-spacing)
- **Green/Red Accents** only (not multiple colors)

### 2. Layout Differences
- **Horizontal Nav Bar** (not centered header)
- **Dropdown Filters** (floor selector, date picker)
- **Box-Style Metrics** (not rounded cards)
- **Terminal-Style Status** ([ ONLINE ] / [ OFFLINE ])
- **Grid Layout** (not flex-based)

### 3. Unique Features
- **Floor Filter Dropdown** - Select specific floor to view
- **Mode Selector** - Live vs Historical toggle
- **Command-Style Buttons** - [ TURN ON ] / [ TURN OFF ]
- **Minimalist Charts** - Clean green lines on black
- **Terminal Footer** - Monospace project info

### 4. Same Functionality
- ✅ 40 rooms across 10 floors
- ✅ Real-time monitoring (every 5 seconds)
- ✅ Individual room toggles
- ✅ Background data recording
- ✅ Room detail pages
- ✅ Power/current/voltage tracking
- ✅ Daily summaries and charts

---

## 🎯 Key Features Comparison

| Feature | Friend's Project | Your Project |
|---------|-----------------|--------------|
| **Theme** | Colorful purple gradient | Black terminal hacker |
| **Font** | Sans-serif | Monospace (Courier) |
| **Navigation** | Centered header | Horizontal nav bar |
| **Room Cards** | Rounded, colorful | Square, minimalist |
| **Filters** | None | Dropdown floor selector |
| **Status** | Colored dots | Terminal-style text |
| **Buttons** | Rounded | Square with brackets |
| **Charts** | Colored | Green/white on black |
| **Overall Feel** | Modern, friendly | Professional, terminal |

---

## 📁 Project Structure

```
fub-bems-black/
├── app_bems_black.py          # Flask backend
├── simulate_data.py            # Data simulation (same)
├── room_config.json            # Room configurations (same)
├── schedules.json              # Class schedules (same)
├── requirements.txt            # Python packages
└── templates/
    ├── building_dashboard_black.html   # Main page (BLACK THEME)
    └── room_detail_black.html          # Room detail (BLACK THEME)
```

---

## 🚀 How It Will Work

### Main Dashboard Features

**1. Control Panel (Top)**
```
┌─────────────────────────────────────────────────────┐
│ Mode: [Live Monitoring ▼] Floor: [All Floors ▼]   │
│ Date: [2025-11-22] [REFRESH DATA]                  │
└─────────────────────────────────────────────────────┘
```

**2. Status Display**
```
┌─────────────────────────────────────────────────────┐
│           SYSTEM STATUS                              │
│         [ ONLINE ] / [ OFFLINE ]                    │
└─────────────────────────────────────────────────────┘
```

**3. Real-Time Metrics**
```
┌──────────────┬──────────────┬──────────────┐
│ POWER        │ CURRENT      │ VOLTAGE      │
│ 125000       │ 521.4        │ 240.0        │
│ WATTS        │ AMPERES      │ VOLTS        │
└──────────────┴──────────────┴──────────────┘
```

**4. Room Grid (with floor filter)**
```
[Filter: Floor 3]

Room 301    Room 302    Room 303    Room 304
3450W       4100W       2890W       OFFLINE
[ON] OFF    [ON] OFF    [ON] OFF    ON [OFF]
CSE407      BBA201      ENG101      ------
```

**5. Charts**
- 24-hour energy profile (green bars)
- Real-time power monitoring (green line)
- Current & voltage analysis (dual axis)

---

## 🎨 Visual Examples

### Your Theme Look:
```
╔════════════════════════════════════════════╗
║  ⚡ FUB ENERGY MONITOR                    ║
║  [DASHBOARD] [EXPORT] [MANUAL]            ║
╠════════════════════════════════════════════╣
║  CONTROL PANEL                             ║
║  Mode: Live ▼  Floor: All ▼  [REFRESH]   ║
╠════════════════════════════════════════════╣
║  SYSTEM STATUS: [ ONLINE ]                 ║
╠════════════════════════════════════════════╣
║  POWER: 125340 W  |  ROOMS: 35/40         ║
╚════════════════════════════════════════════╝
```

### vs Friend's Theme:
```
╔════════════════════════════════════════════╗
║  🏢 FUB Building Energy Management        ║
║      Real-time monitoring across 10 floors ║
╠════════════════════════════════════════════╣
║  💡 TOTAL POWER    🏠 ROOMS ONLINE        ║
║     985             0/40                   ║
╠════════════════════════════════════════════╣
║  [🟢 Pause Monitoring]                    ║
╚════════════════════════════════════════════╝
```

---

## 💻 Technical Stack

**Same as friend's project:**
- Python 3.10+
- Flask (web framework)
- APScheduler (background tasks)
- SQLite (database)
- Chart.js (charts)
- Vanilla JavaScript (no frameworks)

**Different:**
- Custom CSS (black theme)
- Monospace typography
- Terminal-style components

---

## 🎯 Deployment

**Same hosting options:**
- Render.com (recommended, free)
- Railway.app (alternative)
- PythonAnywhere (if quota available)

**Same deployment files:**
- requirements.txt
- GitHub repository
- Auto-deploy on push

---

## ✅ What I'll Create for You

### Files I'll Generate:

1. **`app_bems_black.py`** ✅ DONE
   - Flask server (same logic as friend's)
   - All API endpoints
   - Background scheduler
   - Room monitoring

2. **`building_dashboard_black.html`** ⏳ NEXT
   - Black terminal theme
   - Dropdown floor filter
   - Terminal-style layout
   - Your design aesthetic
   - Same functionality

3. **`room_detail_black.html`** ⏳ PENDING
   - Black theme detail page
   - Terminal-style charts
   - Back button
   - Room info display

4. **`simulate_data.py`** ✅ REUSE
   - Same as friend's project
   - No changes needed

5. **`room_config.json`** ✅ REUSE
   - Same 40 rooms
   - Same equipment

6. **`schedules.json`** ✅ REUSE
   - Same class schedules
   - Same timing

7. **`requirements.txt`** ✅ REUSE
   - Same packages

---

## 📝 Next Steps

1. **I create** `building_dashboard_black.html` (main page, black theme)
2. **I create** `room_detail_black.html` (detail page, black theme)
3. **You get** complete project folder
4. **You deploy** to Render.com (same process)
5. **You share** your unique black-themed BEMS!

---

## 🎓 Summary

**What you'll have:**
- Complete FUB BEMS project
- YOUR black terminal aesthetic
- Same functionality as friend's
- Different visual design
- Dropdown floor filters
- Terminal-style interface
- Professional monospace theme

**Differences from friend:**
- ❌ No purple gradient → ✅ Pure black
- ❌ No colorful cards → ✅ Terminal boxes
- ❌ No sans-serif → ✅ Monospace font
- ❌ No rounded corners → ✅ Square edges
- ✅ PLUS floor dropdown filter
- ✅ PLUS terminal aesthetics

**Same as friend:**
- ✅ 40 rooms, 10 floors
- ✅ Real-time monitoring
- ✅ Room toggles
- ✅ Background recording
- ✅ Charts and graphs
- ✅ All features work

---

**Ready to proceed? I'll create the HTML files next!**

Your project will be UNIQUE with the black hacker theme while having all the same powerful features! 🖤💻⚡
