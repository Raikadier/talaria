# Graph Report - RoundedTB  (2026-08-01)

## Corpus Check
- 26 files · ~345,639 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 440 nodes · 801 edges · 21 communities
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 11 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b78e5d6e`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- LocalPInvoke
- Window
- TaskbarEffect
- Interaction
- MainWindow
- Window
- AppListXaml
- RoundedTB
- AppBars
- MonitorStuff
- Button
- RoundedTB.csproj
- IAppVisibility.cs
- TextBox
- RoundedTB — Mapa de arquitectura (fork base `b78e5d6`)
- RoutedEventArgs
- Settings
- cornerRadiusSlider
- RoundedTB
- .ShowMenuItem_Click

## God Nodes (most connected - your core abstractions)
1. `LocalPInvoke` - 59 edges
2. `MainWindow` - 54 edges
3. `Window` - 42 edges
4. `Window` - 24 edges
5. `Interaction` - 22 edges
6. `RoundedTB` - 14 edges
7. `Taskbar` - 13 edges
8. `TaskbarEffect` - 11 edges
9. `CheckBox` - 10 edges
10. `AppListXaml` - 10 edges

## Surprising Connections (you probably didn't know these)
- `Background` --references--> `MainWindow`  [EXTRACTED]
  RoundedTB/Background.cs → RoundedTB/MainWindow.xaml.cs
- `Interaction` --references--> `MainWindow`  [EXTRACTED]
  RoundedTB/Interaction.cs → RoundedTB/MainWindow.xaml.cs
- `Window` --references--> `MainWindow`  [EXTRACTED]
  RoundedTB/MainWindow.xaml → RoundedTB/MainWindow.xaml.cs
- `Taskbar` --references--> `TaskbarEffect`  [EXTRACTED]
  RoundedTB/Types.cs → RoundedTB/TaskbarEffect.xaml.cs
- `Window` --references--> `AboutWindow`  [EXTRACTED]
  RoundedTB/AboutWindow.xaml → RoundedTB/AboutWindow.xaml.cs

## Import Cycles
- None detected.

## Communities (21 total, 0 thin omitted)

### Community 0 - "LocalPInvoke"
Cohesion: 0.05
Nodes (42): ABM, AccentState, DWMWINDOWATTRIBUTE, EnumWindowsProc, EventArgs, HandleRef, RedrawWindowFlags, DoWorkEventArgs (+34 more)

### Community 1 - "Window"
Cohesion: 0.09
Nodes (30): RequestNavigateEventArgs, aboutTitleBar, bannerCan, bannerDev, bannerMst, bodyBlock0, bodyBlock1, bodyBlock2 (+22 more)

### Community 2 - "TaskbarEffect"
Cohesion: 0.07
Nodes (26): Rectangle, bodyBlock, okButton, titleBlock, Window, RoutedEventArgs, Infobox, Button (+18 more)

### Community 3 - "Interaction"
Cohesion: 0.09
Nodes (9): CancelEventArgs, IntPtr, List, RECT, Settings, string, Interaction, TaskbarPosition (+1 more)

### Community 4 - "MainWindow"
Cohesion: 0.11
Nodes (13): HwndSource, MouseEventArgs, fillMaximisedCheckBox, BackgroundWorker, bool, int, IntPtr, Settings (+5 more)

### Community 5 - "Window"
Cohesion: 0.12
Nodes (24): autoHideComboBox, centredCheckBox, clockWidthLabel, compositionFixCheckBox, cornerRadiusLabel, fillAltTabCheckBox, MainGrid, mainTitleBar (+16 more)

### Community 6 - "AppListXaml"
Cohesion: 0.11
Nodes (17): IDisposable, IUIAutomation, IUIAutomationElement, AppListXaml, bool, IntPtr, RECT, SegmentSettings (+9 more)

### Community 7 - "RoundedTB"
Cohesion: 0.09
Nodes (11): Action, RoundedTB, IEnumerable, Application, App, bool, int, Background (+3 more)

### Community 8 - "AppBars"
Cohesion: 0.15
Nodes (16): ABE, AppBarStates, Int32, APPBARDATA, DllImport, IntPtr, RECT, APPBARDATA (+8 more)

### Community 9 - "MonitorStuff"
Cohesion: 0.14
Nodes (15): DisplayInfo, DisplayInfoCollection, EnumMonitorsDelegate, List, MONITORINFO, DllImport, int, IntPtr (+7 more)

### Community 10 - "Button"
Cohesion: 0.16
Nodes (11): IReadOnlyList, applyButton, clockRectStandIn, splitHelpButton, taskbarRectStandIn, trayRectStandIn, widgetsRectStandIn, SegmentSettings (+3 more)

### Community 11 - "RoundedTB.csproj"
Cohesion: 0.12
Nodes (13): net6.0-windows10.0.19041, DesktopBridge.Helpers, Hardcodet.NotifyIcon.Wpf, Interop.UIAutomationClient, Interop.UIAutomationCore, Microsoft.CSharp (4.7.0), Microsoft.DotNet.UpgradeAssistant.Extensions.Default.Analyzers (0.3.261602), Microsoft.Windows.Compatibility (6.0.0) (+5 more)

### Community 12 - "IAppVisibility.cs"
Cohesion: 0.21
Nodes (6): IntPtr, MarshalAs, AppVisibility, IAppVisibility, IAppVisibilityEvents, MONITOR_APP_VISIBILITY

### Community 13 - "TextBox"
Cohesion: 0.15
Nodes (8): clockWidthInput, cornerRadiusInput, mBottomInput, mLeftInput, mRightInput, mTopInput, widgetWidthInput, TextBox

### Community 14 - "RoundedTB — Mapa de arquitectura (fork base `b78e5d6`)"
Cohesion: 0.18
Nodes (10): Backlog propuesto (desde este mapa), Código muerto a no tocar (salvo limpieza), Estado compartido, Flujo runtime, Hotspots (prioridad), Módulos, Orden de lectura, Qué es (+2 more)

### Community 15 - "RoutedEventArgs"
Cohesion: 0.24
Nodes (4): aboutButton, dynamicCheckBox, showSegmentsOnHoverCheckBox, RoutedEventArgs

### Community 16 - "Settings"
Cohesion: 0.29
Nodes (6): ApplicationSettingsBase, RoundedTB.Properties, CultureInfo, ResourceManager, Resources, Settings

### Community 17 - "cornerRadiusSlider"
Cohesion: 0.33
Nodes (4): DragCompletedEventArgs, cornerRadiusSlider, RoutedPropertyChangedEventArgs, Slider

### Community 18 - "RoundedTB"
Cohesion: 0.33
Nodes (5): Add margins, rounded corners and segments to your taskbars!, How do I get it?, Known issues, Other info, RoundedTB

### Community 19 - ".ShowMenuItem_Click"
Cohesion: 0.33
Nodes (4): CloseMenuItem, DebugMenuItem, ShowMenuItem, MenuItem

## Knowledge Gaps
- **54 isolated node(s):** `TitleBar`, `AppBarMessages`, `AppBarStates`, `ReloadChecker`, `AppVisibility` (+49 more)
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `MainWindow` connect `MainWindow` to `LocalPInvoke`, `TaskbarEffect`, `Interaction`, `Window`, `RoundedTB`, `Button`, `TextBox`, `RoutedEventArgs`, `cornerRadiusSlider`, `.ShowMenuItem_Click`?**
  _High betweenness centrality (0.380) - this node is a cross-community bridge._
- **Why does `RoundedTB` connect `RoundedTB` to `Window`, `TaskbarEffect`, `AppListXaml`, `MonitorStuff`, `IAppVisibility.cs`?**
  _High betweenness centrality (0.214) - this node is a cross-community bridge._
- **Why does `LocalPInvoke` connect `LocalPInvoke` to `AppBars`, `Interaction`, `AppListXaml`, `RoundedTB`?**
  _High betweenness centrality (0.157) - this node is a cross-community bridge._
- **What connects `TitleBar`, `AppBarMessages`, `AppBarStates` to the rest of the system?**
  _54 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `LocalPInvoke` be split into smaller, more focused modules?**
  _Cohesion score 0.05464725643896976 - nodes in this community are weakly interconnected._
- **Should `Window` be split into smaller, more focused modules?**
  _Cohesion score 0.09047619047619047 - nodes in this community are weakly interconnected._
- **Should `TaskbarEffect` be split into smaller, more focused modules?**
  _Cohesion score 0.07007575757575757 - nodes in this community are weakly interconnected._