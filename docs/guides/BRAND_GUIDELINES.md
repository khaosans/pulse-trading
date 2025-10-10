# 🎨 PulseTrade Brand Guidelines

## Brand Identity

### Mission Statement
**"Empowering Retail Investors Through Emotion-Aware Trading"**

Smart Trading Through Data + Community + Emotional Intelligence

---

## 🎨 Visual Identity

### Logo Usage

#### Primary Logo
- **Symbol:** Heart pulse wave + Trading graph fusion
- **Shape:** Circular badge design
- **Style:** Modern, clean, professional
- **Animation:** Subtle pulse effect (2s loop)

#### Logo Variations
1. **Full Color** - Primary use on light backgrounds
2. **White** - Use on dark/colored backgrounds
3. **Monochrome** - Single color applications
4. **Icon Only** - Small sizes, app icons

#### Clear Space
- Minimum clear space: 0.25x logo height on all sides
- Never place logo smaller than 32px width

---

## 🎨 Color Palette

### Primary Colors

```css
--primary-color: #1D6F7A      /* Teal - Trust, stability */
--primary-light: #2AA5B3      /* Aqua - Innovation */
--primary-dark: #155259       /* Deep Teal - Depth */
```

**Usage:**
- Primary: Main CTAs, headers, key UI elements
- Light: Hover states, highlights, accents
- Dark: Text on light backgrounds, shadows

### Secondary Colors

```css
--secondary-teal: #0D9488     /* Vibrant Teal */
--secondary-cyan: #06B6D4     /* Bright Cyan */
```

**Usage:**
- Secondary actions
- Links and navigation
- Decorative elements

### Semantic Colors

```css
--success: #10B981            /* Green - Success states */
--warning: #F59E0B            /* Amber - Warnings */
--error: #EF4444              /* Red - Errors */
--info: #3B82F6               /* Blue - Information */
```

### Text Colors

```css
--text-primary: #1A202C       /* Primary text */
--text-secondary: #4A5568     /* Secondary text */
--text-light: #718096         /* Muted text */
--text-white: #FFFFFF         /* White text */
```

### Background Colors

```css
--bg-primary: #FFFFFF         /* Main background */
--bg-secondary: #F7FAFC       /* Section backgrounds */
--bg-tertiary: #EDF2F7        /* Tertiary backgrounds */
--bg-dark: #1A202C            /* Dark mode background */
```

---

## 📝 Typography

### Font Family

```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 
             'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 
             'Fira Sans', 'Droid Sans', 'Helvetica Neue', 
             sans-serif;
```

**Fallback Strategy:**
1. System fonts first (performance)
2. Popular sans-serif fonts
3. Generic sans-serif

### Font Sizes

| Element | Size | Weight | Use Case |
|---------|------|--------|----------|
| H1 | 2.5rem (40px) | 800 | Page titles |
| H2 | 2rem (32px) | 700 | Section headers |
| H3 | 1.75rem (28px) | 700 | Subsection headers |
| H4 | 1.5rem (24px) | 600 | Card headers |
| H5 | 1.25rem (20px) | 600 | Small headers |
| H6 | 1.125rem (18px) | 600 | Micro headers |
| Body | 1rem (16px) | 400 | Body text |
| Small | 0.875rem (14px) | 400 | Helper text |
| Tiny | 0.75rem (12px) | 500 | Labels |

### Font Weights

- **300 (Light):** Rarely used
- **400 (Regular):** Body text
- **500 (Medium):** Emphasized text
- **600 (Semibold):** Subheadings
- **700 (Bold):** Headings
- **800 (Extra Bold):** Hero text, numbers

---

## 🎯 Design Principles

### 1. Clarity Over Complexity
- Clean, uncluttered interfaces
- Clear visual hierarchy
- Obvious user actions

### 2. Emotion-First Design
- Empathetic color choices
- Calming animations
- Supportive messaging

### 3. Data-Driven Aesthetics
- Charts and graphs prominent
- Numbers clearly displayed
- Real-time indicators visible

