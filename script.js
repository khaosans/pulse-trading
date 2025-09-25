// Pulse Trading Presentation SPA with Ollama AI Integration
class PulseTradingPresentation {
    constructor() {
        this.currentSlide = 1;
        this.totalSlides = 15;
        this.speakerNotes = {
            1: "Welcome to our Pulse Trading Final Marketing Plan. This presentation outlines our data-driven, community-focused strategy to scale our platform and deliver strong ROI for investors.",
            2: "Everyday investors face a critical gap: they're either overwhelmed by institutional-grade complexity or underserved by basic platforms. Pulse Trading solves this by delivering professional-grade analytics in a community-driven, mobile-first experience.",
            3: "Our comprehensive PEST and SWOT analysis reveals a perfect storm of opportunity. Regulatory support for fintech innovation, explosive growth in retail investing, and a digital-native generation demanding mobile-first experiences create an ideal market entry window.",
            4: "Our SMART objectives are designed to demonstrate clear traction to investors while building a sustainable growth foundation. Each target is specific, measurable, and directly tied to our value proposition.",
            5: "Our value proposition directly addresses the three core jobs our customers need to accomplish: making informed trades, learning from others, and accessing professional tools. We eliminate their biggest pain points while delivering the gains they most desire.",
            6: "Our target customer is the digital-native investor who's comfortable with technology but wants more than basic trading tools. They're active on social media, value community input, and make data-driven decisions.",
            7: "Our integrated marketing mix creates a cohesive strategy that addresses each customer touchpoint. The freemium model removes barriers to entry while premium features capture value.",
            8: "Our customer journey strategy addresses each decision stage with targeted tactics. We recognize that modern investors research extensively before committing, so we provide educational content and social proof throughout their journey.",
            9: "Service excellence is critical in financial services. Our people, process, and physical evidence all reinforce our brand promise of professional-grade tools with community support.",
            10: "Our disciplined budget allocation ensures optimal ROI while building sustainable growth. The 2.5x return demonstrates strong unit economics, and our break-even timeline shows realistic path to profitability.",
            11: "Our KPI framework ensures we stay on track while maintaining flexibility to adapt. Monthly reviews allow for quick course corrections, while quarterly assessments enable strategic pivots.",
            12: "Our survey results provide strong validation for our strategy. The high percentages across all key metrics demonstrate clear product-market fit. Most importantly, 70% willingness to pay premium pricing validates our revenue model.",
            13: "Our team brings diverse expertise across all critical areas of marketing strategy. Each member leads their domain while collaborating closely with others. This structure ensures deep expertise in each area while maintaining integrated execution.",
            14: "Our phased approach ensures steady progress while allowing for learning and optimization. Each phase builds on the previous one, with clear milestones that demonstrate traction to investors.",
            15: "We're ready to move from strategy to execution. Our plan is comprehensive, our team is committed, and our market opportunity is validated. We're seeking $500K in funding to execute this strategy and capture the significant market opportunity we've identified."
        };
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.updateSlideCounter();
        this.updateSpeakerNotes();
        this.setupKeyboardNavigation();
        this.initializeAI();
    }

    setupEventListeners() {
        // Navigation buttons
        document.getElementById('prevBtn').addEventListener('click', () => this.previousSlide());
        document.getElementById('nextBtn').addEventListener('click', () => this.nextSlide());
        document.getElementById('fullscreenBtn').addEventListener('click', () => this.toggleFullscreen());
        
        // Speaker notes toggle
        document.getElementById('toggleNotes').addEventListener('click', () => this.toggleSpeakerNotes());
        
        // AI panel toggle
        document.getElementById('toggleAI').addEventListener('click', () => this.toggleAIPanel());
        
        // AI enhancement buttons
        document.getElementById('enhanceContent').addEventListener('click', () => this.enhanceContent());
        document.getElementById('generateInsights').addEventListener('click', () => this.generateInsights());
        document.getElementById('improveNarrative').addEventListener('click', () => this.improveNarrative());
    }

    setupKeyboardNavigation() {
        document.addEventListener('keydown', (e) => {
            switch(e.key) {
                case 'ArrowLeft':
                case 'ArrowUp':
                    e.preventDefault();
                    this.previousSlide();
                    break;
                case 'ArrowRight':
                case 'ArrowDown':
                case ' ':
                    e.preventDefault();
                    this.nextSlide();
                    break;
                case 'f':
                case 'F':
                    e.preventDefault();
                    this.toggleFullscreen();
                    break;
                case 'n':
                case 'N':
                    e.preventDefault();
                    this.toggleSpeakerNotes();
                    break;
                case 'a':
                case 'A':
                    e.preventDefault();
                    this.toggleAIPanel();
                    break;
                case 'Escape':
                    this.exitFullscreen();
                    break;
            }
        });
    }

