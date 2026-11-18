# Maya Extension — Project Details

> Namma plan ellam inga. User solla solla append aagum.
> Fedora KDE (Plasma) — premium liquid glass theme. UI-UX focus.

---

## 1. Context Menu + Full Fedora Glass Morphism

- **Context menu:** premium **liquid glass morphism** venum
  (translucent, blur, rounded corners, subtle border + highlight)
- **Full Fedora desktop:** glass morphism theme throughout
  (oru app mattum illa, full OS glass-ah irukanum)
  - GTK/Qt apps, panels, windows, notifications — ellam glass
- **Scope:** desktop-level theming, not single widget

### Decisions
- DE: **KDE Plasma** ✅
- Blur/transparency: **user-selectable** ✅
- Light/Dark glass: **user choice (toggle)** ✅
- Accent color: **user-selectable (color picker)** ✅
- Scope: **all parts user-selectable/toggleable** ✅ (KWin, Qt, GTK, panels, notifications, icons, cursors)
- Performance: **user choice, optional** ✅ (blur toggle + auto-disable option)
- Packaging: **both (package + install script)** ✅

---

## 2. Fedora Settings Page

- Clean, professional, Windows-style settings page venum
- Both: standalone app + KDE System Settings module
- Settings items: all (glass on/off, blur, light/dark, accent, scope, performance, about)
- Navigation: both (sidebar + tabs, responsive)
- Search box: yes
- Live preview: both (instant + undo)
- Maya branding: yes

---

## 3. Right-Side Quick Settings Shade

- Theme part (Maya extension scope)
- Windows-style right-side shade (notification center / quick settings)
- All toggles (WiFi, Bluetooth, brightness, volume, dark mode, Maya quick actions)
- Glass morphism on shade: yes
- Maya quick actions in shade: yes

---

## 4. Pinned Apps Center (Windows 11 Style Taskbar)

- Theme part (Maya extension scope)
- Panel position: user choice
- Apps: **centered** ✅
- Search bar: **left corner** ✅
- Settings, battery, date-time, notification: **right side corner** ✅
- Icon size: user choice
- Hover effect: user choice
- Running app indicator: user choice
- Grouping: user choice

---

## 5. Wallpaper (Theme Part)

- Theme part (Maya extension scope)
- Wallpaper type: user choice (static / animated / slideshow)
- Glass blur/parallax: user choice
- Maya-themed wallpapers: user choice
- Custom wallpaper upload: yes
- Light/dark auto-switch: user choice

---

## 6. Visual System Monitoring

- Theme part (Maya extension scope)
- Display: all (desktop widget, panel, settings, quick shade)
- Visual style: user choice (cards / graphs / rings / bars)
- Update interval: user choice (1s / 2s / 5s)
- Metrics: all (CPU, RAM, GPU, NPU, battery, disk, network, temp, processes)
- Alert thresholds: user choice
- Click to detailed view: user choice

---

## 7. Maya Extension — UI/UX Design (Beautiful, Fedora KDE)

> Extension UI-UX mattum change. System-level changes illa.

### 7.1 Design Language
- **Style:** Premium liquid glass morphism (frosted glass, blur, soft edges)
- **Feel:** Calm, modern, slightly playful (Maya personality)
- **Depth:** Layered (background → glass card → content → floating actions)
- **Motion:** Smooth, subtle, 60fps

### 7.2 Color System
- **Base (dark):** `#0B0F19` + `rgba(255,255,255,0.06)` glass
- **Base (light):** `#F5F7FB` + `rgba(255,255,255,0.55)` glass
- **Maya accent:** Pink `#FF7AB8` → Purple `#A855F7` (gradient)
- **Success:** `#4ADE80`  **Warning:** `#FBBF24`  **Danger:** `#F87171`
- **Text primary:** `rgba(255,255,255,0.96)` / `#1F2937`
- **Text secondary:** `rgba(255,255,255,0.55)` / `#6B7280`
- **Borders:** `rgba(255,255,255,0.18)` (1px)

