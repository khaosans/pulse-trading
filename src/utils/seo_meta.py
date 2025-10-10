"""
SEO & Meta Tags Module
Improves discoverability and browser compatibility
"""

import streamlit as st
from typing import Optional, List, Dict


class SEOManager:
    """Manages SEO meta tags and social media cards"""
    
    @staticmethod
    def add_meta_tags(
        title: str = "PulseTrade - Emotion-Aware Trading Platform",
        description: str = "Revolutionary trading platform combining real-time biometric emotion tracking with AI-powered analytics",
        keywords: List[str] = None,
        author: str = "PulseTrade Team",
        image_url: Optional[str] = None,
        url: str = "https://github.com/khaosans/pulse-trading"
    ) -> None:
        """
        Add comprehensive SEO meta tags
        
        Args:
            title: Page title
            description: Page description
            keywords: List of keywords
            author: Page author
            image_url: Social media image URL
            url: Canonical URL
        """
        if keywords is None:
            keywords = [
                "trading",
                "emotion tracking",
                "biometric",
                "AI trading",
                "fintech",
                "stock market",
                "portfolio management",
                "trading psychology"
            ]
        
        keywords_str = ", ".join(keywords)
        
        # Standard meta tags
        st.markdown(f"""
        <meta name="description" content="{description}">
        <meta name="keywords" content="{keywords_str}">
        <meta name="author" content="{author}">
        <meta name="robots" content="index, follow">
        <meta name="language" content="English">
        <meta name="revisit-after" content="7 days">
        
        <!-- Open Graph / Facebook -->
        <meta property="og:type" content="website">
        <meta property="og:url" content="{url}">
        <meta property="og:title" content="{title}">
        <meta property="og:description" content="{description}">
        {f'<meta property="og:image" content="{image_url}">' if image_url else ''}
        
        <!-- Twitter -->
        <meta property="twitter:card" content="summary_large_image">
        <meta property="twitter:url" content="{url}">
        <meta property="twitter:title" content="{title}">
        <meta property="twitter:description" content="{description}">
        {f'<meta property="twitter:image" content="{image_url}">' if image_url else ''}
        
        <!-- Canonical URL -->
        <link rel="canonical" href="{url}">
        """, unsafe_allow_html=True)
    
    @staticmethod
    def add_browser_compatibility_tags() -> None:
        """Add browser compatibility and optimization tags"""
        st.markdown("""
        <!-- Viewport and compatibility -->
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        
        <!-- Theme color for mobile browsers -->
        <meta name="theme-color" content="#1D6F7A">
        <meta name="msapplication-TileColor" content="#1D6F7A">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
        
        <!-- Preconnect to external domains for performance -->
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://cdn.plot.ly">
        <link rel="dns-prefetch" href="https://fonts.googleapis.com">
        
        <!-- Performance hints -->
        <meta http-equiv="x-dns-prefetch-control" content="on">
        
        <!-- Security headers (Content Security Policy) -->
        <meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests">
        """, unsafe_allow_html=True)
    
    @staticmethod
    def add_structured_data(data: Dict) -> None:
        """
        Add JSON-LD structured data for rich snippets
        
        Args:
            data: Structured data dictionary
        """
        import json
        
        structured_data = {
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": data.get("name", "PulseTrade"),
            "description": data.get("description", "Emotion-Aware Trading Platform"),
            "applicationCategory": "FinanceApplication",
            "operatingSystem": "Web",
            "offers": {
                "@type": "Offer",
                "price": data.get("price", "0"),
                "priceCurrency": "USD"
            }
        }
        
        st.markdown(f"""
        <script type="application/ld+json">
        {json.dumps(structured_data, indent=2)}
        </script>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def add_favicon_links() -> None:
        """Add favicon links for multiple devices"""
        st.markdown("""
        <!-- Favicons -->
        <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
        <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
        <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
        <link rel="manifest" href="/site.webmanifest">
        """, unsafe_allow_html=True)
    
    @staticmethod
    def add_progressive_web_app_tags() -> None:
        """Add PWA (Progressive Web App) meta tags"""
        st.markdown("""
        <!-- PWA -->
        <link rel="manifest" href="/manifest.json">
        <meta name="mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="application-name" content="PulseTrade">
        <meta name="apple-mobile-web-app-title" content="PulseTrade">
        <meta name="msapplication-starturl" content="/">
        <meta name="msapplication-TileColor" content="#1D6F7A">
        """, unsafe_allow_html=True)


class AccessibilityEnhancer:
    """Enhances accessibility beyond WCAG compliance"""
    
    @staticmethod
    def add_aria_live_regions() -> None:
        """Add ARIA live regions for dynamic content"""
        st.markdown("""
        <!-- ARIA Live Regions -->
        <div id="status-messages" aria-live="polite" aria-atomic="true" class="sr-only"></div>
        <div id="alert-messages" aria-live="assertive" aria-atomic="true" class="sr-only"></div>
        
        <style>
        .sr-only {
            position: absolute;
            width: 1px;
            height: 1px;
            padding: 0;
            margin: -1px;
            overflow: hidden;
            clip: rect(0, 0, 0, 0);
            white-space: nowrap;
            border-width: 0;
        }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def add_keyboard_shortcuts() -> None:
        """Add keyboard shortcut hints"""
        st.markdown("""
        <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Add keyboard shortcuts
            document.addEventListener('keydown', function(e) {
                // ? key - show help
                if (e.key === '?' && !e.ctrlKey && !e.metaKey) {
                    const helpElement = document.querySelector('[data-testid="stSidebar"]');
                    if (helpElement) {
                        helpElement.scrollIntoView({ behavior: 'smooth' });
                    }
                }
                
                // Escape key - close modals
                if (e.key === 'Escape') {
                    const modals = document.querySelectorAll('[role="dialog"]');
                    modals.forEach(modal => {
                        modal.style.display = 'none';
                    });
                }
            });
        });
        </script>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def add_focus_trap() -> None:
        """Add focus trap for modal dialogs"""
        st.markdown("""
        <script>
        function trapFocus(element) {
            const focusableElements = element.querySelectorAll(
                'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
            );
            const firstFocusable = focusableElements[0];
            const lastFocusable = focusableElements[focusableElements.length - 1];
            
            element.addEventListener('keydown', function(e) {
                if (e.key === 'Tab') {
                    if (e.shiftKey) {
                        if (document.activeElement === firstFocusable) {
                            lastFocusable.focus();
                            e.preventDefault();
                        }
                    } else {
                        if (document.activeElement === lastFocusable) {
                            firstFocusable.focus();
                            e.preventDefault();
                        }
                    }
                }
            });
        }
        
        // Apply to modals when they appear
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                mutation.addedNodes.forEach(function(node) {
                    if (node.nodeType === 1 && node.getAttribute('role') === 'dialog') {
                        trapFocus(node);
                    }
                });
            });
        });
        
        observer.observe(document.body, { childList: true, subtree: true });
        </script>
        """, unsafe_allow_html=True)


class PerformanceOptimizer:
    """Additional performance optimizations"""
    
    @staticmethod
    def add_resource_hints() -> None:
        """Add resource hints for better performance"""
        st.markdown("""
        <!-- Resource hints -->
        <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap">
        <link rel="prefetch" href="/data/market-data.json">
        
        <!-- Prerender hint for next likely page -->
        <link rel="prerender" href="/dashboard">
        """, unsafe_allow_html=True)
    
    @staticmethod
    def add_lazy_loading_script() -> None:
        """Add intersection observer for lazy loading"""
        st.markdown("""
        <script>
        // Lazy loading for images
        document.addEventListener('DOMContentLoaded', function() {
            const images = document.querySelectorAll('img[data-src]');
            
            const imageObserver = new IntersectionObserver(function(entries, observer) {
                entries.forEach(function(entry) {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                        imageObserver.unobserve(img);
                    }
                });
            });
            
            images.forEach(function(img) {
                imageObserver.observe(img);
            });
        });
        </script>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def add_service_worker_hint() -> None:
        """Add service worker registration hint (for future PWA support)"""
        st.markdown("""
        <script>
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', function() {
                // Uncomment when service worker is available
                // navigator.serviceWorker.register('/service-worker.js');
                console.log('Service Worker support detected');
            });
        }
        </script>
        """, unsafe_allow_html=True)


def initialize_seo_and_meta():
    """
    Initialize all SEO, meta tags, and enhancements
    Call this at the start of your Streamlit app
    """
    # Add SEO meta tags
    SEOManager.add_meta_tags()
    SEOManager.add_browser_compatibility_tags()
    SEOManager.add_structured_data({
        "name": "PulseTrade",
        "description": "Emotion-Aware Trading Platform with Biometric Monitoring",
        "price": "0"
    })
    
    # Add accessibility enhancements
    AccessibilityEnhancer.add_aria_live_regions()
    AccessibilityEnhancer.add_keyboard_shortcuts()
    
    # Add performance optimizations
    PerformanceOptimizer.add_resource_hints()
    PerformanceOptimizer.add_lazy_loading_script()
    PerformanceOptimizer.add_service_worker_hint()


# Export commonly used functions
__all__ = [
    'SEOManager',
    'AccessibilityEnhancer',
    'PerformanceOptimizer',
    'initialize_seo_and_meta',
]