    nextSlide() {
        if (this.currentSlide < this.totalSlides) {
            this.currentSlide++;
            this.updateSlide();
        }
    }

    previousSlide() {
        if (this.currentSlide > 1) {
            this.currentSlide--;
            this.updateSlide();
        }
    }

    updateSlide() {
        // Remove active class from all slides
        document.querySelectorAll('.slide').forEach(slide => {
            slide.classList.remove('active');
        });

        // Add active class to current slide
        const currentSlideElement = document.querySelector(`[data-slide="${this.currentSlide}"]`);
        if (currentSlideElement) {
            currentSlideElement.classList.add('active');
        }

        this.updateSlideCounter();
        this.updateSpeakerNotes();
        this.updateNavigationButtons();
    }

    updateSlideCounter() {
        document.getElementById('slideCounter').textContent = `${this.currentSlide} / ${this.totalSlides}`;
    }

    updateSpeakerNotes() {
        const notesText = document.getElementById('notesText');
        if (notesText && this.speakerNotes[this.currentSlide]) {
            notesText.textContent = this.speakerNotes[this.currentSlide];
        }
    }

    updateNavigationButtons() {
        const prevBtn = document.getElementById('prevBtn');
        const nextBtn = document.getElementById('nextBtn');
        
        prevBtn.disabled = this.currentSlide === 1;
        nextBtn.disabled = this.currentSlide === this.totalSlides;
    }

    toggleFullscreen() {
        if (!document.fullscreenElement) {
            document.documentElement.requestFullscreen().catch(err => {
                console.log('Error attempting to enable fullscreen:', err);
            });
        } else {
            document.exitFullscreen();
        }
    }

    exitFullscreen() {
        if (document.fullscreenElement) {
            document.exitFullscreen();
        }
    }

    toggleSpeakerNotes() {
        const notesPanel = document.getElementById('speakerNotes');
        const toggleBtn = document.getElementById('toggleNotes');
        const icon = toggleBtn.querySelector('i');
        
        notesPanel.classList.toggle('visible');
        
        if (notesPanel.classList.contains('visible')) {
            icon.className = 'fas fa-eye-slash';
        } else {
            icon.className = 'fas fa-eye';
        }
    }

    toggleAIPanel() {
        const aiPanel = document.getElementById('aiPanel');
        const toggleBtn = document.getElementById('toggleAI');
        const icon = toggleBtn.querySelector('i');
        
        aiPanel.classList.toggle('visible');
        
        if (aiPanel.classList.contains('visible')) {
            icon.className = 'fas fa-chevron-down';
        } else {
            icon.className = 'fas fa-chevron-up';
        }
    }

    initializeAI() {
        // Check if Ollama is available
        this.checkOllamaConnection();
    }

    async checkOllamaConnection() {
        try {
            const response = await fetch('http://localhost:11434/api/tags');
            if (response.ok) {
                this.ollamaAvailable = true;
                console.log('Ollama connection established');
            } else {
                this.ollamaAvailable = false;
                console.log('Ollama not available');
            }
        } catch (error) {
            this.ollamaAvailable = false;
            console.log('Ollama not available:', error);
        }
    }