### 7.3 Typography
- **UI font:** Inter / Noto Sans
- **Heading:** 18-20px bold  **Body:** 14px  **Caption:** 11-12px
- **Monospace:** JetBrains Mono / Fira Code

### 7.4 Spacing & Radius
- **Grid:** 8px (multiples)  **Card radius:** 16-18px  **Button radius:** 10-12px
- **Padding:** 16px card / 12px button / 8px compact

### 7.5 Glass Spec (Liquid Glass)
- **Blur:** 20-40px gaussian (KWin)
- **Transparency:** 60-80% dark / 40-60% light
- **Border:** 1px `rgba(255,255,255,0.18)` + 0.5px inner highlight
- **Top highlight:** `rgba(255,255,255,0.14)` → 0 (top 35%)
- **Shadow:** `0 8px 32px rgba(0,0,0,0.35)`
- **Noise:** 2-3% grain (optional)

### 7.6 Components
- **Button primary:** Maya gradient, white text, hover glow
- **Button secondary:** glass fill, 1px border, hover brighten
- **Toggle:** pill, Maya accent on, glass off, smooth slide
- **Slider:** thin track, Maya accent thumb
- **Card:** glass bg, 18px radius, top highlight, soft shadow
- **Input:** glass bg, focus = Maya accent border + glow
- **Tab:** underline Maya gradient indicator
- **Sidebar item:** icon + label, glass highlight, left accent bar when active

### 7.7 Animations
- **Page transition:** fade + slide (200ms)
- **Popup open:** 3D flip-in (420ms, ease-out-cubic)
- **Hover:** 120-150ms  **Toggle:** 200ms slide
- **Loading:** Maya shimmer  **Success:** scale bounce (1.0→1.05→1.0)

### 7.8 Iconography
- **Style:** rounded outlined, 2px stroke (Lucide/Tabler)
- **Size:** 16 / 20 / 24px
- **Color:** Maya accent active, white/gray inactive
- **Custom:** chat, voice, monitor, settings, glass toggle

### 7.9 Layout (Settings Page)
- **Left:** sidebar 240px (sections + search)
- **Right:** scrollable cards
- **Top:** title bar with Maya logo + glass window controls
- **Bottom:** status bar (version, apply/undo)

### 7.10 Accessibility
- WCAG AA (4.5:1 text), visible focus rings (2px Maya)
- Keyboard nav + screen reader labels
- Respect `prefers-reduced-motion` → disable 3D flip

### 7.11 Responsive
- **>=1024px:** sidebar + content
- **768-1023px:** collapsible sidebar
- **<768px:** bottom tabs, single column

### 7.12 Branding
- Logo: "✦ Maya AI" pink-purple gradient
- Tagline: "local only • your assistant"
- Accent: pink-purple everywhere
- Tone: friendly Thanglish-friendly

### 7.13 Do's & Don'ts
- ✅ 8px grid, glass everywhere, smooth animations, dark default
- ❌ No mixed blur levels, no pure black/white, no animations > 500ms

### 7.14 Tech Stack (UI only)
- PySide6 (Qt6) + QML animations, QSS, SVG icons, bundled fonts

---

## 8. Installation & Rollback

> Naan own plan — safe install, easy rollback.

### 8.1 Install Flow
1. Pre-check: Plasma version, Qt version, GPU driver, disk space
2. Backup current theme state ( KDE config export )
3. Install theme files to `~/.local/share/` (user-level, no root)
4. Apply config via `kwriteconfig6` / Plasma API
5. Restart Plasma shell (`plasmashell --replace`) — with 5s confirm timeout
6. Verify: screenshot smoke test, config check
7. Success message + "What's new" note

### 8.2 Uninstall
- Restore backed-up config first
- Remove theme files
- Restart Plasma shell
- Confirm default theme restored

### 8.3 Rollback (if break)
- **Auto rollback:** if shell doesn't come back in 10s → restore backup automatically
- **Manual rollback:** `maya-theme rollback` command
- **Safe mode:** hold Shift on login → skip Maya theme load
- Backup location: `~/.local/share/maya-theme/backups/<timestamp>/`
- Keep last 5 backups, rotate old ones

