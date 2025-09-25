// Pulse Trading Presentation App
class PresentationApp {
  constructor() {
    this.currentSlide = 1;
    this.totalSlides = 16;
    this.slides = document.querySelectorAll('.slide');
    this.navItems = document.querySelectorAll('.nav-item');
    this.slideCounter = document.getElementById('slide-counter');
    this.prevBtn = document.getElementById('prev-btn');
    this.nextBtn = document.getElementById('next-btn');
    
    // Narrative system
    this.narrativeSystem = new NarrativeSystem();
    this.isNarrating = false;
    this.narrativeQueue = [];
    this.currentNarrative = null;
    
    this.init();
  }
  
  init() {
    console.log('Initializing Pulse Trading Presentation...');
    
    // Configure and initialize Mermaid
    this.initializeMermaid();
    
    // Initialize narrative system
    this.narrativeSystem.init();
    
    // Set up event listeners
    this.setupEventListeners();
    
    // Update initial state
    this.updateSlideCounter();
    this.updateNavigationState();
    
    // Show first slide
    this.showSlide(1);
    
    // Force render all diagrams after a delay
    setTimeout(() => {
      this.renderAllMermaidDiagrams();
    }, 1000);
  }
  
  initializeMermaid() {
    // Initialize Mermaid with proper configuration
    mermaid.initialize({
      startOnLoad: false,
      theme: 'base',
      themeVariables: {
        primaryColor: '#21808D',
        primaryTextColor: '#134252',
        primaryBorderColor: '#1D7485',
        lineColor: '#626C7C',
        sectionBkgColor: '#f8f9fa',
        altSectionBkgColor: '#ffffff',
        gridColor: '#e0e0e0',
        secondaryColor: '#FFC185',
        tertiaryColor: '#ECEBD5',
        background: '#ffffff',
        mainBkg: '#ffffff',
        secondBkg: '#f8f9fa',
        labelBoxBkgColor: '#ffffff',
        labelBoxBorderColor: '#626C7C',
        labelTextColor: '#134252',
        loopTextColor: '#134252',
        noteBkgColor: '#FFC185',
        noteTextColor: '#134252',
        activationBkgColor: '#21808D',
        activationBorderColor: '#1D7485',
        sequenceNumberColor: '#ffffff',
        pieTitleTextSize: '18px',
        pieTitleTextColor: '#134252',
        pieSectionTextSize: '14px',
        pieSectionTextColor: '#134252',
        pieOuterStrokeWidth: '2px',
        pieOuterStrokeColor: '#134252',
        pieStrokeColor: '#ffffff',
        pieStrokeWidth: '2px',
        pieOpacity: '0.8'
      },
      flowchart: {
        htmlLabels: true,
        curve: 'basis',
        useMaxWidth: true,
        padding: 15
      },
      sequence: {
        diagramMarginX: 20,
        diagramMarginY: 20,
        actorMargin: 50,
        width: 150,
        height: 50,
        boxMargin: 10,
        boxTextMargin: 5,
        noteMargin: 10,
        messageMargin: 35,
        mirrorActors: false,
        bottomMarginAdj: 1,
        useMaxWidth: true,
        rightAngles: false,
        showSequenceNumbers: false
      },
      pie: {
        textPosition: 0.75,
        useMaxWidth: true
      }
    });
  }
  
  async renderAllMermaidDiagrams() {
    const diagrams = document.querySelectorAll('.mermaid');
    console.log(`Found ${diagrams.length} Mermaid diagrams to render`);
    
    for (let i = 0; i < diagrams.length; i++) {
      const diagram = diagrams[i];
      try {
        const definition = diagram.textContent.trim();
        if (definition && definition.length > 0) {
          console.log(`Rendering diagram ${i + 1}:`, definition);
          
          const id = `mermaid-diagram-${Date.now()}-${i}`;
          
          // Clear existing content
          diagram.innerHTML = '<div style="text-align: center; padding: 20px; color: #626C7C;">Loading diagram...</div>';
          
          // Use the modern mermaid.render method
          try {
            const { svg } = await mermaid.render(id, definition);
            diagram.innerHTML = svg;
            console.log(`Successfully rendered diagram ${i + 1}`);
          } catch (renderError) {
            console.error(`Failed to render diagram ${i + 1}:`, renderError);
            // Create fallback content based on diagram type
            const fallbackContent = this.createFallbackDiagram(definition);
            diagram.innerHTML = fallbackContent;
          }
        } else {
          console.warn(`Empty definition for diagram ${i + 1}`);
          diagram.innerHTML = '<div style="text-align: center; padding: 20px; color: #626C7C;">Diagram content not available</div>';
        }
      } catch (error) {
        console.error(`Error processing diagram ${i + 1}:`, error);
        diagram.innerHTML = '<div style="text-align: center; padding: 20px; color: #626C7C;">Diagram rendering error</div>';
      }
      
      // Add a small delay between renders
      await new Promise(resolve => setTimeout(resolve, 100));
    }
  }
  