    async enhanceContent() {
        const output = document.getElementById('aiOutput');
        output.innerHTML = '<p><i class="fas fa-spinner fa-spin"></i> Enhancing content with AI...</p>';

        if (!this.ollamaAvailable) {
            output.innerHTML = '<p>Ollama is not available. Please ensure Ollama is running locally.</p>';
            return;
        }

        try {
            const currentSlideContent = this.getCurrentSlideContent();
            const prompt = `Enhance the following presentation slide content for a professional business presentation about Pulse Trading, a fintech platform for retail investors. Make it more compelling and data-driven:

${currentSlideContent}

Provide specific improvements and additional insights that would strengthen this slide for a VC presentation.`;

            const response = await fetch('http://localhost:11434/api/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    model: 'llama3.2',
                    prompt: prompt,
                    stream: false
                })
            });

            if (response.ok) {
                const data = await response.json();
                output.innerHTML = `<div class="ai-enhancement">
                    <h4>AI Enhancement Suggestions:</h4>
                    <p>${data.response}</p>
                </div>`;
            } else {
                throw new Error('Failed to get AI response');
            }
        } catch (error) {
            output.innerHTML = `<p>Error enhancing content: ${error.message}</p>`;
        }
    }

    async generateInsights() {
        const output = document.getElementById('aiOutput');
        output.innerHTML = '<p><i class="fas fa-spinner fa-spin"></i> Generating insights...</p>';

        if (!this.ollamaAvailable) {
            output.innerHTML = '<p>Ollama is not available. Please ensure Ollama is running locally.</p>';
            return;
        }

        try {
            const prompt = `Based on the Pulse Trading marketing plan presentation, generate 3-5 key strategic insights that would be valuable for investors and stakeholders. Focus on market opportunities, competitive advantages, and growth potential. Be specific and data-driven.`;

            const response = await fetch('http://localhost:11434/api/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    model: 'llama3.2',
                    prompt: prompt,
                    stream: false
                })
            });

            if (response.ok) {
                const data = await response.json();
                output.innerHTML = `<div class="ai-insights">
                    <h4>Strategic Insights:</h4>
                    <p>${data.response}</p>
                </div>`;
            } else {
                throw new Error('Failed to get AI response');
            }
        } catch (error) {
            output.innerHTML = `<p>Error generating insights: ${error.message}</p>`;
        }
    }

    async improveNarrative() {
        const output = document.getElementById('aiOutput');
        output.innerHTML = '<p><i class="fas fa-spinner fa-spin"></i> Improving narrative...</p>';

        if (!this.ollamaAvailable) {
            output.innerHTML = '<p>Ollama is not available. Please ensure Ollama is running locally.</p>';
            return;
        }

        try {
            const currentSlideContent = this.getCurrentSlideContent();
            const prompt = `Improve the narrative flow and storytelling for this presentation slide about Pulse Trading. Make it more engaging and persuasive for a VC audience. Focus on creating a compelling story that connects with investors:

${currentSlideContent}

Provide an improved narrative that maintains the key information while making it more compelling and memorable.`;

            const response = await fetch('http://localhost:11434/api/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    model: 'llama3.2',
                    prompt: prompt,
                    stream: false
                })
            });

            if (response.ok) {
                const data = await response.json();
                output.innerHTML = `<div class="ai-narrative">
                    <h4>Improved Narrative:</h4>
                    <p>${data.response}</p>
                </div>`;
            } else {
                throw new Error('Failed to get AI response');
            }
        } catch (error) {
            output.innerHTML = `<p>Error improving narrative: ${error.message}</p>`;
        }
    }

    getCurrentSlideContent() {
        const currentSlideElement = document.querySelector(`[data-slide="${this.currentSlide}"]`);
        if (currentSlideElement) {
            return currentSlideElement.textContent.trim();
        }
        return '';
    }
}

// Initialize the presentation when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new PulseTradingPresentation();
});

// Add some additional utility functions
class PresentationUtils {
    static formatNumber(num) {
        return new Intl.NumberFormat().format(num);
    }

    static formatCurrency(amount) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD',
            minimumFractionDigits: 0,
            maximumFractionDigits: 0
        }).format(amount);
    }

    static formatPercentage(value) {
        return new Intl.NumberFormat('en-US', {
            style: 'percent',
            minimumFractionDigits: 0,
            maximumFractionDigits: 1
        }).format(value / 100);
    }

    static animateCounter(element, start, end, duration) {
        const startTime = performance.now();
        const difference = end - start;

        function updateCounter(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const current = Math.floor(start + (difference * progress));
            
            element.textContent = current;
            
            if (progress < 1) {
                requestAnimationFrame(updateCounter);
            }
        }

        requestAnimationFrame(updateCounter);
    }
}

// Add smooth scrolling and animations
document.addEventListener('DOMContentLoaded', () => {
    // Add intersection observer for animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe all slide content for animations
    document.querySelectorAll('.slide-content > *').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
});

// Add export functionality
class PresentationExporter {
    static exportToPDF() {
        // This would integrate with a PDF generation library
        console.log('Export to PDF functionality would be implemented here');
    }

    static exportToPowerPoint() {
        // This would integrate with a PowerPoint generation library
        console.log('Export to PowerPoint functionality would be implemented here');
    }

    static exportSpeakerNotes() {
        const notes = document.getElementById('notesText').textContent;
        const blob = new Blob([notes], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'pulse-trading-speaker-notes.txt';
        a.click();
        URL.revokeObjectURL(url);
    }
}

// Add keyboard shortcuts help
document.addEventListener('keydown', (e) => {
    if (e.key === '?' || e.key === '/') {
        e.preventDefault();
        alert(`Keyboard Shortcuts:
• Arrow Keys / Space: Navigate slides
• F: Toggle fullscreen
• N: Toggle speaker notes
• A: Toggle AI panel
• Escape: Exit fullscreen
• ?: Show this help`);
    }
});
