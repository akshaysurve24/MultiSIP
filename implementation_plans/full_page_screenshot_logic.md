# Full-Page Screenshot Strategy & Animation Disabling

## The Problem
Default Playwright screenshots only capture the visible above-the-fold viewport (typically 1280x720). In long forms, tables, and stepper flows (like mutual fund SIP setup or mandate verification), crucial validation errors or bottom action buttons are often clipped off.

Furthermore, CSS keyframe animations, blinking cursors, and spinner fades introduce anti-aliasing artifacts and visual flakiness when screenshots are inspected or diffed.

## Solution
We enforce two mandatory options in all screenshot calls:
1. `full_page=True`: Scrolls through the document and stitches together the entire rendered canvas from top to bottom.
2. `animations="disabled"`: Freezes all CSS transitions, animations, and infinite keyframes immediately before capturing pixels.

```python
self.page.screenshot(path=screenshot_path, full_page=True, animations="disabled")
```

## Special Considerations for Sticky Elements
If an application uses fixed headers (`position: fixed`), Playwright's full-page renderer handles standard fixed positioning natively. If custom sticky containers fail to expand, `BasePage.js_click` and smooth scroll triggers ensure elements are brought into view before capturing.