### 8.4 Commands
| Command | Purpose |
|---|---|
| `maya-theme install` | Install + apply |
| `maya-theme uninstall` | Remove + restore |
| `maya-theme rollback` | Restore last backup |
| `maya-theme status` | Current state + version |
| `maya-theme backup` | Manual backup |

---

## 9. Compatibility

### 9.1 Target
- **OS:** Fedora 40+ (Workstation)
- **DE:** KDE Plasma 6.x (target), Plasma 5.x (best-effort fallback)
- **Session:** Wayland primary, X11 fallback
- **Qt:** 6.6+ (PySide6 6.6+)
- **Python:** 3.12+

### 9.2 Version Matrix
| Fedora | Plasma | Status |
|---|---|---|
| 42 | 6.3+ | Full support ✅ |
| 41 | 6.2 | Full support ✅ |
| 40 | 6.0/6.1 | Support ✅ |
| 39 | 5.27 | Best-effort ⚠️ |
| <39 | — | Not supported ❌ |

### 9.3 Feature Gates
- KWin blur → Plasma 6 compositor (Wayland/X11)
- Qt app theming → Qt6 style + QSS
- GTK app theming → gtk4 config (separate, optional)
- SNI tray → StatusNotifierItem spec (DE independent)

### 9.4 Handling Mismatch
- If unsupported version → warn + offer "basic mode" (no blur, glass colors only)
- Never hard-crash; degrade gracefully
- Log compatibility info to `~/.local/state/maya-theme/compat.log`

---

## 10. Performance Budget

### 10.1 Limits (Ryzen AI 5 340 iGPU)
- **Extra CPU (idle):** < 2% (monitoring widget)
- **Extra RAM:** < 150 MB (theme + settings + widgets)
- **Blur GPU cost:** < 5% GPU when enabled
- **Frame rate:** 60fps animations, no dropped frames on hover

### 10.2 Fallbacks
- Low GPU / battery saver → auto reduce blur radius (40px → 16px)
- Very low → disable blur, keep glass colors + borders
- User toggle in settings: `Performance: Quality / Balanced / Battery`

### 10.3 Monitoring
- Built-in perf counter in settings page (show own CPU/RAM usage)
- If budget exceeded for 30s → auto suggest "Balanced mode"
- Logs: no personal data, only metrics

### 10.4 Rules
- No always-on heavy shaders
- Timers pause when widget hidden / screen locked
- Avoid repaint storms — cache glass gradients as textures

---

## 11. Testing Plan

### 11.1 Levels
| Level | What | How |
|---|---|---|
| Unit | settings logic, config parse | pytest (Python) |
| Component | QML components render | Qt Test / screenshots |
| Integration | theme apply/rollback | auto script on clean Fedora VM |
| Visual | glass correctness | screenshot diff (golden images) |
| Accessibility | keyboard, contrast, screen reader | manual + axe-like checks |
| Multi-monitor | different DPI/resolutions | manual on 2 monitors |
| Performance | budget check | perf counters, 1h soak test |

### 11.2 Test Cases (key)
- Install → apply → rollback → uninstall (clean restore)
- Light/Dark toggle preserves other settings
- Blur disable → glass still visible (colors)
- Multi-monitor DPI scaling (100%, 125%, 150%)
- Wayland + X11 both sessions
- Low-battery → auto blur reduce
- Settings search finds all items
- Undo after instant-apply works
- Reduced-motion → no 3D flip

### 11.3 Environments
- Fedora 42 Plasma 6.3 (Wayland) — primary
- Fedora 40 Plasma 6.0 (X11) — fallback
- VMs: GNOME session (ensure no break, even if unsupported)

### 11.4 Exit Criteria
- All unit tests pass
- Visual diff within threshold
- No config leak after uninstall
- Perf within budget (Section 10)

---

## 12. Backup & Restore Settings