### 4. Professional Trust
- Consistent spacing
- Polished details
- High-quality visuals

---

## 📐 Spacing System

### Scale (8px base unit)

```css
--space-1: 0.25rem  /* 4px */
--space-2: 0.5rem   /* 8px */
--space-3: 0.75rem  /* 12px */
--space-4: 1rem     /* 16px */
--space-5: 1.5rem   /* 24px */
--space-6: 2rem     /* 32px */
--space-8: 3rem     /* 48px */
--space-10: 4rem    /* 64px */
```

### Usage Guidelines

- **Tight:** 4-8px (related elements)
- **Normal:** 16-24px (section spacing)
- **Loose:** 32-48px (major sections)
- **Extra Loose:** 64px+ (page sections)

---

## 🎨 Border Radius

```css
--radius-sm: 6px     /* Small elements */
--radius-md: 8px     /* Buttons, inputs */
--radius-lg: 12px    /* Cards, modals */
--radius-xl: 16px    /* Large containers */
--radius-full: 50%   /* Circles, pills */
```

---

## 🌈 Shadows

### Elevation System

```css
/* Small - Subtle depth */
--shadow-sm: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 
             0 1px 2px 0 rgba(0, 0, 0, 0.06);

/* Medium - Cards */
--shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 
             0 2px 4px -1px rgba(0, 0, 0, 0.06);

/* Large - Modals, dialogs */
--shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 
             0 4px 6px -2px rgba(0, 0, 0, 0.05);

/* Extra Large - Dropdowns */
--shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 
             0 10px 10px -5px rgba(0, 0, 0, 0.04);
```

---

## 🎬 Animation Guidelines

### Timing

```css
--transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
--transition-normal: 300ms cubic-bezier(0.4, 0, 0.2, 1);
--transition-slow: 500ms cubic-bezier(0.4, 0, 0.2, 1);
```

### Easing Curves

- **Ease-out:** Elements entering view
- **Ease-in:** Elements leaving view
- **Ease-in-out:** Elements moving on screen
- **Linear:** Continuous looping

### Animation Principles

1. **Purposeful:** Every animation serves a function
2. **Subtle:** Never distracting
3. **Smooth:** 60fps target
4. **Responsive:** Adapts to device capability
5. **Accessible:** Respects reduced motion

---

## 🖼️ Iconography

### Icon Style

- **Type:** Line icons (stroke-based)
- **Weight:** 2px stroke
- **Style:** Rounded corners
- **Size:** 16px, 20px, 24px, 32px

### Icon Colors

- **Default:** var(--text-secondary)
- **Hover:** var(--primary-color)
- **Active:** var(--primary-dark)
- **Disabled:** var(--text-light)

---

## 🎯 Component Patterns

### Buttons

#### Primary Button
```css
background: linear-gradient(135deg, #1D6F7A 0%, #2AA5B3 100%);
color: white;
padding: 0.875rem 2.5rem;
border-radius: 8px;
font-weight: 700;
```

#### Secondary Button
```css
background: transparent;
color: #1D6F7A;
border: 2px solid #1D6F7A;
padding: 0.875rem 2.5rem;
border-radius: 8px;
font-weight: 600;
```

#### Ghost Button
```css
background: transparent;
color: #1D6F7A;
border: none;
padding: 0.875rem 1.5rem;
font-weight: 600;
```

### Cards

```css
background: white;
border-radius: 12px;
padding: 2rem;
box-shadow: var(--shadow-md);
border: 1px solid #E5E7EB;
```

### Inputs

```css
border: 2px solid #E5E7EB;
border-radius: 8px;
padding: 0.75rem 1rem;
font-size: 1rem;
transition: border-color 0.2s;
```

**Focus State:**
```css
border-color: #2AA5B3;
box-shadow: 0 0 0 3px rgba(42, 165, 179, 0.1);
```

---

## 📱 Responsive Breakpoints