  createFallbackDiagram(definition) {
    // Create simple fallback content based on diagram type
    if (definition.includes('flowchart') || definition.includes('graph')) {
      return `<div style="text-align: center; padding: 30px; border: 2px dashed #21808D; border-radius: 8px; background: #f8f9fa;">
        <h4 style="color: #21808D; margin: 0 0 10px 0;">Process Flow Diagram</h4>
        <p style="color: #626C7C; margin: 0;">Interactive diagram available in live presentation</p>
      </div>`;
    } else if (definition.includes('sequenceDiagram')) {
      return `<div style="text-align: center; padding: 30px; border: 2px dashed #21808D; border-radius: 8px; background: #f8f9fa;">
        <h4 style="color: #21808D; margin: 0 0 10px 0;">User Journey Sequence</h4>
        <p style="color: #626C7C; margin: 0;">Step-by-step interaction flow</p>
      </div>`;
    } else if (definition.includes('pie')) {
      return `<div style="text-align: center; padding: 30px; border: 2px dashed #21808D; border-radius: 8px; background: #f8f9fa;">
        <h4 style="color: #21808D; margin: 0 0 10px 0;">Budget Allocation Chart</h4>
        <p style="color: #626C7C; margin: 0;">Visual breakdown of resource distribution</p>
      </div>`;
    }
    
    return `<div style="text-align: center; padding: 30px; border: 2px dashed #21808D; border-radius: 8px; background: #f8f9fa;">
      <h4 style="color: #21808D; margin: 0 0 10px 0;">Interactive Diagram</h4>
      <p style="color: #626C7C; margin: 0;">Visual content optimized for live presentation</p>
    </div>`;
  }
  
  setupEventListeners() {
    // Navigation buttons
    if (this.prevBtn) {
      this.prevBtn.addEventListener('click', (e) => {
        e.preventDefault();
        this.previousSlide();
      });
    }
    
    if (this.nextBtn) {
      this.nextBtn.addEventListener('click', (e) => {
        e.preventDefault();
        this.nextSlide();
      });
    }
    
    // Sidebar navigation
    this.navItems.forEach((item, index) => {
      item.addEventListener('click', (e) => {
        e.preventDefault();
        const slideNumber = parseInt(item.dataset.slide);
        this.goToSlide(slideNumber);
      });
    });
    
    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
      // Only handle if not typing in an input
      if (e.target.matches('input, textarea, [contenteditable]')) {
        return;
      }
      
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
        case 'Home':
          e.preventDefault();
          this.goToSlide(1);
          break;
        case 'End':
          e.preventDefault();
          this.goToSlide(this.totalSlides);
          break;
        case 'Escape':
          if (document.fullscreenElement) {
            document.exitFullscreen();
          }
          break;
      }
    });
  }
  
  showSlide(slideNumber) {
    console.log(`Showing slide ${slideNumber}`);
    
    // Stop current narrative if playing
    if (this.isNarrating) {
      this.stopNarrative();
    }
    
    // Hide all slides
    this.slides.forEach(slide => {
      slide.classList.remove('active');
    });
    
    // Show current slide
    const targetSlide = document.getElementById(`slide-${slideNumber}`);
    if (targetSlide) {
      targetSlide.classList.add('active');
      
      // Scroll to top of slide container
      const slideContainer = document.querySelector('.slide-container');
      if (slideContainer) {
        slideContainer.scrollTop = 0;
      }
    }
    
    this.currentSlide = slideNumber;
    this.updateSlideCounter();
    this.updateNavigationState();
    this.updateSidebarActive();
    
    // Update narrative system with current slide
    this.narrativeSystem.setCurrentSlide(slideNumber);
  }
  
  nextSlide() {
    if (this.currentSlide < this.totalSlides) {
      this.showSlide(this.currentSlide + 1);
    }
  }
  
  previousSlide() {
    if (this.currentSlide > 1) {
      this.showSlide(this.currentSlide - 1);
    }
  }
  
  goToSlide(slideNumber) {
    if (slideNumber >= 1 && slideNumber <= this.totalSlides) {
      this.showSlide(slideNumber);
    }
  }
  
  updateSlideCounter() {
    if (this.slideCounter) {
      this.slideCounter.textContent = `${this.currentSlide} / ${this.totalSlides}`;
    }
  }
  
  updateNavigationState() {
    // Update previous button
    if (this.prevBtn) {
      if (this.currentSlide <= 1) {
        this.prevBtn.disabled = true;
        this.prevBtn.style.opacity = '0.5';
        this.prevBtn.style.cursor = 'not-allowed';
      } else {
        this.prevBtn.disabled = false;
        this.prevBtn.style.opacity = '1';
        this.prevBtn.style.cursor = 'pointer';
      }
    }
    
    // Update next button
    if (this.nextBtn) {
      if (this.currentSlide >= this.totalSlides) {
        this.nextBtn.disabled = true;
        this.nextBtn.style.opacity = '0.5';
        this.nextBtn.style.cursor = 'not-allowed';
      } else {
        this.nextBtn.disabled = false;
        this.nextBtn.style.opacity = '1';
        this.nextBtn.style.cursor = 'pointer';
      }
    }
  }
  
  updateSidebarActive() {
    // Remove active class from all nav items
    this.navItems.forEach(item => {
      item.classList.remove('active');
    });
    
    // Add active class to current slide nav item
    const currentNavItem = document.querySelector(`[data-slide="${this.currentSlide}"]`);
    if (currentNavItem) {
      currentNavItem.classList.add('active');
    }
  }
  
  // Presentation utilities
  toggleFullscreen() {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch(err => {
        console.log(`Error enabling fullscreen: ${err.message}`);
      });
    } else {
      document.exitFullscreen();
    }
  }
  
  // Narrative control methods
  playNarrative() {
    if (!this.isNarrating) {
      this.narrativeSystem.playNarrative(this.currentSlide);
      this.isNarrating = true;
    }
  }
  
  pauseNarrative() {
    if (this.isNarrating) {
      this.narrativeSystem.pauseNarrative();
    }
  }
  
  stopNarrative() {
    if (this.isNarrating) {
      this.narrativeSystem.stopNarrative();
      this.isNarrating = false;
    }
  }
  
  toggleNarrative() {
    if (this.isNarrating) {
      this.pauseNarrative();
    } else {
      this.playNarrative();
    }
  }
  
  playFullPresentation() {
    this.narrativeSystem.playFullPresentation();
    this.isNarrating = true;
  }

  exportNotes() {
    const notes = [];
    this.slides.forEach((slide, index) => {
      const slideNumber = index + 1;
      const title = slide.querySelector('.slide-header h1')?.textContent || `Slide ${slideNumber}`;
      const narrative = slide.querySelector('.narrative p')?.textContent || '';
      const speakerInfo = slide.querySelector('.speaker-info')?.textContent || '';
      
      notes.push({
        slide: slideNumber,
        title: title,
        narrative: narrative,
        speaker: speakerInfo
      });
    });
    
    return notes;
  }
}

