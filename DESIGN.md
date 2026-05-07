---
name: Cyberpunk Minimalist
colors:
  surface: '#12121d'
  surface-dim: '#12121d'
  surface-bright: '#393844'
  surface-container-lowest: '#0d0d18'
  surface-container-low: '#1b1b26'
  surface-container: '#1f1f2a'
  surface-container-high: '#292934'
  surface-container-highest: '#343440'
  on-surface: '#e4e0f0'
  on-surface-variant: '#c7c4d7'
  inverse-surface: '#e4e0f0'
  inverse-on-surface: '#302f3b'
  outline: '#908fa0'
  outline-variant: '#464554'
  surface-tint: '#c0c1ff'
  primary: '#c0c1ff'
  on-primary: '#1000a9'
  primary-container: '#8083ff'
  on-primary-container: '#0d0096'
  inverse-primary: '#494bd6'
  secondary: '#56d5fe'
  on-secondary: '#003544'
  secondary-container: '#00a9d0'
  on-secondary-container: '#003847'
  tertiary: '#ffb783'
  on-tertiary: '#4f2500'
  tertiary-container: '#d97721'
  on-tertiary-container: '#452000'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#e1e0ff'
  primary-fixed-dim: '#c0c1ff'
  on-primary-fixed: '#07006c'
  on-primary-fixed-variant: '#2f2ebe'
  secondary-fixed: '#b8eaff'
  secondary-fixed-dim: '#56d5fe'
  on-secondary-fixed: '#001f28'
  on-secondary-fixed-variant: '#004d61'
  tertiary-fixed: '#ffdcc5'
  tertiary-fixed-dim: '#ffb783'
  on-tertiary-fixed: '#301400'
  on-tertiary-fixed-variant: '#703700'
  background: '#12121d'
  on-background: '#e4e0f0'
  surface-variant: '#343440'
typography:
  display-xl:
    fontFamily: Space Grotesk
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Space Grotesk
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.2'
  headline-md:
    fontFamily: Space Grotesk
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.3'
  body-base:
    fontFamily: Space Grotesk
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
  data-mono:
    fontFamily: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace
    fontSize: 14px
    fontWeight: '500'
    lineHeight: '1.5'
    letterSpacing: 0.05em
  label-caps:
    fontFamily: Space Grotesk
    fontSize: 12px
    fontWeight: '700'
    lineHeight: '1'
    letterSpacing: 0.1em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  container-margin: 2rem
  gutter: 1.5rem
  sidebar-width: 280px
  unit: 4px
---

## Brand & Style

The design system is engineered for high-performance professionals who require a focus-driven, high-utility environment. It embodies a **Cyberpunk Minimalist** aesthetic, stripping away unnecessary ornamentation to focus on raw data and precision. 

The emotional response is one of "The Void"—a deep, immersive space where neon accents guide the user's attention to critical path actions. The visual language balances the ethereal nature of glassmorphism with the cold, hard edges of technical precision, creating a premium feel that differentiates the product from standard enterprise tools.

## Colors

The palette is anchored by a deep-space navy background that provides infinite depth. **Neon Indigo** serves as the primary driver for "Energy" and core actions, while **Electric Cyan** is reserved for secondary interactions and interactive highlights. 

To maintain the cyberpunk aesthetic, status colors are highly saturated and "vibrant," cutting through the dark background with high contrast. Use subtle mesh gradients (Indigo to Transparent) in the background to provide a sense of atmospheric light without distracting from the data.

## Typography

This design system utilizes **Space Grotesk** across all primary UI levels to evoke a technical, cutting-edge personality. Headings should be bold and tightly tracked to create a sense of structural authority.

For data-dense areas, such as project IDs, timestamps, and numerical metrics, use a **highly legible monospace stack**. This ensures that vertical columns of data align perfectly, aiding in rapid scanning and comparative analysis. Small labels should be uppercase with increased letter spacing for a "HUD" (Heads-Up Display) effect.

## Layout & Spacing

The layout follows a **fluid grid** model optimized for ultra-wide desktop monitors. The primary navigation is anchored to a fixed-width left sidebar (280px) to maximize vertical real estate for project timelines and Kanban boards.

Main content areas utilize a 12-column grid system with generous gutters (24px) to prevent data overcrowding. Spacing follows a 4px base unit, ensuring that while the aesthetic is "minimal," the density remains high enough for professional workflows. Use "Void Space" (large areas of empty background) to separate major logical sections rather than heavy dividers.

## Elevation & Depth

Depth in this system is achieved through **Glassmorphism** and light-based layering rather than traditional drop shadows.

- **Surface Layers:** Use semi-transparent layers with a 20px+ backdrop blur to create a frosted glass effect.
- **Borders:** Every glass surface must have a 1px translucent border (`rgba(255, 255, 255, 0.1)`) to define its edges against the dark background.
- **Atmospheric Glow:** Use Indigo or Cyan outer glows (spread 15px, opacity 20%) for active states or high-priority alerts to simulate neon light reflecting off a surface.
- **Z-Index Strategy:** Higher elevation levels should be represented by increased background opacity (lighter) and sharper border contrast.

## Shapes

The design system employs a "Hybrid Geometric" approach to shapes:

1.  **Cards & Containers:** Use a soft 16px radius (`rounded-lg`) for large containers and cards. This softens the tech-heavy aesthetic and makes the "glass" panels feel more premium and approachable.
2.  **UI Controls:** Buttons, input fields, and checkboxes must utilize **sharp precision** (0px - 2px radius). This creates a distinct visual contrast between the "frame" (the container) and the "tools" (the controls), emphasizing technical accuracy.
3.  **Active Indicators:** Use 1px vertical or horizontal lines with sharp edges to denote selected states in sidebars and lists.

## Components

- **Glass Cards:** Primary containers for modules. Use a 20px backdrop blur, 1px white/10% border, and a subtle top-left to bottom-right mesh gradient.
- **Precision Buttons:** Sharp corners. Primary buttons use a solid Neon Indigo fill with white text. Secondary buttons use a Cyan 1px border and transparent background.
- **Data Tables:** Row-based layouts with no vertical borders. Use 1px translucent horizontal separators. Hover states should trigger a subtle Indigo glow on the left edge of the row.
- **Status Pills:** Small, high-contrast badges using the Emerald, Amber, and Crimson palette. Text should be uppercase and monospaced.
- **Input Fields:** Darker than the background (#000000) with a sharp 0px radius. The bottom border should glow Cyan when focused.
- **Sidebars:** Integrated glass blur that spans the full height of the viewport, visually separating the "control center" from the "workplace."