### 12.1 What to Backup
- Full theme config: blur level, accent color, light/dark, scope toggles
- Wallpaper selection + path (not the file itself by default)
- Panel layout preference, shade settings, monitor widget prefs
- Version tag (for restore compatibility)

### 12.2 Formats
- **Export:** `maya-theme-<version>-<date>.json` (human readable)
- **Import:** validate schema + version before apply
- Optional: include wallpaper files → `.zip` bundle

### 12.3 Behavior
- Export via settings page ("Export theme") or CLI
- Import → preview changes → confirm → apply (with undo)
- Incompatible version → warn + offer migration
- Secrets: no tokens / personal data in export (privacy rule)

### 12.4 Location
- Auto backups: `~/.local/share/maya-theme/backups/`
- User exports: `~/Documents/` (user picks)
- Keep last N backups configurable (default 5)

---

## 13. Auto-Update Mechanism

### 13.1 Source
- Update manifest JSON (version, changelog, checksum, URL)
- Hosted locally or user-provided URL (no forced cloud)
- Signed manifest (GPG/checksum) — optional but recommended

### 13.2 Flow
1. Check on app start + manual "Check for updates"
2. If new version → show non-blocking notification with changelog
3. User clicks "Update" → download → verify checksum → backup → install
4. Apply with rollback safety (Section 8)
5. Confirm → done; failure → auto rollback

### 13.3 Rules
- **Opt-in by default** (user enables auto-check)
- Never auto-install without permission
- Offline → silent skip, no error spam
- No personal data sent to update server (only version + OS info)
- Privacy: manifest URL user-configurable; default = none (manual updates)

### 13.4 Commands
| Command | Purpose |
|---|---|
| `maya-theme update check` | Check available version |
| `maya-theme update apply` | Download + install (with confirm) |
| `maya-theme update configure` | Set source URL / opt-in |

---

## 14. Roadmap / Phases

### Phase 0 — Foundation ✅ (design)
- Plan lock, folder structure, decisions (Sections 1-7)

### Phase 1 — MVP (core glass)
- Glass color palette + KWin blur toggle
- Settings page skeleton (standalone app)
- Install / uninstall / rollback (Section 8)
- Basic tests

### Phase 2 — UI/UX Full
- Full glass component library (Section 7)
- Sidebar + tabs, search, instant + undo
- KDE System Settings module
- Right-side Quick Settings shade (Section 3)

### Phase 3 — Shell Integration
- Pinned apps center taskbar (Section 4)
- Wallpaper system (Section 5)
- Visual system monitoring (Section 6)

### Phase 4 — Polish
- Themed wallpapers, glass icons, animations
- Accessibility + responsive + i18n (future)
- Multi-monitor, performance tuning (Section 10)

### Phase 5 — Distribution
- Package (tar/zip) + install script (Section 8)
- Auto-update (Section 13)
- Docs, license, credits

### Phase 6 — Future
- GNOME support (if requested)
- Cross-toolkit GTK deeper theming
- Voice/AI-driven theme switching ("Maya, change to dark glass")

---

## 15. Privacy

### 15.1 Hard Rules
- **Local-first** — theme config, wallpapers, settings all on device
- **No telemetry** — no usage stats sent anywhere
- **No cloud calls** by default (update source = none/manual)
- No personal data in logs (only version + OS + metrics)
- Maya project privacy rules follow (DEVARAJ/ folder never touched)

### 15.2 What Leaves Device (only if user enables)
- Update check: version number + OS/Plasma version → update server
- Nothing else. No chat, no files, no details.

### 15.3 Settings
- Privacy page in settings: "Update checks" toggle (default off)
- "Diagnostics" toggle (default off) — logs stay local anyway
- Clear local logs button

### 15.4 Audit
- All network calls listed in docs (only update check)
- Code review checklist: no phone-home, no hidden endpoints
- Firewall-friendly: works fully offline

---

## Summary
Maya Extension = Fedora KDE premium liquid glass theme.
15 sections covering design, settings, shell integration, monitoring, install/rollback,
compatibility, performance, testing, backup, updates, roadmap, privacy.
UI-UX focus. Local-first. All settings user-selectable.