// Narrative System Class
class NarrativeSystem {
  constructor() {
    this.currentSlide = 1;
    this.isPlaying = false;
    this.isPaused = false;
    this.isFullPresentation = false;
    this.advanceTimer = null;
    this.currentAudio = null;
    this.speechSynthesis = window.speechSynthesis;
    this.utterance = null;
    this.narrativeData = this.initializeNarrativeData();
    this.controlsElement = null;
    this.progressElement = null;
  }
  
  init() {
    this.createNarrativeControls();
    this.setupEventListeners();
  }
  
  initializeNarrativeData() {
    return {
      1: { 
        duration: 35, 
        text: "Welcome to our Pulse Trading Final Marketing Plan. I'm excited to present our comprehensive, data-driven strategy that positions Pulse Trading to capture significant market share in the $2.7 billion retail trading space. Over the next 15 minutes, we'll walk through our research findings, strategic framework, and implementation roadmap that will deliver strong ROI for investors. Let's begin with the market challenge that sparked our innovative solution.",
        readingTime: 5
      },
      2: { 
        duration: 50, 
        text: "The retail trading market presents a clear opportunity, but everyday investors face a fundamental problem: they're caught between two extremes. On one side, professional trading platforms are too complex and intimidating. On the other, basic apps lack the community support and data insights that drive successful trading decisions. This gap represents a $2.7 billion market opportunity. Our solution, Pulse Trading, bridges this divide by delivering real-time analytics combined with social learning in one seamless, mobile-first experience. This foundation leads us to our comprehensive environmental analysis.",
        readingTime: 8
      },
      3: { 
        duration: 70, 
        text: "Our comprehensive PESTELE and SWOT analyses reveal a compelling market landscape. While regulatory changes and competitive pressure present challenges, the trends strongly favor our approach. Digital adoption is accelerating rapidly, with 85% of our target demographic preferring mobile-first solutions. The social trading trend is gaining momentum, with 65% of investors valuing community features. Our analysis shows that Pulse Trading's community-focused approach is perfectly positioned to capitalize on these trends. These insights directly inform our strategic objectives for 2026.",
        readingTime: 10
      },
      4: { 
        duration: 70, 
        text: "These four strategic objectives translate our market insights into measurable, achievable targets. First, we aim to acquire 5,000 new sign-ups by Q2 2026, representing a 150% growth trajectory. Second, we'll achieve 25% monthly active user retention, demonstrating strong product-market fit. Third, we'll generate $250,000 in revenue by year-end, with a 2.5x marketing return on investment. Finally, we'll establish Pulse Trading as a top-3 community platform in the retail trading space. Each objective has defined tactics, timelines, and success metrics. Now let's see how these objectives connect to our value proposition framework.",
        readingTime: 12
      },
      5: { 
        duration: 55, 
        text: "Our value proposition ladder demonstrates how technical features translate into meaningful emotional benefits for users. At the functional level, real-time analytics and community features deliver immediate value. But the real power lies in the emotional benefits: confidence in trading decisions, belonging to a supportive community, and the satisfaction of continuous learning. This emotional connection drives long-term engagement and platform loyalty. Our research shows that users who engage with community features have 40% higher retention rates. This value proposition directly addresses the needs we identified in our target customer research.",
        readingTime: 8
      },
      6: { 
        duration: 70, 
        text: "Our 50-person Qualtrics survey validates this persona profile with compelling data. 85% of respondents prefer mobile-first solutions, confirming our platform strategy. 80% want real-time analytics, validating our core feature set. Most importantly, 65% value community features, proving our social learning approach. The survey also revealed that our target demographic is willing to pay premium prices for quality tools, with 70% indicating they would pay $9.99 monthly for our premium features. This validation gives us confidence in our product-market fit and pricing strategy.",
        readingTime: 10
      },
      7: { 
        duration: 55, 
        text: "Our product architecture directly responds to these user preferences with a mobile-first design, real-time data integration, and seamless community features. The freemium model strategically lowers barriers to entry while premium features drive sustainable revenue growth. Our core features include advanced charting tools, social trading capabilities, and educational content. The premium tier adds AI-powered insights, priority customer support, and exclusive community access. This product strategy supports our pricing approach and creates multiple revenue streams.",
        readingTime: 8
      },
      8: { 
        duration: 55, 
        text: "Our $9.99 premium price point strikes the optimal balance between accessibility and value. This pricing is accessible for our target demographic while being validated by our survey data showing 70% willingness-to-pay. It positions us competitively against alternatives priced at $15-25 monthly, giving us a significant price advantage. Our pricing strategy includes a 30-day free trial to reduce friction and demonstrate value. This approach maximizes conversion while maintaining healthy unit economics. Now let's see how our promotional strategy brings this value proposition to market.",
        readingTime: 8
      },
      9: { 
        duration: 55, 
        text: "Our integrated promotional strategy addresses each stage of the customer decision journey with precision. For awareness, we leverage digital advertising and content marketing to reach our target audience. During consideration, we use influencer partnerships and community testimonials to build credibility. For conversion, we offer free trials and onboarding support. Post-purchase, we focus on community engagement and feature education to drive retention. Each touchpoint is designed to maximize conversion rates and build long-term community engagement. This promotional approach complements our distribution strategy perfectly.",
        readingTime: 8
      },
      10: { 
        duration: 55, 
        text: "Our digital-first distribution strategy ensures broad reach while maintaining cost efficiency. We focus on urban and suburban US markets where our target demographic is concentrated, allowing us to maximize marketing spend efficiency. Our distribution channels include app stores, social media platforms, and strategic partnerships with financial education providers. This geographic focus enables us to achieve higher conversion rates and lower customer acquisition costs. Our distribution approach supports our service design framework and ensures consistent brand experience across all touchpoints.",
        readingTime: 8
      },
      11: { 
        duration: 55, 
        text: "Our service design framework ensures every customer touchpoint reinforces our brand promise of accessible, community-driven trading education. We provide expert team support through multiple channels, intuitive onboarding processes that reduce learning curves, and visible community success stories that inspire confidence. Our customer success team is trained to help users maximize platform value, while our community moderators ensure a supportive, educational environment. This service excellence directly supports our financial projections and customer lifetime value targets.",
        readingTime: 8
      },
      12: { 
        duration: 70, 
        text: "Our disciplined budget allocation prioritizes high-impact channels based on data-driven insights. 40% of our $100,000 budget goes to digital advertising for maximum reach and targeting precision. 25% is allocated to content marketing for long-term SEO and thought leadership. 20% supports influencer partnerships for credibility and authentic reach. The remaining 15% covers tools, analytics, and operational support. Our 2.5x marketing return on investment target demonstrates strong financial discipline and sustainable growth potential. This financial foundation enables our comprehensive KPI framework for ongoing optimization.",
        readingTime: 10
      },
      13: { 
        duration: 70, 
        text: "Our KPI framework provides monthly tracking with predefined remediation plans for each metric. We monitor user acquisition costs, monthly active users, revenue per user, and community engagement rates. Each KPI has specific targets, measurement methods, and action plans if performance falls below expectations. This systematic approach de-risks our marketing investment and demonstrates operational maturity to potential investors. Our dashboard provides real-time visibility into performance, enabling rapid response to market changes and optimization opportunities.",
        readingTime: 10
      },
      14: { 
        duration: 55, 
        text: "Our primary research validates every major strategic decision we've made. The 85% mobile preference directly supports our platform development priorities. The 70% willingness-to-pay validates our pricing strategy. The 65% community feature preference confirms our social learning approach. This research foundation enabled our entire team's collaborative success and gives us confidence in our go-to-market strategy. The data-driven approach reduces risk and increases our probability of success in the competitive retail trading market.",
        readingTime: 8
      },
      15: { 
        duration: 55, 
        text: "Our collaborative approach ensures every element of this strategy is both expert-driven and strategically integrated. Each team member brought specialized expertise while maintaining alignment with our overall vision. From research and pricing to product development and financial modeling, every component works together to create a cohesive, executable plan. This integrated approach is what sets Pulse Trading apart from competitors who focus on individual features rather than holistic user experience.",
        readingTime: 8
      },
      16: { 
        duration: 70, 
        text: "Our implementation timeline demonstrates project discipline and readiness for immediate execution. With survey completion and financial review completed this week, we're on track to deliver a compelling, investor-ready presentation that showcases both strategic thinking and operational excellence. Our next steps include finalizing partnerships, launching our beta program, and beginning our marketing campaign. We're confident that this comprehensive strategy will position Pulse Trading for success in the competitive retail trading market. Thank you for joining us on this journey through Pulse Trading's marketing strategy. We're excited to bring this vision to life.",
        readingTime: 10
      }
    };
  }
  
