# Recruiting Frontend
---

## Task Description
For this task you are asked to design and develop a simple website frontend using **Next.js 14+ (App Router)**.
You can choose whatever you like as subject for the website, for example a personal portfolio, a digital agency, a website for a new product or brand, etc.

You are asked to:
1. Design the interface using Figma
2. Develop the website based on the previous design using Next.js

The website should consist of at least three pages: Home, About and Contacts.
Create a light mode and a dark mode for each page.

### **Overview**
Each level introduces new challenges for the website frontend. Candidates will earn **points** for each completed level.

| **Level** | **Task** | **Description** |
|-----------|----------|-----------------|
| **1** | **Figma Design System** | Design complete mockups in Figma for all 3 pages (Home, About, Contacts) with light/dark mode variants, color palette (#000000, #ffffff, #f3ff14), Helvetica Neue typography hierarchy, and responsive breakpoints (mobile, tablet, desktop) |
| **2** | **Structure & Core Components** | Build Next.js 14+ project structure with App Router, implement consistent navbar with navigation using `<Link>`, create reusable footer component, set up color system using CSS variables (Tailwind recommended) for easy theme switching, and establish typographic hierarchy |
| **3** | **Home Page Implementation** | Develop full-screen hero section with black background, centered title with fade-in animation (client component), yellow CTA button using `<Link>`; create highlights section with 3 expertise cards featuring grayscale images (use `next/image`) and yellow hover effects; ensure responsive layout |
| **4** | **About Page & Services** | Build About page with white header, 2-column layout (image + text) using `next/image` that stacks vertically on mobile, implement 3-4 service blocks with icons and yellow hover backgrounds, add final CTA section with yellow button using `<Link>` to Contact page |
| **5** | **Contact Page, Form & Theme Toggle** | Create contact form (client component) with Name, Email, Message fields and frontend validation (React state or React Hook Form), style with yellow submit button, add contact information section, implement dark/light mode toggle (Context API or next-themes) that works across all pages while maintaining design consistency |
| **Bonus 1** | **Advanced Animations & Video** | Add black & white background video section to Home page with dark overlay and yellow text, implement typing effect for hero title as alternative animation, create smooth page transitions (Framer Motion) and micro-interactions on hover states |
| **Bonus 2** | **Performance & Polish** | Optimize for mobile touch interactions, implement lazy loading for images/video (dynamic imports), add smooth scrolling navigation, ensure WCAG accessibility standards, optimize with proper code splitting, add loading animations and error states for form validation |

## Requirements
The following requirements **have to** be followed.

### Technology Stack
- **Framework**: Next.js 14+ with App Router (mandatory)
- **Language**: TypeScript (recommended) or JavaScript
- **Styling**: Tailwind CSS (recommended) or CSS Modules
- **Package Manager**: npm, yarn, or pnpm

### Color palette
- **Pure Black (#000000)**: as dominant color with shades if needed
- **Pure White (#ffffff)**: as secondary color
- **Yellow E-Agle (#f3ff14)**: as accent color 

> [!TIP]
> You can use the 60-30-10 rule to balance the colors: 60% dominant, 30% secondary and 10% accent

### Typography
- Font: **Helvetica Neue** (use `next/font` for optimization)
- Use a clear font hierarchy between titles and text

### Style
- Minimal and modern design
- Avoid adding too much elements if not needed
- Avoid overuse of animations

### Responsiveness
- Keep the layout as adaptive as possible
- The website should be easy to use and visually appealing.
- Scalable text and buttons
- Touch-friendly elements 

### Page 1 - Home
### Sections to be implemented
1. Navbar (in `app/layout.tsx` for sharing across pages)
    - Use `<Link>` from `next/link` for navigation
2. Hero section (full screen)
    - Solid black background
    - Large, centered title: "Minimal design, maximum impact." (or similar)
    - Yellow call-to-action button using `<Link href="/contact">`
    - Add a small animation (fade-in, typing effect, or other) - requires client component with `'use client'`
    - Alternative: automatic slider with 2-3 black and white images 
3. Highlights section
    - White background with black text
    - Present 3 areas of expertise (e.g., Design, Development, Strategy)
    - Use cards or blocks with minimal icons or grayscale images
    - Use `next/image` for optimized image loading
    - Hover effect with yellow color 
4. Video section (optional)
    - Black and white background video
    - Dark overlay with yellow text 
5. Footer (in `app/layout.tsx`)
    - Black background, white text 

### Page 2 - About/Services
### Sections to be implemented
1. Navbar (automatically included from layout)
2. Header
    - White background
    - Main title: "About us" or "Services"
    - Descriptive subtitle 
3. main content
    - 2-column layout on desktop (image + text) using CSS Grid/Flexbox
    - On mobile: vertical layout (image above, text below) - use responsive Tailwind classes
    - Black and white images using `next/image` for optimization
    - Text with good readability (generous spacing) 
4.  Services Section 
    - Present 3-4 services offered
    - Blocks with small icons and concise text
    - Hover with yellow background 
5. Final Call-to-Action
    - Call-to-action text (e.g., "Ready to collaborate?")
    - Yellow button that leads to the Contact page using `<Link href="/contact">`
6. Footer (automatically included from layout)

### Page 3 - Contacts
### Sections to be implemented
1. Navbar (automatically included from layout)
2. Header
    - Black background
    - Yellow title: "Contact us" 
3. Contact Form (must be client component with `'use client'`)
    - Fields to include: Name, Email, Message
    - Minimalist style with clean edges (light gray)
    - Yellow submit button with black text
    - Frontend validation using React state or React Hook Form
    - No functioning backend required 
4. Additional Information
    - Address, email, or phone number (even fictitious)
    - Option to add a stylized black and white map or decorative image using `next/image`
5. Footer (automatically included from layout)
    - Consistent with other pages