```css
/* Mobile First Approach */
--mobile: 320px
--mobile-lg: 480px
--tablet: 768px
--desktop: 1024px
--desktop-lg: 1280px
--desktop-xl: 1536px
```

### Grid System

- **Mobile:** 1 column
- **Tablet:** 2 columns
- **Desktop:** 3-4 columns
- **Large Desktop:** 4-6 columns

---

## ♿ Accessibility Standards

### Color Contrast

- **Normal Text:** Minimum 4.5:1 ratio (WCAG AA)
- **Large Text:** Minimum 3:1 ratio
- **Interactive Elements:** Minimum 3:1 ratio

### Focus States

```css
outline: 3px solid #2AA5B3;
outline-offset: 2px;
border-radius: 4px;
```

### Touch Targets

- **Minimum Size:** 44x44px
- **Spacing:** 8px between targets
- **Visual Feedback:** Instant on tap

---

## 🎨 Logo Implementation

### SVG Logo
```html
<svg class="logo-animated" width="80" height="80">
  <!-- Logo content -->
</svg>
```

### Fallback Logo
```html
<div class="logo-fallback">
  <span>PT</span>
</div>
```

### Logo Colors

**On Light Background:**
- Primary: #1D6F7A
- Gradient: #1D6F7A → #2AA5B3

**On Dark Background:**
- Primary: #FFFFFF
- Gradient: #FFFFFF → #2AA5B3

---

## 📊 Data Visualization

### Chart Colors

**Primary Data:**
- Main Line: #1D6F7A
- Fill: rgba(29, 111, 122, 0.1)

**Secondary Data:**
- Line: #2AA5B3
- Fill: rgba(42, 165, 179, 0.1)

**Positive Values:**
- Color: #10B981
- Background: #D1FAE5

**Negative Values:**
- Color: #EF4444
- Background: #FEE2E2

---

## 🎯 Usage Examples

### Correct ✅

```css
/* Consistent spacing */
.card {
  padding: var(--space-6);
  margin-bottom: var(--space-4);
}

/* Proper color usage */
.button-primary {
  background: var(--primary-color);
  color: var(--text-white);
}

/* Accessible contrast */
.text-on-primary {
  color: white; /* Passes WCAG AA */
}
```

### Incorrect ❌

```css
/* Random spacing */
.card {
  padding: 15px;
  margin-bottom: 23px;
}

/* Wrong color */
.button-primary {
  background: #0000FF; /* Not brand color */
}

/* Poor contrast */
.text-on-primary {
  color: #CCCCCC; /* Fails WCAG */
}
```

---

## 📝 Voice & Tone

### Brand Voice

- **Professional** yet **approachable**
- **Data-driven** yet **empathetic**
- **Confident** yet **supportive**
- **Technical** yet **accessible**

### Writing Guidelines

**Do:**
- Use active voice
- Be concise and clear
- Explain technical terms
- Provide context

**Don't:**
- Use jargon unnecessarily
- Be overly casual
- Make assumptions
- Hide important information

---

## 🚀 Implementation Checklist

### Every Component Should Have:

- [ ] Consistent color palette
- [ ] Proper spacing (8px grid)
- [ ] Appropriate shadows
- [ ] Smooth transitions
- [ ] Accessible focus states
- [ ] Mobile responsiveness
- [ ] Loading states
- [ ] Error states
- [ ] Success states
- [ ] Hover effects

---

## 📚 Resources

### Design Tools
- Figma: Component library
- Adobe Color: Color palette generator
- Contrast Checker: Accessibility validation

### Code Resources
- CSS Variables: `assets/css/variables.css`
- Animation Library: `ai_animations.css`
- Component Styles: Embedded in `demo_app.py`

---

## 🔄 Version History

- **v1.0** (Oct 2025) - Initial brand guidelines
- Establishes core visual identity
- Defines color system and typography
- Sets animation standards

---

*These guidelines ensure consistent, professional, and accessible design across all PulseTrade touchpoints.*

**Questions?** Refer to this guide or contact the design team.