  createNarrativeControls() {
    // Create narrative controls container
    const controlsContainer = document.createElement('div');
    controlsContainer.className = 'narrative-controls';
    controlsContainer.style.cssText = `
      position: fixed;
      bottom: 20px;
      left: 50%;
      transform: translateX(-50%);
      background: rgba(255, 255, 255, 0.95);
      backdrop-filter: blur(10px);
      -webkit-backdrop-filter: blur(10px);
      border: 1px solid rgba(0, 0, 0, 0.1);
      border-radius: 16px;
      padding: 16px 24px;
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
      z-index: 1000;
      display: flex;
      align-items: center;
      gap: 16px;
      font-family: var(--font-family-base);
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      opacity: 0;
      transform: translateX(-50%) translateY(20px);
    `;
    
    // Play/Pause button
    const playBtn = document.createElement('button');
    playBtn.className = 'narrative-play-btn';
    playBtn.innerHTML = '<span class="btn-icon">▶️</span><span class="btn-text">Play</span>';
    playBtn.style.cssText = `
      padding: 12px 20px;
      border: none;
      border-radius: 12px;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      cursor: pointer;
      font-size: 14px;
      font-weight: 600;
      transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
      display: flex;
      align-items: center;
      gap: 8px;
      box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
      position: relative;
      overflow: hidden;
    `;
    
    // Progress bar
    const progressContainer = document.createElement('div');
    progressContainer.style.cssText = `
      width: 240px;
      height: 6px;
      background: rgba(0, 0, 0, 0.1);
      border-radius: 3px;
      overflow: hidden;
      position: relative;
      cursor: pointer;
    `;
    
    const progressBar = document.createElement('div');
    progressBar.className = 'narrative-progress';
    progressBar.style.cssText = `
      height: 100%;
      background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
      width: 0%;
      transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      border-radius: 3px;
      position: relative;
    `;
    
    progressContainer.appendChild(progressBar);
    
    // Time display
    const timeDisplay = document.createElement('span');
    timeDisplay.className = 'narrative-time';
    timeDisplay.style.cssText = `
      font-size: 13px;
      color: #666;
      min-width: 90px;
      text-align: center;
      font-weight: 500;
      font-family: 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, 'Courier New', monospace;
    `;
    timeDisplay.textContent = '0:00 / 0:00';
    
    // Full presentation button
    const fullBtn = document.createElement('button');
    fullBtn.className = 'narrative-full-btn';
    fullBtn.innerHTML = '<span class="btn-icon">🎬</span><span class="btn-text">Full</span>';
    fullBtn.style.cssText = `
      padding: 12px 20px;
      border: 2px solid #667eea;
      border-radius: 12px;
      background: transparent;
      color: #667eea;
      cursor: pointer;
      font-size: 14px;
      font-weight: 600;
      transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
      display: flex;
      align-items: center;
      gap: 8px;
    `;
    
    // Assemble controls
    controlsContainer.appendChild(playBtn);
    controlsContainer.appendChild(progressContainer);
    controlsContainer.appendChild(timeDisplay);
    controlsContainer.appendChild(fullBtn);
    
    document.body.appendChild(controlsContainer);
    
    this.controlsElement = controlsContainer;
    this.progressElement = progressBar;
    this.playBtn = playBtn;
    this.timeDisplay = timeDisplay;
    this.fullBtn = fullBtn;
    
    // Add smooth entrance animation
    requestAnimationFrame(() => {
      controlsContainer.style.opacity = '1';
      controlsContainer.style.transform = 'translateX(-50%) translateY(0)';
    });
    
    // Add hover effects
    this.addHoverEffects(playBtn, fullBtn);
  }
  
  addHoverEffects(playBtn, fullBtn) {
    // Play button hover effects
    playBtn.addEventListener('mouseenter', () => {
      playBtn.style.transform = 'translateY(-2px)';
      playBtn.style.boxShadow = '0 6px 20px rgba(102, 126, 234, 0.4)';
    });
    
    playBtn.addEventListener('mouseleave', () => {
      playBtn.style.transform = 'translateY(0)';
      playBtn.style.boxShadow = '0 4px 12px rgba(102, 126, 234, 0.3)';
    });
    
    playBtn.addEventListener('mousedown', () => {
      playBtn.style.transform = 'translateY(0) scale(0.98)';
    });
    
    playBtn.addEventListener('mouseup', () => {
      playBtn.style.transform = 'translateY(-2px) scale(1)';
    });
    
    // Full button hover effects
    fullBtn.addEventListener('mouseenter', () => {
      fullBtn.style.background = '#667eea';
      fullBtn.style.color = 'white';
      fullBtn.style.transform = 'translateY(-2px)';
    });
    
    fullBtn.addEventListener('mouseleave', () => {
      fullBtn.style.background = 'transparent';
      fullBtn.style.color = '#667eea';
      fullBtn.style.transform = 'translateY(0)';
    });
    
    fullBtn.addEventListener('mousedown', () => {
      fullBtn.style.transform = 'translateY(0) scale(0.98)';
    });
    
    fullBtn.addEventListener('mouseup', () => {
      fullBtn.style.transform = 'translateY(-2px) scale(1)';
    });
  }
  
  setupEventListeners() {
    if (this.playBtn) {
      this.playBtn.addEventListener('click', () => this.toggleNarrative());
    }
    
    if (this.fullBtn) {
      this.fullBtn.addEventListener('click', () => this.playFullPresentation());
    }
    
    // Handle speech synthesis events
    if (this.speechSynthesis) {
      this.speechSynthesis.onvoiceschanged = () => {
        this.setupVoice();
      };
    }
  }
  
  setupVoice() {
    const voices = this.speechSynthesis.getVoices();
    // Prefer a natural-sounding voice
    const preferredVoice = voices.find(voice => 
      voice.name.includes('Google') || 
      voice.name.includes('Microsoft') ||
      voice.name.includes('Samantha') ||
      voice.name.includes('Alex')
    ) || voices[0];
    
    if (preferredVoice) {
      this.selectedVoice = preferredVoice;
    }
  }
  
  setCurrentSlide(slideNumber) {
    this.currentSlide = slideNumber;
    this.updateControls();
  }
  
  updateControls() {
    const narrative = this.narrativeData[this.currentSlide];
    if (narrative && this.timeDisplay) {
      const totalDuration = narrative.duration + narrative.readingTime;
      this.timeDisplay.textContent = `0:00 / ${Math.floor(totalDuration / 60)}:${(totalDuration % 60).toString().padStart(2, '0')}`;
    }
  }
  
  playNarrative(slideNumber = this.currentSlide) {
    const narrative = this.narrativeData[slideNumber];
    if (!narrative) return;
    
    this.stopNarrative();
    
    // Highlight the narrative text display
    this.highlightNarrativeText(slideNumber);
    
    if (this.speechSynthesis) {
      this.utterance = new SpeechSynthesisUtterance(narrative.text);
      
      if (this.selectedVoice) {
        this.utterance.voice = this.selectedVoice;
      }
      
      this.utterance.rate = 0.9;
      this.utterance.pitch = 1;
      this.utterance.volume = 0.8;
      
      this.utterance.onstart = () => {
        this.isPlaying = true;
        this.isPaused = false;
        this.updatePlayButton();
        this.startProgress(narrative.duration + narrative.readingTime);
      };
      
      this.utterance.onend = () => {
        if (!this.isFullPresentation) {
          this.isPlaying = false;
          this.isPaused = false;
          this.updatePlayButton();
          this.resetProgress();
          this.unhighlightNarrativeText(slideNumber);
        }
      };
      
      this.utterance.onerror = () => {
        this.isPlaying = false;
        this.isPaused = false;
        this.updatePlayButton();
        this.resetProgress();
        this.unhighlightNarrativeText(slideNumber);
      };
      
      this.speechSynthesis.speak(this.utterance);
    } else {
      // Fallback: simulate with text highlighting
      this.simulateNarrative(narrative);
    }
  }
  
  highlightNarrativeText(slideNumber) {
    const narrativeElement = document.getElementById(`narrative-text-${slideNumber}`);
    if (narrativeElement) {
      narrativeElement.classList.add('highlighted');
    }
  }
  
  unhighlightNarrativeText(slideNumber) {
    const narrativeElement = document.getElementById(`narrative-text-${slideNumber}`);
    if (narrativeElement) {
      narrativeElement.classList.remove('highlighted');
    }
  }
  
  simulateNarrative(narrative) {
    this.isPlaying = true;
    this.updatePlayButton();
    this.startProgress(narrative.duration + narrative.readingTime);
    
    // Highlight the narrative text
    const narrativeElement = document.querySelector(`#slide-${this.currentSlide} .narrative p`);
    if (narrativeElement) {
      narrativeElement.style.backgroundColor = 'var(--color-bg-1)';
      narrativeElement.style.transition = 'background-color 0.3s ease';
    }
    
    setTimeout(() => {
      this.isPlaying = false;
      this.updatePlayButton();
      this.resetProgress();
      
      if (narrativeElement) {
        narrativeElement.style.backgroundColor = '';
      }
    }, (narrative.duration + narrative.readingTime) * 1000);
  }
  
  pauseNarrative() {
    if (this.speechSynthesis && this.isPlaying) {
      this.speechSynthesis.pause();
      this.isPaused = true;
      this.updatePlayButton();
    }
  }
  
  resumeNarrative() {
    if (this.speechSynthesis && this.isPaused) {
      this.speechSynthesis.resume();
      this.isPaused = false;
      this.updatePlayButton();
    }
  }
  
  stopNarrative() {
    if (this.speechSynthesis) {
      this.speechSynthesis.cancel();
    }
    
    this.isPlaying = false;
    this.isPaused = false;
    this.updatePlayButton();
    this.resetProgress();
    
    // Unhighlight any currently highlighted narrative text
    this.unhighlightNarrativeText(this.currentSlide);
  }
  
  toggleNarrative() {
    if (this.isFullPresentation) {
      // Handle full presentation mode
      if (this.isPaused) {
        this.resumeFullPresentation();
      } else {
        this.pauseFullPresentation();
      }
    } else {
      // Handle single slide mode
      if (this.isPlaying) {
        if (this.isPaused) {
          this.resumeNarrative();
        } else {
          this.pauseNarrative();
        }
      } else {
        this.playNarrative();
      }
    }
  }
  
  playFullPresentation() {
    console.log('🎬 Starting full presentation mode...');
    
    // Reset to first slide
    this.currentSlide = 1;
    this.isPlaying = true;
    this.isPaused = false;
    this.isFullPresentation = true;
    
    // Stop any current narration
    this.stopNarrative();
    
    // Start with slide 1
    if (window.presentationApp) {
      window.presentationApp.showSlide(1);
    }
    
    // Begin the presentation sequence
    this.startPresentationSequence();
  }
  
  startPresentationSequence() {
    if (!this.isFullPresentation || this.isPaused) {
      return;
    }
    
    const narrative = this.narrativeData[this.currentSlide];
    if (!narrative) {
      console.log('🎬 Full presentation completed!');
      this.isFullPresentation = false;
      this.updatePlayButton();
      return;
    }
    
    console.log(`🎬 Playing slide ${this.currentSlide}: ${narrative.duration}s speech + ${narrative.readingTime}s reading`);
    
    // Play current slide narrative
    this.playNarrative(this.currentSlide);
    
    // Calculate total time: speech duration + reading time
    const totalTime = (narrative.duration + narrative.readingTime) * 1000;
    
    // Schedule next slide after speech completes + reading time
    this.advanceTimer = setTimeout(() => {
      if (this.isFullPresentation && !this.isPaused) {
        this.currentSlide++;
        if (this.currentSlide <= 16) {
          if (window.presentationApp) {
            window.presentationApp.showSlide(this.currentSlide);
          }
          // Recursively continue the sequence
          this.startPresentationSequence();
        } else {
          // Presentation complete
          console.log('🎬 Full presentation completed!');
          this.isFullPresentation = false;
          this.isPlaying = false;
          this.updatePlayButton();
        }
      }
    }, totalTime);
  }
  
  pauseFullPresentation() {
    if (this.isFullPresentation) {
      this.isPaused = true;
      this.pauseNarrative();
      if (this.advanceTimer) {
        clearTimeout(this.advanceTimer);
        this.advanceTimer = null;
      }
      console.log('⏸️ Full presentation paused');
    }
  }
  
  resumeFullPresentation() {
    if (this.isFullPresentation && this.isPaused) {
      this.isPaused = false;
      this.resumeNarrative();
      // Continue from current slide
      this.startPresentationSequence();
      console.log('▶️ Full presentation resumed');
    }
  }
  
  stopFullPresentation() {
    if (this.isFullPresentation) {
      this.isFullPresentation = false;
      this.isPlaying = false;
      this.isPaused = false;
      this.stopNarrative();
      if (this.advanceTimer) {
        clearTimeout(this.advanceTimer);
        this.advanceTimer = null;
      }
      console.log('⏹️ Full presentation stopped');
    }
  }
  
  updatePlayButton() {
    if (!this.playBtn) return;
    
    const icon = this.playBtn.querySelector('.btn-icon');
    const text = this.playBtn.querySelector('.btn-text');
    
    if (!icon || !text) return;
    
    if (this.isPlaying) {
      if (this.isPaused) {
        icon.textContent = '▶️';
        text.textContent = 'Resume';
      } else {
        icon.textContent = '⏸️';
        text.textContent = 'Pause';
      }
    } else {
      icon.textContent = '▶️';
      text.textContent = 'Play';
    }
  }
  
  startProgress(duration) {
    if (!this.progressElement) return;
    
    const startTime = Date.now();
    const updateProgress = () => {
      if (!this.isPlaying) return;
      
      const elapsed = (Date.now() - startTime) / 1000;
      const progress = Math.min((elapsed / duration) * 100, 100);
      
      this.progressElement.style.width = `${progress}%`;
      
      if (this.timeDisplay) {
        const remaining = Math.max(0, duration - elapsed);
        this.timeDisplay.textContent = `${Math.floor(elapsed / 60)}:${(elapsed % 60).toString().padStart(2, '0')} / ${Math.floor(duration / 60)}:${(duration % 60).toString().padStart(2, '0')}`;
      }
      
      if (progress < 100) {
        requestAnimationFrame(updateProgress);
      }
    };
    
    updateProgress();
  }
  
  resetProgress() {
    if (this.progressElement) {
      this.progressElement.style.width = '0%';
    }
    this.updateControls();
  }
}

// Presentation Timer Class
class PresentationTimer {
  constructor() {
    this.startTime = null;
    this.elapsed = 0;
    this.isRunning = false;
    this.timerElement = null;
    this.createTimerElement();
  }
  
  createTimerElement() {
    this.timerElement = document.createElement('div');
    this.timerElement.className = 'presentation-timer';
    this.timerElement.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      background: var(--color-surface);
      border: 1px solid var(--color-border);
      padding: 8px 16px;
      border-radius: var(--radius-base);
      font-family: var(--font-family-mono);
      font-size: var(--font-size-sm);
      color: var(--color-text);
      box-shadow: var(--shadow-sm);
      z-index: 1000;
      cursor: pointer;
      user-select: none;
    `;
    this.timerElement.textContent = '00:00';
    this.timerElement.title = 'Click to start/stop presentation timer';
    this.timerElement.addEventListener('click', () => this.toggle());
    document.body.appendChild(this.timerElement);
  }
  
  start() {
    if (!this.isRunning) {
      this.startTime = Date.now() - this.elapsed;
      this.isRunning = true;
      this.tick();
      console.log('Presentation timer started');
    }
  }
  
  stop() {
    this.isRunning = false;
    console.log('Presentation timer stopped');
  }
  
  reset() {
    this.stop();
    this.elapsed = 0;
    this.updateDisplay();
    console.log('Presentation timer reset');
  }
  
  toggle() {
    if (this.isRunning) {
      this.stop();
    } else {
      this.start();
    }
  }
  
  tick() {
    if (this.isRunning) {
      this.elapsed = Date.now() - this.startTime;
      this.updateDisplay();
      requestAnimationFrame(() => this.tick());
    }
  }
  
  updateDisplay() {
    const seconds = Math.floor(this.elapsed / 1000);
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    this.timerElement.textContent = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    
    // Change color based on time (15-20 minute target)
    if (seconds > 1200) { // 20 minutes - over target
      this.timerElement.style.color = 'var(--color-error)';
      this.timerElement.style.backgroundColor = 'rgba(var(--color-error-rgb), 0.1)';
    } else if (seconds > 900) { // 15 minutes - approaching target
      this.timerElement.style.color = 'var(--color-warning)';
      this.timerElement.style.backgroundColor = 'rgba(var(--color-warning-rgb), 0.1)';
    } else {
      this.timerElement.style.color = 'var(--color-text)';
      this.timerElement.style.backgroundColor = 'var(--color-surface)';
    }
  }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  console.log('DOM loaded, initializing Pulse Trading Presentation...');
  
  // Wait for Mermaid to be available
  if (typeof mermaid === 'undefined') {
    console.error('Mermaid library not loaded!');
    setTimeout(() => {
      initializeApp();
    }, 1000);
  } else {
    initializeApp();
  }
  
  function initializeApp() {
    // Initialize the main presentation app
    window.presentationApp = new PresentationApp();
    
    // Initialize the presentation timer
    window.presentationTimer = new PresentationTimer();
    
    // Add touch/swipe support for mobile
    let touchStartX = null;
    let touchStartY = null;
    
    document.addEventListener('touchstart', (e) => {
      touchStartX = e.touches[0].clientX;
      touchStartY = e.touches[0].clientY;
    }, { passive: true });
    
    document.addEventListener('touchend', (e) => {
      if (!touchStartX || !touchStartY) return;
      
      const touchEndX = e.changedTouches[0].clientX;
      const touchEndY = e.changedTouches[0].clientY;
      
      const deltaX = touchEndX - touchStartX;
      const deltaY = touchEndY - touchStartY;
      
      // Check if it's a horizontal swipe (not vertical scroll)
      if (Math.abs(deltaX) > Math.abs(deltaY) && Math.abs(deltaX) > 50) {
        if (deltaX > 0) {
          // Swipe right - previous slide
          window.presentationApp.previousSlide();
        } else {
          // Swipe left - next slide
          window.presentationApp.nextSlide();
        }
      }
      
      touchStartX = null;
      touchStartY = null;
    }, { passive: true });
    
    // Global keyboard shortcuts
    document.addEventListener('keydown', (e) => {
      // Ctrl/Cmd + F for fullscreen
      if ((e.ctrlKey || e.metaKey) && e.key === 'f') {
        e.preventDefault();
        window.presentationApp.toggleFullscreen();
      }
      
      // 'T' to toggle timer
      if (e.key === 't' || e.key === 'T') {
        if (!e.target.matches('input, textarea, [contenteditable]')) {
          window.presentationTimer.toggle();
        }
      }
      
      // 'R' to reset timer
      if (e.key === 'r' || e.key === 'R') {
        if (!e.target.matches('input, textarea, [contenteditable]')) {
          window.presentationTimer.reset();
        }
      }
      
      // 'N' to toggle narrative
      if (e.key === 'n' || e.key === 'N') {
        if (!e.target.matches('input, textarea, [contenteditable]')) {
          window.presentationApp.toggleNarrative();
        }
      }
      
      // 'P' to play full presentation
      if (e.key === 'p' || e.key === 'P') {
        if (!e.target.matches('input, textarea, [contenteditable]')) {
          window.presentationApp.playFullPresentation();
        }
      }
    });
    
    console.log('✅ Pulse Trading Presentation App initialized successfully!');
    console.log('📖 Keyboard shortcuts:');
    console.log('   - Arrow keys/Space: Navigate slides');
    console.log('   - T: Toggle timer');
    console.log('   - R: Reset timer');
    console.log('   - N: Toggle narrative');
    console.log('   - P: Play full presentation');
    console.log('   - Ctrl/Cmd + F: Fullscreen mode');
    console.log('   - Home/End: First/Last slide');
    console.log('   - ESC: Exit fullscreen');
  }
});